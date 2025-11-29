from flask import Flask, render_template, request, redirect, url_for, session
import Functions
from authentication import authenticate
from GenerateSchedule import GenerateSchedule
from Functions import (
    get_student_data,
    get_student_programs,
    get_program_requirements,
    get_requirement_courses,
    get_user_data_by_username,
    get_courses_for_display,
    get_student_schedule,
    get_student_full_schedule,
    get_students_for_advisor
)

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# -------------------------------------------------------------
# HOME ROUTE
# -------------------------------------------------------------
@app.route('/')
def home():
    return render_template("index.html")


# -------------------------------------------------------------
# LOGIN ROUTE
# -------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        role, name = authenticate(username, password)

        if role in ["student", "faculty", "admin"]:
            session['username'] = username
            session['name'] = name
            session['role'] = role
            return redirect(url_for('loading'))
        else:
            return render_template(
                "login.html",
                error="Incorrect Username or Password. Please Try Again."
            )

    return render_template("login.html")


# -------------------------------------------------------------
# LOADING ROUTE
# -------------------------------------------------------------
@app.route('/loading')
def loading():
    name = session.get('name', '')
    role = session.get('role', '')

    if not role:
        return redirect(url_for('login'))

    return render_template('loading.html', name=name, role=role)


# -------------------------------------------------------------
# STUDENT DASHBOARD
# -------------------------------------------------------------
@app.route('/student')
def student_dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    username = session.get('name')
    user_data = get_user_data_by_username(session.get('username'))

    if not user_data:
        return render_template("student.html", name=username, error="Student data not found")

    # Student ID
    student_id = user_data['data'][0]

    # Student core data
    student = get_student_data(student_id)
    programs = get_student_programs(student_id)

    # Email
    student_email = user_data['data'][3] if len(user_data['data']) > 3 else "N/A"

    # Majors & minors
    major_names = []
    minor_names = []

    for prog in programs:
        if prog[2].lower() == "major":
            major_names.append(prog[1])
        elif prog[2].lower() == "minor":
            minor_names.append(prog[1])

    major_name = ", ".join(major_names) if major_names else "N/A"
    minor_name = ", ".join(minor_names) if minor_names else "N/A"

    grad_date = "TBD"

    # Requirements + course lists
    program_data = []
    for program in programs:
        program_id = program[0]
        requirements = get_program_requirements(program_id)

        req_list = []
        for req in requirements:
            courses = get_requirement_courses(req[0])
            req_list.append({
                'requirement': req,
                'courses': courses
            })

        program_data.append({
            'program': program,
            'requirements': req_list
        })

    schedule_data = get_student_full_schedule(student_id)

    return render_template(
        "student.html",
        name=username,
        student=student,
        student_email=student_email,
        major_name=major_name,
        minor_name=minor_name,
        grad_date=grad_date,
        data=program_data,
        schedule=schedule_data
    )

# -------------------------------------------------------------
# UPDATE SUMMER SEMESTER PREFERENCE
# -------------------------------------------------------------
@app.route('/student/update_summer', methods=['POST'])
def update_summer():
    if session.get('role') != 'student':
        return {"status": "error", "message": "Unauthorized"}, 403

    user = get_user_data_by_username(session.get('username'))
    student_id = user['data'][0]

    data = request.get_json()
    summer_value = data.get("summer", "no")

    conn = Functions.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Student
        SET SummerSemester = ?
        WHERE student_id = ?;
    """, (summer_value, student_id))

    conn.commit()
    conn.close()

    return {"status": "success"}

# -------------------------------------------------------------
# UPDATE NUMBER OF COOPS
# -------------------------------------------------------------
@app.route('/student/update_coops', methods=['POST'])
def update_coops():
    if session.get('role') != 'student':
        return {"status": "error", "message": "Unauthorized"}, 403

    user = get_user_data_by_username(session.get('username'))
    student_id = user['data'][0]

    data = request.get_json()
    coops = int(data.get("coops", 0))

    if coops < 0 or coops > 3:
        return {"status": "error", "message": "Invalid range"}, 400

    conn = Functions.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Student
        SET NumCoOps = ?
        WHERE student_id = ?;
    """, (coops, student_id))

    conn.commit()
    conn.close()

    return {"status": "success"}



# -------------------------------------------------------------
# GENERATE SCHEDULE FOR STUDENT
# -------------------------------------------------------------
@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    if session.get('role') != 'student':
        return redirect(url_for('login'))

    # Get student ID from session username
    user_data = get_user_data_by_username(session.get('username'))
    student_id = user_data['data'][0]

    # 1. Check if a schedule already exists and delete it
    existing = get_student_schedule(student_id)
    if existing:
        schedule_id = existing[0][0]
        from Functions import delete_schedule
        delete_schedule(schedule_id)

    # 2. Generate new schedule (THIS RUNS your debug-enabled GenerateSchedule.py)
    scheduler = GenerateSchedule(student_id)
    result = scheduler.begin_generation()

    # 3. If generation failed, report it
    if result != 0:
        return "Schedule generation failed", 500

    # 4. Save to the database
    scheduler.schedule.add_schedule_to_database()

    return redirect(url_for('student_dashboard'))



# -------------------------------------------------------------
# FACULTY DASHBOARD
# -------------------------------------------------------------
@app.route('/faculty')
def faculty_dashboard():
    if session.get('role') != 'faculty':
        return redirect(url_for('login'))

    username = session.get('username')
    name = session.get('name')

    user_data = get_user_data_by_username(username)

    if not user_data:
        return render_template("faculty.html", name=name, error="Advisor data not found")

    advisor_record = user_data['data']

    advisor = {
        "id": advisor_record[0],
        "first": advisor_record[1],
        "last": advisor_record[2],
        "email": advisor_record[7],
        "office_name": advisor_record[5],
        "office_num": advisor_record[6]
    }

    students = get_students_for_advisor(advisor["id"])

    return render_template("faculty.html", name=name, advisor=advisor, students=students)

@app.route('/faculty/student/<int:student_id>/schedule')
def faculty_view_schedule(student_id):
    if session.get('role') != 'faculty':
        return redirect(url_for('login'))

    # Get basic student info
    schedule = get_student_full_schedule(student_id)   # already imported
    user = get_student_data(student_id)

    if not schedule:
        return render_template("faculty_schedule.html",
                               student=user,
                               schedule=None,
                               message="No schedule exists for this student yet.")

    return render_template("faculty_schedule.html",
                           student=user,
                           schedule=schedule)


# -------------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------------
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    username = session.get('username')
    name = session.get('name')

    user_data = get_user_data_by_username(username)

    if not user_data:
        return render_template("admin.html", name=name, error="Admin data not found")

    rec = user_data['data']

    admin = {
        "id": rec[0],
        "first": rec[1],
        "last": rec[2],
        "email": rec[7],
        "office_name": rec[5],
        "office_num": rec[6]
    }

    return render_template("admin.html", name=name, admin=admin)

# -------------------------------------------------------------
# MANAGE COURSES PAGE
# -------------------------------------------------------------
@app.route('/manage-courses')
def manage_courses():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    from Functions import get_all_courses
    courses = get_all_courses()

    return render_template("manageCourses.html", courses=courses)

# -------------------------------------------------------------
# MANAGE COURSES PAGE (ADD)
# -------------------------------------------------------------
@app.route('/add-course', methods=['POST'])
def add_course_route():
    if session.get('role') != 'admin':
        return {"success": False, "error": "Unauthorized"}, 403

    from Functions import add_course

    data = request.json
    course_id = data.get("id")
    semester = data.get("semester")
    course_code = data.get("code")
    course_name = data.get("name")
    credits = data.get("credits")

    success = add_course(course_id, semester, course_code, course_name, credits)
    return {"success": success}

# -------------------------------------------------------------
# MANAGE COURSES PAGE (DELETE)
# -------------------------------------------------------------
@app.route('/delete-course', methods=['POST'])
def delete_course_route():
    if session.get('role') != 'admin':
        return {"success": False, "error": "Unauthorized"}, 403

    from Functions import delete_course

    data = request.json
    course_id = data.get("course_id")

    success = delete_course(course_id)
    return {"success": success}

# -------------------------------------------------------------
# ALL COURSES PAGE
# -------------------------------------------------------------
@app.route('/all-courses')
def all_courses():
    if 'role' not in session:
        return redirect(url_for('login'))

    courses = get_courses_for_display()
    return render_template("allCourses.html", courses=courses)


# -------------------------------------------------------------
# LOGOUT
# -------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# -------------------------------------------------------------
# MAIN ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5050)
