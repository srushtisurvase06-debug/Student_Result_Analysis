"""Admin Profile and Account Settings routes.

Allows authenticated admin to:
- View profile information
- Update admin name, username, email
- Change password with current password verification
"""

import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from utils.db import execute_query, fetch_one
from utils.decorators import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Display and update admin profile."""
    admin_id = session.get('admin_id')
    
    # Fetch current admin data
    admin = fetch_one(
        'SELECT id, username, email, full_name FROM admins WHERE id = %s',
        (admin_id,)
    )
    
    if not admin:
        flash('Admin account not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        action = request.form.get('action', '').strip()
        
        if action == 'update_profile':
            return _update_profile(admin)
        elif action == 'change_password':
            return _change_password(admin)
    
    return render_template('profile/index.html', admin=admin)


def _update_profile(admin):
    """Handle profile information update."""
    admin_id = admin['id']
    
    # Get form data
    full_name = (request.form.get('full_name') or '').strip()
    username = (request.form.get('username') or '').strip()
    email = (request.form.get('email') or '').strip()
    
    # Validation
    errors = {}
    
    if not full_name:
        errors['full_name'] = 'Admin name is required'
    
    if not username:
        errors['username'] = 'Username is required'
    elif len(username) < 3:
        errors['username'] = 'Username must be at least 3 characters'
    elif len(username) > 50:
        errors['username'] = 'Username must be at most 50 characters'
    
    if not email:
        errors['email'] = 'Email is required'
    elif '@' not in email or '.' not in email.split('@')[-1]:
        errors['email'] = 'Invalid email format'
    
    if errors:
        return render_template('profile/index.html', admin=admin, errors=errors, form_data={
            'full_name': full_name,
            'username': username,
            'email': email
        })
    
    # Check for duplicate username (excluding current admin)
    if username != admin['username']:
        existing_username = fetch_one(
            'SELECT id FROM admins WHERE username = %s AND id != %s',
            (username, admin_id)
        )
        if existing_username:
            errors['username'] = 'Username is already in use'
            return render_template('profile/index.html', admin=admin, errors=errors, form_data={
                'full_name': full_name,
                'username': username,
                'email': email
            })
    
    # Check for duplicate email (excluding current admin)
    if email != admin['email']:
        existing_email = fetch_one(
            'SELECT id FROM admins WHERE email = %s AND id != %s',
            (email, admin_id)
        )
        if existing_email:
            errors['email'] = 'Email is already in use'
            return render_template('profile/index.html', admin=admin, errors=errors, form_data={
                'full_name': full_name,
                'username': username,
                'email': email
            })
    
    # Update admin profile
    execute_query(
        'UPDATE admins SET full_name = %s, username = %s, email = %s WHERE id = %s',
        (full_name, username, email, admin_id)
    )
    
    # Update session with new username and email
    session['username'] = username
    session['email'] = email
    
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('profile.index'))


def _change_password(admin):
    """Handle password change with current password verification."""
    admin_id = admin['id']
    
    # Get form data
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validation
    password_errors = {}
    
    if not current_password:
        password_errors['current_password'] = 'Current password is required'
    
    if not new_password:
        password_errors['new_password'] = 'New password is required'
    elif len(new_password) < 6:
        password_errors['new_password'] = 'New password must be at least 6 characters'
    
    if not confirm_password:
        password_errors['confirm_password'] = 'Password confirmation is required'
    elif new_password != confirm_password:
        password_errors['confirm_password'] = 'New passwords do not match'
    
    if password_errors:
        return render_template('profile/index.html', admin=admin, password_errors=password_errors)
    
    # Verify current password
    admin_with_password = fetch_one(
        'SELECT password_hash FROM admins WHERE id = %s',
        (admin_id,)
    )
    
    if not admin_with_password:
        flash('Admin account not found.', 'error')
        return redirect(url_for('auth.logout'))
    
    # Check current password
    if not bcrypt.checkpw(current_password.encode('utf-8'), admin_with_password['password_hash'].encode('utf-8')):
        password_errors['current_password'] = 'Current password is incorrect'
        return render_template('profile/index.html', admin=admin, password_errors=password_errors)
    
    # Hash new password
    new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Update password
    execute_query(
        'UPDATE admins SET password_hash = %s WHERE id = %s',
        (new_password_hash, admin_id)
    )
    
    flash('Password updated successfully.', 'success')
    return redirect(url_for('profile.index'))
