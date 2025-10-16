# KAMA University - Degree Admin
## Overview
**KAMA University** is a multi-role web application designed to simplify academic management for students, faculty, and administrators.  
It provides secure login-based dashboards, enabling different users to access features tailored to their roles.

Built with **Flask (Python)** for the backend, **HTML/CSS** for the frontend, and **MariaDB** for database management, this project demonstrates full-stack integration and modular development principles.

---

## Team Members
- **Kalli Koppin**
- **Ava M.**
- **Morgan H.**
- **Austin K.**

---

## Features
### Student Dashboard
- View enrolled courses and semester information  
- Access schedules  

### Faculty Dashboard
- Update course details or grades  
- Display name dynamically based on login  

### Admin Dashboard
- Manage programs, users, and course data  
- Add, update, or remove database entries  
- Oversee faculty and student records  

---

## ⚙️ Tech Stack
| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS |
| **Backend** | Python (Flask) |
| **Database** | MariaDB |
| **Version Control & Deployment** | GitHub + GitHub Pages |

---

## Project Structure
```
degree-admin/
│
├── app.py                      # Main Flask application (handles routes and role-based redirects)
├── authentication.py            # Authenticates users and determines their roles (student, faculty, admin)
├── connection.py                # Handles MariaDB connection setup
│
├── databaseScript.sql           # SQL file to create and populate tables
│
├── /templates/                  # HTML templates rendered by Flask
│   ├── index.html               # Homepage (team/project overview)
│   ├── login.html               # Login page with username/password form
│   ├── student.html             # Student dashboard (dynamic name, semester info)
│   ├── faculty.html             # Faculty dashboard (dynamic table, name display)
│   ├── admin.html               # Admin dashboard (manage users, programs, courses)
│   └── error.html               # (Optional) Error or 404 page
│
├── /static/                     # Static frontend assets
│   ├── style.css                # Central stylesheet (used by all pages)
│   ├── chameleon.png            # KAMA University logo
│   ├── bell.png                 # Notification icon
│
├── /venv/                       # Python virtual environment (not tracked in Git)
│
├── README.md                    # Project overview and setup guide
├── .gitignore                   # Ignore venv, __pycache__, and other unnecessary files

```

## Setup Instructions

**Follow these steps to set up and run the **KAMA University - Degree Admin** project locally.**

---

### Clone the Repository
```bash
git@github.com:WSU-kduncan/KAMA-University.git
cd degree-admin
```

### Create Virtual Enviorment

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Required Dependencies

Install Flask and MariaDB connector using pip.

```bash
pip install flask 
pip install mariadb
```

### Set Up the MariaDB Database
Ensure MariaDB is installed and running on your machine.

**macOS/Linux**
```bash
brew services start mariadb
```

**Windows**
```bash
sudo systemctl start mariadb
```


**Access MariaDB in the Terminal**
```bash
mysql -u root -p
```

**Create the Database**

**Inside the MariaDB shell:**

```sql
CREATE DATABASE kama;
USE kama;
SOURCE databaseScript.sql;
EXIT;
```

### Configure Database Connection

**Open the `connection.py` file in your editor and ensure the credentials match your local MariaDB setup.**

### Run the Flask Application

```bash
python app.py
```
