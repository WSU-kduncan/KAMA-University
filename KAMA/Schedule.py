import Functions
from Course import Course
from Term import Term

class Semester:

    def __init__(self, maxCreditHours):
        self.maxCreditHours = maxCreditHours
        self.courses = []
        self.creditHourCount = 0

    def add_course(self, course: Course):

        # Co-op ALWAYS allowed (credit = -1)
        if course.credits == -1:
            self.courses.append(course)
            self.creditHourCount = -1
            return

        # No adding courses to a co-op semester
        if self.creditHourCount == -1:
            return

        if self.creditHourCount + course.credits <= self.maxCreditHours:
            self.courses.append(course)
            self.creditHourCount += course.credits

class Schedule:

    def __init__(self, maxCreditHours, student_id):
        self.maxCreditHours = maxCreditHours
        self.course_ids = []
        self.years = {}
        self.student_id = student_id

    def get_or_create_semester(self, term, year):
        if year not in self.years:
            self.years[year] = {}

        if term not in self.years[year]:
            self.years[year][term] = Semester(self.maxCreditHours)

        return self.years[year][term]

    def add_course(self, course: Course, year: int, term: Term):
        sem = self.get_or_create_semester(term, year)

        # Prevent academic courses in a co-op term
        if sem.creditHourCount == -1 and course.credits != -1:
            return

        self.course_ids.append(course.id)
        sem.add_course(course)

    def course_in_schedule(self, course: Course):
        return course.id in self.course_ids

    def course_in_schdule_id(self, course_id: int):
        return course_id in self.course_ids

    def evaluate_current_semester(self, current_term, current_year, course: Course):
        sem = self.years[current_year][current_term]

        # Co-op ALWAYS fits (it overwrites)
        if course.credits == -1:
            return False

        # Academic courses cannot go in co-op semester
        if sem.creditHourCount == -1:
            return True

        return (sem.creditHourCount + course.credits) > sem.maxCreditHours

    def credit_hours_in_current_semester(self, current_term, current_year):
        return self.years[current_year][current_term].creditHourCount

    def find_course_in_schedule(self, current_term, current_year, course: Course):
        for year, terms in self.years.items():
            for term, semester in terms.items():
                for c in semester.courses:
                    if c.id == course.id:
                        return [year, term]
        return [1]

    def add_schedule_to_database(self):
        if not Functions.get_student_schedule(self.student_id):

            schedule_id = Functions.add_student_schedule(self.student_id)

            for year, terms in self.years.items():
                for term, semester in terms.items():

                    if len(semester.courses) == 0:
                        continue

                    sem_name = "Year " + str(year + 1) + " - " + Term.int_to_Term(term)
                    sem_id = Functions.add_schedule_semester(schedule_id, sem_name)

                    for course in semester.courses:
                        Functions.add_semester_course(sem_id, course.id)
