import Functions
from Course import Course
from Schedule import Schedule
from Term import Term

class GenerateSchedule:
    MIN_CREDIT_HOURS = 120
    COOP_COURSE_ID = 52
    ASL_REQUIREMENT_ID = 16

    def __init__(self, id):
        student = Functions.get_student_data(id)

        self.id = id
        self.years = student[4]               # originally allowed years
        self.num_coops = student[3]
        self.summer_semesters = student[6]
        self.credit_hours_per_semester = student[5]

        # Allow up to two extra years for co-ops
        self.max_year = self.years + 5            # year 0..years allowed

        self.total_credit_hours = 0
        self.current_semester = 0
        self.current_year = 0
        self.semesters_per_year = 0

        self.schedule = Schedule(self.credit_hours_per_semester, self.id)
        self.schedule.get_or_create_semester(self.current_semester, self.current_year)

    # -------------------------------------------------------------
    # Begin generation
    # -------------------------------------------------------------
    def begin_generation(self):

        if self.test_base_possibility():
            self.programs = Functions.get_student_programs(self.id)
            returnValue =  self.generate_schedule()
            if returnValue == 0:
                #self.schedule.add_schedule_to_database()
                print("Adding schedule to database")
            return returnValue
            
        else:
            return 1

    # -------------------------------------------------------------
    # Determine semesters per year
    # -------------------------------------------------------------
    def test_base_possibility(self):

        if self.summer_semesters == 'yes':
            self.semesters_per_year = 3
        else:
            self.semesters_per_year = 2

        possible = (
            (self.semesters_per_year * self.years) * self.credit_hours_per_semester >= self.MIN_CREDIT_HOURS
        )

        return possible

    # -------------------------------------------------------------
    # MAIN GENERATION LOOP
    # -------------------------------------------------------------
    def generate_schedule(self):
        returnValue = 0

        # --- ASL requirement ---
        asl_courses = Functions.get_requirement_courses(self.ASL_REQUIREMENT_ID)
        courses_to_add = [Course(c[0]) for c in asl_courses[::-1]]
        returnValue = self.add_course_to_schedule(courses_to_add)
        if returnValue != 0:
            return returnValue

        # --- First year seminars ---
        for program in self.programs:
            seminars = []
            if program[0] == 1:
                seminars.append(Course(6))
            if program[0] == 2:
                seminars.append(Course(7))
            returnValue = self.add_course_to_schedule(seminars)
            if returnValue != 0:
                return returnValue

        #  --- Requirements per program ---
        for program in self.programs:
            requirements = Functions.get_program_requirements(program[0])

            for requirement in requirements:
                courses = Functions.get_requirement_courses(requirement[0])
                credit_sum = 0

                for course in courses:
                    chain = []

                    if Functions.get_prerequisite(course[0]) is None:
                        chain = [Course(course[0])]
                    else:
                        chain = self.create_courses_to_add(Course(course[0]))

                    returnValue = self.add_course_to_schedule(chain)
                    if returnValue != 0:
                        return returnValue

                    credit_sum += course[3]

                    if credit_sum >= requirement[2]:
                        break

        # --- Fill remaining credits with electives ---
        all_courses = Functions.get_courses()
        for course in all_courses:
            if self.total_credit_hours >= self.MIN_CREDIT_HOURS:
                break

            if not self.schedule.course_in_schdule_id(course[0]):
                chain = self.create_courses_to_add(Course(course[0]))
                # never fill with co-op
                if len(chain) == 1 and chain[0].id != self.COOP_COURSE_ID:
                    returnValue = self.add_course_to_schedule(chain)
                    if returnValue != 0:
                        return returnValue

        return 0

    # -------------------------------------------------------------
    # Build prerequisite chain
    # -------------------------------------------------------------
    def create_courses_to_add(self, course):
        temp = course
        stack = []

        while Functions.get_prerequisite(temp.id) is not None:
            stack.append(temp)
            temp = Course(Functions.get_prerequisite(temp.id)[0])

        stack.append(temp)
        return stack

    def should_place_coop(self):
        if self.num_coops <= 0:
            return False

        # Must have 25 completed credits before FIRST co-op
        if self.total_credit_hours < 25:
            return False

        # Check if semester is empty
        sem = self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        if sem.creditHourCount != 0:
            return False

        # Check summer permission
        if self.current_semester == 2 and self.summer_semesters != "yes":
            return False

        return True

    # -------------------------------------------------------------
    # PLACE CO-OP
    # -------------------------------------------------------------
    def place_coop(self):
        coop = Course(self.COOP_COURSE_ID)
        self.schedule.add_course(coop, self.current_year, self.current_semester)

        self.num_coops -= 1

        # Advance to next semester
        self.advance_semester()

    # -------------------------------------------------------------
    # ADVANCE SEMESTER + AUTO-EXTEND IF NEEDED
    # -------------------------------------------------------------
    def advance_semester(self):

        if self.current_semester == self.semesters_per_year - 1:
            self.current_semester = 0
            self.current_year += 1
        else:
            self.current_semester += 1

        # Auto-extend
        if self.current_year > self.max_year:
            self.max_year += 1

        self.schedule.get_or_create_semester(self.current_semester, self.current_year)

    # -------------------------------------------------------------
    # ADD COURSE OR CO-OP TO SCHEDULE
    # -------------------------------------------------------------
    def add_course_to_schedule(self, courses):

        # Safety check
        if not courses:
            return 0

        # ----------------------------------------------------------
        # BEFORE placing any courses → try placing co-op (Option A)
        # ----------------------------------------------------------
        if self.should_place_coop():
            self.place_coop()
            # move on; do not attempt courses this term
            # we intentionally DO NOT return, because after placing
            # a co-op we still need to schedule the given courses

        # ----------------------------------------------------------
        # Check if adding THIS course chain overflows current semester
        # ----------------------------------------------------------
        if self.schedule.evaluate_current_semester(
            self.current_semester, self.current_year, courses[0]
        ):
            self.advance_semester()

    # ----------------------------------------------------------
    # CASE 1 — Single course (no prereq chain)
    # ----------------------------------------------------------
        if len(courses) == 1:
            course = courses[0]

            if not self.schedule.course_in_schedule(course):

                # Find a valid semester for this course
                time = self.find_available_semester(
                    self.current_semester, self.current_year, course
                )

                # Overflow or cannot find placement
                if isinstance(time, int) or time[1] > self.max_year:
                    return 1

                sem, yr = time

                # Add course
                self.schedule.add_course(course, yr, sem)
                self.total_credit_hours += course.credits

    # ----------------------------------------------------------
    # Prerequisite chain
    # ----------------------------------------------------------
        else:
            prereq_sem = self.current_semester
            prereq_year = self.current_year

            while courses:
                course = courses.pop()

                if not self.schedule.course_in_schedule(course):

                    time = self.find_available_semester(
                        prereq_sem, prereq_year, course
                    )

                    if isinstance(time, int) or time[1] > self.max_year:
                        return 1

                    prereq_sem, prereq_year = time

                    self.schedule.add_course(course, prereq_year, prereq_sem)
                    self.total_credit_hours += course.credits

        # ----------------------------------------------------------
        # AFTER placing courses try to place REMAINING co-ops
        # This is the new logic that allows multiple co-ops to be placed.
        # ----------------------------------------------------------
        while self.num_coops > 0 and self.total_credit_hours >= 25:

            sem = self.schedule.get_or_create_semester(
                self.current_semester, self.current_year
            )

            # If empty + allowed → place co-op HERE
            if sem.creditHourCount == 0 and self.coop_semester_allowed(self.current_semester):
                self.place_coop()
                continue

            # Otherwise, advance semester (auto-extend allowed)
            self.advance_semester()

        return 0
    
    # -------------------------------------------------------------
    # Check if a semester is allowed for co-op placement
    # -------------------------------------------------------------
    def coop_semester_allowed(self, semester_index):
        # semester_index: 0 = Fall, 1 = Spring, 2 = Summer
        # summer co-op allowed only if student preference says "yes"
        if semester_index == 2 and self.summer_semesters != "yes":
            return False
        return True

    # -------------------------------------------------------------
    # FIND SEMESTER FOR COURSE
    # -------------------------------------------------------------
    def find_available_semester(self, current_semester, current_year, course):

        prereq = Functions.get_prerequisite(course.id)
        if prereq is not None:
            prereq_course = Course(prereq[0])
            loc = self.schedule.find_course_in_schedule(
                current_semester, current_year, prereq_course
            )

            if len(loc) == 2:
                if loc[1] < self.semesters_per_year - 1:
                    current_semester = loc[1] + 1
                    current_year = loc[0]
                else:
                    current_semester = 0
                    current_year = loc[0] + 1

        i = 0
        while True:
            self.schedule.get_or_create_semester(current_semester, current_year)

            if i > 12:
                return 1

            term = (
                Term.F if current_semester == 0 else
                Term.S if current_semester == 1 else
                Term.Q
            )

            if (
                term in course.offered_terms
                and not self.schedule.evaluate_current_semester(
                    current_semester, current_year, course
                )
            ):
                return [current_semester, current_year]

            # Advance
            if current_semester == self.semesters_per_year - 1:
                current_semester = 0
                current_year += 1
            else:
                current_semester += 1
                term = term.next()

            if current_year > self.max_year:
                return 1

            i += 1

# # not generating
# print("Student 4")
# student4 = GenerateSchedule(4)
# value = student4.begin_generation()
# print(value)
# student4.schedule.to_string()
