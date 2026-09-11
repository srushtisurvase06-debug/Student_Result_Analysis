#!/usr/bin/env python
"""Quick verification that the 2026 batch seed data is correct."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor, sslmode='require')
cursor = conn.cursor()

print("VERIFICATION OF 2026 BATCH SEED DATA")
print("=" * 50)

# Check students
cursor.execute("SELECT COUNT(*) as c FROM students WHERE roll_number LIKE '2026%'")
count = cursor.fetchone()['c']
print(f"Students: {count} (expected: 15)")

# Check subjects
cursor.execute("SELECT COUNT(*) as c FROM subjects WHERE subject_code LIKE 'SUB%'")
count = cursor.fetchone()['c']
print(f"Subjects: {count} (expected: 6)")

# Check marks
cursor.execute("SELECT COUNT(*) as c FROM marks")
count = cursor.fetchone()['c']
print(f"Marks: {count} (expected: 90)")

# Check absent
cursor.execute("SELECT COUNT(*) as c FROM marks WHERE is_absent = TRUE")
count = cursor.fetchone()['c']
print(f"Absent cases: {count} (expected: 1)")

# Sample results
cursor.execute("""
    SELECT s.roll_number, s.name, 
           SUM(m.marks_obtained) as total,
           SUM(s2.max_marks) as max,
           (SUM(m.marks_obtained) * 100.0 / SUM(s2.max_marks)) as pct
    FROM students s
    JOIN marks m ON s.id = m.student_id
    JOIN subjects s2 ON m.subject_id = s2.id
    WHERE s.roll_number LIKE '2026%'
    GROUP BY s.id, s.roll_number, s.name
    ORDER BY pct DESC
    LIMIT 3
""")
print("\nTop 3 Students:")
for row in cursor.fetchall():
    print(f"  {row['roll_number']}: {row['name']} - {row['pct']:.2f}%")

cursor.close()
conn.close()
print("\n✓ Verification complete")
