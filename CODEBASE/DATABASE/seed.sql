BEGIN;

INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
VALUES
    ('2024001', 'Aarav Sharma', 'aarav.sharma@example.com', '2005-02-15', 'Male', '9876543210'),
    ('2024002', 'Diya Patel', 'diya.patel@example.com', '2005-03-22', 'Female', '9123456789'),
    ('2024003', 'Rohan Verma', 'rohan.verma@example.com', '2005-05-12', 'Male', '9988776655'),
    ('2024004', 'Meera Nair', 'meera.nair@example.com', '2005-07-04', 'Female', '9765432109'),
    ('2024005', 'Kabir Singh', 'kabir.singh@example.com', '2005-11-18', 'Male', '9654321098'),
    ('2024006', 'Saanvi Iyer', 'saanvi.iyer@example.com', '2005-01-29', 'Female', '9543210987'),
    ('2024007', 'Vihaan Rao', 'vihaan.rao@example.com', '2005-10-10', 'Male', '9432109876'),
    ('2024008', 'Ananya Das', 'ananya.das@example.com', '2005-09-07', 'Female', '9321098765'),
    ('2024009', 'Yash Malhotra', 'yash.malhotra@example.com', '2005-04-14', 'Male', '9210987654'),
    ('2024010', 'Pooja Sen', 'pooja.sen@example.com', '2005-06-25', 'Female', '9109876543'),
    ('2024011', 'Arjun Gupta', 'arjun.gupta@example.com', '2005-08-13', 'Male', '9098765432'),
    ('2024012', 'Nisha Reddy', 'nisha.reddy@example.com', '2005-12-21', 'Female', '8987654321'),
    ('2024013', 'Kunal Joshi', 'kunal.joshi@example.com', '2005-02-28', 'Male', '8876543210'),
    ('2024014', 'Ishita Banerjee', 'ishita.banerjee@example.com', '2005-03-30', 'Female', '8765432109'),
    ('2024015', 'Harsh Kapoor', 'harsh.kapoor@example.com', '2005-07-19', 'Male', '8654321098')
ON CONFLICT (roll_number) DO NOTHING;

INSERT INTO subjects (subject_code, subject_name, max_marks)
VALUES
    ('MATH101', 'Mathematics', 100),
    ('SCI102', 'Science', 100),
    ('ENG103', 'English', 100),
    ('CS104', 'Computer Science', 100),
    ('SS105', 'Social Studies', 100),
    ('PHY106', 'Physics', 100)
ON CONFLICT (subject_code) DO NOTHING;

WITH student_map AS (
    SELECT id, roll_number FROM students
),
subject_map AS (
    SELECT id, subject_code FROM subjects
)
INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent)
SELECT s.id, subj.id,
       CASE
           WHEN s.roll_number = '2024001' THEN 92
           WHEN s.roll_number = '2024002' THEN 88
           WHEN s.roll_number = '2024003' THEN 74
           WHEN s.roll_number = '2024004' THEN 81
           WHEN s.roll_number = '2024005' THEN 68
           WHEN s.roll_number = '2024006' THEN 90
           WHEN s.roll_number = '2024007' THEN 73
           WHEN s.roll_number = '2024008' THEN 59
           WHEN s.roll_number = '2024009' THEN 46
           WHEN s.roll_number = '2024010' THEN 84
           WHEN s.roll_number = '2024011' THEN 64
           WHEN s.roll_number = '2024012' THEN 93
           WHEN s.roll_number = '2024013' THEN 51
           WHEN s.roll_number = '2024014' THEN 37
           WHEN s.roll_number = '2024015' THEN 77
           ELSE 0
       END,
       CASE
           WHEN s.roll_number = '2024008' AND subj.subject_code = 'PHY106' THEN TRUE
           ELSE FALSE
       END
FROM student_map s
CROSS JOIN subject_map subj
ON CONFLICT (student_id, subject_id) DO NOTHING;

COMMIT;
