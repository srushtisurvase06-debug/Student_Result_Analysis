"""Student Management CRUD routes.

Phase 7: Student CRUD with validation, search, and filter.
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from utils.db import execute_query, fetch_all, fetch_one
from utils.decorators import login_required
from utils.validators import validate_student_data, validate_roll_number

bp = Blueprint('students', __name__, url_prefix='/students')


@bp.route('/')
@login_required
def list_students():
    """Display list of all students with search and filter."""
    # Get search and filter parameters
    search = request.args.get('search', '').strip()
    gender = request.args.get('gender', '').strip()
    
    # Build query with optional search and filter
    query = "SELECT * FROM students"
    params = []
    
    if search:
        query += " WHERE roll_number ILIKE %s OR name ILIKE %s"
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    if gender:
        if search:
            query += " AND gender = %s"
        else:
            query += " WHERE gender = %s"
        params.append(gender)
    
    query += " ORDER BY roll_number"
    
    students = fetch_all(query, params)
    
    return render_template(
        'students/list.html',
        students=students,
        search=search,
        gender=gender
    )


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add new student."""
    if request.method == 'POST':
        roll_number = (request.form.get('roll_number') or '').strip()
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        date_of_birth = (request.form.get('date_of_birth') or '').strip()
        gender = (request.form.get('gender') or '').strip()
        contact_number = (request.form.get('contact_number') or '').strip()
        
        # Validate all fields
        errors = validate_student_data({
            'roll_number': roll_number,
            'name': name,
            'email': email,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'contact_number': contact_number,
        })
        
        if errors:
            return render_template(
                'students/add.html',
                errors=errors,
                form_data={
                    'roll_number': roll_number,
                    'name': name,
                    'email': email,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'contact_number': contact_number,
                }
            )
        
        # Check for duplicate roll number
        existing = fetch_one(
            'SELECT id FROM students WHERE roll_number = %s',
            (roll_number,)
        )
        
        if existing:
            errors = {'roll_number': 'A student with this roll number already exists'}
            return render_template(
                'students/add.html',
                errors=errors,
                form_data={
                    'roll_number': roll_number,
                    'name': name,
                    'email': email,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'contact_number': contact_number,
                }
            )
        
        # Insert student
        execute_query(
            'INSERT INTO students (roll_number, name, email, date_of_birth, gender, contact_number) VALUES (%s, %s, %s, %s, %s, %s)',
            (roll_number, name, email, date_of_birth, gender, contact_number)
        )
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('students.list_students'))
    
    return render_template('students/add.html')


@bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """Edit existing student."""
    student = fetch_one(
        'SELECT * FROM students WHERE id = %s',
        (student_id,)
    )
    
    if not student:
        flash('Student not found.', 'error')
        return redirect(url_for('students.list_students'))
    
    if request.method == 'POST':
        roll_number = (request.form.get('roll_number') or '').strip()
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        date_of_birth = (request.form.get('date_of_birth') or '').strip()
        gender = (request.form.get('gender') or '').strip()
        contact_number = (request.form.get('contact_number') or '').strip()
        
        # Validate all fields
        errors = validate_student_data({
            'roll_number': roll_number,
            'name': name,
            'email': email,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'contact_number': contact_number,
        })
        
        if errors:
            return render_template(
                'students/edit.html',
                errors=errors,
                student=student,
                form_data={
                    'roll_number': roll_number,
                    'name': name,
                    'email': email,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'contact_number': contact_number,
                }
            )
        
        # Check for duplicate roll number (excluding current student)
        if roll_number != student['roll_number']:
            existing = fetch_one(
                'SELECT id FROM students WHERE roll_number = %s AND id != %s',
                (roll_number, student_id)
            )
            
            if existing:
                errors = {'roll_number': 'A student with this roll number already exists'}
                return render_template(
                    'students/edit.html',
                    errors=errors,
                    student=student,
                    form_data={
                        'roll_number': roll_number,
                        'name': name,
                        'email': email,
                        'date_of_birth': date_of_birth,
                        'gender': gender,
                        'contact_number': contact_number,
                    }
                )
        
        # Update student
        execute_query(
            'UPDATE students SET roll_number = %s, name = %s, email = %s, date_of_birth = %s, gender = %s, contact_number = %s, updated_at = NOW() WHERE id = %s',
            (roll_number, name, email, date_of_birth, gender, contact_number, student_id)
        )
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.list_students'))
    
    return render_template('students/edit.html', student=student)


@bp.route('/<int:student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id):
    """Delete student (with marks cascade)."""
    # Check for existing marks
    marks_count = fetch_one(
        'SELECT COUNT(*) AS count FROM marks WHERE student_id = %s',
        (student_id,)
    )
    
    marks_count = marks_count['count'] if marks_count else 0
    
    if marks_count > 0:
        # Store student ID in session for confirmation
        session['pending_student_delete'] = student_id
    
    # Delete student (CASCADE will delete marks)
    execute_query('DELETE FROM students WHERE id = %s', (student_id,))
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students.list_students'))


@bp.route('/confirm-delete', methods=['POST'])
@login_required
def confirm_delete():
    """Confirm delete of student with marks."""
    student_id = session.pop('pending_student_delete', None)
    
    if not student_id:
        flash('Invalid delete request.', 'error')
        return redirect(url_for('students.list_students'))
    
    # Delete student (CASCADE will delete marks)
    execute_query('DELETE FROM students WHERE id = %s', (student_id,))
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students.list_students'))