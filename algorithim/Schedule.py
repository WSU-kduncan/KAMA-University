
from enum import Enum
from database import Functions
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

    def next(self):
        order = [Term.F, Term.S, Term.Q]
        idx = order.index(self)
        return order[(idx + 1) % len(order)]  # wrap around


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
        self.maxCreditHours : int
        self.course_ids : Course
        self.years = {}
    
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
            self.years[year][term] = Semester(term, self.maxCreditHours)
            
        return self.years[year][term]

    def add_course(self, course: Course, year: int, term: Term):
        sem = self.get_or_create_semester(term, year)
        self.course_ids.append(course[0])
        sem.add_course(course)

    def list_schedule(self):
        for year_index, terms in self.years.items():
            print(f"\nYear {year_index}:")
            for term, semester in terms.items():
                semester.list_courses()

    def course_in_schedule(self, course : Course):
        if course[0] in self.course_ids:
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
    def evaluate_current_semester(self, current_term, current_year, course):
        temp_semester : Semester = self.years[current_year][current_term]
        if (temp_semester.creditHourCount + course[3]) < temp_semester.maxCreditHours:
            return True
        else:
            return False
        
    def credit_hours_in_current_semester(self, current_term : int, current_year: int):
        temp_semester : Semester = self.years[current_year][current_term]
        return temp_semester.creditHourCount


