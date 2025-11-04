-- This script will insert all data for the program info
-- Courses
-- F = Fall
-- S = Spring
-- Q = Summer

-- Department is the credit it accounts for



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
(10, 'EC 2900', 'FSQ', 'Global Economic, Business and Social Issues', 0, NULL),
(11, 'BIO 1150/L', 'FSQ', 'Biology of Food', 4, NULL),
(12, 'PHY 1110/L,R', 'FSQ', 'Principles of Physics', 5, NULL),
(13, 'PHY 2400', 'FSQ', 'General Physics 1', 4, 16),
(14, 'PHY 2400L', 'FSQ', 'General Physics Lab', 1, 13),
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
(51, 'PLS 4440', 'F', 'Methods of Crime Scene Investigation', 3, NULL);




INSERT INTO Program(program_id, program_name, degree_type, creditHours) VALUES
(1, 'Psychology', 'Major', 120),
(2, 'Criminal Justice', 'Major', 120),
(3, 'Sociology', 'Minor', 18),
(4, 'Forensic Studies', 'Minor', 18);
