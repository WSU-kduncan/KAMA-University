
a KAMA University - Degree Admin
## Overview
rs/minors)
- Modify Schedule preferences (Co-Ops, Summer Semesters, Amount of Semesters)
- Access course lists and semester information
- Display student data (credits, years, preferences, etc.)

### Faculty Dashboard
- Update course details or grades  
- Display name dynamically based on login  

### Admin Dashboard
- Manage programs, users, and course data  
- Add, update, or remove courses

---

## ⚙️ Tech Stack
| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Flask) |
| **Database** | MariaDB |
| **Tools** | GitHub, GitHub Pages, DBeaver |

---

## Project Structure
```

KAMA-University/
│
├── app.py
├── authentication.py
├── Functions.py
├── Course.py
├── GenerateSche# KAMA University - Degree Admin
## Overview

**KAMA University** is a multi-role, full-stack academic management system designed for students, faculty, and administrators.
It incorporates authentication, personalized dashboards, automated schedule generation, and database-driven student program and information tracking.

Built using **Flask (Python)**, **JavaScript**, **HTML/CSS**, and **MariaDB**, this project demonstrates full-stack development, database design, UI/UX collaboration, and modular code architecture.

---

## Team Members
- **Kalli Koppin** - UI/UX Lead
- **Ava McIntosh.** - Database Administrator
- **Morgan Hunt.** - Algorithms Lead
- **Austin K.** – Authentication & Testing

---

## Features
### Student Dashboard
- View all registereddule.py
├── Schedule.py
├── Term.py
├── setup.sh                     # setup script <3
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── loading.html
│   ├── student.html
│   ├── faculty.html
│   └── admin.html
│
├── database/
│   ├── databaseScript.sql
│
├── static/
│   ├── bell.png
│   ├── chameleon.png
│   ├── loading.png
│   ├── KAMA Chameleon.mp3
│   ├── facts.txt
│   ├── loading.js
│   ├── student.js
│   ├── allCourses.js
│   ├── faculty.js
│   ├── admin.js
│   ├── manageCourses.js
│   ├── style.css
│
├── venv/                      # Local Python environment
│
└── README.md

```

## Setup Instructions

**Below is the full setup process for running KAMA University – Degree Admin locally.**

---

### Clone the Repository
```bash
git clone https://github.com/<your-username>/degree-admin.git
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

### Database Setup

1. Install DBeaver Community
- https://dbeaver.io/download/

2. Install mariaDB 
   - Windows: https://mariadb.org/download/?t=mariadb&p=mariadb&r=12.0.2&os=windows&cpu=x86_64&pkg=msi&mirror=acorn
   
   - Mac:
      ```bash
       - 'brew install mariadb'
       - 'brew services start mariadb'
        ```
   - Linux:
   ```bash
       - 'sudo apt update'
       - 'sudo apt install mariadb-server'
       - 'sudo systemctl start mariadb'
       - 'sudo systemctl enable mariadb'
    ```

3. Create DBeaver Database
    1. Open DBeaver
    2. Slightly left from the top middle click Database
    3.  Click New Database Connection
    4.  Choose MariaDB and hit next
    5.  In the Database box write "Kama"
    6.  In the password box write "password"
    7.  Click Test Connection
    8.  If connection goes through click Finish
    9.  Run the databaseScript.sql in MariaDB

4. Connection
1. Run the connection.py script
2. Database should be connected!

5. Run Flask Application

Run this python command in your terminal where `app.py` is located
```bash
python3 app.py
```

Application should start and you should be able to click the link that pops up.
**KAMA University** is a multi-role web application designed to simplify academic management for students, faculty, and administrators.  
It provides secure login-based dashboards, enabling different users to access features tailored to their roles.

Built with **Flask (Python)** and **Javascript** for the backend, **HTML/CSS** for the frontend, and **MariaDB** for database management, this project demonstrates full-stack integration and modular development principles.

---

## Team Members
- **Kalli Koppin**
- **Ava Mcintosh**
- **Morgan Hunt**
- **Austin Kellough**

---

## Features
### Student Dashboard
- View enrolled courses and semester information for major(s) and/or minor (s) 
- Access student information

### Faculty Dashboard
- Approve or deny student requests based on schedules or co-op/summer courses

---

## Tech Stack
| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS |
| **Backend** | Python (Flask), Javascript |
| **Database** | MariaDB |
| **Version Control & Deployment** | GitHub + GitHub Pages |

---

## Project Structure
```
KAMA-University/
│
├── app.py
├── authentication.py
├── Functions.py
├── Course.py
├── GenerateScheduke.py
├── Schedule.py
├── Term.py
├── setup.sh                     # setup script <3
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── loading.html
│   ├── student.html
│   ├── faculty.html
│   └── admin.html
│
├── database/
│   ├── databaseScript.sql
│
├── static/
│   ├── bell.png
│   ├── chameleon.png
│   ├── loading.png
│   ├── KAMA Chameleon.mp3
│   ├── facts.txt
│   ├── loading.js
│   ├── student.js
│   ├── allCourses.js
│   ├── faculty.js
│   ├── admin.js
│   ├── manageCourses.js
│   ├── style.css
│
├── venv/                      # local Python environment
│
└──  README.md

```

## Setup Instructions

**Follow these steps to set up and run the **KAMA University - Degree Admin** project locally.**

---

### Clone the Repository

**HTTPS Cloning**
```bash
git clone https://github.com/WSU-kduncan/KAMA-University.git
cd KAMA-University
```

**SSH Cloning**
```bash
git clone git@github.com:WSU-kduncan/KAMA-University.git
cd KAMA-University
```

### Create Virtual Python Enviorment

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
mysql -u root
```

**Create the Database Server**
```sql
CREATE SERVER KAMA
FOREIGN DATA WRAPPER mariadb
OPTIONS (
HOST 'localhost',
USER 'root',
PASSWORD 'password',
PORT '3306');
```

**Connect to the MariaDb Shell**
```mariadb -u root```

**Inside the MariaDB shell:**
```sql
SOURCE databaseScript.sql;
EXIT;
```

### Configure Database Connection

**Open the `connection.py` file in your editor and ensure the credentials match your local MariaDB setup.**

### Run the Flask Application

**Staying in the main directory where app.py is, run the application**

```bash
python app.py
```
