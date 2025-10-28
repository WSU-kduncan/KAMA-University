-- This script creates all the tables for the database
-- You should only need to run this once
DROP DATABASE IF EXISTS kama;
CREATE DATABASE kama;
USE kama;

-- ======================
-- 1. PROGRAMS
-- ======================
CREATE TABLE Program (
    program_id INT PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL,
    degree_type VARCHAR(20) NOT NULL,
    creditHours INT NOT NULL
);

-- ======================
-- 2. REQUIREMENTS
-- ======================
CREATE TABLE Requirement (
    requirement_id INT PRIMARY KEY,
    requirement_type VARCHAR(50),     
    min_credits INT
);

-- ======================
-- 2. Connects all the Requirments that each Program has
-- ======================
CREATE TABLE Program_Requirements (
    program_id INT NOT NULL,
    requirement_id INT NOT NULL,
    PRIMARY KEY (program_id, requirement_id),
    FOREIGN KEY (program_id) REFERENCES Program(program_id),
    FOREIGN KEY (requirement_id) REFERENCES Requirement(requirement_id)
);

-- ======================
-- 3. COURSES
-- ======================
CREATE TABLE Course (
    course_id INT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    prereq VARCHAR(50)
);


-- ======================
-- 4. REQUIREMENT_COURSE: Matches what courses meet a requirement
-- ======================
CREATE TABLE Requirement_Course (
    requirement_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (requirement_id, course_id),
    FOREIGN KEY (requirement_id) REFERENCES Requirement(requirement_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);



-- ======================
-- 7. ADVISOR
-- ======================
CREATE TABLE Advisor (
    advisor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    office_number VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

-- ======================
-- 8. STUDENT
-- ======================
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    NumYears INT NOT NULL,
    NumCoOps INT NOT NULL,
    SummerSemester VARCHAR(3) NOT NULL,
    CrdtHrsPrSem INT NOT NULL,
    advisor_id INT NULL,
    FOREIGN KEY (advisor_id) REFERENCES Advisor(advisor_id)
);

-- ======================
-- 9. ADMIN
-- ======================
CREATE TABLE Admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- ======================
-- 10. STUDENTPROGRAM
-- ======================
CREATE TABLE StudentProgram (
    student_id INT,
    program_id INT,
    PRIMARY KEY (student_id, program_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (program_id) REFERENCES Program(program_id)
);

-- ======================
-- 11. STUDENT_SCHEDULE
-- ======================
CREATE TABLE Student_Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    semester_number INT NOT NULL,
    semester_name VARCHAR(20),
    year_number INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

-- ======================
-- 12. STUDENT_SCHEDULE_COURSE
-- ======================
CREATE TABLE Student_Schedule_Course (
    schedule_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (schedule_id, course_id),
    FOREIGN KEY (schedule_id) REFERENCES Student_Schedule(schedule_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- View all tables
SHOW TABLES;
