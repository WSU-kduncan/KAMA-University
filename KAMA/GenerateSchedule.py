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

        # allow one extra overflow year
        self.max_year = self.years            # year 0..years allowed

        self.total_credit_hours = 0
        self.current_semester = 0
        self.current_year = 0
        self.semesters_per_year = 0

        self.schedule = Schedule(self.credit_hours_per_semester, self.id)
        self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        
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


    def test_base_possibility(self):

        if self.summer_semesters == 'yes':
            self.semesters_per_year = 3
        else:
            self.semesters_per_year = 2

        
        possible = ((self.semesters_per_year * self.years) - self.num_coops) * self.credit_hours_per_semester >= self.MIN_CREDIT_HOURS

        return possible


    def generate_schedule(self):

        returnValue = 0

        # --- ASL requirement ---
        asl_courses = Functions.get_requirement_courses(self.ASL_REQUIREMENT_ID)
        
        courses_to_add = []
        for asl_course in asl_courses:
            courses_to_add.insert(0, Course(asl_course[0]))

        seminars = []
        for program in self.programs:

            
            if program[0] == 1:
                 # first year seminar for pysch
                seminars.insert(0, Course(6))
            if program[0] == 2:
                # first year seminar for criminal justice
                seminars.insert(0, Course(7))
        returnValue = self.add_course_to_schedule(seminars)

        returnValue = self.add_course_to_schedule(courses_to_add)

        if returnValue != 0:
            return returnValue

        # --- Requirements per program ---
        for program in self.programs:
            requirements = Functions.get_program_requirements(program[0])
            
            for requirement in requirements:
                courses = Functions.get_requirement_courses(requirement[0])

                credit_hours_per_requirement = 0

                for course in courses:
                    courses_to_add = []

                    if Functions.get_prerequisite(course[0]) is None:
                        courses_to_add.append(Course(course[0])) 
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    else:
                        courses_to_add = self.create_courses_to_add(Course(course[0]))
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    
                    if returnValue != 0:
                        return returnValue
                    
                    credit_hours_per_requirement += course[3]

                    if credit_hours_per_requirement >= requirement[2]:
                        break
                    
        # --- Fill remaining credits ---
        all_courses = Functions.get_courses()

        for course in all_courses:
            if self.total_credit_hours < self.MIN_CREDIT_HOURS:
                if not self.schedule.course_in_schdule_id(course[0]):
                    courses_to_add = self.create_courses_to_add(Course(course[0]))
                    if len(courses_to_add) == 1:
                        temp_course = courses_to_add[0]
                        if temp_course.id != self.COOP_COURSE_ID:
                            returnValue = self.add_course_to_schedule(courses_to_add)
            else:
                break

        # --- Co-op placement ---
        if (self.current_semester * self.current_year + self.num_coops) <= (self.semesters_per_year * self.years):

            i = 0
            while i < self.num_coops:
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)

                if self.schedule.credit_hours_in_current_semester(self.current_semester, self.current_year) == 0:
                    courses_to_add = self.create_courses_to_add(Course(self.COOP_COURSE_ID))
                    self.add_course_to_schedule(courses_to_add)
                    i += 1
                
                if self.current_semester == (self.semesters_per_year - 1):
                    self.current_year += 1
                    self.current_semester = 0
                else:
                    self.current_semester += 1

                # overflow handling
                if self.current_year > self.max_year:
                    return 1

            returnValue = 0
        else:
            returnValue = 1

        return returnValue


    # ---------------------
    # Helper Subfunctions
    # ---------------------

    def create_courses_to_add(self, course):
        temp = course
        stack = []

        while Functions.get_prerequisite(temp.id) is not None:
            stack.append(temp)
            temp = Course(Functions.get_prerequisite(temp.id)[0])

        stack.append(temp)
        return stack

    def add_course_to_schedule(self, courses):

        # SAFETY CHECK — prevent IndexError on empty list
        if not courses:
            print("[DEBUG] add_course_to_schedule() received EMPTY course list → skipping")
            return 0

        # Check if adding the first course would overflow current semester
        if self.schedule.evaluate_current_semester(self.current_semester, self.current_year, courses[0]):
            if self.current_semester + 1 <= self.semesters_per_year - 1:
                self.current_semester += 1
            else:
                self.current_year += 1
                self.current_semester = 0

            self.schedule.get_or_create_semester(self.current_semester, self.current_year)

        # Overflow year not allowed beyond max_year
        if self.current_year > self.max_year:
            return 1

        if len(courses) == 1:
            course = courses[0]

            if course.id == self.COOP_COURSE_ID:
                #coops get added without checking
                self.schedule.add_course(course, self.current_year, self.current_semester)
                return 0

            if not self.schedule.course_in_schedule(course):
                time = self.find_available_semester(self.current_semester, self.current_year, course)

                # Overflow check
                if isinstance(time, int) or time[1] > self.max_year:
                    return 1

                # Add course
                self.schedule.add_course(course, time[1], time[0])
                self.total_credit_hours += course.credits

        elif len(courses) > 1:
            prereq_sem = self.current_semester
            prereq_year = self.current_year

            while len(courses) > 0:
                course = courses.pop()

                if not self.schedule.course_in_schedule(course):
                    time = self.find_available_semester(prereq_sem, prereq_year, course)

                    # Overflow check
                    if isinstance(time, int) or time[1] > self.max_year:
                        return 1

                    prereq_sem, prereq_year = time

                    # Add course
                    self.schedule.add_course(course, prereq_year, prereq_sem)
                    self.total_credit_hours += course.credits

        # Should never happen
        else:
            print("[ERROR] add_course_to_schedule(): Unexpected empty course chain.")
            return 1

        return 0

    def find_available_semester(self, current_semester, current_year, course):

        prereq = Functions.get_prerequisite(course.id)
        if prereq is not None:
            prereq_course = Course(prereq[0])
            loc = self.schedule.find_course_in_schedule(current_semester, current_year, prereq_course)

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

            if term in course.offered_terms and not self.schedule.evaluate_current_semester(current_semester, current_year, course):
                return [current_semester, current_year]

            if current_semester + 1 <= self.semesters_per_year - 1:
                current_semester += 1
                term = term.next()
            else:
                current_semester = 0
                current_year += 1

            # overflow allowed
            if current_year > self.max_year:
                return 1

            i += 1

# # not generating
# print("Student 4")
# student4 = GenerateSchedule(2)
# value = student4.begin_generation()
# print(value)
# student4.schedule.to_string()
