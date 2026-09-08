"""Tests for Student Management CRUD routes (Phase 7)."""

import pytest

import routes.students as students
import routes.auth as auth


def test_list_students_renders(client, admin_hash, monkeypatch):
    """Test that list students page renders correctly."""
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
    
    # Setup students mocks
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [
        {'id': 1, 'roll_number': 'STD001', 'name': 'John Doe', 'email': 'john@example.com',
         'date_of_birth': '2000-01-15', 'gender': 'Male', 'contact_number': '1234567890'},
    ])

    response = client.get('/students/')
    assert response.status_code == 200
    assert b'Students' in response.data
    assert b'STD001' in response.data
    assert b'John Doe' in response.data


def test_list_students_with_search(client, admin_hash, monkeypatch):
    """Test that search parameter filters students."""
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

    monkeypatch.setattr(students, 'fetch_all', mock_fetch_all)

    response = client.get('/students/?search=john')
    assert response.status_code == 200
    assert b'Search' in response.data


def test_list_students_with_gender_filter(client, admin_hash, monkeypatch):
    """Test that gender filter works correctly."""
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
    
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])

    response = client.get('/students/?gender=Male')
    assert response.status_code == 200
    assert b'Filter by Gender' in response.data


def test_add_student_get_request(client, admin_hash, monkeypatch):
    """Test that add student page renders on GET."""
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
    
    response = client.get('/students/add')
    assert response.status_code == 200
    assert b'Add Student' in response.data


def test_add_student_valid_data(client, admin_hash, monkeypatch):
    """Test adding a student with valid data."""
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
    
    # Setup students mocks
    monkeypatch.setattr(students, 'fetch_one', lambda query, params=None: None)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/students/add', data={
        'roll_number': 'STD001',
        'name': 'John Doe',
        'email': 'john@example.com',
        'date_of_birth': '2000-01-15',
        'gender': 'Male',
        'contact_number': '1234567890',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student added successfully' in response.data


def test_add_student_duplicate_roll_number(client, admin_hash, monkeypatch):
    """Test adding a student with duplicate roll number."""
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
    
    # Setup students mocks
    monkeypatch.setattr(students, 'fetch_one', lambda query, params=None: {
        'id': 1,
    } if 'students WHERE roll_number' in query else None)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])

    response = client.post('/students/add', data={
        'roll_number': 'STD001',
        'name': 'John Doe',
        'email': 'john@example.com',
        'date_of_birth': '2000-01-15',
        'gender': 'Male',
        'contact_number': '1234567890',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'A student with this roll number already exists' in response.data


def test_add_student_invalid_data(client, admin_hash, monkeypatch):
    """Test adding a student with invalid data."""
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
    
    response = client.post('/students/add', data={
        'roll_number': 'AB',  # Too short
        'name': 'John Doe',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Roll number must be 5-20 characters' in response.data


def test_edit_student_get_request(client, admin_hash, monkeypatch):
    """Test that edit student page renders on GET."""
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
    
    # Setup students mocks
    monkeypatch.setattr(students, 'fetch_one', lambda query, params=None: {
        'id': 1,
        'roll_number': 'STD001',
        'name': 'John Doe',
        'email': 'john@example.com',
        'date_of_birth': '2000-01-15',
        'gender': 'Male',
        'contact_number': '1234567890',
    })

    response = client.get('/students/1/edit')
    assert response.status_code == 200
    assert b'Edit Student' in response.data
    assert b'STD001' in response.data


def test_edit_student_not_found(client, admin_hash, monkeypatch):
    """Test editing a non-existent student."""
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
    
    # Setup students mocks
    def mock_fetch_one(query, params=None):
        return None
    monkeypatch.setattr(students, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)

    response = client.get('/students/999/edit', follow_redirects=True)

    assert response.status_code == 200
    assert b'Student not found' in response.data


def test_edit_student_valid_data(client, admin_hash, monkeypatch):
    """Test editing a student with valid data."""
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
    
    # Setup students mocks
    def mock_fetch_one(query, params=None):
        if 'students WHERE id' in query:
            return {
                'id': 1,
                'roll_number': 'STD001',
                'name': 'John Doe',
                'email': 'john@example.com',
                'date_of_birth': '2000-01-15',
                'gender': 'Male',
                'contact_number': '1234567890',
            }
        return None

    monkeypatch.setattr(students, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/students/1/edit', data={
        'roll_number': 'STD001',
        'name': 'John Updated',
        'email': 'john.updated@example.com',
        'date_of_birth': '2000-01-15',
        'gender': 'Male',
        'contact_number': '1234567890',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Student updated successfully' in response.data


def test_delete_student(client, admin_hash, monkeypatch):
    """Test deleting a student without marks."""
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
    
    # Setup students mocks
    def mock_fetch_one(query, params=None):
        if 'COUNT(*)' in query:
            return {'count': 0}
        return None

    monkeypatch.setattr(students, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)

    response = client.post('/students/1/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Student deleted successfully' in response.data


def test_delete_student_with_marks(client, admin_hash, monkeypatch):
    """Test deleting a student with marks (creates confirmation)."""
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
    
    # Setup students mocks
    def mock_fetch_one(query, params=None):
        if 'COUNT(*)' in query:
            return {'count': 3}
        return None

    monkeypatch.setattr(students, 'fetch_one', mock_fetch_one)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])
    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)

    with client as c:
        response = c.post('/students/1/delete', follow_redirects=True)

        assert response.status_code == 200
        assert b'Student deleted successfully' in response.data
        with c.session_transaction() as session:
            assert session.get('pending_student_delete') == 1


def test_confirm_delete(client, admin_hash, monkeypatch):
    """Test confirm delete route."""
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

    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])

    with client.session_transaction() as session:
        session['pending_student_delete'] = 1

    response = client.post('/students/confirm-delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Student deleted successfully' in response.data


def test_confirm_delete_no_pending(client, admin_hash, monkeypatch):
    """Test confirm delete with no pending deletion."""
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

    monkeypatch.setattr(students, 'execute_query', lambda *args, **kwargs: None)
    monkeypatch.setattr(students, 'fetch_all', lambda query, params=None: [])

    response = client.post('/students/confirm-delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid delete request' in response.data


def test_students_routes_blueprint_registered(app):
    """Test that students blueprint is properly registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/students/' in rules
    assert '/students/add' in rules
    assert '/students/<int:student_id>/edit' in rules
    assert '/students/<int:student_id>/delete' in rules
    assert '/students/confirm-delete' in rules


def test_students_routes_login_required(client):
    """Test that students routes require login."""
    response = client.get('/students/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

    response = client.get('/students/add')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']