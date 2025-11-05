
import mariadb

def get_db_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="password",
            host="localhost",
            port=3306,
            database="kama"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None


# needs to take in min of First Name, Last Name, email, password
# Student_id will auto increment
# Fname, Lname, email, password
def add_student(first_name, last_name, email, username, password, advisor_id):
    # get greatest pk
    # new pk = greatest pk + 1
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query1 = """SELECT MAX(student_id)
                FROM Student"""
    
    cur.execute(query1)
    result = cur.fetchone()
    student_id = result[0] + 1
    
    query2 = """INSERT INTO Student (student_id, first_name, last_name, email, username, password, advisor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)"""


    cur.execute(query2, (student_id, first_name, last_name, email, username, password, advisor_id))
    conn.commit()
    conn.close()
    
    return query2

#add_student("John", "Doe", "testemail", "username", "password", 3)

    
# takes in the student_id
# removes all cases where student_id is in the database
# make this so it removes all cases of this student Id it doesn't matter what table
def remove_student(student_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """DELETE FROM Student
    WHERE student_id = ?;"""
    cur.execute(query, (student_id,))
    conn.commit()
    conn.close()
    return 1

#remove_student(7)

# takes in the student_id of the student you want to change
# takes in the username you want to change it to
# change the username of the student
def change_username(student_id, newUsername):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET username = ?
    WHERE student_id = ?"""
    cur.execute(query, (newUsername, student_id,))
    conn.commit()
    return 1
#change_username(7, "Bob")

# Same as above but for password
def change_password(student_id, newPassword):

    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET password = ?
    WHERE student_id = ?"""
    cur.execute(query, (newPassword, student_id,))
    conn.commit()
    conn.close()
    return 1
#change_password(7, "testing")

# takes in student_id and the program_id of the program you want to add
# will add element to Student_programs table
def add_program(student_id, program_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """INSERT INTO StudentProgram (student_id, program_id)
    VALUES (?, ?)"""
    cur.execute(query, (student_id, program_id))
    conn.commit()
    conn.close()
    return 1
#add_program(7, 1)

# takes in student_id of the student you want to edit
# oldProgram_id is the id of the Program you want to change
# newProgram_id is the id of the Program you want to replace the old with
# removes the old pairing from Student_programs and adds the new pairing to Student_programs table
def change_program(student_id, oldProgram_id, newProgram_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE StudentProgram
    SET program_id = ?
    WHERE student_id = ? AND program_id = ?"""
    cur.execute(query, (newProgram_id, student_id, oldProgram_id))
    conn.commit()
    conn.close()
    return 1

#change_program(7, 1, 2)

# takes in student_id you want to change
# takes in the id of the program you want to remove
def remove_program(student_id, program_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """DELETE FROM StudentProgram
    WHERE student_id = ? AND program_id = ?;"""
    cur.execute(query, (student_id, program_id))
    conn.commit()
    conn.close()
    return 1
#remove_program(7, 2)

def edit_numCreditHours(student_id, CrdtHrsPrSem):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET CrdtHrsPrSem = ?
    WHERE student_id = ?"""
    cur.execute(query, (CrdtHrsPrSem, student_id,))
    conn.commit()
    conn.close()
    return 1
# edit_numCreditHours(7, 15)

# boolean = yes / no
def change_SummerSemester(student_id, boolean):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET SummerSemester = ?
    WHERE student_id = ?"""
    cur.execute(query, (boolean, student_id,))
    conn.commit()
    conn.close()
    return 1

#change_SummerSemester(7, "yes")
def change_numYears(student_id, numYears):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET NumYears = ?
    WHERE student_id = ?"""
    cur.execute(query, (numYears, student_id,))
    conn.commit()
    conn.close()
    return 1
#change_numYears(7, 5)

def change_numCoOps(student_id, numCoOps):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET numCoOps = ?
    WHERE student_id = ?"""
    cur.execute(query, (numCoOps, student_id,))
    conn.commit()
    conn.close()
    return 1
#change_numCoOps(7, 2)

def change_advisor(student_id, advisor_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """UPDATE Student
    SET advisor_id = ?
    WHERE student_id = ?"""
    cur.execute(query, (advisor_id, student_id,))
    conn.commit()
    conn.close()
    return 1
#change_advisor(6, 2)

def add_advisor(first_name, last_name, email, username, password, office_name, office_num):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query1 = """SELECT MAX(advisor_id)
                FROM Advisor"""
    
    cur.execute(query1)
    result = cur.fetchone()
    advisor_id = result[0] + 1
    
    query2 = """INSERT INTO Advisor (advisor_id, first_name, last_name, email, username, password, office_name, office_num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""


    cur.execute(query2, (advisor_id, first_name, last_name, email, username, password, office_name, office_num))
    conn.commit()
    conn.close()
    return 1
#add_advisor("Amy", "Smith", "email", "username", "password", "officeName", 301)

def remove_advisor(advisor_id):
    conn = get_db_connection()
    if not conn:
        return[]
    cur = conn.cursor()
    query = """DELETE FROM Advisor
    WHERE advisor_id = ?;"""
    cur.execute(query, (advisor_id,))
    conn.commit()
    conn.close()
    return 1
remove_advisor(4)




# A schedule can have only 1 student
# it can have many semesters
# a semester can be in many schdeles
# a semester can have many courses
# a course can have many semesters
