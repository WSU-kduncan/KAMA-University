
from enum import Enum
from database import Functions
from Schedule import Schedule, Term
from Course import Course


# class Course:
    
#     #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')

#     def __init__(self, id):
#         temp_course = Functions.get_course_by_id(id) # returns #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
#         self.id = id
#         self.code = temp_course[1]
#         self.name = temp_course[2]
#         self.credits = temp_course[3]
#         self.offered_terms = temp_course[4]


class Term(str, Enum):
    F = "Fall"
    S = "Spring"
    Q = "Summer"


# ---- Semester & schedule containers --------------------------------------------------------------------

class Semester:

    def __init__(self, name, maxCreditHours):
        self.name = name
        self.maxCreditHours = maxCreditHours
        self.courses = []
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

    def __init__(self, maxCreditHours):
        # self.years: dict[str, dict[Term, Semester]] = {}
        self.years = {}
        self.maxCreditHours
    
    def get_or_create_semester(self, term: Term, year: int):
        if year not in self.years:
            self.years[year] = {}
        
        if term not in self.years[year]:
            self.years[year][term] = Semester(term, self.maxCreditHours)
            
        return self.years[year][term]

    def add_course(self, course: Course, year: int, term: Term):
        sem = self.get_or_create_semester(term, year)
        sem.add_course(course)

    def list_schedule(self):
        for year_index, terms in self.years.items():
            print(f"\nYear {year_index}:")
            for term, semester in terms.items():
                semester.list_courses()

