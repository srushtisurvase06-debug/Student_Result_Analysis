"""Subject Management CRUD routes.

Phase 8: Subject CRUD with validation and search.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from utils.db import execute_query, fetch_all, fetch_one
from utils.decorators import login_required
from utils.validators import validate_subject_data

bp = Blueprint('subjects', __name__, url_prefix='/subjects')


@bp.route('/')
@login_required
def list_subjects():
    """Display list of all subjects with search."""
    # Get search parameter
    search = request.args.get('search', '').strip()
    
    # Build query with optional search
    query = "SELECT * FROM subjects"
    params = []
    
    if search:
        query += " WHERE subject_code ILIKE %s OR subject_name ILIKE %s"
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    query += " ORDER BY subject_code"
    
    subjects = fetch_all(query, params)
    
    return render_template(
        'subjects/list.html',
        subjects=subjects,
        search=search
    )


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    """Add new subject."""
    if request.method == 'POST':
        subject_code = (request.form.get('subject_code') or '').strip().upper()
        subject_name = (request.form.get('subject_name') or '').strip()
        max_marks = (request.form.get('max_marks') or '').strip()
        
        # Validate all fields
        errors = validate_subject_data({
            'subject_code': subject_code,
            'subject_name': subject_name,
            'max_marks': max_marks,
        })
        
        if errors:
            return render_template(
                'subjects/add.html',
                errors=errors,
                form_data={
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'max_marks': max_marks,
                }
            )
        
        # Check for duplicate subject code (case-insensitive)
        existing = fetch_one(
            'SELECT id FROM subjects WHERE UPPER(subject_code) = UPPER(%s)',
            (subject_code,)
        )
        
        if existing:
            errors = {'subject_code': 'A subject with this Subject Code already exists'}
            return render_template(
                'subjects/add.html',
                errors=errors,
                form_data={
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'max_marks': max_marks,
                }
            )
        
        # Insert subject
        execute_query(
            'INSERT INTO subjects (subject_code, subject_name, max_marks) VALUES (%s, %s, %s)',
            (subject_code, subject_name, int(max_marks))
        )
        
        flash('Subject added successfully!', 'success')
        return redirect(url_for('subjects.list_subjects'))
    
    return render_template('subjects/add.html')


@bp.route('/<int:subject_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    """Edit existing subject."""
    subject = fetch_one(
        'SELECT * FROM subjects WHERE id = %s',
        (subject_id,)
    )
    
    if not subject:
        flash('Subject not found.', 'error')
        return redirect(url_for('subjects.list_subjects'))
    
    if request.method == 'POST':
        subject_code = (request.form.get('subject_code') or '').strip().upper()
        subject_name = (request.form.get('subject_name') or '').strip()
        max_marks = (request.form.get('max_marks') or '').strip()
        
        # Validate all fields
        errors = validate_subject_data({
            'subject_code': subject_code,
            'subject_name': subject_name,
            'max_marks': max_marks,
        })
        
        if errors:
            return render_template(
                'subjects/edit.html',
                errors=errors,
                subject=subject,
                form_data={
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'max_marks': max_marks,
                }
            )
        
        # Check for duplicate subject code (excluding current subject, case-insensitive)
        if subject_code.upper() != subject['subject_code'].upper():
            existing = fetch_one(
                'SELECT id FROM subjects WHERE UPPER(subject_code) = UPPER(%s) AND id != %s',
                (subject_code, subject_id)
            )
            
            if existing:
                errors = {'subject_code': 'A subject with this Subject Code already exists'}
                return render_template(
                    'subjects/edit.html',
                    errors=errors,
                    subject=subject,
                    form_data={
                        'subject_code': subject_code,
                        'subject_name': subject_name,
                        'max_marks': max_marks,
                    }
                )
        
        # Update subject
        execute_query(
            'UPDATE subjects SET subject_code = %s, subject_name = %s, max_marks = %s, updated_at = NOW() WHERE id = %s',
            (subject_code, subject_name, int(max_marks), subject_id)
        )
        
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('subjects.list_subjects'))
    
    return render_template('subjects/edit.html', subject=subject)


@bp.route('/<int:subject_id>/delete', methods=['POST'])
@login_required
def delete_subject(subject_id):
    """Delete subject (with marks dependency check)."""
    # Check for existing marks
    marks_count = fetch_one(
        'SELECT COUNT(*) AS count FROM marks WHERE subject_id = %s',
        (subject_id,)
    )
    
    marks_count = marks_count['count'] if marks_count else 0
    
    if marks_count > 0:
        flash('Cannot delete subject. Marks records exist for this subject.', 'error')
        return redirect(url_for('subjects.list_subjects'))
    
    # Delete subject
    execute_query('DELETE FROM subjects WHERE id = %s', (subject_id,))
    
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('subjects.list_subjects'))
