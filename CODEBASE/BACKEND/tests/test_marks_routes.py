"""Tests for Marks Management CRUD routes (Phase 9)."""

import pytest

import routes.marks as marks
import routes.auth as auth


def test_list_marks_renders(client, admin_hash, monkeypatch):
    """Test that list marks page renders correctly."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    monkeypatch.setattr(marks, 'fetch_all', lambda query, params=None: [
        {
            'id': 1,
            'roll_number': '2024001',
            'student_name': 'Aarav Sharma',
            'subject_code': 'MATH101',
            'subject_name': 'Mathematics',
            'max_marks': 100,
            'marks_obtained': 85,
            'is_absent': False,
        },
    ])

    response = client.get('/marks/')
    assert response.status_code == 200
    assert b'Marks' in response.data
    assert b'2024001' in response.data
    assert b'Aarav Sharma' in response.data
    assert b'MATH101' in response.data
    assert b'85' in response.data


def test_add_marks_get_request(client, admin_hash, monkeypatch):
    """Test that add marks page renders on GET."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup students and subjects mocks
    monkeypatch.setattr(marks, 'fetch_all', lambda query, params=None: [])

    response = client.get('/marks/add')
    assert response.status_code == 200
    assert b'Add Marks' in response.data


def test_add_marks_valid_data(client, admin_hash, monkeypatch):
    """Test adding marks with valid data."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    def mock_fetch_one(query, params=None):
        if 'subjects' in query:
            return {'id': 1, 'subject_code': 'MATH101', 'subject_name': 'Mathematics', 'max_marks': 100}
        return None

    monkeypatch.setattr(marks, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(marks, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(marks, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/marks/add', data={
        'student_id': '1',
        'subject_id': '1',
        'marks_obtained': '85',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks added successfully' in response.data


def test_add_marks_duplicate_entry(client, admin_hash, monkeypatch):
    """Test adding marks with duplicate student-subject combination."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    def mock_fetch_one(query, params=None):
        if 'subjects' in query:
            return {'id': 1, 'subject_code': 'MATH101', 'subject_name': 'Mathematics', 'max_marks': 100}
        if 'marks WHERE student_id' in query:
            return {'id': 1}
        return None

    monkeypatch.setattr(marks, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(marks, 'fetch_all', lambda query, params=None: [])

    response = client.post('/marks/add', data={
        'student_id': '1',
        'subject_id': '1',
        'marks_obtained': '85',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks already exist for this student-subject combination' in response.data


def test_add_marks_exceeds_max_marks(client, admin_hash, monkeypatch):
    """Test adding marks exceeding subject max marks."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    def mock_fetch_one(query, params=None):
        if 'subjects' in query:
            return {'id': 1, 'subject_code': 'MATH101', 'subject_name': 'Mathematics', 'max_marks': 100}
        return None

    monkeypatch.setattr(marks, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(marks, 'fetch_all', lambda query, params=None: [])

    response = client.post('/marks/add', data={
        'student_id': '1',
        'subject_id': '1',
        'marks_obtained': '150',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks cannot exceed 100' in response.data


def test_edit_marks_get_request(client, admin_hash, monkeypatch):
    """Test that edit marks page renders on GET."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    monkeypatch.setattr(marks, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'student_id': 1,
        'subject_id': 1,
        'marks_obtained': 85,
        'is_absent': False,
        'roll_number': '2024001',
        'student_name': 'Aarav Sharma',
        'subject_code': 'MATH101',
        'subject_name': 'Mathematics',
        'max_marks': 100,
    })

    response = client.get('/marks/1/edit')
    assert response.status_code == 200
    assert b'Edit Marks' in response.data
    assert b'2024001' in response.data


def test_edit_marks_not_found(client, admin_hash, monkeypatch):
    """Test editing a non-existent marks record."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    monkeypatch.setattr(marks, 'fetch_one', lambda query, params=None: None)

    response = client.get('/marks/999/edit', follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks record not found' in response.data


def test_delete_marks(client, admin_hash, monkeypatch):
    """Test deleting a marks record."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    # Setup marks mocks
    def mock_fetch_one(query, params=None):
        if 'SELECT id FROM marks WHERE id' in query:
            return {'id': 1}
        return None

    monkeypatch.setattr(marks, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(marks, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/marks/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks record deleted successfully' in response.data


def test_delete_marks_not_found(client, admin_hash, monkeypatch):
    """Test deleting a non-existent marks record."""
    # Setup auth mocks
    monkeypatch.setattr(auth, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'username': 'admin',
        'email': 'admin@resultportal.com',
        'password_hash': admin_hash,
        'full_name': 'System Administrator',
    })
    monkeypatch.setattr(auth, 'execute_query', lambda *args, **kwargs: None)
    
    # Login
    login_response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login_response.status_code == 302
    
    # Verify session was set
    with client.session_transaction() as session:
        assert session.get('admin_id') == 1
    
    monkeypatch.setattr(marks, 'fetch_one', lambda query, params=None: None)

    response = client.post('/marks/999/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Marks record not found' in response.data


def test_marks_routes_blueprint_registered(app):
    """Test that marks blueprint is properly registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/marks/' in rules
    assert '/marks/add' in rules
    assert '/marks/<int:marks_id>/edit' in rules
    assert '/marks/<int:marks_id>/delete' in rules


def test_marks_routes_login_required(client):
    """Test that marks routes require login."""
    response = client.get('/marks/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

    response = client.get('/marks/add')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_marks_routes_blueprint_url_prefix(app):
    """Test that marks blueprint has correct URL prefix."""
    from routes.marks import bp
    assert bp.url_prefix == '/marks'