from database import Functions

class Course:
    #(1,           'ENG 1100',    'Academic Writing and Reading',  3,             'FSQ')
    def __init__(self, id):
        temp_course = Functions.get_course_by_id(id) # returns #(Primary Key, 'Course Code', 'Name of Course', Credit Hours,  'Semesters Offered')
        self.id = id
        self.code = temp_course[1]
        self.name = temp_course[2]
        self.credits = temp_course[3]
        self.offered_terms = temp_course[4]