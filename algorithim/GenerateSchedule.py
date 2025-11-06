from database import Functions
from Course import Course
from Schedule import Schedule, Term

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
        self.schedule = Schedule(student[1], self.credit_hours_per_semester)
        
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
                courses = Functions.get_requirement_courses(requirement[0])
                #(Primary Key, 'Course Code', 'Name of Course',                Credit Hours,  'Semesters Offered')
                #[(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')]
                for course in courses:
                    #TODO fix course logic to fit how prequisites are set
                    #figure out how to work with terms
                    #Course is set up as an array (course id, prereq name)

                    courses_to_add = []
                    #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
                    #add_course will return 0 if successful and not 0 if not
                    if(Functions.get_prerequisite(course[0]) is None):
                        courses_to_add.append(Course(course[0])) #this creates a course object to add
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    else:
                        courses_to_add = self.create_courses_to_add(Course(course[0])) #creates course to start function
                        returnValue = self.add_course_to_schedule(courses_to_add)
                    
                    # if at any point in the loop the generation fails stop loop and return.
                    if returnValue != 0:
                        return returnValue
                    
                
            
        #after going through every program, consider adding random as couses until minimum credit hours are reached
        while (self.total_credit_hours < self.MIN_CREDIT_HOURS):
            #TODO
            # I need a method to get an array of all the courses or course id's in the database.
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
            # TODO add specific numbers for error codes
            returnValue = 1

        #if it even gets here lol
        return returnValue


    def create_courses_to_add(self, course):
        # given a course that has a prerequisite, create a list of all the courses that you have to take to take this course in the order of how you should take them
        temp_course = course
        course_stack = []
        while Functions.get_prerequisite(temp_course.id) is not None:
            course_stack.append(temp_course)
            #(PreReq Primary Key, 'Prereq Name')
            # index 0 will be the course id for the prerequisite
            temp_course = Course(Functions.get_prerequisite[0])
        return course_stack

        
        

    #courses is a list of ids
    def add_course_to_schedule(self, courses : Course):
        #TODO
        # Change current year or semester if necessary
        if self.schedule.evaluate_current_semester(self.current_semester, self.current_year, courses[0]):
            if (self.current_semester + 1) <= self.semesters_per_year:
                self.current_semester += 1
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
            else:
                self.current_year += 1
                self.current_semester = 0;
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        if(self.current_year > self.years):
            #schedule generation failure
            # TODO add specific numbers for error codes
            return 1
        # decribed in flow chart
        # courses is a stack
        if len(courses) == 1:
            if not(self.schedule.course_in_schedule(courses[0])):
                time = self.find_available_semester(self.current_semester, self.current_year, courses[0])
                #(semester, year)
                if time[1] > self.years:
                    #TODO breakpoint error codes
                    return 1
                self.schedule.add_course(courses[0], time[1], time[0])

        
        elif len(courses) > 1:
            i = 0
            prereq_semester = self.current_semester
            prereq_year = self.current_year
            while(len(courses) > 0):
                
                course = courses.pop()
                if not(self.schedule.course_in_schedule(course)):
                    time == self.find_available_semester(prereq_semester, prereq_year, course)

                    if(time[1] > self.years):
                        #TODO breakpoint error codess
                        return 1
                    else:
                        prereq_semester = time[0]
                        prereq_year = time[1]
                        self.schedule.add_course(course, prereq_year, prereq_semester)
                
        else:
            # somehow failed again lol
            # TODO add specific numbers for error codes
            return 1
        
        # if you have gone through everything and it didn't stop then it succeeded
        return 0
        
    # returns array in order of  (semester, year)
    def find_available_semester(self, current_semester, current_year, course):
        # Course
        #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')
        current_term : Term
        if current_semester == 0:
            current_term = Term.F
        elif current_semester == 1:
            current_term = Term.S
        else:
            current_term = Term.Q
        i = 0
        while 1:
            if i > 12:
                # this failed, could not find space to put the class
                return 1
            # the function returns false if the current semester doesn't need to be incremented. Meaning there is room for it to be added
            if (current_term in course[4]) and not(self.schedule.evaluate_current_semester(current_semester, current_year, course)) :
                return [current_semester, current_year]
            else:
                if (current_semester + 1) <= self.semesters_per_year:
                    current_semester += 1
                    current_term.next
                else:
                    current_semester = 0
                    current_term = Term.F
                    current_year += 1
            i + 1


            
            

    



   



