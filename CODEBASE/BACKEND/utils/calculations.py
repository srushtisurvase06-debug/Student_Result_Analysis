"""Result calculation utilities.

All calculation functions implement the result calculation logic from PRD Section 4.
Phase 10: Result Calculation Engine only.

Calculation Rules (PRD Section 4):
- Percentage = (Total Obtained / Total Maximum) × 100, rounded to 2 decimals
- Grade assignment based on percentage ranges (A: 90-100, B: 75-89, C: 60-74, D: 40-59, F: 0-39)
- Pass/Fail: Student must score ≥40% in EACH subject AND overall percentage ≥40%
- Absent students: marks=0, status=FAIL
"""

from typing import Optional


def calculate_percentage(total_obtained: float, total_maximum: float) -> float:
    """Calculate percentage from total marks.
    
    Args:
        total_obtained: Total marks obtained by student
        total_maximum: Total maximum marks possible
        
    Returns:
        Percentage rounded to 2 decimal places
        Returns 0.0 if total_maximum is 0
    """
    if total_maximum == 0:
        return 0.0
    percentage = (total_obtained / total_maximum) * 100
    return round(percentage, 2)


def calculate_grade(percentage: float) -> str:
    """Assign grade based on percentage.
    
    Grading Scale (PRD Section 4.1.3):
    | Percentage Range | Grade | Description |
    |-----------------|-------|-------------|
    | 90 - 100 | A | Outstanding |
    | 75 - 89 | B | Excellent |
    | 60 - 74 | C | Good |
    | 40 - 59 | D | Pass |
    | 0 - 39 | F | Fail |
    
    Args:
        percentage: Student's calculated percentage
        
    Returns:
        Grade character: 'A', 'B', 'C', 'D', or 'F'
    """
    if percentage >= 90:
        return 'A'
    elif percentage >= 75:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'


def calculate_status_from_percentage(percentage: float) -> str:
    """Determine pass/fail status from percentage only.
    
    Uses the overall percentage threshold of 40%.
    Note: This does not check individual subject pass/fail.
    
    Args:
        percentage: Student's calculated percentage
        
    Returns:
        'PASS' if percentage >= 40, otherwise 'FAIL'
    """
    return 'PASS' if percentage >= 40 else 'FAIL'


def calculate_status(student_id: int, db_connection) -> dict:
    """Determine pass/fail status for a student.
    
    Pass/Fail Rules (PRD Section 4.1.4):
    1. **Pass:** Student must score ≥ 40% in EACH subject AND overall percentage ≥ 40%
    2. **Fail:** Student fails if:
       - Any subject marks < 40% of that subject's maximum marks, OR
       - Overall percentage < 40%, OR
       - Student is Absent in any subject
    
    Args:
        student_id: ID of the student
        db_connection: Database connection object with cursor
            
    Returns:
        Dictionary with:
        - 'status': 'PASS' or 'FAIL'
        - 'reason': Description of why student passed or failed
        - 'subject_results': List of subject pass/fail details
    """
    cursor = db_connection.cursor()
    
    try:
        # Check for absent students
        cursor.execute("""
            SELECT COUNT(*) as absent_count
            FROM marks
            WHERE student_id = %s AND is_absent = TRUE
        """, (student_id,))
        absent_count = cursor.fetchone()['absent_count']
        
        if absent_count > 0:
            return {
                'status': 'FAIL',
                'reason': f'Absent in {absent_count} subject(s)',
                'subject_results': []
            }
        
        # Get all subject results for this student
        cursor.execute("""
            SELECT 
                s.subject_name,
                s.max_marks,
                m.marks_obtained,
                (s.max_marks * 0.40) as passing_marks
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = %s
            ORDER BY s.subject_name
        """, (student_id,))
        
        subject_results = cursor.fetchall()
        failed_subjects = []
        
        for subject in subject_results:
            subject_passed = subject['marks_obtained'] >= subject['passing_marks']
            if not subject_passed:
                failed_subjects.append({
                    'subject_name': subject['subject_name'],
                    'marks_obtained': subject['marks_obtained'],
                    'passing_marks': subject['passing_marks']
                })
        
        # Check if all subjects passed
        if failed_subjects:
            subject_names = ', '.join([s['subject_name'] for s in failed_subjects])
            return {
                'status': 'FAIL',
                'reason': f'Failed in: {subject_names}',
                'subject_results': failed_subjects
            }
        
        # Calculate overall percentage and check if >= 40%
        cursor.execute("""
            SELECT 
                SUM(m.marks_obtained) as total_obtained,
                SUM(s.max_marks) as total_maximum
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = %s
        """, (student_id,))
        
        totals = cursor.fetchone()
        total_obtained = totals['total_obtained'] or 0
        total_maximum = totals['total_maximum'] or 0
        
        if total_maximum == 0:
            return {
                'status': 'FAIL',
                'reason': 'No marks found for student',
                'subject_results': []
            }
        
        percentage = (total_obtained / total_maximum) * 100
        if percentage < 40:
            return {
                'status': 'FAIL',
                'reason': f'Overall percentage ({round(percentage, 2)}%) below 40%',
                'subject_results': []
            }
        
        return {
            'status': 'PASS',
            'reason': 'Passed all subjects with overall percentage >= 40%',
            'subject_results': subject_results
        }
        
    finally:
        cursor.close()


def generate_full_result(student_id: int, db_connection) -> Optional[dict]:
    """Generate complete result for a student.
    
    Args:
        student_id: ID of the student
        db_connection: Database connection object
            
    Returns:
        Complete result dictionary or None if student not found
        Structure:
        {
            'student': {id, roll_number, name, ...},
            'total_obtained': int,
            'total_maximum': int,
            'percentage': float,
            'grade': str,
            'status': 'PASS'/'FAIL'/'incomplete',
            'status_reason': str,
            'subject_count': int,
            'subjects_total': int,
            'subjects': list of subject result dicts
        }
    """
    cursor = db_connection.cursor()
    
    try:
        # Get student info
        cursor.execute("""
            SELECT id, roll_number, name, email, date_of_birth, gender, contact_number
            FROM students WHERE id = %s
        """, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            return None
        
        # Get total subjects count
        cursor.execute("SELECT COUNT(*) as count FROM subjects")
        subjects_total = cursor.fetchone()['count']
        
        # Get marks count for this student
        cursor.execute("""
            SELECT COUNT(*) as count FROM marks WHERE student_id = %s
        """, (student_id,))
        marks_count = cursor.fetchone()['count']
        
        # Check if all subjects have marks
        if marks_count < subjects_total:
            return {
                'student': dict(student),
                'status': 'incomplete',
                'message': 'Result not yet published',
                'subjects_completed': marks_count,
                'subjects_total': subjects_total
            }
        
        # Calculate total marks
        cursor.execute("""
            SELECT 
                SUM(m.marks_obtained) as total_obtained,
                SUM(s.max_marks) as total_maximum
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = %s
        """, (student_id,))
        
        totals = cursor.fetchone()
        total_obtained = totals['total_obtained'] or 0
        total_maximum = totals['total_maximum'] or 0
        
        # Calculate percentage
        percentage = calculate_percentage(total_obtained, total_maximum)
        
        # Assign grade
        grade = calculate_grade(percentage)
        
        # Determine pass/fail status
        status_info = calculate_status(student_id, db_connection)
        
        # Get subject-wise details with calculated fields
        cursor.execute("""
            SELECT 
                s.subject_code,
                s.subject_name,
                m.marks_obtained,
                s.max_marks,
                (s.max_marks * 0.40) as passing_marks,
                CASE WHEN m.marks_obtained >= (s.max_marks * 0.40) THEN 'PASS' ELSE 'FAIL' END as status
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = %s
            ORDER BY s.subject_code
        """, (student_id,))
        
        subject_results = []
        for row in cursor.fetchall():
            subject_dict = dict(row)
            # Calculate percentage and grade for each subject
            subject_dict['percentage'] = calculate_percentage(subject_dict['marks_obtained'], subject_dict['max_marks'])
            subject_dict['grade'] = calculate_grade(subject_dict['percentage'])
            subject_results.append(subject_dict)
        
        return {
            'student': dict(student),
            'total_obtained': total_obtained,
            'total_maximum': total_maximum,
            'percentage': percentage,
            'grade': grade,
            'status': status_info['status'],
            'status_reason': status_info['reason'],
            'subjects': subject_results,  # Changed from 'subject_results' to 'subjects'
            'subject_count': marks_count,
            'subjects_total': subjects_total
        }
        
    finally:
        cursor.close()


def calculate_class_average(db_connection) -> float:
    """Calculate class average percentage.
    
    Args:
        db_connection: Database connection object
            
    Returns:
        Average percentage of all students with complete results
    """
    cursor = db_connection.cursor()
    
    try:
        # Get all students with complete results (all subjects have marks)
        cursor.execute("""
            SELECT s.id
            FROM students s
            WHERE (
                SELECT COUNT(*) 
                FROM marks m 
                WHERE m.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
        """)
        students = cursor.fetchall()
        
        if not students:
            return 0.0
        
        # Calculate class average using single SQL query (no N+1)
        cursor.execute("""
            SELECT AVG(percentage) as avg_percentage
            FROM (
                SELECT 
                    s.id,
                    SUM(m.marks_obtained) as total_obtained,
                    SUM(s2.max_marks) as total_maximum,
                    (SUM(m.marks_obtained) * 100.0 / SUM(s2.max_marks)) as percentage
                FROM students s
                JOIN marks m ON s.id = m.student_id
                JOIN subjects s2 ON m.subject_id = s2.id
                WHERE (
                    SELECT COUNT(*) 
                    FROM marks m2 
                    WHERE m2.student_id = s.id
                ) = (SELECT COUNT(*) FROM subjects)
                GROUP BY s.id
            ) as student_totals
        """)
        
        row = cursor.fetchone()
        avg = row['avg_percentage'] if row and row['avg_percentage'] else 0
        
        return round(float(avg), 2)
        
    finally:
        cursor.close()


def calculate_pass_fail_stats(db_connection) -> dict:
    """Calculate pass/fail statistics.
    
    Args:
        db_connection: Database connection object
            
    Returns:
        Dictionary with:
        - 'pass_count': Number of passing students
        - 'fail_count': Number of failing students
        - 'total': Total students with results
        - 'pass_percentage': Pass percentage
        - 'fail_percentage': Fail percentage
    """
    cursor = db_connection.cursor()
    
    try:
        # Get all students with complete results
        cursor.execute("""
            SELECT s.id
            FROM students s
            WHERE (
                SELECT COUNT(*) 
                FROM marks m 
                WHERE m.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
        """)
        students = cursor.fetchall()
        
        pass_count = 0
        fail_count = 0
        
        # Get all students with complete results in one query
        cursor.execute("""
            SELECT 
                s.id,
                SUM(m.marks_obtained) as total_obtained,
                SUM(s2.max_marks) as total_maximum
            FROM students s
            JOIN marks m ON s.id = m.student_id
            JOIN subjects s2 ON m.subject_id = s2.id
            WHERE (
                SELECT COUNT(*) 
                FROM marks m2 
                WHERE m2.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
            GROUP BY s.id
        """)
        students = cursor.fetchall()
        
        for student in students:
            percentage = calculate_percentage(
                student['total_obtained'] or 0,
                student['total_maximum'] or 0
            )
            status = calculate_status_from_percentage(percentage)
            if status == 'PASS':
                pass_count += 1
            else:
                fail_count += 1
        
        total = pass_count + fail_count
        pass_percentage = round((pass_count / total * 100), 2) if total > 0 else 0.0
        fail_percentage = round((fail_count / total * 100), 2) if total > 0 else 0.0
        
        return {
            'pass_count': pass_count,
            'fail_count': fail_count,
            'total': total,
            'pass_percentage': pass_percentage,
            'fail_percentage': fail_percentage
        }
        
    finally:
        cursor.close()


def calculate_grade_distribution(db_connection) -> dict:
    """Calculate grade distribution.
    
    Args:
        db_connection: Database connection object
            
    Returns:
        Dictionary with grade counts: {'A': int, 'B': int, 'C': int, 'D': int, 'F': int}
    """
    cursor = db_connection.cursor()
    
    try:
        # Initialize distribution
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        # Get all students with complete results in one query
        cursor.execute("""
            SELECT 
                s.id,
                SUM(m.marks_obtained) as total_obtained,
                SUM(s2.max_marks) as total_maximum
            FROM students s
            JOIN marks m ON s.id = m.student_id
            JOIN subjects s2 ON m.subject_id = s2.id
            WHERE (
                SELECT COUNT(*) 
                FROM marks m2 
                WHERE m2.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
            GROUP BY s.id
        """)
        students = cursor.fetchall()
        
        for student in students:
            percentage = calculate_percentage(
                student['total_obtained'] or 0,
                student['total_maximum'] or 0
            )
            grade = calculate_grade(percentage)
            distribution[grade] += 1
        
        return distribution
        
    finally:
        cursor.close()


def get_subject_averages(db_connection) -> list:
    """Calculate subject-wise average marks.
    
    Args:
        db_connection: Database connection object
            
    Returns:
        List of subject statistics:
        [{
            'subject_id': int,
            'subject_code': str,
            'subject_name': str,
            'average_marks': float,
            'highest_marks': float,
            'lowest_marks': float,
            'pass_count': int,
            'fail_count': int
        }, ...]
    """
    cursor = db_connection.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                s.id as subject_id,
                s.subject_code,
                s.subject_name,
                s.max_marks,
                AVG(m.marks_obtained) as average_marks,
                MAX(m.marks_obtained) as highest_marks,
                MIN(m.marks_obtained) as lowest_marks,
                COUNT(*) as total_students
            FROM subjects s
            JOIN marks m ON s.id = m.subject_id
            GROUP BY s.id, s.subject_code, s.subject_name, s.max_marks
            ORDER BY s.subject_code
        """)
        
        subjects = cursor.fetchall()
        result = []
        
        for subject in subjects:
            # Calculate pass/fail count for this subject
            passing_marks = subject['max_marks'] * 0.40
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN marks_obtained >= %s THEN 1 ELSE 0 END) as pass_count,
                    SUM(CASE WHEN marks_obtained < %s THEN 1 ELSE 0 END) as fail_count
                FROM marks
                WHERE subject_id = %s
            """, (passing_marks, passing_marks, subject['subject_id']))
            
            stats = cursor.fetchone()
            
            result.append({
                'subject_id': subject['subject_id'],
                'subject_code': subject['subject_code'],
                'subject_name': subject['subject_name'],
                'average_marks': round(subject['average_marks'], 2) if subject['average_marks'] else 0,
                'highest_marks': subject['highest_marks'] or 0,
                'lowest_marks': subject['lowest_marks'] or 0,
                'pass_count': stats['pass_count'] or 0,
                'fail_count': stats['fail_count'] or 0,
                'total_students': subject['total_students']
            })
        
        return result
        
    finally:
        cursor.close()


def get_top_performers(limit: int, db_connection) -> list:
    """Get top performing students.
    
    Args:
        limit: Maximum number of students to return
        db_connection: Database connection object
            
    Returns:
        List of top students sorted by percentage (descending):
        [{
            'student_id': int,
            'roll_number': str,
            'name': str,
            'percentage': float,
            'grade': str
        }, ...]
    """
    cursor = db_connection.cursor()
    
    try:
        # Get all students with complete results in one query
        cursor.execute("""
            SELECT 
                s.id as student_id,
                s.roll_number,
                s.name,
                SUM(m.marks_obtained) as total_obtained,
                SUM(s2.max_marks) as total_maximum
            FROM students s
            JOIN marks m ON s.id = m.student_id
            JOIN subjects s2 ON m.subject_id = s2.id
            WHERE (
                SELECT COUNT(*) 
                FROM marks m2 
                WHERE m2.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
            GROUP BY s.id, s.roll_number, s.name
        """)
        students = cursor.fetchall()
        
        results = []
        for student in students:
            percentage = calculate_percentage(
                student['total_obtained'] or 0,
                student['total_maximum'] or 0
            )
            grade = calculate_grade(percentage)
            results.append({
                'student_id': student['student_id'],
                'roll_number': student['roll_number'],
                'name': student['name'],
                'percentage': percentage,
                'grade': grade
            })
        
        # Sort by percentage descending
        results.sort(key=lambda x: x['percentage'], reverse=True)
        
        return results[:limit]
        
    finally:
        cursor.close()


def calculate_subject_pass_fail_stats(db_connection) -> dict:
    """Calculate pass/fail statistics per subject.
    
    Args:
        db_connection: Database connection object
            
    Returns:
        Dictionary with subject pass/fail stats
    """
    cursor = db_connection.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                s.id as subject_id,
                s.subject_name,
                s.max_marks,
                COUNT(m.id) as total_appeared,
                SUM(CASE WHEN m.marks_obtained >= (s.max_marks * 0.40) THEN 1 ELSE 0 END) as passed,
                SUM(CASE WHEN m.marks_obtained < (s.max_marks * 0.40) THEN 1 ELSE 0 END) as failed
            FROM subjects s
            LEFT JOIN marks m ON s.id = m.subject_id
            GROUP BY s.id, s.subject_name, s.max_marks
            ORDER BY s.subject_name
        """)
        
        subjects = cursor.fetchall()
        
        result = []
        for subject in subjects:
            total = subject['total_appeared'] or 0
            pass_pct = round((subject['passed'] / total * 100), 2) if total > 0 else 0.0
            fail_pct = round((subject['failed'] / total * 100), 2) if total > 0 else 0.0
            
            result.append({
                'subject_name': subject['subject_name'],
                'total_appeared': total,
                'passed': subject['passed'] or 0,
                'failed': subject['failed'] or 0,
                'pass_percentage': pass_pct,
                'fail_percentage': fail_pct
            })
        
        return {'subjects': result}
        
    finally:
        cursor.close()