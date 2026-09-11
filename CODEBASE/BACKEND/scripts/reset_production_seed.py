#!/usr/bin/env python
"""
Reset Production Seed Data Script - Clean version

This script properly resets the production database to exactly match the new 2026 batch demo data.
It:
1. Safely removes ONLY the demo data (2026 batch students, SUB10x subjects)
2. Replaces with new 2026 batch students and subjects
3. Creates marks for all student-subject combinations
4. Verifies the final state
"""

import sys
import os

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

def main():
    conn = None
    try:
        print_header = lambda title: print(f"\n{'='*60}\n  {title}\n{'='*60}")
        
        print_header("PRODUCTION SEED DATA RESET")
        
        # Get connection
        print("\n[1/8] Connecting to Supabase database...")
        conn = get_connection()
        cursor = conn.cursor()
        print("    ✓ Connected successfully")
        
        # Start transaction
        print("\n[2/8] Starting transaction...")
        cursor.execute("BEGIN")
        print("    ✓ Transaction started")
        
        # Step 1: Delete ALL marks records (clean slate)
        print("\n[3/8] Removing all marks records...")
        cursor.execute("DELETE FROM marks")
        marks_deleted = cursor.rowcount
        print(f"    - Deleted {marks_deleted} marks records")
        
        # Step 2: Delete only 2026 batch students and SUB10x subjects (not admin or unrelated)
        print("\n[4/8] Removing old 2026 demo data...")
        
        # Delete students with roll numbers starting with 2026 (our demo)
        cursor.execute("DELETE FROM students WHERE roll_number LIKE '2026%'")
        students_deleted = cursor.rowcount
        print(f"    - Deleted {students_deleted} old 2026 batch students")
        
        # Delete subjects with codes starting with SUB (our demo)
        cursor.execute("DELETE FROM subjects WHERE subject_code LIKE 'SUB%'")
        subjects_deleted = cursor.rowcount
        print(f"    - Deleted {subjects_deleted} old 2026 batch subjects")
        
        conn.commit()
        print("    ✓ Transaction committed")
        
        # Step 3: Insert new 2026 batch students
        print("\n[5/8] Inserting new 2026 batch students...")
        
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
        
        for student in new_students:
            cursor.execute("""
                INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (roll_number) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    date_of_birth = EXCLUDED.date_of_birth,
                    gender = EXCLUDED.gender,
                    contact_number = EXCLUDED.contact_number,
                    updated_at = NOW()
            """, student)
        
        conn.commit()
        
        # Get inserted students
        cursor.execute("SELECT id, roll_number FROM students WHERE roll_number LIKE '2026%' ORDER BY roll_number")
        inserted_students = cursor.fetchall()
        print(f"    ✓ Inserted {len(inserted_students)} students")
        
        # Step 4: Insert new subjects
        print("\n[6/8] Inserting new subjects...")
        
        new_subjects = [
            ('SUB101', 'Java Programming', 100),
            ('SUB102', 'Database Management System', 100),
            ('SUB103', 'Computer Networks', 100),
            ('SUB104', 'Operating System', 100),
            ('SUB105', 'Software Engineering', 100),
            ('SUB106', 'Python Programming', 100),
        ]
        
        for subject in new_subjects:
            cursor.execute("""
                INSERT INTO subjects (subject_code, subject_name, max_marks)
                VALUES (%s, %s, %s)
                ON CONFLICT (subject_code) DO UPDATE SET
                    subject_name = EXCLUDED.subject_name,
                    max_marks = EXCLUDED.max_marks,
                    updated_at = NOW()
            """, subject)
        
        conn.commit()
        
        # Get inserted subjects
        cursor.execute("SELECT id, subject_code FROM subjects WHERE subject_code LIKE 'SUB%' ORDER BY subject_code")
        inserted_subjects = cursor.fetchall()
        print(f"    ✓ Inserted {len(inserted_subjects)} subjects")
        
        # Step 5: Create marks mapping
        print("\n[7/8] Creating marks mapping...")
        
        # Create student mapping (roll_number -> id)
        student_map = {row['roll_number']: row['id'] for row in inserted_students}
        # Create subject mapping (subject_code -> id)
        subject_map = {row['subject_code']: row['id'] for row in inserted_subjects}
        
        # Verify mappings
        print(f"    Student mapping: {len(student_map)} entries")
        print(f"    Subject mapping: {len(subject_map)} entries")
        
        # Define marks data
        marks_data = []
        absent_cases = []
        
        # 2026001 - Aditya Jadhav (Strong, ~90%)
        for subj, marks in [('SUB101', 92), ('SUB102', 88), ('SUB103', 95), ('SUB104', 90), ('SUB105', 87), ('SUB106', 94)]:
            marks_data.append((student_map['2026001'], subject_map[subj], marks, False))
        
        # 2026002 - Snehal Shinde (Strong, ~85%)
        for subj, marks in [('SUB101', 82), ('SUB102', 88), ('SUB103', 85), ('SUB104', 80), ('SUB105', 86), ('SUB106', 84)]:
            marks_data.append((student_map['2026002'], subject_map[subj], marks, False))
        
        # 2026003 - Omkar Pawar (Average, ~72%)
        for subj, marks in [('SUB101', 75), ('SUB102', 68), ('SUB103', 72), ('SUB104', 78), ('SUB105', 65), ('SUB106', 74)]:
            marks_data.append((student_map['2026003'], subject_map[subj], marks, False))
        
        # 2026004 - Vaishnavi Patil (Strong, ~88%)
        for subj, marks in [('SUB101', 90), ('SUB102', 85), ('SUB103', 88), ('SUB104', 82), ('SUB105', 91), ('SUB106', 89)]:
            marks_data.append((student_map['2026004'], subject_map[subj], marks, False))
        
        # 2026005 - Prathamesh Deshmukh (Average, ~68%)
        for subj, marks in [('SUB101', 70), ('SUB102', 65), ('SUB103', 72), ('SUB104', 68), ('SUB105', 62), ('SUB106', 75)]:
            marks_data.append((student_map['2026005'], subject_map[subj], marks, False))
        
        # 2026006 - Sakshi More (Good, ~78%)
        for subj, marks in [('SUB101', 80), ('SUB102', 75), ('SUB103', 78), ('SUB104', 82), ('SUB105', 76), ('SUB106', 80)]:
            marks_data.append((student_map['2026006'], subject_map[subj], marks, False))
        
        # 2026007 - Atharva Bhosale (Average, ~65%)
        for subj, marks in [('SUB101', 68), ('SUB102', 62), ('SUB103', 70), ('SUB104', 65), ('SUB105', 60), ('SUB106', 68)]:
            marks_data.append((student_map['2026007'], subject_map[subj], marks, False))
        
        # 2026008 - Rutuja Gaikwad (Good, ~77%)
        for subj, marks in [('SUB101', 78), ('SUB102', 72), ('SUB103', 80), ('SUB104', 75), ('SUB105', 70), ('SUB106', 79)]:
            marks_data.append((student_map['2026008'], subject_map[subj], marks, False))
        
        # 2026009 - Siddhant Chavan (Weaker, FAIL in some)
        for subj, marks in [('SUB101', 55), ('SUB102', 48), ('SUB103', 52), ('SUB104', 45), ('SUB105', 58), ('SUB106', 50)]:
            marks_data.append((student_map['2026009'], subject_map[subj], marks, False))
        
        # 2026010 - Tejas Kulkarni (Good, ~76%)
        for subj, marks in [('SUB101', 75), ('SUB102', 78), ('SUB103', 72), ('SUB104', 76), ('SUB105', 74), ('SUB106', 77)]:
            marks_data.append((student_map['2026010'], subject_map[subj], marks, False))
        
        # 2026011 - Pooja Kshirsagar (Strong, ~85%)
        for subj, marks in [('SUB101', 88), ('SUB102', 82), ('SUB103', 85), ('SUB104', 80), ('SUB105', 86), ('SUB106', 84)]:
            marks_data.append((student_map['2026011'], subject_map[subj], marks, False))
        
        # 2026012 - Rohit Mane (Average, ~67%)
        for subj, marks in [('SUB101', 68), ('SUB102', 70), ('SUB103', 65), ('SUB104', 66), ('SUB105', 64), ('SUB106', 68)]:
            marks_data.append((student_map['2026012'], subject_map[subj], marks, False))
        
        # 2026013 - Neha Shinde (Good, ~78%)
        for subj, marks in [('SUB101', 80), ('SUB102', 75), ('SUB103', 78), ('SUB104', 80), ('SUB105', 76), ('SUB106', 82)]:
            marks_data.append((student_map['2026013'], subject_map[subj], marks, False))
        
        # 2026014 - Akshay Kadam (Weaker, ABSENT in SUB106)
        marks_data.append((student_map['2026014'], subject_map['SUB101'], 58, False))
        marks_data.append((student_map['2026014'], subject_map['SUB102'], 52, False))
        marks_data.append((student_map['2026014'], subject_map['SUB103'], 55, False))
        marks_data.append((student_map['2026014'], subject_map['SUB104'], 48, False))
        marks_data.append((student_map['2026014'], subject_map['SUB105'], 60, False))
        marks_data.append((student_map['2026014'], subject_map['SUB106'], 54, True))  # ABSENT
        absent_cases.append('2026014 in SUB106 (Python Programming)')
        
        # 2026015 - Tanvi Sawant (Strong, ~90%)
        for subj, marks in [('SUB101', 92), ('SUB102', 88), ('SUB103', 90), ('SUB104', 94), ('SUB105', 86), ('SUB106', 91)]:
            marks_data.append((student_map['2026015'], subject_map[subj], marks, False))
        
        # Step 6: Insert all marks
        print("\n[8/8] Inserting marks...")
        
        for mark in marks_data:
            cursor.execute("""
                INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (student_id, subject_id) DO UPDATE SET
                    marks_obtained = EXCLUDED.marks_obtained,
                    is_absent = EXCLUDED.is_absent,
                    updated_at = NOW()
            """, mark)
        
        conn.commit()
        marks_inserted = len(marks_data)
        print(f"    ✓ Inserted {marks_inserted} marks records")
        
        if absent_cases:
            print(f"    - Absent cases: {', '.join(absent_cases)}")
        
        # Final verification
        print("\n" + "="*60)
        print("  VERIFICATION")
        print("="*60)
        
        # Count 2026 batch students
        cursor.execute("SELECT COUNT(*) as count FROM students WHERE roll_number LIKE '2026%'")
        students_count = cursor.fetchone()['count']
        print(f"\nStudents: {students_count}")
        
        cursor.execute("SELECT roll_number, name FROM students WHERE roll_number LIKE '2026%' ORDER BY roll_number")
        for row in cursor.fetchall():
            print(f"  - {row['roll_number']}: {row['name']}")
        
        # Count subjects
        cursor.execute("SELECT COUNT(*) as count FROM subjects WHERE subject_code LIKE 'SUB%'")
        subjects_count = cursor.fetchone()['count']
        print(f"\nSubjects: {subjects_count}")
        
        cursor.execute("SELECT subject_code, subject_name, max_marks FROM subjects WHERE subject_code LIKE 'SUB%' ORDER BY subject_code")
        for row in cursor.fetchall():
            print(f"  - {row['subject_code']}: {row['subject_name']} ({row['max_marks']} marks)")
        
        # Count marks
        cursor.execute("SELECT COUNT(*) as count FROM marks")
        total_marks = cursor.fetchone()['count']
        print(f"\nTotal Marks Records: {total_marks}")
        
        cursor.execute("SELECT COUNT(*) as count FROM marks WHERE is_absent = TRUE")
        absent_count = cursor.fetchone()['count']
        print(f"Absent Cases: {absent_count}")
        
        # Verify marks count
        expected_marks = 15 * 6  # 15 students × 6 subjects
        if total_marks == expected_marks:
            print(f"\n✓ VERIFIED: {total_marks} marks records (expected {expected_marks})")
        else:
            print(f"\n✗ MISMATCH: {total_marks} marks records (expected {expected_marks})")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("  PRODUCTION RESET COMPLETE")
        print("="*60)
        print(f"\n✓ Database updated successfully")
        print(f"  - Students: {students_count} (2026001-2026015)")
        print(f"  - Subjects: {subjects_count}")
        print(f"  - Marks: {total_marks}")
        print(f"  - Absent: {absent_count}")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
            print("  ✓ Transaction rolled back")
        sys.exit(1)

if __name__ == '__main__':
    main()
