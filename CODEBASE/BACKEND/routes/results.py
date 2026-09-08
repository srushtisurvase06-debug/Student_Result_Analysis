"""Admin Results View routes.

Phase 11: Admin view of all student results with filtering and details.

Phase 12: Public result lookup without authentication.
"""

from flask import Blueprint, render_template, request, flash

from utils.calculations import calculate_percentage, calculate_grade, generate_full_result
from utils.db import fetch_all, get_db_connection
from utils.decorators import login_required

bp = Blueprint('results', __name__, url_prefix='/results')


@bp.route('/lookup', methods=['GET', 'POST'])
def lookup():
    """Public result lookup page - students can find results without login."""
    if request.method == 'POST':
        roll_number = request.form.get('roll_number', '').strip()
        date_of_birth = request.form.get('date_of_birth', '').strip()
        
        # Validate required fields
        if not roll_number or not date_of_birth:
            flash('Please enter both Roll Number and Date of Birth.', 'error')
            return render_template('results/lookup.html')
        
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Find student by roll_number and DOB
            cursor.execute("""
                SELECT id, roll_number, name, email, date_of_birth, gender, contact_number
                FROM students
                WHERE roll_number = %s AND date_of_birth = %s
            """, (roll_number, date_of_birth))
            
            student = cursor.fetchone()
            cursor.close()
            
            if not student:
                # Security: Don't reveal which field was wrong
                flash('Invalid credentials. Please check your Roll Number and Date of Birth.', 'error')
                return render_template('results/lookup.html')
            
            # Get result using existing Phase 10 calculation logic
            result = generate_full_result(student['id'], conn)
            
            if not result:
                flash('Result not yet published. Please contact your administrator.', 'error')
                return render_template('results/lookup.html')
            
            # Redirect to result display page
            return render_template('results/student_result.html', result=result)
            
        finally:
            conn.close()
    
    return render_template('results/lookup.html')


@bp.route('/')
@login_required
def list_results():
    """Display list of all students with their results."""
    # Get search parameter
    search = request.args.get('search', '').strip()
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get all students with complete results (all subjects have marks)
        base_query = """
            SELECT s.id, s.roll_number, s.name, s.email, s.date_of_birth, s.gender, s.contact_number
            FROM students s
            WHERE (
                SELECT COUNT(*) 
                FROM marks m 
                WHERE m.student_id = s.id
            ) = (SELECT COUNT(*) FROM subjects)
        """
        params = []
        
        if search:
            base_query += " AND (s.roll_number ILIKE %s OR s.name ILIKE %s)"
            search_param = f'%{search}%'
            params.extend([search_param, search_param])
        
        base_query += " ORDER BY s.roll_number"
        
        students = fetch_all(base_query, params)
        
        # Get all subjects once
        cursor.execute("SELECT id, subject_code, subject_name, max_marks FROM subjects ORDER BY subject_code")
        subjects = {row['id']: dict(row) for row in cursor.fetchall()}
        total_subjects = len(subjects)
        
        # Batch query for all marks at once
        student_ids = [s['id'] for s in students]
        if student_ids:
            placeholders = ','.join(['%s'] * len(student_ids))
            cursor.execute(f"""
                SELECT 
                    m.student_id,
                    s.subject_code,
                    s.subject_name,
                    s.max_marks,
                    m.marks_obtained
                FROM marks m
                JOIN subjects s ON m.subject_id = s.id
                WHERE m.student_id IN ({placeholders})
                ORDER BY m.student_id, s.subject_code
            """, student_ids)
            all_marks = cursor.fetchall()
        else:
            all_marks = []
        
        # Group marks by student
        marks_by_student = {}
        for mark in all_marks:
            student_id = mark['student_id']
            if student_id not in marks_by_student:
                marks_by_student[student_id] = []
            marks_by_student[student_id].append(dict(mark))
        
        # Batch query for pass/fail status for all students
        if student_ids:
            placeholders = ','.join(['%s'] * len(student_ids))
            cursor.execute(f"""
                SELECT student_id, 
                       COUNT(*) FILTER (WHERE is_absent = TRUE) as absent_count,
                       COUNT(*) FILTER (WHERE marks_obtained < (s.max_marks * 0.40)) as fail_count,
                       SUM(marks_obtained) as total_obtained,
                       SUM(s.max_marks) as total_maximum
                FROM marks m
                JOIN subjects s ON m.subject_id = s.id
                WHERE student_id IN ({placeholders})
                GROUP BY student_id
                HAVING COUNT(*) = {total_subjects}
            """, student_ids)
            status_rows = cursor.fetchall()
        else:
            status_rows = []
        
        status_by_student = {row['student_id']: dict(row) for row in status_rows}
        
        cursor.close()
    finally:
        conn.close()
    
    # Calculate results for each student
    results = []
    for student in students:
        student_marks = marks_by_student.get(student['id'], [])
        
        if len(student_marks) < total_subjects:
            continue
        
        total_obtained = sum(m['marks_obtained'] or 0 for m in student_marks)
        total_maximum = sum(m['max_marks'] for m in student_marks)
        
        percentage = calculate_percentage(total_obtained, total_maximum)
        grade = calculate_grade(percentage)
        
        # Determine pass/fail
        status_info = status_by_student.get(student['id'], {})
        absent_count = status_info.get('absent_count', 0)
        if absent_count > 0:
            status = 'FAIL'
            reason = f'Absent in {absent_count} subject(s)'
        else:
            if total_maximum == 0:
                status = 'FAIL'
                reason = 'No marks found for student'
            else:
                pct = (total_obtained / total_maximum) * 100
                if pct < 40:
                    status = 'FAIL'
                    reason = f'Overall percentage ({round(pct, 2)}%) below 40%'
                else:
                    # Check subject-wise passing
                    subject_failures = []
                    for mark in student_marks:
                        passing = mark['marks_obtained'] >= (mark['max_marks'] * 0.40)
                        if not passing:
                            subject_failures.append(mark['subject_name'])
                    
                    if subject_failures:
                        status = 'FAIL'
                        reason = f'Failed in: {", ".join(subject_failures)}'
                    else:
                        status = 'PASS'
                        reason = 'Passed all subjects with overall percentage >= 40%'
        
        # Build subject-wise details
        subject_results = []
        for mark in student_marks:
            passing_marks = mark['max_marks'] * 0.40
            subject_passed = mark['marks_obtained'] >= passing_marks
            subject_results.append({
                'subject_code': mark['subject_code'],
                'subject_name': mark['subject_name'],
                'marks_obtained': mark['marks_obtained'],
                'max_marks': mark['max_marks'],
                'passing_marks': passing_marks,
                'subject_status': 'PASS' if subject_passed else 'FAIL'
            })
        
        result = {
            'student': {
                'id': student['id'],
                'roll_number': student['roll_number'],
                'name': student['name'],
                'email': student['email'],
                'date_of_birth': student['date_of_birth'],
                'gender': student['gender'],
                'contact_number': student['contact_number']
            },
            'total_obtained': total_obtained,
            'total_maximum': total_maximum,
            'percentage': percentage,
            'grade': grade,
            'status': status,
            'status_reason': reason,
            'subject_results': subject_results,
            'subject_count': len(student_marks),
            'subjects_total': total_subjects
        }
        results.append(result)
    
    return render_template(
        'results/list.html',
        results=results,
        search=search
    )


@bp.route('/<int:student_id>')
@login_required
def detail(student_id):
    """Display detailed result for a specific student."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute("""
            SELECT id, roll_number, name, email, date_of_birth, gender, contact_number
            FROM students WHERE id = %s
        """, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            return render_template('results/not_found.html'), 404
        
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
            return render_template(
                'results/incomplete.html',
                result={
                    'student': dict(student),
                    'status': 'incomplete',
                    'message': 'Result not yet published',
                    'subjects_completed': marks_count,
                    'subjects_total': subjects_total
                }
            )
        
        # Get all marks for this student
        cursor.execute("""
            SELECT 
                s.subject_code,
                s.subject_name,
                m.marks_obtained,
                s.max_marks
            FROM marks m
            JOIN subjects s ON m.subject_id = s.id
            WHERE m.student_id = %s
            ORDER BY s.subject_code
        """, (student_id,))
        all_marks = cursor.fetchall()
        
        # Calculate totals
        total_obtained = sum(m['marks_obtained'] or 0 for m in all_marks)
        total_maximum = sum(m['max_marks'] for m in all_marks)
        
        # Calculate percentage
        percentage = calculate_percentage(total_obtained, total_maximum)
        
        # Assign grade
        grade = calculate_grade(percentage)
        
        # Determine pass/fail status
        absent_count = sum(1 for m in all_marks if m['marks_obtained'] == 0)  # Simplified - check if any absent
        
        if absent_count > 0:
            status = 'FAIL'
            reason = f'Absent in {absent_count} subject(s)'
        elif total_maximum == 0:
            status = 'FAIL'
            reason = 'No marks found for student'
        else:
            pct = (total_obtained / total_maximum) * 100
            if pct < 40:
                status = 'FAIL'
                reason = f'Overall percentage ({round(pct, 2)}%) below 40%'
            else:
                # Check subject-wise passing
                subject_failures = []
                for mark in all_marks:
                    if mark['marks_obtained'] < (mark['max_marks'] * 0.40):
                        subject_failures.append(mark['subject_name'])
                
                if subject_failures:
                    status = 'FAIL'
                    reason = f'Failed in: {", ".join(subject_failures)}'
                else:
                    status = 'PASS'
                    reason = 'Passed all subjects with overall percentage >= 40%'
        
        # Build subject-wise details
        subject_results = []
        for mark in all_marks:
            passing_marks = mark['max_marks'] * 0.40
            subject_passed = mark['marks_obtained'] >= passing_marks
            subject_results.append({
                'subject_code': mark['subject_code'],
                'subject_name': mark['subject_name'],
                'marks_obtained': mark['marks_obtained'],
                'max_marks': mark['max_marks'],
                'passing_marks': passing_marks,
                'subject_status': 'PASS' if subject_passed else 'FAIL'
            })
        
        result = {
            'student': dict(student),
            'total_obtained': total_obtained,
            'total_maximum': total_maximum,
            'percentage': percentage,
            'grade': grade,
            'status': status,
            'status_reason': reason,
            'subject_results': subject_results,
            'subject_count': marks_count,
            'subjects_total': subjects_total
        }
        
    finally:
        conn.close()
    
    return render_template('results/detail.html', result=result)