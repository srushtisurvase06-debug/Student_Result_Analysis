BEGIN;

CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    roll_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    contact_number VARCHAR(15) NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    max_marks INTEGER NOT NULL CHECK (max_marks > 0),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS marks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    marks_obtained INTEGER NOT NULL CHECK (marks_obtained >= 0),
    is_absent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_student_subject UNIQUE (student_id, subject_id),
    CONSTRAINT fk_marks_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_marks_subject
        FOREIGN KEY (subject_id)
        REFERENCES subjects(id)
        ON DELETE RESTRICT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_students_roll_number ON students(roll_number);
CREATE INDEX IF NOT EXISTS idx_students_lookup ON students(roll_number, date_of_birth);
CREATE UNIQUE INDEX IF NOT EXISTS idx_subjects_code ON subjects(subject_code);
CREATE UNIQUE INDEX IF NOT EXISTS idx_marks_student_subject ON marks(student_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_marks_student ON marks(student_id);
CREATE INDEX IF NOT EXISTS idx_marks_subject ON marks(subject_id);

INSERT INTO admins (username, email, password_hash, full_name)
VALUES (
    'admin',
    'admin@resultportal.com',
    '$2b$12$B9wCP7S5cUHIk5RteYo62.HEugMyIKkKhkb5SXnbWv5/3ApeyfwI.',
    'System Administrator'
)
ON CONFLICT (username) DO NOTHING;

COMMIT;
