# TODO: TURN DATA INTO OBJECTS
# TODO: ADD PREREQS TO COURSES : THESE WILL BE THE iDS OF THE COURSE

import mariadb

# -------------------------------------------------------------
# Database Connection
# -------------------------------------------------------------
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


# -------------------------------------------------------------
# Student Programs: Returns a list of the Programs a student is enlisted in
# -------------------------------------------------------------
def get_student_programs(student_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """
        SELECT p.program_id, p.program_name, p.degree_type, p.creditHours
        FROM StudentProgram sp
        JOIN Program p ON sp.program_id = p.program_id
        WHERE sp.student_id = ?;
    """
    cur.execute(query, (student_id,))
    results = cur.fetchall()
    conn.close()
    return results


# -------------------------------------------------------------
# Program Requirements: Returns a list of the requirements of a program
# -------------------------------------------------------------
def get_program_requirements(program_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """
        SELECT r.requirement_id, r.requirement_type, r.min_credits
        FROM Program_Requirements pr
        JOIN Requirement r ON pr.requirement_id = r.requirement_id
        WHERE pr.program_id = ?;
    """
    cur.execute(query, (program_id,))
    results = cur.fetchall()
    conn.close()
    return results


# -------------------------------------------------------------
# Requirement Courses: Returns all the courses that match that requirement
# -------------------------------------------------------------
def get_requirement_courses(requirement_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """
        SELECT c.course_id, c.course_code, c.course_name, c.credits, c.semester
        FROM Requirement_Course rc
        JOIN Course c ON rc.course_id = c.course_id
        WHERE rc.requirement_id = ?;
    """
    cur.execute(query, (requirement_id,))
    results = cur.fetchall()
    conn.close()
    return results

# -------------------------------------------------------------
# Course by ID: Returns everything except department
# -------------------------------------------------------------
def get_course_by_id(course_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    query = """
        SELECT course_id, course_code, course_name, credits, semester
        FROM Course
        WHERE course_id = ?;
    """
    cur.execute(query, (course_id,))
    result = cur.fetchone()
    conn.close()
    return result


#TODO: add prereq to courses
# -------------------------------------------------------------
# Prerequisites: Returns the prerequisites of a course
# -------------------------------------------------------------
def get_prerequisites(course_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """
        SELECT prereq_id, prereq_course_id
        FROM Prerequisite
        WHERE course_id = ?;
    """
    cur.execute(query, (course_id,))
    results = cur.fetchall()
    conn.close()
    return results


# -------------------------------------------------------------
# Student Data: Returns full data about a student
# -------------------------------------------------------------
def get_student_data(student_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    query = """
        SELECT s.student_id, s.first_name, s.last_name, s.NumcoOps, 
            s.numYears, s.CrdtHrsPrSem, s.summerSemester, s.advisor_id
        FROM Student s
        WHERE s.student_id = ?;
    """
    cur.execute(query, (student_id,))
    result = cur.fetchone()
    conn.close()
    return result

# -------------------------------------------------------------
# Returns user data based on the username
# -------------------------------------------------------------
def get_user_data_by_username(username):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()

    # List of tables to search
    tables = ["Student", "Admin", "Advisor"]

    result = None

    for table in tables:
        query = f"SELECT * FROM {table} WHERE username = ?;"
        cur.execute(query, (username,))
        result = cur.fetchone()
        if result:
            # Include which table we found it in
            result_dict = {"user_type": table, "data": result}
            conn.close()
            return result_dict

    # Not found in any table
    conn.close()
    return None

# -------------------------------------------------------------
# Example usage (for testing)
# -------------------------------------------------------------
if __name__ == "__main__":
    print("Testing database functions...\n")

    # Test connection
    conn = get_db_connection()
    if conn:
        print("✅ Connection successful!\n")
        conn.close()

    # Example test calls
# print(get_student_programs(1))
#print(get_program_requirements(1))
#print(get_requirement_courses(2))
#print(get_course_by_id(1))
#print(get_prerequisites(2))
#print(get_student_data(1))
print(get_user_data_by_username('jacksonv'))

