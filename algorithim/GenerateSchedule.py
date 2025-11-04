from database import Functions
from Course import Course

class GenerateSchedule:
    # generates on creation
    MIN_CREDIT_HOURS = 120 # minimum credit hours needed to graduate
    
    
    #returns not 0 if failed
    def __init__(self, id):
        #check if schedule is even remotely possible
        # pull student info
        # print(get_student_data(1))
        #(Primary Key 0, 'First Name' 1, 'Last Name' 2, 'email' 3,            'username' 4, 'password' 5,     Num Years 6, Num CoOps 7, Summer Semester 8, Credit Hours 9, AdvisorID 10)
        #(1,           'Jackson',    'Vail',      'JVail.1@KAMA.edu', 'jacksonv', 'JacksonV123!', 4,         0,         'yes',           15,           1)
        student = Functions.get_student_data(id)
        self.id = id
        self.years = student[6] # int
        self.num_coops = student[7] # int
        self.summer_semesters = student[8] # 'yes' or 'no'
        self.credit_hours_per_semester = student[9]
        self.total_credit_hours = 0
        self.current_semester = 0
        self.current_year = 0
        self.semesters_per_year = 0
        
        if self.test_base_possibility():
            # pull programs
            # print(get_student_programs(1))
            # (Primary Key, Program, Type of Major, Number of Credit Hours)
            # [(2, 'Criminal Justice', 'Major', 120)]
            self.programs = Functions.get_student_programs(self.id)
            self.generate_schedule()
        else:
            # do nothing
            # TODO last : write error messages
            self.generate_schedule()

    def test_base_possibility(self):
        if self.summer_semesters == 'yes':
            self.semesters_per_year = 3
        else:
            self.semesters_per_year = 2

        if ((self.semesters_per_year * self.years) - self.num_coops) * self.credit_hours_per_semester >= self.MIN_CREDIT_HOURS:
            return True 
        else:
            return False #this means there is physically not enough room in the plan for graduation

    def generate_schedule(self):
        # program is also an array
        # it looks like this (Primary Key, Program, Type of Major, Number of Credit Hours)
        returnValue = 0
        for program in self.programs:
            #list of lists again
            requirements = Functions.get_program_requirements(program[0])
            
            #requirement
            #(Primary Key, 'Requirement', Min Credit Hours)
            for requirement in requirements:
                #grab the courses for this requirement
                courses = Functions.get_requirement_courses(requirement[1])
                for course in courses:

                    courses_to_add = []
                    #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
                    #add_course will return 0 if successful and not 0 if not
                    if(Functions.get_prerequisite(course[0]) is None):
                        courses_to_add.append(course)
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    else:
                        courses_to_add = create_courses_to_add(course)
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    
                    if returnValue != 0:
                        return returnValue
                    
                
            
        #after going through every program, consider adding random as couses until minimum credit hours are reached
        while (self.total_credit_hours < self.MIN_CREDIT_HOURS):
            #TODO
            #add random courses to the semeser
            i = 0
        
        # "add" coops
        if (self.current_semester * self.current_year + self.num_coops) <= (self.semesters_per_year * self.years):
            #TODO
            #add each coop
            #just represent as a basic course called coop.
            #filler
            returnValue = 0
        else:
            returnValue = 1

        #if it even gets here lol
        return returnValue

        
                        

    def create_courses_to_add(self, course_id):
        # given a course that has a prerequisite, create a list of all the courses that you have to take to take this course in the order of how you should take them
        temp_course = Course(course_id)
        course_stack = []
        while Functions.get_prerequisite(temp_course.id) is not None:
            course_stack.append(temp_course)
            #(PreReq Primary Key, 'Prereq Name')
            # index 0 will be the course id for the prerequisite
            temp_course = Course(Functions.get_prerequisite[0])
        return course_stack

        
        

    #courses is a list of ids
    def add_course_to_schedule(self, courses):
        #TODO
        #decribed in flow chart
        #courses is a stack

   



