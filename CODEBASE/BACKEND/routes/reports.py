"""Reports & Print Functionality routes.

Phase 14: Printable reports for individual students and class-wide reports.
Provides print-friendly views and report generation functionality.
"""

from flask import Blueprint, render_template, request, abort
from utils.db import get_db_connection
from utils.decorators import login_required
from utils.calculations import (
    generate_full_result,
    calculate_pass_fail_stats,
    calculate_grade_distribution,
    calculate_class_average,
    get_top_performers,
    get_subject_averages
)

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/')
@login_required
def index():
    """Display reports menu."""
    # Get analytics using Phase 10 calculation logic
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Total counts
        cursor.execute('SELECT COUNT(*) AS count FROM students')
        total_students = cursor.fetchone()['count'] or 0
        
        cursor.execute('SELECT COUNT(*) AS count FROM subjects')
        total_subjects = cursor.fetchone()['count'] or 0
        
        # Students with complete results
        if total_subjects > 0:
            cursor.execute('''
                SELECT COUNT(*) AS count
                FROM (
                    SELECT student_id
                    FROM marks
                    GROUP BY student_id
                    HAVING COUNT(subject_id) = %s
                ) t
            ''', (total_subjects,))
            result = cursor.fetchone()
            students_with_results = result['count'] if result else 0
        else:
            students_with_results = 0
        
        # Get analytics
        pass_fail_stats = calculate_pass_fail_stats(conn)
        grade_dist = calculate_grade_distribution(conn)
        class_avg = calculate_class_average(conn)
        
        cursor.close()
    finally:
        conn.close()
    
    stats = {
        'total_students': int(total_students),
        'total_subjects': int(total_subjects),
        'students_with_results': int(students_with_results),
        'pass_percentage': pass_fail_stats.get('pass_percentage', 0.0),
        'fail_percentage': pass_fail_stats.get('fail_percentage', 0.0),
        'grade_distribution': grade_dist,
        'pass_count': pass_fail_stats.get('pass_count', 0),
        'fail_count': pass_fail_stats.get('fail_count', 0),
        'class_average': class_avg,
    }
    
    return render_template(
        'reports/index.html',
        stats=stats
    )


@bp.route('/individual')
@login_required
def individual():
    """Generate individual student report with student selection."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get all students with complete results
        cursor.execute('''
            SELECT s.id, s.roll_number, s.name
            FROM students s
            WHERE (
                SELECT COUNT(*) 
                FROM marks m 
                WHERE m.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
            ORDER BY s.roll_number
        ''')
        students = cursor.fetchall()
        
        # Get student_id from query parameter or use first student
        student_id = request.args.get('student_id', type=int)
        if not student_id and students:
            student_id = students[0]['id']
        
        student = None
        result = None
        
        if student_id:
            cursor.execute("SELECT id, roll_number, name, email, date_of_birth, gender, contact_number FROM students WHERE id = %s", (student_id,))
            student = cursor.fetchone()
            
            if student:
                result = generate_full_result(student_id, conn)
        
        cursor.close()
    finally:
        conn.close()
    
    return render_template(
        'reports/individual.html',
        students=students if students else [],
        student=dict(student) if student else None,
        result=result
    )


@bp.route('/class')
@login_required
def class_report():
    """Generate class-wide report."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Total counts
        cursor.execute('SELECT COUNT(*) AS count FROM students')
        total_students = cursor.fetchone()['count'] or 0
        
        cursor.execute('SELECT COUNT(*) AS count FROM subjects')
        total_subjects = cursor.fetchone()['count'] or 0
        
        # Students with complete results
        if total_subjects > 0:
            cursor.execute('''
                SELECT COUNT(*) AS count
                FROM (
                    SELECT student_id
                    FROM marks
                    GROUP BY student_id
                    HAVING COUNT(subject_id) = %s
                ) t
            ''', (total_subjects,))
            result = cursor.fetchone()
            students_with_results = result['count'] if result else 0
        else:
            students_with_results = 0
        
        # Get analytics
        pass_fail_stats = calculate_pass_fail_stats(conn)
        grade_dist = calculate_grade_distribution(conn)
        class_avg = calculate_class_average(conn)
        top_students = get_top_performers(10, conn)
        subject_avgs = get_subject_averages(conn)
        
        cursor.close()
    finally:
        conn.close()
    
    stats = {
        'total_students': int(total_students),
        'total_subjects': int(total_subjects),
        'students_with_results': int(students_with_results),
        'pass_percentage': pass_fail_stats.get('pass_percentage', 0.0),
        'fail_percentage': pass_fail_stats.get('fail_percentage', 0.0),
        'grade_distribution': grade_dist,
        'pass_fail_count': {
            'pass': pass_fail_stats.get('pass_count', 0),
            'fail': pass_fail_stats.get('fail_count', 0)
        },
        'class_average': class_avg,
        'top_students': top_students,
        'subject_averages': subject_avgs,
    }
    
    return render_template(
        'reports/class.html',
        stats=stats
    )


@bp.route('/class-rank')
@login_required
def class_rank():
    """Generate class rank report."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get students with complete results sorted by percentage
        cursor.execute('''
            SELECT 
                s.id,
                s.roll_number,
                s.name as student_name,
                SUM(m.marks_obtained) as total_marks,
                (SUM(m.marks_obtained) * 100.0 / SUM(s2.max_marks)) as percentage,
                s2.max_marks
            FROM students s
            JOIN marks m ON s.id = m.student_id
            JOIN subjects s2 ON m.subject_id = s2.id
            WHERE (
                SELECT COUNT(*) 
                FROM marks m2 
                WHERE m2.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
            GROUP BY s.id, s.roll_number, s.name, s2.max_marks
            ORDER BY percentage DESC
        ''')
        
        students = cursor.fetchall()
        
        # Calculate grades and status for each student
        results = []
        for student in students:
            percentage = student['percentage'] or 0
            grade = 'A' if percentage >= 90 else 'B' if percentage >= 75 else 'C' if percentage >= 60 else 'D' if percentage >= 40 else 'F'
            status = 'PASS' if percentage >= 40 else 'FAIL'
            results.append({
                'student_id': student['id'],
                'roll_number': student['roll_number'],
                'student_name': student['student_name'],
                'total_marks': student['total_marks'] or 0,
                'percentage': round(percentage, 2),
                'grade': grade,
                'status': status
            })
        
        cursor.close()
    finally:
        conn.close()
    
    return render_template(
        'reports/class_rank.html',
        students=results
    )


@bp.route('/subject')
@login_required
def subject():
    """Generate subject performance report - allows selecting a specific subject."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get all subjects
        cursor.execute("SELECT id, subject_code, subject_name, max_marks FROM subjects ORDER BY subject_code")
        subjects = cursor.fetchall()
        
        # Get subject_id from query parameter or use first subject
        subject_id = request.args.get('subject_id', type=int)
        if not subject_id and subjects:
            subject_id = subjects[0]['id']
        
        subject = None
        results = []
        stats = {}
        
        if subject_id:
            # Get subject info
            cursor.execute("SELECT id, subject_code, subject_name, max_marks FROM subjects WHERE id = %s", (subject_id,))
            subject = cursor.fetchone()
            
            if subject:
                # Get subject stats
                passing_marks = subject['max_marks'] * 0.40
                
                cursor.execute("""
                    SELECT 
                        s.roll_number,
                        s.name as student_name,
                        m.marks_obtained,
                        (m.marks_obtained * 100.0 / s2.max_marks) as percentage,
                        CASE WHEN m.marks_obtained >= %s THEN 'PASS' ELSE 'FAIL' END as status
                    FROM marks m
                    JOIN students s ON m.student_id = s.id
                    JOIN subjects s2 ON m.subject_id = s2.id
                    WHERE m.subject_id = %s
                    ORDER BY percentage DESC
                """, (passing_marks, subject_id))
                
                results = [dict(row) for row in cursor.fetchall()]
                
                # Calculate grade for each result
                for r in results:
                    if r['percentage'] >= 90:
                        r['grade'] = 'A'
                    elif r['percentage'] >= 75:
                        r['grade'] = 'B'
                    elif r['percentage'] >= 60:
                        r['grade'] = 'C'
                    elif r['percentage'] >= 40:
                        r['grade'] = 'D'
                    else:
                        r['grade'] = 'F'
                
                # Calculate stats
                total_students = len(results)
                pass_count = sum(1 for r in results if r['status'] == 'PASS')
                fail_count = total_students - pass_count
                
                if total_students > 0:
                    highest_score = max(r['marks_obtained'] for r in results)
                    lowest_score = min(r['marks_obtained'] for r in results)
                    average_score = sum(r['marks_obtained'] for r in results) / total_students
                else:
                    highest_score = 0
                    lowest_score = 0
                    average_score = 0
                
                # Grade distribution
                grade_dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
                for r in results:
                    grade_dist[r['grade']] += 1
                
                stats = {
                    'highest_score': highest_score,
                    'lowest_score': lowest_score,
                    'average_score': round(average_score, 2) if total_students > 0 else 0,
                    'total_students': total_students,
                    'pass_count': pass_count,
                    'fail_count': fail_count,
                    'pass_percentage': round(pass_count / total_students * 100, 2) if total_students > 0 else 0,
                    'fail_percentage': round(fail_count / total_students * 100, 2) if total_students > 0 else 0,
                    'grade_distribution': grade_dist,
                }
        
        cursor.close()
    finally:
        conn.close()
    
    return render_template(
        'reports/subject.html',
        subjects=subjects if subjects else [],
        subject=dict(subject) if subject else None,
        stats=stats,
        results=results
    )


@bp.route('/grade-distribution')
@login_required
def grade_distribution():
    """Generate grade distribution report."""
    conn = get_db_connection()
    try:
        # Get analytics
        pass_fail_stats = calculate_pass_fail_stats(conn)
        grade_dist = calculate_grade_distribution(conn)
        class_avg = calculate_class_average(conn)
        
        # Total students count
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) AS count FROM students')
        total_students = cursor.fetchone()['count'] or 0
        cursor.close()
    finally:
        conn.close()
    
    stats = {
        'total_students': int(total_students),
        'pass_percentage': pass_fail_stats.get('pass_percentage', 0.0),
        'fail_percentage': pass_fail_stats.get('fail_percentage', 0.0),
        'grade_distribution': grade_dist,
        'pass_count': pass_fail_stats.get('pass_count', 0),
        'fail_count': pass_fail_stats.get('fail_count', 0),
        'class_average': class_avg,
    }
    
    return render_template(
        'reports/grade_distribution.html',
        stats=stats
    )
