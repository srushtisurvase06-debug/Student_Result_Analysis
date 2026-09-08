"""Tests for Subject Management CRUD routes (Phase 8)."""

import pytest

import routes.subjects as subjects
import routes.auth as auth


def test_list_subjects_renders(client, admin_hash, monkeypatch):
    """Test that list subjects page renders correctly."""
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
    
    # Setup subjects mocks
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [
        {'id': 1, 'subject_code': 'MATH101', 'subject_name': 'Mathematics', 'max_marks': 100},
    ])

    response = client.get('/subjects/')
    assert response.status_code == 200
    assert b'Subjects' in response.data
    assert b'MATH101' in response.data
    assert b'Mathematics' in response.data


def test_list_subjects_with_search(client, admin_hash, monkeypatch):
    """Test that search parameter filters subjects."""
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
    
    search_results = []

    def mock_fetch_all(query, params=None):
        return search_results

    monkeypatch.setattr(subjects, 'fetch_all', mock_fetch_all)

    response = client.get('/subjects/?search=math')
    assert response.status_code == 200
    assert b'Search' in response.data


def test_add_subject_get_request(client, admin_hash, monkeypatch):
    """Test that add subject page renders on GET."""
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
    
    response = client.get('/subjects/add')
    assert response.status_code == 200
    assert b'Add Subject' in response.data


def test_add_subject_valid_data(client, admin_hash, monkeypatch):
    """Test adding a subject with valid data."""
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
    
    # Setup subjects mocks
    monkeypatch.setattr(subjects, 'fetch_one', lambda query, params=None: None)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(subjects, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/subjects/add', data={
        'subject_code': 'MATH101',
        'subject_name': 'Mathematics',
        'max_marks': '100',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Subject added successfully' in response.data


def test_add_subject_duplicate_code(client, admin_hash, monkeypatch):
    """Test adding a subject with duplicate code."""
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
    
    # Setup subjects mocks
    monkeypatch.setattr(subjects, 'fetch_one', lambda query, params=None: {
        'id': 1,
    } if 'subjects WHERE' in query else None)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])

    response = client.post('/subjects/add', data={
        'subject_code': 'MATH101',
        'subject_name': 'Mathematics',
        'max_marks': '100',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'A subject with this Subject Code already exists' in response.data


def test_add_subject_invalid_data(client, admin_hash, monkeypatch):
    """Test adding a subject with invalid data."""
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
    
    response = client.post('/subjects/add', data={
        'subject_code': 'MA',  # Too short
        'subject_name': 'Mathematics',
        'max_marks': '100',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Subject code must be 3-10 characters' in response.data


def test_add_subject_invalid_max_marks(client, admin_hash, monkeypatch):
    """Test adding a subject with invalid max marks."""
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
    
    # Test negative marks
    response = client.post('/subjects/add', data={
        'subject_code': 'MATH101',
        'subject_name': 'Mathematics',
        'max_marks': '0',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Maximum marks must be at least 1' in response.data


def test_edit_subject_get_request(client, admin_hash, monkeypatch):
    """Test that edit subject page renders on GET."""
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
    
    # Setup subjects mocks
    monkeypatch.setattr(subjects, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'subject_code': 'MATH101',
        'subject_name': 'Mathematics',
        'max_marks': 100,
    })

    response = client.get('/subjects/1/edit')
    assert response.status_code == 200
    assert b'Edit Subject' in response.data
    assert b'MATH101' in response.data


def test_edit_subject_not_found(client, admin_hash, monkeypatch):
    """Test editing a non-existent subject."""
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
    
    # Setup subjects mocks
    def mock_fetch_one(query, params=None):
        return None
    monkeypatch.setattr(subjects, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(subjects, 'execute_query', lambda *args, **kwargs: None)

    response = client.get('/subjects/999/edit', follow_redirects=True)

    assert response.status_code == 200
    assert b'Subject not found' in response.data


def test_edit_subject_valid_data(client, admin_hash, monkeypatch):
    """Test editing a subject with valid data."""
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
    
    # Setup subjects mocks
    def mock_fetch_one(query, params=None):
        if 'subjects WHERE id' in query:
            return {
                'id': 1,
                'subject_code': 'MATH101',
                'subject_name': 'Mathematics',
                'max_marks': 100,
            }
        return None

    monkeypatch.setattr(subjects, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(subjects, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/subjects/1/edit', data={
        'subject_code': 'MATH101',
        'subject_name': 'Advanced Mathematics',
        'max_marks': '150',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Subject updated successfully' in response.data


def test_delete_subject(client, admin_hash, monkeypatch):
    """Test deleting a subject without marks."""
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
    
    # Setup subjects mocks
    def mock_fetch_one(query, params=None):
        if 'COUNT(*)' in query:
            return {'count': 0}
        return None

    monkeypatch.setattr(subjects, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(subjects, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/subjects/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Subject deleted successfully' in response.data


def test_delete_subject_with_marks(client, admin_hash, monkeypatch):
    """Test deleting a subject with marks (should be prevented)."""
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
    
    # Setup subjects mocks
    def mock_fetch_one(query, params=None):
        if 'COUNT(*)' in query:
            return {'count': 5}
        return None

    monkeypatch.setattr(subjects, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(subjects, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(subjects, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/subjects/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Cannot delete subject. Marks records exist for this subject' in response.data


def test_subjects_routes_blueprint_registered(app):
    """Test that subjects blueprint is properly registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/subjects/' in rules
    assert '/subjects/add' in rules
    assert '/subjects/<int:subject_id>/edit' in rules
    assert '/subjects/<int:subject_id>/delete' in rules


def test_subjects_routes_login_required(client):
    """Test that subjects routes require login."""
    response = client.get('/subjects/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

    response = client.get('/subjects/add')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']


def test_subjects_routes_blueprint_url_prefix(app):
    """Test that subjects blueprint has correct URL prefix."""
    from routes.subjects import bp
    assert bp.url_prefix == '/subjects'
