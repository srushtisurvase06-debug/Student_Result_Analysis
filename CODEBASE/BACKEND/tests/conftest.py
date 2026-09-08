"""Shared fixtures for the Phase 3 test suite.

The suite runs entirely offline. Nothing here opens a network connection or
touches the real database; tests that need database behaviour substitute a fake
driver (see test_db.py). Live-database checks are marked `integration` and skip
themselves when DATABASE_URL is unset.
"""

import sys
from pathlib import Path

import bcrypt
import pytest

# The backend directory must be importable as the package root, because that is
# how the application is imported in production (`gunicorn app:app`).
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import create_app  # noqa: E402  (import requires the sys.path setup above)


@pytest.fixture
def app():
    """A Flask application built from the testing configuration."""
    return create_app('testing')


@pytest.fixture
def client(app):
    """A test client for the testing-configuration app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A CLI runner for the testing-configuration app."""
    return app.test_cli_runner()


@pytest.fixture
def admin_hash():
    """Hashed password for admin user."""
    return bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=12)).decode('utf-8')


@pytest.fixture
def auth(client, admin_hash, monkeypatch):
    """Helper to perform admin login."""
    import routes.auth as auth
    
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)

    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    
    # Return the client so tests can use it
    return client
