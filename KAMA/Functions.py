# TODO: TURN DATA INTO OBJECTS


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
        print("Primary connection failed: {e}")
        print("Using fallback password")
        
        try:
            conn = mariadb.connect(
                user="root",
                password="3665",
                host="localhost",
                port=3306,
                database="kama"
            )
            print("Connected")
            return conn
        except mariadb.Error as e2:
            print("Connection Failed")
            return None
        
# -------------------------------------------------------------
# Get All Courses
# -------------------------------------------------------------
def get_courses():
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()
    query = """SELECT *
    FROM COURSE"""
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

# -------------------------------------------------------------
# Get ALL courses in database
# -------------------------------------------------------------
def get_courses_for_display():
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()

    query = (
        "SELECT course_id, course_code, course_name, credits, semester, prereq "
        "FROM Course "
        "ORDER BY "
        "SUBSTRING_INDEX(course_code, ' ', 1), "
        "CAST(SUBSTRING_INDEX(course_code, ' ', -1) AS UNSIGNED);"
    )

    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results


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


# -------------------------------------------------------------
# Prerequisites: Returns the prerequisites of a course
# -------------------------------------------------------------
def get_prerequisite(course_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()

    # Step 1: get the prereq ID for this course
    query = "SELECT prereq FROM Course WHERE course_id = ?;"
    cur.execute(query, (course_id,))
    prereq_row = cur.fetchone()

    # If no prereq or course not found
    if not prereq_row or prereq_row[0] is None:
        conn.close()
        return None

    prereq_id = prereq_row[0]

    # Step 2: get the id and name of the prereq course
    query = "SELECT course_id, course_name FROM Course WHERE course_id = ?;"
    cur.execute(query, (prereq_id,))
    prereq_course = cur.fetchone()

    conn.close()
    return prereq_course



# -------------------------------------------------------------
# Student Data: Returns full data about a student
# -------------------------------------------------------------
def get_student_data(student_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()

    # FIXED: column order now matches what GenerateSchedule expects
    query = """
        SELECT 
            student_id,
            first_name,
            last_name,
            NumCoOps,
            NumYears,
            CrdtHrsPrSem,
            SummerSemester,
            advisor_id,
            username,
            password
        FROM Student
        WHERE student_id = ?;
    """

    cur.execute(query, (student_id,))
    result = cur.fetchone()
    conn.close()
    return result

# -------------------------------------------------------------
# Advisor Data: Returns full data about a student
# -------------------------------------------------------------
def get_advisor_data(advisor_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    query = """
        SELECT *
        FROM Advisor 
        WHERE advisor_id = ?;
    """
    cur.execute(query, (advisor_id,))
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

def getRequirement(reqID):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    query = """
        SELECT * FROM Requirement WHERE requirement_id = ?;
    """
    cur.execute(query, (reqID,))
    results = cur.fetchall()
    conn.close()
    return results



# -------------------------------------------------------------
# Adding Students Schedule to database
# -------------------------------------------------------------

# Inserting Schedule for Student
def add_student_schedule(student_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()

    # Get next schedule_id
    cur.execute("SELECT MAX(schedule_id) FROM Student_Schedule;")
    result = cur.fetchone()
    next_id = (result[0] + 1) if result[0] is not None else 1

    # Insert schedule
    query = """
        INSERT INTO Student_Schedule (schedule_id, student_id)
        VALUES (?, ?);
    """
    cur.execute(query, (next_id, student_id))

    conn.commit()
    conn.close()
    print(next_id)
    return next_id     # return schedule_id
#add_student_schedule(1)

# Inserting the each semester into the schedule
def add_schedule_semester(schedule_id, name):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()

    # Get next semester_id
    cur.execute("SELECT MAX(semester_id) FROM Schedule_Semesters;")
    result = cur.fetchone()
    next_id = (result[0] + 1) if result[0] is not None else 1

    # Insert semester
    query = """
        INSERT INTO Schedule_Semesters (semester_id, schedule_id, name)
        VALUES (?, ?, ?);
    """
    cur.execute(query, (next_id, schedule_id, name))

    conn.commit()
    conn.close()
    print(next_id)
    return next_id     # return semester_id
# add_schedule_semester(1, "Fall 2025")

# Inserting the courses into the semesters
def add_semester_course(semester_id, course_id):
    conn = get_db_connection()
    if not conn:
        return []

    cur = conn.cursor()

    query = """
        INSERT INTO Semester_Courses (semester_id, course_id)
        VALUES (?, ?);
    """
    try:
        cur.execute(query, (semester_id, course_id))
    except Exception as e:
        conn.close()
        return f"Error: {e}"

    conn.commit()
    conn.close()
    return 1     # success
# add_semester_course(1, 2)
# add_semester_course(1, 5)
# add_semester_course(1, 21)
# add_semester_course(1, 40)

# -------------------------------------------------------------
# Return Schedule id based on student id
# -------------------------------------------------------------
def get_student_schedule(student_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()
    query = """
        SELECT schedule_id FROM Student_Schedule WHERE student_id = ?;
    """
    cur.execute(query, (student_id,))
    results = cur.fetchall()
    conn.close()
    return results
#get_student_schedule(1)

# -------------------------------------------------------------
# Delete students schedule based on schedule id
# -------------------------------------------------------------
def delete_schedule(schedule_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()

    query = """ SELECT semester_id FROM Schedule_Semesters WHERE schedule_id = ?;"""
    cur.execute(query, (schedule_id,))
    semesters = cur.fetchall()
    for semester_id in semesters:
        query2 = """ DELETE FROM Semester_Courses WHERE semester_id = ?;"""
        cur.execute(query2, (semester_id,))
    query1 = """
        DELETE FROM Student_Schedule WHERE schedule_id = ?;
    """
    cur.execute(query1, (schedule_id,))
    conn.commit()
    conn.close()
    return 1


# -------------------------------------------------------------
# Get full schedule with semesters + courses for a student
# -------------------------------------------------------------
def get_student_full_schedule(student_id):
    conn = get_db_connection()
    if not conn:
        return None

    cur = conn.cursor()

    cur.execute(
        "SELECT schedule_id FROM Student_Schedule WHERE student_id = ?;",
        (student_id,)
    )
    schedule = cur.fetchone()
    if not schedule:
        conn.close()
        return None

    schedule_id = schedule[0]

    cur.execute(
        "SELECT semester_id, name FROM Schedule_Semesters WHERE schedule_id = ?;",
        (schedule_id,)
    )
    semesters_raw = cur.fetchall()

    if not semesters_raw:
        conn.close()
        return None

    schedule_data = []

    for sem_id, sem_name in semesters_raw:
        cur.execute("""
            SELECT c.course_code, c.course_name, c.credits
            FROM Semester_Courses sc
            JOIN Course c ON sc.course_id = c.course_id
            WHERE sc.semester_id = ?;
        """, (sem_id,))
        courses = cur.fetchall()

        schedule_data.append({
            "name": sem_name,
            "courses": courses
        })

    conn.close()
    return schedule_data

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
