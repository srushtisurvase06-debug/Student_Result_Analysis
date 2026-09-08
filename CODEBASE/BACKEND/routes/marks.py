"""Marks Management CRUD routes.

Phase 9: Marks CRUD with student-subject selection, validation, and absent marking.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from utils.db import execute_query, fetch_all, fetch_one
from utils.decorators import login_required
from utils.validators import validate_marks_data, validate_subject_code

bp = Blueprint('marks', __name__, url_prefix='/marks')


@bp.route('/')
@login_required
def list_marks():
    """Display list of all marks with search."""
    # Get search parameter
    search = request.args.get('search', '').strip()
    
    # Build query with optional search
    query = """
        SELECT m.id, s.roll_number, s.name AS student_name,
               sub.subject_code, sub.subject_name, sub.max_marks,
               m.marks_obtained, m.is_absent,
               m.created_at, m.updated_at
        FROM marks m
        JOIN students s ON m.student_id = s.id
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE 1=1
    """
    params = []
    
    if search:
        query += """
            AND (s.roll_number ILIKE %s 
                 OR s.name ILIKE %s 
                 OR sub.subject_code ILIKE %s 
                 OR sub.subject_name ILIKE %s)
        """
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param, search_param])
    
    query += " ORDER BY s.roll_number, sub.subject_code"
    
    marks = fetch_all(query, params)
    
    return render_template(
        'marks/list.html',
        marks=marks,
        search=search
    )


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_marks():
    """Add new marks entry."""
    # Get students and subjects for dropdowns
    students = fetch_all('SELECT id, roll_number, name FROM students ORDER BY roll_number')
    subjects = fetch_all('SELECT id, subject_code, subject_name, max_marks FROM subjects ORDER BY subject_code')
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        marks_obtained = (request.form.get('marks_obtained') or '').strip()
        is_absent = request.form.get('is_absent') == 'on'
        
        # Get subject max_marks for validation
        subject = fetch_one(
            'SELECT id, subject_code, subject_name, max_marks FROM subjects WHERE id = %s',
            (subject_id,)
        )
        
        if not subject:
            flash('Subject not found.', 'error')
            return render_template(
                'marks/add.html',
                students=students,
                subjects=subjects,
                selected_student=student_id,
                selected_subject=subject_id,
                marks_obtained=marks_obtained,
                is_absent=is_absent
            )
        
        # Prepare form data
        form_data = {
            'marks_obtained': marks_obtained,
            'max_marks': subject['max_marks'],
            'is_absent': is_absent
        }
        
        # If absent, marks must be 0
        if is_absent:
            form_data['marks_obtained'] = '0'
        
        # Validate
        errors = validate_marks_data(form_data)
        
        if errors:
            return render_template(
                'marks/add.html',
                students=students,
                subjects=subjects,
                selected_student=student_id,
                selected_subject=subject_id,
                marks_obtained=marks_obtained,
                is_absent=is_absent,
                errors=errors,
                subject_info=subject
            )
        
        # Check for duplicate marks entry
        existing = fetch_one(
            'SELECT id FROM marks WHERE student_id = %s AND subject_id = %s',
            (student_id, subject_id)
        )
        
        if existing:
            errors = {'marks_obtained': 'Marks already exist for this student-subject combination. Please edit the existing record.'}
            return render_template(
                'marks/add.html',
                students=students,
                subjects=subjects,
                selected_student=student_id,
                selected_subject=subject_id,
                marks_obtained=marks_obtained,
                is_absent=is_absent,
                errors=errors,
                subject_info=subject
            )
        
        # Insert marks
        execute_query(
            'INSERT INTO marks (student_id, subject_id, marks_obtained, is_absent) VALUES (%s, %s, %s, %s)',
            (student_id, subject_id, int(form_data['marks_obtained']), is_absent)
        )
        
        flash('Marks added successfully!', 'success')
        return redirect(url_for('marks.list_marks'))
    
    return render_template(
        'marks/add.html',
        students=students,
        subjects=subjects
    )


@bp.route('/<int:marks_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_marks(marks_id):
    """Edit existing marks entry."""
    # Get marks record
    marks = fetch_one('''
        SELECT m.id, m.student_id, m.subject_id, m.marks_obtained, m.is_absent,
               s.roll_number, s.name AS student_name,
               sub.subject_code, sub.subject_name, sub.max_marks
        FROM marks m
        JOIN students s ON m.student_id = s.id
        JOIN subjects sub ON m.subject_id = sub.id
        WHERE m.id = %s
    ''', (marks_id,))
    
    if not marks:
        flash('Marks record not found.', 'error')
        return redirect(url_for('marks.list_marks'))
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject_id = request.form.get('subject_id')
        marks_obtained = (request.form.get('marks_obtained') or '').strip()
        is_absent = request.form.get('is_absent') == 'on'
        
        # Get subject max_marks for validation
        subject = fetch_one(
            'SELECT id, subject_code, subject_name, max_marks FROM subjects WHERE id = %s',
            (subject_id,)
        )
        
        if not subject:
            flash('Subject not found.', 'error')
            return render_template(
                'marks/edit.html',
                marks=marks,
                students=[marks],
                subjects=[subject],
                marks_obtained=marks_obtained,
                is_absent=is_absent
            )
        
        # Prepare form data
        form_data = {
            'marks_obtained': marks_obtained,
            'max_marks': subject['max_marks'],
            'is_absent': is_absent
        }
        
        # If absent, marks must be 0
        if is_absent:
            form_data['marks_obtained'] = '0'
        
        # Validate
        errors = validate_marks_data(form_data)
        
        if errors:
            return render_template(
                'marks/edit.html',
                marks=marks,
                students=[marks],
                subjects=[subject],
                marks_obtained=marks_obtained,
                is_absent=is_absent,
                errors=errors,
                subject_info=subject
            )
        
        # Check for duplicate marks entry (excluding current record)
        existing = fetch_one(
            'SELECT id FROM marks WHERE student_id = %s AND subject_id = %s AND id != %s',
            (student_id, subject_id, marks_id)
        )
        
        if existing:
            errors = {'marks_obtained': 'Marks already exist for this student-subject combination. Please edit the existing record.'}
            return render_template(
                'marks/edit.html',
                marks=marks,
                students=[marks],
                subjects=[subject],
                marks_obtained=marks_obtained,
                is_absent=is_absent,
                errors=errors,
                subject_info=subject
            )
        
        # Update marks
        execute_query(
            'UPDATE marks SET student_id = %s, subject_id = %s, marks_obtained = %s, is_absent = %s, updated_at = NOW() WHERE id = %s',
            (student_id, subject_id, int(form_data['marks_obtained']), is_absent, marks_id)
        )
        
        flash('Marks updated successfully!', 'success')
        return redirect(url_for('marks.list_marks'))
    
    return render_template('marks/edit.html', marks=marks)


@bp.route('/<int:marks_id>/delete', methods=['POST'])
@login_required
def delete_marks(marks_id):
    """Delete marks entry."""
    # Check if marks exists
    marks = fetch_one('SELECT id FROM marks WHERE id = %s', (marks_id,))
    
    if not marks:
        flash('Marks record not found.', 'error')
        return redirect(url_for('marks.list_marks'))
    
    # Delete marks
    execute_query('DELETE FROM marks WHERE id = %s', (marks_id,))
    
    flash('Marks record deleted successfully!', 'success')
    return redirect(url_for('marks.list_marks'))