from flask import Flask, render_template, request, redirect, url_for, session
from authentication import authenticate
from Functions import (
    get_student_data,
    get_student_programs,
    get_program_requirements,
    get_requirement_courses,
    get_user_data_by_username
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

    # get emails
    student_email = user_data['data'][3] if len(user_data['data']) > 3 else "N/A"

    # get major and minor from get_student_programs()
    major_name = None
    minor_name = None
    for prog in programs:
        if prog[2].lower() == "major":
            major_name = prog[1]
        elif prog[2].lower() == "minor":
            minor_name = prog[1]

    # defaults
    major_name = major_name or "N/A"
    minor_name = minor_name or "N/A"
    grad_date = "TBD"  # Placeholder (no schema changes)

    # get program/requirement data
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

    # send all data to template
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
    name = session.get('name', '')
    if session.get('role') != 'faculty':
        return redirect(url_for('login'))
    return render_template("faculty.html", name=name)


# -------------------------------------------------------------
# ADMIN DASHBOARD
# -------------------------------------------------------------
@app.route('/admin')
def admin_dashboard():
    name = session.get('name', '')
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template("admin.html", name=name)


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

