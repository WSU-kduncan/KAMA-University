-- This script will insert all data for the program info
-- Programs
-- Program Requirements
-- Course Requirements
-- You should only need to run this once

-- Courses
-- F = Fall
-- S = Spring
-- Q = Summer
-- 
-- Department is the credit it accounts for
-- There is also the requirements table which 
INSERT IGNORE INTO Course (course_id, course_code, semester, course_name, credits, department) VALUES
(1, 'ENG 1100', 'FSPS', 'Academic Writing and Reading', 3, 'English Comp'),
(2, 'ENG 2100', 'FSPS', 'Research Writing and Argumentation', 3, 'English Comp'),
(3, 'HST 1500', 'FSPS', 'Introduction to Greek and Roman Culture', 3, 'Arts and Humanities (History)'),
(4, 'ART 2140', 'FSPS', 'Themes in Visual Culture', 4, 'Extra Arts & Humanities'),
(5, 'STT 1600', 'FSPS', 'Statistical Concepts', 4, 'Wright State Core Math'),
(6, 'UVC 1010', 'FS', 'First Year Seminar', 3, 'Wright State Core FYS'),
(7, 'LA 1020', 'FSS', 'First-Year Seminar: College of Liberal Arts', 3, 'First Year Seminar'),
(8, 'PSY 1010', 'FSS', 'Intro to Psychology', 4, 'Wright State Core Social Science'),
(9, 'PSY 1010L', 'FSS', 'Intro to Psychology/L', 0, 'Wright State Core Social Science'),
(10, 'EC 2900', '', 'Global Economic, Business and Social Issues', 0, 'Wright State Core Social Science'),
(11, 'BIO 1150/L', '', 'Biology of Food', 4, 'Wright State Core Natural Science'),
(12, 'PHY 1110/L,R', '', 'Principles of Physics', 5, 'Wright State Core Natural Science'),
(13, 'PHY 2400', '', 'General Physics 1', 4, 'Extra'),
(14, 'PHY 2400L', '', 'General Physics Lab', 1, 'Extra'),
(15, 'PHY 2400R', '', 'General Physics Recitation', 0, 'Extra'),
(16, 'MTH 2300', 'FSS', 'Calculus I', 4, 'Extra Core Credits'),
(17, 'SOC 3410', 'FSu', 'Research Methods', 3, ''),
(18, 'URS 4280', 'F', 'CJ Organization and Management', 3, 'CJS Core'),
(19, 'SOC 3700', 'F', 'Criminology', 3, 'CJS Core'),
(20, 'SOC 4700 IW', 'F', 'Explaining Crime', 3, 'CJS Core'),
(21, 'PLS 4400', 'F', 'Constitutional Law', 3, 'Core CJS'),
(22, 'PSY 2810', 'FS', 'Psychology of Incarceration', 3, 'FA #1'),
(23, 'SOC 3210', 'S', 'Deviance', 3, 'FA #1'),
(24, 'PSY 2520', 'FS', 'Forensic Psychology', 3, 'FA #2'),
(25, 'PLS 3410', 'S', 'Fundamentals of Criminal Investigation', 3, 'FA #2'),
(26, 'PLS 4150', 'F', 'Law, Lawyers, and the Legal System', 3, 'FA #3'),
(27, 'SOC 3620', 'S', 'Race and Ethnicity', 3, 'FA #4'),
(28, 'SOC 4600 IW', 'F', 'Sociology of Sexuality', 3, 'FA #4'),
(29, 'PSY 2910', 'S', 'Drugs and Behavior', 3, 'ADV CJS'),
(30, 'PSY 3510', 'FSS', 'Social Psychology', 3, 'ADV CJS'),
(31, 'PHL 3110', 'F', 'Ethics', 3, 'ADV CJS'),
(32, 'ASL 1010', '', 'Beginner American Sign Language I', 4, 'Foreign Language'),
(33, 'ASL 1020', '', 'Beginner American Sign Language II', 4, 'Foreign Language'),
(34, 'ASL 2010', '', 'Intermediate American Sign Language I', 4, 'Foreign Language'),
(35, 'ASL 2020', '', 'Intermediate American Sign Language II', 4, 'Foreign Language'),
(36, 'PHL 3000', 'FSS', 'Critical Thinking', 3, 'CoLA Methods'),
(37, 'PLS 3100', 'FS', 'Quantitative Methods', 3, 'CoLA Methods'),
(38, 'PSY 3010/L', 'FSS', 'Research Methods in Psychology I and Lab', 4, 'Department Core'),
(39, 'PSY 3020/L', 'FSS', 'Research Methods in Psychology II and Lab', 4, 'Department Core'),
(40, 'PSY 3710', 'FSS', 'Perception', 3, 'Department Core Row 1'),
(41, 'PSY 3910', 'FSS', 'Behavioral Neuroscience I', 3, 'Department Core Row 1'),
(42, 'PSY 3410', 'FSS', 'Lifespan Development Psychology', 3, 'Department Core Row 2'),
(43, 'PSY 3090', 'FSS', 'Psychology of Health Behaviors', 3, 'Department Core Row 3'),
(44, 'PSY 3070', 'FS', 'Tests and Measures', 3, 'Department Core Row 3'),
(45, 'PSY 2020', 'FSS', 'Careers in Psychology', 1, 'Department Core Career (1)'),
(46, 'PSY 4520', 'FS', 'Advanced Topics in Prejudice Research', 3, 'Department Seminar'),
(47, 'PSY 4650', 'F', 'Mind and Environment Capstone', 3, 'Department Seminar'),
(48, 'PSY 2160', 'FSS', 'Counseling Psychology', 3, 'Department Electives'),
(49, 'PSY 2580', 'FSS', 'Profiling and Serial Crimes', 3, 'Department Electives'),
(50, 'SOC 2000', 'FSS', 'Introduction to Sociology', 3, ''),
(51, 'PLS 4440', 'F', 'Methods of Crime Scene Investigation', 3, ''),
(52, 'PSY 2520', 'FS', 'Forensic Psychology', 3, 'Department Electives');



INSERT IGNORE INTO Program(program_id, program_name, degree_type) VALUES
(1, 'Psychology', 'Major'),
(2, 'Criminal Justice', 'Major'),
(3, 'Sociology', 'Minor'),
(4, 'Forensic Studies', 'Minor');


--Need to add Requirement Table for each Program
--Need to add PreReq for ENG 2100
--Could make requirements table for only IW, IE, GI
-- Department will handle department requirements
--Can make a search to see if string matches
-- we just need to make sure our strings match
-- 3 is a GI
-- 8 is IE, IW
-- 10 is all 3
-- could add 3 other attributes for GI, IE, IW and make them boolean

-- Course_Requirements: Pairs the Requirement with its Courses

--Program_Requirements: Pairs the Program with its requirements

-- Test if people can connect to my host

-- Requirements
    -- Psychology Requirements : Classes you need to take for Psych
        --UVC 1010
        --ENG 1100
        --STT 1600
        --PSY 1010
        --PSY 1010L
        --PSY 3010/L
        --PSY 3020/L
    -- Sociology
    -- Criminal Justice
    -- Forensics

    -- Core A
        --ENG 1100
        --ENG 2100
    -- Core B
        --STT 1600
    -- Core C (ART)
        -- ART 2140
    -- Core C (HIS)
        -- HST 1500
    -- Core D 
        --PSY 1010/L
        --EC 2900
    -- Core E
        --BIO 1150/L
        --PHY 1110/L, R
    -- Core 
        --MTH 2300/L, R

    -- GI 

    -- IE
    -- IW


-- Requirement Course Connection
-- Core math 1 + Stats 1 = 1
-- Coure math 1 + Math 3 = 2
