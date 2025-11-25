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
        self.years = student[4]
        self.num_coops = student[3]
        self.summer_semesters = student[6]
        self.credit_hours_per_semester = student[5]
        self.total_credit_hours = 0
        self.current_semester = 0
        self.current_year = 0
        self.semesters_per_year = 0
        self.schedule = Schedule(self.credit_hours_per_semester, self.id)
        self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        
    def begin_generation(self):
        if self.test_base_possibility():
            self.programs = Functions.get_student_programs(self.id)
            return self.generate_schedule()
        else:
            return 1

    def test_base_possibility(self):
        if self.summer_semesters == 'yes':
            self.semesters_per_year = 3
        else:
            self.semesters_per_year = 2

        if ((self.semesters_per_year * self.years) - self.num_coops) * self.credit_hours_per_semester >= self.MIN_CREDIT_HOURS:
            return True 
        else:
            return False 

    def generate_schedule(self):
        returnValue = 0

        asl_courses = Functions.get_requirement_courses(self.ASL_REQUIREMENT_ID)
        
        courses_to_add = []
        for asl_course in asl_courses:
            courses_to_add.insert(0, Course(asl_course[0]))
        
        returnValue = self.add_course_to_schedule(courses_to_add)

        for program in self.programs:
            requirements = Functions.get_program_requirements(program[0])
            
            for requirement in requirements:
                courses = Functions.get_requirement_courses(requirement[0])

                credit_hours_per_requirement = 0

                for course in courses:
                    courses_to_add = []
                    if(Functions.get_prerequisite(course[0]) is None):
                        courses_to_add.append(Course(course[0])) 
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    else:
                        courses_to_add = self.create_courses_to_add(Course(course[0]))
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    
                    if returnValue != 0:
                        return returnValue
                    else:
                        credit_hours_per_requirement += course[3]
                    
                    if credit_hours_per_requirement >= requirement[2]:
                        break
                    
        all_courses = Functions.get_courses()

        for course in all_courses:
           
            if self.total_credit_hours < self.MIN_CREDIT_HOURS:
                if not(self.schedule.course_in_schdule_id(course[0])):
                    returnValue = 0
                    courses_to_add = self.create_courses_to_add(Course(course[0]))
                    if len(courses_to_add) == 1:
                        temp_course : Course = courses_to_add[0]
                        if temp_course.id != self.COOP_COURSE_ID:
                            returnValue = self.add_course_to_schedule(courses_to_add)

            else:
                break

        if(returnValue != 0):
            returnValue
        
        if (self.current_semester * self.current_year + self.num_coops) <= (self.semesters_per_year * self.years):
            i = 0
            while i < self.num_coops:
                if(self.schedule.credit_hours_in_current_semester(self.current_semester, self.current_year)) == 0:
                    courses_to_add = self.create_courses_to_add(Course(self.COOP_COURSE_ID))
                    self.add_course_to_schedule(courses_to_add)
                    i += 1
                
                if(self.current_semester == (self.semesters_per_year - 1)):
                    self.current_year += 1
                    self.current_semester = 0
                else:
                    self.current_semester += 1

                if(self.current_year > (self.years - 1)):
                    return 1
            returnValue = 0
        else:
            returnValue = 1

        return returnValue


    def create_courses_to_add(self, course : Course):
        temp_course : Course = course
        course_stack: Course = []
        while Functions.get_prerequisite(temp_course.id) is not None:
            course_stack.append(temp_course)
            temp_course = Course(Functions.get_prerequisite(temp_course.id)[0])
        course_stack.append(temp_course)
        return course_stack

        
    def add_course_to_schedule(self, courses : Course):
        if self.schedule.evaluate_current_semester(self.current_semester, self.current_year, courses[0]):
            if (self.current_semester + 1) <= (self.semesters_per_year - 1):
                self.current_semester += 1
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
            else:
                self.current_year += 1
                self.current_semester = 0
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        if(self.current_year > (self.years - 1)):
            return 1

        if len(courses) == 1:
            if not(self.schedule.course_in_schedule(courses[0])):
                time = self.find_available_semester(self.current_semester, self.current_year, courses[0])
                if time[1] > (self.years - 1):
                    return 1
                self.schedule.add_course(courses[0], time[1], time[0])
                temp_course : Course = courses[0]
                self.total_credit_hours += temp_course.credits 

        
        elif len(courses) > 1:
            i = 0
            prereq_semester = self.current_semester
            prereq_year = self.current_year
            while(len(courses) > 0):
                
                course : Course = courses.pop()
                if not(self.schedule.course_in_schedule(course)):
                    time = self.find_available_semester(prereq_semester, prereq_year, course)

                    if((isinstance(time, int)) or time[1] > (self.years - 1)):
                        return 1
                    else:
                        prereq_semester = time[0]
                        prereq_year = time[1]
                        self.schedule.add_course(course, prereq_year, prereq_semester)
                        self.total_credit_hours += course.credits
                
        else:
            return 1
        
        return 0
        
    def find_available_semester(self, current_semester, current_year, course: Course):
        if Functions.get_prerequisite(course.id) != None:
            prereq = Course(Functions.get_prerequisite(course.id)[0])
            if len(self.schedule.find_course_in_schedule(current_semester, current_year, prereq)) == 2:
                time = self.schedule.find_course_in_schedule(current_semester, current_year, prereq)
                if time[1] < (self.semesters_per_year - 1):
                    current_semester = time[1] + 1
                    current_year = time[0]
                else:
                    current_semester = 0
                    current_year = time[0] + 1
                
        
        current_term : Term
        if current_semester == 0:
            current_term = Term.F
        elif current_semester == 1:
            current_term = Term.S
        else:
            current_term = Term.Q

        i = 0
        while 1:
            self.schedule.get_or_create_semester(current_semester, current_year)
            if i > 12:
                return 1
            if (current_term in course.offered_terms) and not(self.schedule.evaluate_current_semester(current_semester, current_year, course)) :
                return [current_semester, current_year]
            else:
                if (current_semester + 1) <= (self.semesters_per_year - 1):
                    current_semester += 1
                    current_term = current_term.next()
                else:
                    current_semester = 0
                    current_term = Term.F
                    current_year += 1
            i += 1


# ------------------- CLEANED: all debugging commented --------------------

# print("Student 1")
# student1 = GenerateSchedule(1)
# value = student1.begin_generation()
# print(value)
# student1.schedule.to_string()
# student1.schedule.add_schedule_to_database()

# print("Student 2")
# ... etc for others

