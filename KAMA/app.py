from flask import Flask, render_template, request, redirect, url_for, session
from authentication import authenticate
from Functions import (
    get_student_data,
    get_student_programs,
    get_program_requirements,
    get_requirement_courses,
    get_user_data_by_username,
    get_courses
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

    student_id = user_data['data'][0]
    student = get_student_data(student_id)
    programs = get_student_programs(student_id)

    # email
    student_email = user_data['data'][3] if len(user_data['data']) > 3 else "N/A"

    # majors & minors
    major_names = []
    minor_names = []

    for prog in programs:
        if prog[2].lower() == "major":
            major_names.append(prog[1])
        elif prog[2].lower() == "minor":
            minor_names.append(prog[1])

    major_names = major_names or ["N/A"]
    minor_names = minor_names or ["N/A"]

    major_name = ", ".join(major_names)
    minor_name = ", ".join(minor_names)
    grad_date = "TBD"

    # requirements + courses
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

    return render_template(
        "student.html",
        name=username,
        student=student,
        student_email=student_email,
        major_name=major_name,
        minor_name=minor_name,
        grad_date=grad_date,
        data=program_data
    )


# -------------------------------------------------------------
# FACULTY DASHBOARD
# -------------------------------------------------------------
@app.route('/faculty')
def faculty_dashboard():
    if session.get('role') != 'faculty':
        return redirect(url_for('login'))
    name = session.get('name', '')
    return render_template("faculty.html", name=name)


# -------------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------------
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    name = session.get('name', '')
    return render_template("admin.html", name=name)


# -------------------------------------------------------------
# ALL COURSES PAGE
# -------------------------------------------------------------
@app.route('/all-courses')
def all_courses():
    if 'role' not in session:
        return redirect(url_for('login'))

    courses = get_courses()
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

