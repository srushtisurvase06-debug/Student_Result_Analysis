from functools import wraps
from flask import session, redirect, url_for, flash, current_app


def login_required(f):
    """Decorator to protect routes requiring authentication.
    
    Checks if admin is logged in (admin_id in session). If not, redirects to login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            current_app.logger.warning(f'Unauthorized access attempt to {f.__name__}')
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
