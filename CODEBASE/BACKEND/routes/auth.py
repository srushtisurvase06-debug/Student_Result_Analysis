from functools import wraps

import bcrypt
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from utils.db import execute_query, fetch_one

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template('auth/login.html')

        admin = fetch_one(
            'SELECT id, username, email, password_hash, full_name FROM admins WHERE username = %s OR email = %s',
            (username, username),
        )

        if not admin:
            flash('Invalid credentials', 'error')
            return render_template('auth/login.html')

        if not bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'].encode('utf-8')):
            flash('Invalid credentials', 'error')
            return render_template('auth/login.html')

        session.clear()
        session['admin_id'] = admin['id']
        session['username'] = admin['username']
        session['email'] = admin['email']
        session.permanent = True

        execute_query(
            'UPDATE admins SET last_login = NOW() WHERE id = %s',
            (admin['id'],),
        )

        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')


@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view
