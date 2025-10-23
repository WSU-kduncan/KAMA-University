-- This Script will insert all user data
-- You only need to run this once

-- Admin
INSERT INTO Admin (admin_id, first_name, last_name, username, password) VALUES
(1, 'Lowdy', 'Laker', 'lowdylkr', 'LowdyLake24&'),
(2, 'Rowdy', 'Raider', 'rowdyrdr', 'RowdyRad617#');

-- Add email to admin table

-- Advisors
INSERT INTO Advisor (advisor_id, first_name, last_name, email, username, password) VALUES
(1, 'Calum', 'Oust', 'COust.1@KAMA.edu', 'calumous', 'CalumOut%10%'),
(2, 'Miles', 'Pardalis', 'MPardalis@KAMA.edu', 'milespar', 'Milespara11!'),
(3, 'Oliver', 'Meller', 'OMeller.1@KAMA.edu', 'oliverme', 'OliverMe1234@');

-- Students
INSERT INTO Student (student_id, first_name, last_name, email, username, password, NumYears, NumCoOps, SummerSemester, CrdtHrsPrSem, advisor_id) VALUES
(1, 'Jackson', 'Vail', 'JVail.1@KAMA.edu', 'jacksonv', 'JacksonV123!', 4, 0, 'yes', 15, 1),
(2, 'Perry', 'Soni', 'PSoni.1@KAMA.edu', 'perryson', 'PerrySon@456', 4, 0, 'yes', 15, 1),
(3, 'Fischer', 'Ray', 'FRay.1@KAMA.edu', 'fischerr', 'FischerR*909', 4, 0, 'yes', 15, 1),
(4, 'Panthera', 'Leon', 'PLeon.1@KAMA.edu', 'panthera', 'PantheraL23?', 4, 0, 'yes', 15, 1),
(5, 'Elliot', 'Cross', 'ECross.1@KAMA.edu', 'elliotcr', 'ElliotC501!?', 4, 0, 'yes', 15, 1);


