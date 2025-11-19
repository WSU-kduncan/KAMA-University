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
    prereq INT
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
    office_name VARCHAR(20) NOT NULL,
    office_num INT NOT NULL,
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
    NumYears INT NULL,
    NumCoOps INT NULL,
    SummerSemester VARCHAR(3) NULL,
    CrdtHrsPrSem INT NULL,
    advisor_id INT NOT NULL,
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
    office_name VARCHAR(50),
    office_num INT, 
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

-- STUDENT SCHEDULE
CREATE TABLE Student_Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);




-- Semesters that go into a specific schedule
CREATE TABLE Schedule_Semesters (
    semester_id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (schedule_id) REFERENCES Student_Schedule(schedule_id)
);

-- Courses that go into a specific semester inside of a schedule
CREATE TABLE Semester_Courses (
    semester_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (semester_id, course_id),
    FOREIGN KEY (semester_id)
        REFERENCES Schedule_Semesters(semester_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);



-- This script will insert all data for the program info
-- Courses
-- F = Fall
-- S = Spring
-- Q = Summer



INSERT IGNORE INTO Course (course_id, course_code, semester, course_name, credits, prereq) VALUES
(1, 'ENG 1100', 'FSQ', 'Academic Writing and Reading', 3, NULL),
(2, 'ENG 2100', 'FSQ', 'Research Writing and Argumentation', 3, 1),
(3, 'HST 1500', 'FSQ', 'Introduction to Greek and Roman Culture', 3, NULL),
(4, 'ART 2140', 'FSQ', 'Themes in Visual Culture', 4, NULL),
(5, 'STT 1600', 'FSQ', 'Statistical Concepts', 4, NULL),
(6, 'UVC 1010', 'FS', 'First Year Seminar', 3, NULL),
(7, 'LA 1020', 'FSQ', 'First-Year Seminar: College of Liberal Arts', 3, NULL),
(8, 'PSY 1010', 'FSQ', 'Intro to Psychology', 4, NULL),
(9, 'PSY 1010L', 'FSQ', 'Intro to Psychology/L', 0, 8),
(10, 'EC 2900', 'FSQ', 'Global Economic, Business and Social Issues', 3, NULL),
(11, 'BIO 1150/L', 'FSQ', 'Biology of Food', 4, NULL),
(12, 'PHY 1110/L,R', 'FSQ', 'Principles of Physics', 5, NULL),
(13, 'PHY 2400', 'FSQ', 'General Physics 1', 4, 16),
(14, 'PHY 2400L', 'FSQ', 'General Physics Lab', 0, 13),
(15, 'PHY 2400R', 'FSQ', 'General Physics Recitation', 0, 13),
(16, 'MTH 2300', 'FSQ', 'Calculus I', 4, NULL),
(17, 'SOC 3410', 'FQ', 'Research Methods', 3, NULL),
(18, 'URS 4280', 'F', 'CJ Organization and Management', 3, NULL),
(19, 'SOC 3700', 'F', 'Criminology', 3, NULL),
(20, 'SOC 4700 IW', 'F', 'Explaining Crime', 3, NULL),
(21, 'PLS 4400', 'F', 'Constitutional Law', 3, NULL),
(22, 'PSY 2810', 'FS', 'Psychology of Incarceration', 3, 8),
(23, 'SOC 3210', 'S', 'Deviance', 3, NULL),
(24, 'PSY 2520', 'FS', 'Forensic Psychology', 3, 8),
(25, 'PLS 3410', 'S', 'Fundamentals of Criminal Investigation', 3, NULL),
(26, 'PLS 4150', 'F', 'Law, Lawyers, and the Legal System', 3, NULL),
(27, 'SOC 3620', 'S', 'Race and Ethnicity', 3, NULL),
(28, 'SOC 4600 IW', 'F', 'Sociology of Sexuality', 3, NULL),
(29, 'PSY 2910', 'S', 'Drugs and Behavior', 3, 8),
(30, 'PSY 3510', 'FSQ', 'Social Psychology', 3, 8),
(31, 'PHL 3110', 'F', 'Ethics', 3, NULL),
(32, 'ASL 1010', 'FSQ', 'Beginner American Sign Language I', 4, NULL),
(33, 'ASL 1020', 'FSQ', 'Beginner American Sign Language II', 4, 32),
(34, 'ASL 2010', 'FSQ', 'Intermediate American Sign Language I', 4, 33),
(35, 'ASL 2020', 'FSQ', 'Intermediate American Sign Language II', 4, 34),
(36, 'PHL 3000', 'FSQ', 'Critical Thinking', 3, NULL),
(37, 'PLS 3100', 'FS', 'Quantitative Methods', 3, NULL),
(38, 'PSY 3010/L', 'FSQ', 'Research Methods in Psychology I and Lab', 4, 8),
(39, 'PSY 3020/L', 'FSQ', 'Research Methods in Psychology II and Lab', 4, 38),
(40, 'PSY 3710', 'FSQ', 'Perception', 3, 8),
(41, 'PSY 3910', 'FSQ', 'Behavioral Neuroscience I', 3, 8),
(42, 'PSY 3410', 'FSQ', 'Lifespan Development Psychology', 3, 8),
(43, 'PSY 3090', 'FSQ', 'Psychology of Health Behaviors', 3, 8),
(44, 'PSY 3070', 'FS', 'Tests and Measures', 3, 38),
(45, 'PSY 2020', 'FSQ', 'Careers in Psychology', 1, NULL),
(46, 'PSY 4520', 'FS', 'Advanced Topics in Prejudice Research', 3, 39),
(47, 'PSY 4650', 'F', 'Mind and Environment Capstone', 3, 39),
(48, 'PSY 2160', 'FSQ', 'Counseling Psychology', 3, 8),
(49, 'PSY 2580', 'FSQ', 'Profiling and Serial Crimes', 3, 8),
(50, 'SOC 2000', 'FSQ', 'Introduction to Sociology', 3, NULL),
(51, 'PLS 4440', 'F', 'Methods of Crime Scene Investigation', 3, NULL),
(52, 'CoOp', 'FSQ', 'CoOp', -1, NULL);


INSERT INTO Program(program_id, program_name, degree_type, creditHours) VALUES
(1, 'Psychology', 'Major', 120),
(2, 'Criminal Justice', 'Major', 120),
(3, 'Sociology', 'Minor', 18),
(4, 'Forensic Studies', 'Minor', 18);



INSERT IGNORE INTO Requirement (requirement_id, requirement_type, min_credits) VALUES
(2, 'Core A', 6),
(3, 'Core B', 3),
(4, 'Core C(Art)', 3),
(5, 'Core C(His)', 3),
(6, 'Core D', 6),
(7, 'Core Extra', 7),
(8, 'GI', 3),
(9, 'IE', 6),
(10, 'IW', 9),
(11, 'PSY-Core 1', 6),
(12, 'PSY-Core 2', 6),
(13, 'PSY-Core 3', 6),
(14, 'PSY-Seminar', 6),
(15, 'PSY-Electives', 14),
(16, 'Foreign Language', 12),
(18, 'CJ-Core', 15),
(19, 'FA 1', 6),
(20, 'FA 2', 6),
(21, 'FA 3', 3),
(22, 'FA 4', 6),
(23, 'ADV', 9),

(25, 'CJ Classes', 13),
(26, 'PSY Classes', 22),
(28, 'SOC Core', 3),
(29, 'SOC Electivs', 15),
(31, 'FOR Core', 6),
(32, 'FOR Science', 3),
(33, 'FOR Electives', 9),
(34, 'Core E', 9);



INSERT IGNORE INTO Requirement_Course(requirement_id, course_id)VALUES
(2, 1),
(2, 2),
(3, 5),
(4, 4),
(5, 5),
(6, 8),
(6, 9),
(6, 10),
(7, 13),
(7, 14),
(7, 15),
(7, 16), 
(34, 11),
(34, 12),
(8, 10),
(8, 3),
(9, 10),
(9, 8),
(10, 46),
(10, 47),
(10, 38),
(10, 8),
(10, 10),
(10, 20),
(10, 28);


INSERT IGNORE INTO Requirement_Course(requirement_id, course_id)VALUES
(26, 6),
(26, 1),
(26, 5),
(26, 8),
(26, 9),
(26, 38),
(26, 39),
(26, 45),
(11, 40),
(11, 41),
(12, 42),
(13, 43),
(13, 44),
(14, 46),
(14, 47),
(15, 48),
(15, 49),
(15, 29),
(15, 24),
(15, 22);





INSERT IGNORE INTO Requirement_Course(requirement_id, course_id)VALUES
(18, 18),
(18, 19),
(18, 20),
(18, 21),
(18, 17),
(19, 22),
(19, 23),
(20, 24),
(20, 25),
(21, 26),
(22, 27),
(22, 28),
(23, 29),
(23, 30),
(23, 31),
(16, 32),
(16, 33),
(16, 34),
(16, 35),
(25, 7),
(25, 5),
(25, 36),
(25, 37);

INSERT IGNORE INTO Requirement_Course(requirement_id, course_id)VALUES
(28, 17),
(29, 19),
(29, 20),
(29, 23),
(29, 27),
(29, 28),
(29, 50);

INSERT IGNORE INTO Requirement_Course(requirement_id, course_id)VALUES
(31, 25),
(31, 51),
(32, 12),
(32, 13),
(33, 24),
(33, 25),
(33, 23),
(33, 19),
(33, 18);

INSERT IGNORE INTO Program_Requirements(program_id, requirement_id)VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 26);

INSERT IGNORE INTO Program_Requirements(program_id, requirement_id)VALUES
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 16),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22),
(2, 23),
(2, 24),
(2, 25);

INSERT IGNORE INTO Program_Requirements(program_id, requirement_id)VALUES
(3, 27),
(3, 28),
(3, 29),
(3, 30);

INSERT IGNORE INTO Program_Requirements(program_id, requirement_id)VALUES
(4, 27),
(4, 31),
(4, 32),
(4, 33);



-- This Script will insert all user data
-- You only need to run this once
-- Admin
INSERT INTO Admin (admin_id, first_name, last_name, username, password, email, office_name, office_num) VALUES
(1, 'Lowdy', 'Laker', 'lowdylkr', 'LowdyLake24&', 'LLaker.1@KAMA.edu', 'Willsii Hall', 321),
(2, 'Rowdy', 'Raider', 'rowdyrdr', 'RowdyRad617#', 'RRaider.1@KAMA.edu', 'Lateralis Wing', 021);

-- Advisors
INSERT INTO Advisor (advisor_id, first_name, last_name, email, username, password, office_name, office_num) VALUES
(1, 'Calum', 'Oust', 'COust.1@KAMA.edu', 'calumous', 'CalumOut%10%', 'Brookesia Hall', 248),
(2, 'Miles', 'Pardalis', 'MPardalis@KAMA.edu', 'milespar', 'Milespara11!', 'Chamaeleo Complex', 172),
(3, 'Oliver', 'Meller', 'OMeller.1@KAMA.edu', 'oliverme', 'OliverMe1234@', 'Kinyongia Hall', 089);

-- Students
INSERT INTO Student (student_id, first_name, last_name, email, username, password, NumYears, NumCoOps, SummerSemester, CrdtHrsPrSem, advisor_id) VALUES
(1, 'Jackson', 'Vail', 'JVail.1@KAMA.edu', 'jacksonv', 'JacksonV123!', 4, 0, 'no', 18, 1),
(2, 'Perry', 'Soni', 'PSoni.1@KAMA.edu', 'perryson', 'PerrySon@456', 4, 0, 'no', 18, 1),
(3, 'Fischer', 'Ray', 'FRay.1@KAMA.edu', 'fischerr', 'FischerR*909', 4, 0, 'no', 18, 2),
(4, 'Panthera', 'Leon', 'PLeon.1@KAMA.edu', 'panthera', 'PantheraL23?', 4, 0, 'no', 18, 2),
(5, 'Elliot', 'Cross', 'ECross.1@KAMA.edu', 'elliotcr', 'ElliotC501!?', 4, 0, 'no', 18, 2),
(6, 'Hue', 'Varin', 'HVarin@KAMA.edu', 'huevarin', 'HueVarin#890', NULL, NULL, NULL, NULL, 3);

INSERT INTO studentprogram(student_id, program_id)VALUES
-- 1 Major, 1 Minor
(1, 2),
(1, 3),
-- 1 Major, 2 Minors
(2, 1),
(2, 3),
(2, 4),
-- 2 Majors, 1 Minor
(3, 1),
(3, 2),
(3, 3),
-- 2 Majors
(4, 1),
(4, 2),
-- 2 Majors, 2 Minors
(5, 1),
(5, 2),
(5, 3),
(5, 4);







