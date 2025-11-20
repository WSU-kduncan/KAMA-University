import Functions
from Course import Course
from Schedule import Schedule
from Term import Term

class GenerateSchedule:
    # generates on creation
    MIN_CREDIT_HOURS = 120 # minimum credit hours needed to graduate
    COOP_COURSE_ID = 52 # grabbed from th database
    ASL_REQUIREMENT_ID = 16
    
    
    #returns not 0 if failed
    def __init__(self, id):
        #check if schedule is even remotely possible
        # pull student info
        # print(get_student_data(1))
        #(Primary Key 0, 'First Name' 1, 'Last Name' 2, Num Years 3, Num CoOps 4, Summer Semester 5, Credit Hours 6, AdvisorID 7)
        #(1,           'Jackson',    'Vail',      'JVail.1@KAMA.edu', 'jacksonv', 'JacksonV123!', 4,         0,         'yes',           15,           1)
        student = Functions.get_student_data(id)
        self.id = id
        self.years = student[4] # int
        self.num_coops = student[3] # int
        self.summer_semesters = student[6] # 'yes' or 'no'
        self.credit_hours_per_semester = student[5]
        self.total_credit_hours = 0
        self.current_semester = 0
        self.current_year = 0
        self.semesters_per_year = 0
        self.schedule = Schedule(self.credit_hours_per_semester, self.id)
        self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        
    def begin_generation(self):
        if self.test_base_possibility():
            # pull programs
            # print(get_student_programs(1))
            # (Primary Key, Program, Type of Major, Number of Credit Hours)
            # [(2, 'Criminal Justice', 'Major', 120)]
            self.programs = Functions.get_student_programs(self.id)
            return self.generate_schedule()
        else:
            # do nothing
            # TODO last : write error messages
            return 1

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
        # fuck you you're taking ASL
        asl_courses = Functions.get_requirement_courses(self.ASL_REQUIREMENT_ID)
        
        courses_to_add = []
        for asl_course in asl_courses:
            courses_to_add.insert(0, Course(asl_course[0]))
        
        returnValue = self.add_course_to_schedule(courses_to_add)

        for program in self.programs:
            #list of lists again
            requirements = Functions.get_program_requirements(program[0])
            
            #requirement
            #(Primary Key, 'Requirement', Min Credit Hours)
            for requirement in requirements:
                #grab the courses for this requirement
                courses = Functions.get_requirement_courses(requirement[0])

                #Running into a problem where too many courses are added
                # lets set credit hours per requirement to keep track if it is going over
                credit_hours_per_requirement = 0
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
                    else:
                        # 3 is the index of the # of credit hours for a class
                        credit_hours_per_requirement += course[3]
                    
                    # 2 is the index of the min credit hours for a requiremnt
                    if credit_hours_per_requirement >= requirement[2]:
                        #break the loop if we have reached the max credit hours for a requirement
                        break
                    
       # This is an array of all the courses in our database
        all_courses = Functions.get_courses()
        # we are going through each one and add courses without a prereq
        #the general
        for course in all_courses:
           
            if self.total_credit_hours < self.MIN_CREDIT_HOURS:
                if not(self.schedule.course_in_schdule_id(course[0])):
                     # I'm forcing the return value to be zero here
                     #If somehow the loop ends with a return value of 1 then we should be concerned. Otherwise, it's fine
                    returnValue = 0
                    #add course to schedule
                    courses_to_add = self.create_courses_to_add(Course(course[0]))
                    if len(courses_to_add) == 1:
                        #only add if there are no prereqs 
                        temp_course : Course = courses_to_add[0]
                        if temp_course.id != self.COOP_COURSE_ID:
                            # DO NOT ADD COOPS RANDOMLY
                            returnValue = self.add_course_to_schedule(courses_to_add)

            else:
                # break if we meet the min number of credit hours to graudate
                break

        if(returnValue != 0):
            # end generation
            returnValue
        
        # "add" coops
        if (self.current_semester * self.current_year + self.num_coops) <= (self.semesters_per_year * self.years):
            i = 0
            while i < self.num_coops:
                if(self.schedule.credit_hours_in_current_semester(self.current_semester, self.current_year)) == 0:
                    #add the coop to this semester
                    courses_to_add = self.create_courses_to_add(Course(self.COOP_COURSE_ID))
                    self.add_course_to_schedule(courses_to_add)
                    i += 1
                
                #go to next semester and year
                if(self.current_semester == (self.semesters_per_year - 1)):
                    #move up to next year
                    self.current_year += 1
                    self.current_semester = 0
                else:
                    self.current_semester += 1

                if(self.current_year > (self.years - 1)):
                    # TODO add error codes
                    return 1
            returnValue = 0
        else:
            # TODO add specific numbers for error codes
            returnValue = 1

        #if it even gets here lol
        return returnValue


    def create_courses_to_add(self, course : Course):
        # given a course that has a prerequisite, create a list of all the courses that you have to take to take this course in the order of how you should take them
        temp_course : Course = course
        course_stack: Course = []
        while Functions.get_prerequisite(temp_course.id) is not None:
            course_stack.append(temp_course)
            #(PreReq Primary Key, 'Prereq Name')
            # index 0 will be the course id for the prerequisite
            temp_course = Course(Functions.get_prerequisite(temp_course.id)[0])
        #add the last course
        course_stack.append(temp_course)
        return course_stack

        
    #courses is a list of ids
    def add_course_to_schedule(self, courses : Course):
        #TODO
        # Change current year or semester if necessary
        if self.schedule.evaluate_current_semester(self.current_semester, self.current_year, courses[0]):
            if (self.current_semester + 1) <= (self.semesters_per_year - 1):
                self.current_semester += 1
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
            else:
                self.current_year += 1
                self.current_semester = 0;
                self.schedule.get_or_create_semester(self.current_semester, self.current_year)
        
        if(self.current_year > (self.years - 1)):
            #schedule generation failure
            # TODO add specific numbers for error codes
            return 1
        # decribed in flow chart
        # courses is a stack

        #TODO if the course you are adding has a prereq in the same semester, add it to the next semester
        # actually let's just simplify this and do it in the find_available semester
        if len(courses) == 1:
            if not(self.schedule.course_in_schedule(courses[0])):
                time = self.find_available_semester(self.current_semester, self.current_year, courses[0])
                #(semester, year)
                if time[1] > (self.years - 1):
                    #TODO breakpoint error codes
                    return 1
                self.schedule.add_course(courses[0], time[1], time[0])
                temp_course : Course = courses[0]
                self.total_credit_hours += temp_course.credits # adds credits from course to total

        
        elif len(courses) > 1:
            i = 0
            prereq_semester = self.current_semester
            prereq_year = self.current_year
            while(len(courses) > 0):
                
                course : Course = courses.pop()
                if not(self.schedule.course_in_schedule(course)):
                    time = self.find_available_semester(prereq_semester, prereq_year, course)

                    if((isinstance(time, int)) or time[1] > (self.years - 1)):
                        #TODO breakpoint error codess
                        return 1
                    else:
                        prereq_semester = time[0]
                        prereq_year = time[1]
                        self.schedule.add_course(course, prereq_year, prereq_semester)
                        self.total_credit_hours += course.credits
                
        else:
            # somehow failed again lol
            # TODO add specific numbers for error codes
            return 1
        
        # if you have gone through everything and it didn't stop then it succeeded
        return 0
        
    # returns array in order of  (semester, year)
    def find_available_semester(self, current_semester, current_year, course: Course):
        # Course
        #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')
        # does the course have a prereq that is in the current smeester
        if Functions.get_prerequisite(course.id) != None:
            #has prereq
            prereq = Course(Functions.get_prerequisite(course.id)[0])
            if len(self.schedule.find_course_in_schedule(current_semester, current_year, prereq)) == 2:
                #if it return a semester and year, make the current semester and year the semester after
                time = self.schedule.find_course_in_schedule(current_semester, current_year, prereq)
                # [year, semester]
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
                # this failed, could not find space to put the class
                return 1
            # the function returns false if the current semester doesn't need to be incremented. Meaning there is room for it to be added
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
            #create a new semester
            i += 1


#test values for student
#1 major 1 minor
#not generating
print("Student 1")
# when creating students create them as a generation object. TRust
student1 = GenerateSchedule(1)
value = student1.begin_generation()
print(value)
student1.schedule.to_string()
student1.schedule.add_schedule_to_database()

#1 major 2 minors
# not generating
# print("Student 2")
# student2 = GenerateSchedule(2)
# value = student2.begin_generation()
# print(value)
# student2.schedule.to_string()

# #2 majors 1 minor
# # not generating
# print("Student 3")
# student3 = GenerateSchedule(3)
# value = student3.begin_generation()
# print(value)
# student3.schedule.to_string()

# #2 majors
# # not generating
# print("Student 4")
# student4 = GenerateSchedule(4)
# value = student4.begin_generation()
# print(value)
# student4.schedule.to_string()

# # 2 majors 2 minors
# # not generating
# print("Student 5")
# student5 = GenerateSchedule(5)
# value = student5.begin_generation()
# print(value)
# student5.schedule.to_string()




