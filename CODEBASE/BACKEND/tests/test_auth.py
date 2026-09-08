import bcrypt

import pytest

import routes.auth as auth


@pytest.fixture
def admin_hash():
    return bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=12)).decode('utf-8')


def test_login_page_renders(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Admin Login' in response.data


def test_login_sets_session_and_redirects(client, monkeypatch, admin_hash):
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)

    assert response.status_code == 302
    # Dashboard is registered as blueprint with url_prefix='/dashboard'
    # so the redirect is to '/dashboard/'
    assert response.headers['Location'] == '/dashboard/'
    with client.session_transaction() as session:
        assert session['admin_id'] == 1
        assert session['username'] == 'admin'


def test_login_rejects_invalid_credentials(client, monkeypatch, admin_hash):
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })

    response = client.post('/login', data={'username': 'admin', 'password': 'wrongpass'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid credentials' in response.data
    with client.session_transaction() as session:
        assert 'admin_id' not in session


def test_logout_clears_session(client, monkeypatch, admin_hash):
    with client.session_transaction() as session:
        session['admin_id'] = 1
        session['username'] = 'admin'

    response = client.post('/logout', follow_redirects=False)

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')
    with client.session_transaction() as session:
        assert 'admin_id' not in session


def test_dashboard_requires_login(client):
    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
