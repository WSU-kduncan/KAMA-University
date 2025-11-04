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
(1, 'Jackson', 'Vail', 'JVail.1@KAMA.edu', 'jacksonv', 'JacksonV123!', 4, 0, 'no', 15, 1),
(2, 'Perry', 'Soni', 'PSoni.1@KAMA.edu', 'perryson', 'PerrySon@456', 4, 0, 'no', 15, 1),
(3, 'Fischer', 'Ray', 'FRay.1@KAMA.edu', 'fischerr', 'FischerR*909', 4, 0, 'no', 15, 2),
(4, 'Panthera', 'Leon', 'PLeon.1@KAMA.edu', 'panthera', 'PantheraL23?', 4, 0, 'no', 15, 2),
(5, 'Elliot', 'Cross', 'ECross.1@KAMA.edu', 'elliotcr', 'ElliotC501!?', 4, 0, 'no', 15, 2),
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



