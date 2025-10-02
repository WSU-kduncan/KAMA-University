from flask import Flask, render_template, request, redirect, url_for
from authentication import authenticate

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")   # show team site

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = authenticate(username, password)

        if role == "student":
            return redirect(url_for('student_dashboard'))
        elif role == "faculty":
            return redirect(url_for('faculty_dashboard'))
        elif role == "admin":
            return redirect(url_for('admin_dashboard'))
        else:
            return "<h3> Wrong username or password</h3><a href='/login'>Try again</a>"
    return render_template("login.html")   

@app.route('/student')
def student_dashboard():
    return "<h1> Welcome Student!</h1>"

@app.route('/faculty')
def faculty_dashboard():
    return "<h1> Welcome Faculty!</h1>"

@app.route('/admin')
def admin_dashboard():
    return "<h1> Welcome Admin!</h1>"

if __name__ == "__main__":
    app.run(debug=True)

