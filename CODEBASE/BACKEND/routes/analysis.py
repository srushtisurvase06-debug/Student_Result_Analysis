"""Performance Analytics routes.

Phase 13: Charts and analytics dashboard showing Pass/Fail Ratio, Grade Distribution,
Top Performers, and Subject-wise statistics.
"""

from flask import Blueprint, render_template

from utils.calculations import calculate_class_average, calculate_pass_fail_stats, calculate_grade_distribution, get_top_performers, get_subject_averages
from utils.db import get_db_connection
from utils.decorators import login_required

bp = Blueprint('analysis', __name__, url_prefix='/analysis')


@bp.route('/')
@login_required
def index():
    """Display performance analytics dashboard with charts and statistics."""
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
        
        # Get subject data for analysis cards - REUSE SAME CONNECTION
        cursor.execute("""
            SELECT 
                s.id,
                s.subject_code,
                s.subject_name,
                COUNT(m.id) as total_students,
                ROUND(AVG(CASE WHEN m.marks_obtained >= (s.max_marks * 0.40) THEN 100.0 ELSE 0.0 END), 2) as pass_percentage,
                ROUND(AVG(m.marks_obtained), 2) as average_score
            FROM subjects s
            LEFT JOIN marks m ON s.id = m.subject_id
            GROUP BY s.id, s.subject_code, s.subject_name
            ORDER BY s.subject_code
        """)
        
        subjects = [dict(row) for row in cursor.fetchall()]
        
        # Get analytics for charts - REUSE SAME CONNECTION
        grade_distribution = calculate_grade_distribution(conn)
        pass_fail_stats = calculate_pass_fail_stats(conn)
        
        cursor.close()
    finally:
        conn.close()
    
    return render_template(
        'analysis/index.html',
        subjects=subjects,
        grade_distribution=grade_distribution,
        pass_count=pass_fail_stats.get('pass_count', 0),
        fail_count=pass_fail_stats.get('fail_count', 0)
    )


@bp.route('/subject/<int:subject_id>')
@login_required
def subject(subject_id):
    """Display subject-specific analysis."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get subject info
        cursor.execute("SELECT id, subject_code, subject_name, max_marks FROM subjects WHERE id = %s", (subject_id,))
        subject = cursor.fetchone()
        
        if not subject:
            return abort(404)
        
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
            if r['percentage'] >= 90:
                grade_dist['A'] += 1
            elif r['percentage'] >= 75:
                grade_dist['B'] += 1
            elif r['percentage'] >= 60:
                grade_dist['C'] += 1
            elif r['percentage'] >= 40:
                grade_dist['D'] += 1
            else:
                grade_dist['F'] += 1
        
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
        'analysis/subject.html',
        subject=dict(subject),
        stats=stats,
        results=results
    )
