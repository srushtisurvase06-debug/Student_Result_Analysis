"""Dashboard routes for admin statistics and analytics.

Phase 6: Admin dashboard showing total counts.

Phase 13: Performance Analytics - Pass/Fail Ratio, Grade Distribution, Top Performers,
          Class Average, Subject-wise statistics.
"""

from flask import Blueprint, render_template

from utils.calculations import calculate_class_average, calculate_pass_fail_stats, calculate_grade_distribution, get_top_performers, get_subject_averages
from utils.db import get_db_connection
from utils.decorators import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def calculate_dashboard_stats():
    """Calculate all dashboard statistics from database using Phase 10 calculation logic.
    
    Returns dict with:
        total_students: int
        total_subjects: int
        students_with_results: int (students with marks for ALL subjects)
        pass_percentage: float
        fail_percentage: float
        grade_distribution: dict with A, B, C, D, F counts
        pass_fail_count: dict with pass and fail counts
        class_average: float
        top_students: list of top 5 students
        subject_averages: list of subject-wise statistics
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Total counts
        cursor.execute('SELECT COUNT(*) AS count FROM students')
        total_students = cursor.fetchone()['count'] or 0
        
        cursor.execute('SELECT COUNT(*) AS count FROM subjects')
        total_subjects = cursor.fetchone()['count'] or 0
        
        # Students with complete results (have marks for ALL subjects)
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
        
        # Use Phase 10 calculation logic for analytics - REUSE SAME CONNECTION
        # Pass/Fail statistics
        pass_fail_stats = calculate_pass_fail_stats(conn)
        
        # Grade distribution
        grade_dist = calculate_grade_distribution(conn)
        
        # Class average
        class_avg = calculate_class_average(conn)
        
        # Top 5 performers
        top_students = get_top_performers(5, conn)
        
        # Subject averages
        subject_avgs = get_subject_averages(conn)
        
        cursor.close()
    finally:
        conn.close()
    
    return {
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


@bp.route('/')
@login_required
def index():
    """Display admin dashboard with statistics and charts."""
    stats = calculate_dashboard_stats()
    
    return render_template(
        'dashboard/index.html',
        stats=stats
    )