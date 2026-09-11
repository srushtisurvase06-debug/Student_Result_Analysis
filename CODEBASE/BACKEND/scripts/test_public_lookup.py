#!/usr/bin/env python
"""
Test public result lookup functionality with 2026 batch data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extras import RealDictCursor

def test_public_lookup():
    """Test public result lookup with 2026 batch data."""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL not configured")
        return False
    
    conn = psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor,
        sslmode='require',
        connect_timeout=10
    )
    cursor = conn.cursor()
    
    print("="*60)
    print("PUBLIC RESULT LOOKUP TEST")
    print("="*60)
    
    # Test with 2026001 (Aditya Jadhav) - strong student
    roll_number = '2026001'
    date_of_birth = '2005-03-15'
    
    print(f"\nTesting lookup for:")
    print(f"  Roll Number: {roll_number}")
    print(f"  Date of Birth: {date_of_birth}")
    
    # Query student
    cursor.execute("""
        SELECT id, roll_number, name, email, date_of_birth, gender, contact_number
        FROM students
        WHERE roll_number = %s AND date_of_birth = %s
    """, (roll_number, date_of_birth))
    
    student = cursor.fetchone()
    
    if not student:
        print("\n✗ ERROR: Student not found")
        return False
    
    print(f"\n✓ Student found: {student['name']}")
    print(f"  ID: {student['id']}")
    print(f"  Roll Number: {student['roll_number']}")
    
    # Query marks for this student
    cursor.execute("""
        SELECT 
            s.subject_code,
            s.subject_name,
            s.max_marks,
            m.marks_obtained,
            (m.marks_obtained * 100.0 / s.max_marks) as percentage,
            CASE WHEN m.marks_obtained >= (s.max_marks * 0.40) THEN 'PASS' ELSE 'FAIL' END as status
        FROM marks m
        JOIN subjects s ON m.subject_id = s.id
        WHERE m.student_id = %s
        ORDER BY s.subject_code
    """, (student['id'],))
    
    marks = cursor.fetchall()
    
    print(f"\n✓ Found {len(marks)} subject marks")
    
    # Calculate totals
    total_obtained = sum(m['marks_obtained'] or 0 for m in marks)
    total_maximum = sum(m['max_marks'] for m in marks)
    percentage = (total_obtained / total_maximum * 100) if total_maximum > 0 else 0
    
    print(f"\nResult Summary:")
    print(f"  Total Marks: {total_obtained}/{total_maximum}")
    print(f"  Percentage: {percentage:.2f}%")
    
    # Assign grade
    if percentage >= 90:
        grade = 'A'
    elif percentage >= 75:
        grade = 'B'
    elif percentage >= 60:
        grade = 'C'
    elif percentage >= 40:
        grade = 'D'
    else:
        grade = 'F'
    
    print(f"  Grade: {grade}")
    
    # Pass/fail status
    status = 'PASS' if percentage >= 40 else 'FAIL'
    print(f"  Status: {status}")
    
    # Subject-wise details
    print(f"\nSubject-wise Marks:")
    for m in marks:
        print(f"  {m['subject_code']}: {m['marks_obtained']}/{m['max_marks']} ({m['percentage']:.1f}%) - {m['status']}")
    
    # Check for absent
    cursor.execute("SELECT COUNT(*) as count FROM marks WHERE student_id = %s AND is_absent = TRUE", (student['id'],))
    absent = cursor.fetchone()['count']
    if absent > 0:
        print(f"\n⚠ Absent in {absent} subject(s)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✓ PUBLIC RESULT LOOKUP TEST PASSED")
    print("="*60)
    return True

if __name__ == '__main__':
    try:
        success = test_public_lookup()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
