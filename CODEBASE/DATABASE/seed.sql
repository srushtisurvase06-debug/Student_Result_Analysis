BEGIN;

-- Clean up any existing 2026 batch demo data first (for idempotency)
DELETE FROM marks WHERE student_id IN (SELECT id FROM students WHERE roll_number LIKE '2026%');
DELETE FROM students WHERE roll_number LIKE '2026%';
DELETE FROM marks WHERE subject_id IN (SELECT id FROM subjects WHERE subject_code LIKE 'SUB%');
DELETE FROM subjects WHERE subject_code LIKE 'SUB%';

-- Insert 15 students with Diploma Computer Engineering data (2026 batch)
INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
VALUES
    ('2026001', 'Aditya Jadhav', 'aditya.jadhav@example.com', '2005-03-15', 'Male', '9876543210'),
    ('2026002', 'Snehal Shinde', 'snehal.shinde@example.com', '2005-05-22', 'Female', '9123456789'),
    ('2026003', 'Omkar Pawar', 'omkar.pawar@example.com', '2005-07-12', 'Male', '9988776655'),
    ('2026004', 'Vaishnavi Patil', 'vaishnavi.patil@example.com', '2005-01-04', 'Female', '9765432109'),
    ('2026005', 'Prathamesh Deshmukh', 'prathamesh.deshmukh@example.com', '2005-09-18', 'Male', '9654321098'),
    ('2026006', 'Sakshi More', 'sakshi.more@example.com', '2005-11-29', 'Female', '9543210987'),
    ('2026007', 'Atharva Bhosale', 'atharva.bhosale@example.com', '2005-04-10', 'Male', '9432109876'),
    ('2026008', 'Rutuja Gaikwad', 'rutuja.gaikwad@example.com', '2005-06-07', 'Female', '9321098765'),
    ('2026009', 'Siddhant Chavan', 'siddhant.chavan@example.com', '2005-08-14', 'Male', '9210987654'),
    ('2026010', 'Tejas Kulkarni', 'tejas.kulkarni@example.com', '2005-10-25', 'Male', '9109876543'),
    ('2026011', 'Pooja Kshirsagar', 'pooja.kshirsagar@example.com', '2005-02-21', 'Female', '9098765432'),
    ('2026012', 'Rohit Mane', 'rohit.mane@example.com', '2005-12-13', 'Male', '8987654321'),
    ('2026013', 'Neha Shinde', 'neha.shinde@example.com', '2005-04-08', 'Female', '8876543210'),
    ('2026014', 'Akshay Kadam', 'akshay.kadam@example.com', '2005-07-30', 'Male', '8765432109'),
    ('2026015', 'Tanvi Sawant', 'tanvi.sawant@example.com', '2005-09-19', 'Female', '8654321098')
ON CONFLICT (roll_number) DO NOTHING;

-- Insert 6 subjects for Diploma Computer Engineering
INSERT INTO subjects (subject_code, subject_name, max_marks)
VALUES
    ('SUB101', 'Java Programming', 100),
    ('SUB102', 'Database Management System', 100),
    ('SUB103', 'Computer Networks', 100),
    ('SUB104', 'Operating System', 100),
    ('SUB105', 'Software Engineering', 100),
    ('SUB106', 'Python Programming', 100)
ON CONFLICT (subject_code) DO NOTHING;

-- Create marks for all 15 students across all 6 subjects (90 marks total)
-- Each student has marks in all 6 subjects, except 2026014 is ABSENT in SUB106 (Python Programming)

WITH student_map AS (
    SELECT id, roll_number FROM students WHERE roll_number LIKE '2026%'
),
subject_map AS (
    SELECT id, subject_code FROM subjects WHERE subject_code LIKE 'SUB%'
)
INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent)
SELECT s.id, subj.id,
       CASE
           -- Student 2026001 (Aditya Jadhav) - Strong student, 91% total
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB101' THEN 92
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB102' THEN 88
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB103' THEN 95
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB104' THEN 90
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB105' THEN 87
           WHEN s.roll_number = '2026001' AND subj.subject_code = 'SUB106' THEN 94
           
           -- Student 2026002 (Snehal Shinde) - Strong student, 84% total
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB101' THEN 82
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB102' THEN 88
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB103' THEN 85
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB104' THEN 80
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB105' THEN 86
           WHEN s.roll_number = '2026002' AND subj.subject_code = 'SUB106' THEN 84
           
           -- Student 2026003 (Omkar Pawar) - Average student, 72% total
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB101' THEN 75
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB102' THEN 68
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB103' THEN 72
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB104' THEN 78
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB105' THEN 65
           WHEN s.roll_number = '2026003' AND subj.subject_code = 'SUB106' THEN 74
           
           -- Student 2026004 (Vaishnavi Patil) - Strong student, 88% total
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB101' THEN 90
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB102' THEN 85
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB103' THEN 88
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB104' THEN 82
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB105' THEN 91
           WHEN s.roll_number = '2026004' AND subj.subject_code = 'SUB106' THEN 89
           
           -- Student 2026005 (Prathamesh Deshmukh) - Average student, 68% total
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB101' THEN 70
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB102' THEN 65
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB103' THEN 72
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB104' THEN 68
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB105' THEN 62
           WHEN s.roll_number = '2026005' AND subj.subject_code = 'SUB106' THEN 75
           
           -- Student 2026006 (Sakshi More) - Good student, 78% total
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB101' THEN 80
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB102' THEN 75
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB103' THEN 78
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB104' THEN 82
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB105' THEN 76
           WHEN s.roll_number = '2026006' AND subj.subject_code = 'SUB106' THEN 80
           
           -- Student 2026007 (Atharva Bhosale) - Average student, 65% total
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB101' THEN 68
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB102' THEN 62
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB103' THEN 70
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB104' THEN 65
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB105' THEN 60
           WHEN s.roll_number = '2026007' AND subj.subject_code = 'SUB106' THEN 68
           
           -- Student 2026008 (Rutuja Gaikwad) - Good student, 77% total
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB101' THEN 78
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB102' THEN 72
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB103' THEN 80
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB104' THEN 75
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB105' THEN 70
           WHEN s.roll_number = '2026008' AND subj.subject_code = 'SUB106' THEN 79
           
           -- Student 2026009 (Siddhant Chavan) - Weaker student, FAIL in several subjects
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB101' THEN 55
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB102' THEN 48
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB103' THEN 52
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB104' THEN 45
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB105' THEN 58
           WHEN s.roll_number = '2026009' AND subj.subject_code = 'SUB106' THEN 50
           
           -- Student 2026010 (Tejas Kulkarni) - Good student, 76% total
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB101' THEN 75
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB102' THEN 78
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB103' THEN 72
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB104' THEN 76
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB105' THEN 74
           WHEN s.roll_number = '2026010' AND subj.subject_code = 'SUB106' THEN 77
           
           -- Student 2026011 (Pooja Kshirsagar) - Strong student, 85% total
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB101' THEN 88
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB102' THEN 82
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB103' THEN 85
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB104' THEN 80
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB105' THEN 86
           WHEN s.roll_number = '2026011' AND subj.subject_code = 'SUB106' THEN 84
           
           -- Student 2026012 (Rohit Mane) - Average student, 67% total
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB101' THEN 68
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB102' THEN 70
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB103' THEN 65
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB104' THEN 66
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB105' THEN 64
           WHEN s.roll_number = '2026012' AND subj.subject_code = 'SUB106' THEN 68
           
           -- Student 2026013 (Neha Shinde) - Good student, 78% total
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB101' THEN 80
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB102' THEN 75
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB103' THEN 78
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB104' THEN 80
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB105' THEN 76
           WHEN s.roll_number = '2026013' AND subj.subject_code = 'SUB106' THEN 82
           
           -- Student 2026014 (Akshay Kadam) - Weaker student, ABSENT in SUB106
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB101' THEN 58
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB102' THEN 52
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB103' THEN 55
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB104' THEN 48
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB105' THEN 60
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB106' THEN 0  -- ABSENT, stored as 0
           
           -- Student 2026015 (Tanvi Sawant) - Strong student, 90% total
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB101' THEN 92
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB102' THEN 88
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB103' THEN 90
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB104' THEN 94
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB105' THEN 86
           WHEN s.roll_number = '2026015' AND subj.subject_code = 'SUB106' THEN 91
           
           ELSE 0
       END,
       CASE
           -- At least one absent case: 2026014 in SUB106 (Python Programming)
           WHEN s.roll_number = '2026014' AND subj.subject_code = 'SUB106' THEN TRUE
           ELSE FALSE
       END
FROM student_map s
CROSS JOIN subject_map subj
ON CONFLICT (student_id, subject_id) DO NOTHING;

COMMIT;
