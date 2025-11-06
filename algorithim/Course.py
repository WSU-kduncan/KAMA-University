from database import Functions
from Schedule import Term

class Course:
    #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')
    def __init__(self, id):
        temp_course = Functions.get_course_by_id(id) # returns #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
        self.id = id
        self.code = temp_course[1]
        self.name = temp_course[2]
        self.credits = temp_course[3]

        # Translates given string into defined Enum
        terms : Term = []
        if len(temp_course[4]) > 0 :
            for chr in temp_course[4]:
                if chr == 'F':
                    terms.append(Term.F)
                elif chr == 'S':
                    terms.append(Term.S)
                elif chr == 'Q':
                    terms.append(Term.Q)
        else:
            # if for whatever reason a term is not defined it assume that it is available all terms
            terms.append(Term.F)
            terms.append(Term.S)
            terms.append(Term.Q)

        self.offered_terms = terms