
import Functions
from Course import Course
from Term import Term


# class Course:
    
#     #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')

#     def __init__(self, id):
#         temp_course = Functions.get_course_by_id(id) # returns #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
#         self.id = id
#         self.code = temp_course[1]
#         self.name = temp_course[2]
#         self.credits = temp_course[3]
#         self.offered_terms = temp_course[4]


# ---- Semester & schedule containers --------------------------------------------------------------------

class Semester:

    def __init__(self, maxCreditHours):
        self.maxCreditHours = maxCreditHours
        self.courses :Course = []
        self.creditHourCount = 0

    def add_course(self, course: Course):
        if self.creditHourCount + course.credits <= self.maxCreditHours:
            self.courses.append(course)
            self.creditHourCount += course.credits
        else:
            print(f"Cannot add {course.code}: exceeds {self.maxCreditHours}")

    def list_courses(self):
        for c in self.courses:
            print(f"{c.code}")

# Schedule ------------------------------------------------------------------------------------------------
class Schedule:

    def __init__(self, maxCreditHours, student_id):
        # self.years: dict[str, dict[Term, Semester]] = {}
        self.maxCreditHours : int = maxCreditHours
        self.course_ids : Course = []
        self.years = {}
        self.student_id = student_id
    
    def get_or_create_semester(self, term: int, year: int):
        if year not in self.years:
            self.years[year] = {}
        
        if term not in self.years[year]:
            # translated_term = Term.F
            # if term == 0:
            #     translated_term = Term.F
            # elif term == 1:
            #     translated_term = Term.S
            # else:
            #     translated_term = Term.Q
            self.years[year][term] = Semester(self.maxCreditHours)
            
        return self.years[year][term]

    def add_course(self, course: Course, year: int, term: Term):
        sem = self.get_or_create_semester(term, year)
        self.course_ids.append(course.id)
        sem.add_course(course)

    def list_schedule(self):
        for year_index, terms in self.years.items():
            print(f"\nYear {year_index}:")
            for term, semester in terms.items():
                semester.list_courses()

    def course_in_schedule(self, course : Course):
        if course.id in self.course_ids:
            return True
        else:
            return False
    
    #course id
    def course_in_schdule_id(self, course_id : int):
        if course_id in self.course_ids:
            return True
        else:
            return False

    #returns true if the current semester should be incremented
    def evaluate_current_semester(self, current_term, current_year, course: Course):
        temp_semester : Semester = self.years[current_year][current_term]
        if (temp_semester.creditHourCount + course.credits) > temp_semester.maxCreditHours:
            return True
        else:
            return False
        
    def credit_hours_in_current_semester(self, current_term : int, current_year: int):
        temp_semester : Semester = self.years[current_year][current_term]
        return temp_semester.creditHourCount
    
    def to_string(self) -> str:
        for year, terms in self.years.items():
            for term, semester in terms.items():
                print(f"Year {year}, Semester {term}:")
                for course in semester.courses:
                    print(f"    {course.code} ({course.credits} credits)")

    #returns [year, semester]
    def find_course_in_schedule(self, current_term, current_year, course: Course):
        for year, terms in self.years.items():
            for term, semester in terms.items():
                for temp_course in semester.courses:
                    if temp_course.id == course.id:
                        return [year, term]
        return [1]

    # def add_student_schedule(student_id): returns schedule id
    # def add_schedule_semester(schedule_id, name): returns semsterid
    # def add_semester_course(semester_id, course_id): return not really notable
    def add_schedule_to_database(self):
        schedule_id = Functions.add_student_schedule(self.student_id)
        for year, terms in self.years.items():
            for term, semester in terms.items():
                semester_name = "Year " + str(year + 1) + " - " + Term.int_to_Term(term)
                if(len(semester.courses) != 0):
                    semester_id = Functions.add_schedule_semester(schedule_id, semester_name)
                for temp_course in semester.courses:
                    Functions.add_semester_course(semester_id, temp_course.id)
                    
       
