from flask import Flask, render_template, request, redirect, url_for, session
from authentication import authenticate

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role, name = authenticate(username, password)

        if role in ["student", "faculty", "admin"]:
            session['name'] = name
            session['role'] = role
            return redirect(url_for('loading'))
        else:
            return render_template("login.html", error="Incorrect Username or Password. Please Try Again.")
    
    return render_template("login.html")

@app.route('/loading')
def loading():
    name = session.get('name', '')
    role = session.get('role', '')
    if not role:
        return redirect(url_for('login'))
    return render_template('loading.html', name=name, role=role)

@app.route('/student')
def student_dashboard():
    name = session.get('name', '')
    if session.get('role') != 'student':
        return redirect(url_for('login'))
    return render_template("student.html", name=name)

@app.route('/faculty')
def faculty_dashboard():
    name = session.get('name', '')
    if session.get('role') != 'faculty':
        return redirect(url_for('login'))
    return render_template("faculty.html", name=name)

@app.route('/admin')
def admin_dashboard():
    name = session.get('name', '')
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template("admin.html", name=name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5050)

