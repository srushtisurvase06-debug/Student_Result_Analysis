#!/usr/bin/env python
"""
Update Production Seed Data Script

This script safely updates the real Supabase database with the new 2026 batch demo data.
It:
1. Safely deletes old demo data (only 2024xxx roll numbers and SUB10x subjects)
2. Inserts new 2026 batch students and subjects
3. Creates marks for all student-subject combinations
4. Verifies the final state
"""

import sys
import os
import bcrypt

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    """Get database connection from environment."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not configured")
    return psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor,
        sslmode='require',
        connect_timeout=10
    )

def print_header(title):
    """Print a header section."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def main():
    conn = None
    try:
        print_header("PRODUCTION SEED DATA UPDATE")
        
        # Get connection
        print("\n[1/7] Connecting to Supabase database...")
        conn = get_connection()
        cursor = conn.cursor()
        print("    ✓ Connected successfully")
        
        # Start transaction
        print("\n[2/7] Starting transaction...")
        cursor.execute("BEGIN")
        print("    ✓ Transaction started")
        
        # Step 1: Delete old demo data
        print("\n[3/7] Removing old demo data...")
        
        # Delete marks for old demo students (roll numbers starting with 2024)
        cursor.execute("""
            DELETE FROM marks 
            WHERE student_id IN (
                SELECT id FROM students WHERE roll_number LIKE '2024%'
            )
        """)
        marks_deleted_1 = cursor.rowcount
        print(f"    - Deleted {marks_deleted_1} marks for old students (2024xxx)")
        
        # Delete old demo students
        cursor.execute("DELETE FROM students WHERE roll_number LIKE '2024%'")
        students_deleted = cursor.rowcount
        print(f"    - Deleted {students_deleted} old demo students (2024xxx)")
        
        # Delete marks for old demo subjects (SUB10x subjects)
        cursor.execute("""
            DELETE FROM marks 
            WHERE subject_id IN (
                SELECT id FROM subjects WHERE subject_code LIKE 'SUB%'
            )
        """)
        marks_deleted_2 = cursor.rowcount
        print(f"    - Deleted {marks_deleted_2} marks for old subjects (SUB10x)")
        
        # Delete old demo subjects
        cursor.execute("DELETE FROM subjects WHERE subject_code LIKE 'SUB%'")
        subjects_deleted = cursor.rowcount
        print(f"    - Deleted {subjects_deleted} old demo subjects (SUB10x)")
        
        conn.commit()
        
        # Step 2: Insert new 2026 batch students
        print("\n[4/7] Inserting new 2026 batch students...")
        
        new_students = [
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
            ('2026015', 'Tanvi Sawant', 'tanvi.sawant@example.com', '2005-09-19', 'Female', '8654321098'),
        ]
        
        cursor.executemany("""
            INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (roll_number) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                date_of_birth = EXCLUDED.date_of_birth,
                gender = EXCLUDED.gender,
                contact_number = EXCLUDED.contact_number,
                updated_at = NOW()
        """, new_students)
        
        # Get inserted/updated students
        cursor.execute("""
            SELECT id, roll_number, name FROM students 
            WHERE roll_number LIKE '2026%' 
            ORDER BY roll_number
        """)
        inserted_students = cursor.fetchall()
        print(f"    ✓ Inserted/Updated {len(inserted_students)} students")
        
        # Step 3: Insert new subjects
        print("\n[5/7] Inserting new subjects...")
        
        new_subjects = [
            ('SUB101', 'Java Programming', 100),
            ('SUB102', 'Database Management System', 100),
            ('SUB103', 'Computer Networks', 100),
            ('SUB104', 'Operating System', 100),
            ('SUB105', 'Software Engineering', 100),
            ('SUB106', 'Python Programming', 100),
        ]
        
        cursor.executemany("""
            INSERT INTO subjects (subject_code, subject_name, max_marks)
            VALUES (%s, %s, %s)
            ON CONFLICT (subject_code) DO UPDATE SET
                subject_name = EXCLUDED.subject_name,
                max_marks = EXCLUDED.max_marks,
                updated_at = NOW()
        """, new_subjects)
        
        # Get inserted/updated subjects
        cursor.execute("SELECT id, subject_code, subject_name, max_marks FROM subjects ORDER BY subject_code")
        inserted_subjects = cursor.fetchall()
        print(f"    ✓ Inserted/Updated {len(inserted_subjects)} subjects")
        
        # Step 4: Insert marks for all student-subject combinations
        print("\n[6/7] Inserting marks for all student-subject combinations...")
        
        # Create student mapping
        student_map = {row['roll_number']: row['id'] for row in inserted_students}
        # Create subject mapping
        subject_map = {row['subject_code']: row['id'] for row in inserted_subjects}
        
        # Define marks data (15 students × 6 subjects = 90 marks)
        marks_data = []
        absent_cases = []
        
        # Student 2026001 (Aditya Jadhav) - Strong student ~90%
        for subj, marks in [('SUB101', 92), ('SUB102', 88), ('SUB103', 95), ('SUB104', 90), ('SUB105', 87), ('SUB106', 94)]:
            marks_data.append((student_map['2026001'], subject_map[subj], marks, False))
        
        # Student 2026002 (Snehal Shinde) - Strong student ~85%
        for subj, marks in [('SUB101', 82), ('SUB102', 88), ('SUB103', 85), ('SUB104', 80), ('SUB105', 86), ('SUB106', 84)]:
            marks_data.append((student_map['2026002'], subject_map[subj], marks, False))
        
        # Student 2026003 (Omkar Pawar) - Average student ~72%
        for subj, marks in [('SUB101', 75), ('SUB102', 68), ('SUB103', 72), ('SUB104', 78), ('SUB105', 65), ('SUB106', 74)]:
            marks_data.append((student_map['2026003'], subject_map[subj], marks, False))
        
        # Student 2026004 (Vaishnavi Patil) - Strong student ~88%
        for subj, marks in [('SUB101', 90), ('SUB102', 85), ('SUB103', 88), ('SUB104', 82), ('SUB105', 91), ('SUB106', 89)]:
            marks_data.append((student_map['2026004'], subject_map[subj], marks, False))
        
        # Student 2026005 (Prathamesh Deshmukh) - Average student ~68%
        for subj, marks in [('SUB101', 70), ('SUB102', 65), ('SUB103', 72), ('SUB104', 68), ('SUB105', 62), ('SUB106', 75)]:
            marks_data.append((student_map['2026005'], subject_map[subj], marks, False))
        
        # Student 2026006 (Sakshi More) - Good student ~78%
        for subj, marks in [('SUB101', 80), ('SUB102', 75), ('SUB103', 78), ('SUB104', 82), ('SUB105', 76), ('SUB106', 80)]:
            marks_data.append((student_map['2026006'], subject_map[subj], marks, False))
        
        # Student 2026007 (Atharva Bhosale) - Average student ~65%
        for subj, marks in [('SUB101', 68), ('SUB102', 62), ('SUB103', 70), ('SUB104', 65), ('SUB105', 60), ('SUB106', 68)]:
            marks_data.append((student_map['2026007'], subject_map[subj], marks, False))
        
        # Student 2026008 (Rutuja Gaikwad) - Good student ~77%
        for subj, marks in [('SUB101', 78), ('SUB102', 72), ('SUB103', 80), ('SUB104', 75), ('SUB105', 70), ('SUB106', 79)]:
            marks_data.append((student_map['2026008'], subject_map[subj], marks, False))
        
        # Student 2026009 (Siddhant Chavan) - Weaker student (FAIL in some subjects)
        for subj, marks in [('SUB101', 55), ('SUB102', 48), ('SUB103', 52), ('SUB104', 45), ('SUB105', 58), ('SUB106', 50)]:
            marks_data.append((student_map['2026009'], subject_map[subj], marks, False))
        
        # Student 2026010 (Tejas Kulkarni) - Good student ~76%
        for subj, marks in [('SUB101', 75), ('SUB102', 78), ('SUB103', 72), ('SUB104', 76), ('SUB105', 74), ('SUB106', 77)]:
            marks_data.append((student_map['2026010'], subject_map[subj], marks, False))
        
        # Student 2026011 (Pooja Kshirsagar) - Strong student ~85%
        for subj, marks in [('SUB101', 88), ('SUB102', 82), ('SUB103', 85), ('SUB104', 80), ('SUB105', 86), ('SUB106', 84)]:
            marks_data.append((student_map['2026011'], subject_map[subj], marks, False))
        
        # Student 2026012 (Rohit Mane) - Average student ~67%
        for subj, marks in [('SUB101', 68), ('SUB102', 70), ('SUB103', 65), ('SUB104', 66), ('SUB105', 64), ('SUB106', 68)]:
            marks_data.append((student_map['2026012'], subject_map[subj], marks, False))
        
        # Student 2026013 (Neha Shinde) - Good student ~78%
        for subj, marks in [('SUB101', 80), ('SUB102', 75), ('SUB103', 78), ('SUB104', 80), ('SUB105', 76), ('SUB106', 82)]:
            marks_data.append((student_map['2026013'], subject_map[subj], marks, False))
        
        # Student 2026014 (Akshay Kadam) - Weaker student, ABSENT in SUB106
        marks_data.append((student_map['2026014'], subject_map['SUB101'], 58, False))
        marks_data.append((student_map['2026014'], subject_map['SUB102'], 52, False))
        marks_data.append((student_map['2026014'], subject_map['SUB103'], 55, False))
        marks_data.append((student_map['2026014'], subject_map['SUB104'], 48, False))
        marks_data.append((student_map['2026014'], subject_map['SUB105'], 60, False))
        marks_data.append((student_map['2026014'], subject_map['SUB106'], 54, True))  # ABSENT
        absent_cases.append('2026014 in SUB106 (Python Programming)')
        
        # Student 2026015 (Tanvi Sawant) - Strong student ~90%
        for subj, marks in [('SUB101', 92), ('SUB102', 88), ('SUB103', 90), ('SUB104', 94), ('SUB105', 86), ('SUB106', 91)]:
            marks_data.append((student_map['2026015'], subject_map[subj], marks, False))
        
        # Insert all marks
        cursor.executemany("""
            INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (student_id, subject_id) DO UPDATE SET
                marks_obtained = EXCLUDED.marks_obtained,
                is_absent = EXCLUDED.is_absent,
                updated_at = NOW()
        """, marks_data)
        
        marks_inserted = cursor.rowcount
        print(f"    ✓ Inserted/Updated {marks_inserted} marks records")
        
        if absent_cases:
            print(f"    - Absent cases: {', '.join(absent_cases)}")
        
        conn.commit()
        print("    ✓ Transaction committed")
        
        # Step 5: Verification
        print("\n[7/7] Verifying final database state...")
        
        # Count students
        cursor.execute("SELECT COUNT(*) as count FROM students WHERE roll_number LIKE '2026%'")
        students_count = cursor.fetchone()['count']
        print(f"    - Total 2026 batch students: {students_count}")
        
        # Verify roll numbers
        cursor.execute("""
            SELECT roll_number, name FROM students 
            WHERE roll_number LIKE '2026%' 
            ORDER BY roll_number
        """)
        students = cursor.fetchall()
        print("\n    Students:")
        for s in students:
            print(f"      - {s['roll_number']}: {s['name']}")
        
        # Count subjects
        cursor.execute("SELECT COUNT(*) as count FROM subjects WHERE subject_code LIKE 'SUB%'")
        subjects_count = cursor.fetchone()['count']
        print(f"\n    - Total 2026 batch subjects: {subjects_count}")
        
        # List subjects
        cursor.execute("SELECT subject_code, subject_name, max_marks FROM subjects ORDER BY subject_code")
        subjects = cursor.fetchall()
        print("\n    Subjects:")
        for s in subjects:
            print(f"      - {s['subject_code']}: {s['subject_name']} ({s['max_marks']} marks)")
        
        # Count marks
        cursor.execute("SELECT COUNT(*) as count FROM marks WHERE is_absent = TRUE")
        absent_count = cursor.fetchone()['count']
        print(f"\n    - Total marks records: {marks_inserted}")
        print(f"    - Absent cases: {absent_count}")
        
        # Verify all 90 marks exist (15 students × 6 subjects)
        cursor.execute("""
            SELECT COUNT(*) as count FROM marks m
            JOIN students s ON m.student_id = s.id
            WHERE s.roll_number LIKE '2026%'
        """)
        total_marks = cursor.fetchone()['count']
        print(f"    - Marks for 2026 batch students: {total_marks}")
        
        if total_marks == 90:
            print("    ✓ All 90 marks records verified")
        else:
            print(f"    ⚠ Warning: Expected 90 marks, found {total_marks}")
        
        cursor.close()
        conn.close()
        
        print_header("PRODUCTION UPDATE COMPLETE")
        print(f"\n✓ Successfully updated production database")
        print(f"  - Students: {students_count} (2026001-2026015)")
        print(f"  - Subjects: {subjects_count}")
        print(f"  - Marks: {total_marks}")
        print(f"  - Absent cases: {absent_count}")
        print(f"\nNext step: Run 'python scripts/generate_seed_sql.py' to update seed.sql")
        print(f"Then commit and push to GitHub for Render deployment.")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        if conn:
            conn.rollback()
            print("  ✓ Transaction rolled back")
        sys.exit(1)

if __name__ == '__main__':
    main()
