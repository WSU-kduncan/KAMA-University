
# needs to take in min of First Name, Last Name, email, password
# Student_id will auto increment
def add_student(Fname, Lname, email, password):
    # get greatest pk
    # new pk = greatest pk + 1
    query1 = """SELECT MAX(student_id)
                FROM Student"""
    return 1
    
# takes in the student_id
# removes all cases where student_id is in the database
def remove_student(student_id):
    return 1

# takes in the student_id of the student you want to change
# takes in the username you want to change it to
# change the username of the student
def change_username(student_id, newUsername):
    return 1

# Same as above but for password
def change_password(student_id, newPassword):
    return 1

# takes in student_id and the program_id of the program you want to add
# will add element to Student_programs table
def add_program(student_id, program_id):
    return 1

# takes in student_id of the student you want to edit
# oldProgram_id is the id of the Program you want to change
# newProgram_id is the id of the Program you want to replace the old with
# removes the old pairing from Student_programs and adds the new pairing to Student_programs table
def change_program(student_id, oldProgram_id, newProgram_id):
    return 1

# takes in student_id you want to change
# takes in the id of the program you want to remove
def remove_program(student_id, program_id):
    return 1

def edit_numSemester(student_id, numSemesters):
    return 1



# A schedule can have only 1 student
# it can have many semesters
# a semester can be in many schdeles
# a semester can have many courses
# a course can have many semesters
