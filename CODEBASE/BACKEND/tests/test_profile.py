"""Tests for Admin Profile and Account Settings feature.

Tests profile viewing, updating admin information, and password changes
with security verification.
"""

import bcrypt
import pytest


class TestProfileAccess:
    """Test profile page access and authentication."""
    
    def test_profile_requires_authentication(self, client):
        """Unauthenticated users cannot access profile page."""
        response = client.get('/profile/')
        assert response.status_code == 302
        assert '/login' in response.location
    
    def test_authenticated_admin_can_access_profile(self, client, auth, monkeypatch):
        """Authenticated admin can access profile page."""
        # Mock profile fetch
        import routes.profile as profile_module
        monkeypatch.setattr(profile_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'full_name': 'System Administrator',
        })
        
        response = client.get('/profile/')
        assert response.status_code == 200
        assert b'Admin Profile' in response.data
        assert b'Profile Information' in response.data
        assert b'Change Password' in response.data


class TestProfileDisplay:
    """Test profile page displays correct information."""
    
    def test_profile_shows_current_admin_info(self, client, auth, monkeypatch):
        """Profile page displays current admin information."""
        # Mock profile fetch
        import routes.profile as profile_module
        monkeypatch.setattr(profile_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'full_name': 'System Administrator',
        })
        
        response = client.get('/profile/')
        assert response.status_code == 200
        assert b'admin' in response.data  # username
        assert b'admin@resultportal.com' in response.data  # email
        assert b'System Administrator' in response.data  # full_name


class TestProfileUpdate:
    """Test updating profile information."""
    
    def test_update_admin_name(self, client, auth, monkeypatch):
        """Admin can update their name."""
        import routes.profile as profile_module
        
        # Track updates
        updates = []
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            # No duplicates
            return None
        
        def mock_execute(query, params=None):
            updates.append((query, params))
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        monkeypatch.setattr(profile_module, 'execute_query', mock_execute)
        
        response = client.post('/profile/', data={
            'action': 'update_profile',
            'full_name': 'Updated Admin Name',
            'username': 'admin',
            'email': 'admin@resultportal.com'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Profile updated successfully' in response.data
        assert len(updates) == 1
        assert 'UPDATE admins SET full_name' in updates[0][0]
    
    def test_duplicate_username_rejected(self, client, auth, monkeypatch):
        """Cannot update to a username that already exists."""
        import routes.profile as profile_module
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            # Simulate existing username
            if 'WHERE username' in query:
                return {'id': 2}
            return None
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        
        response = client.post('/profile/', data={
            'action': 'update_profile',
            'full_name': 'System Administrator',
            'username': 'existing_admin',
            'email': 'admin@resultportal.com'
        })
        
        assert response.status_code == 200
        assert b'Username is already in use' in response.data
    
    def test_empty_fields_rejected(self, client, auth, monkeypatch):
        """Empty required fields are rejected."""
        import routes.profile as profile_module
        monkeypatch.setattr(profile_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'full_name': 'System Administrator',
        })
        
        response = client.post('/profile/', data={
            'action': 'update_profile',
            'full_name': '',
            'username': '',
            'email': ''
        })
        
        assert response.status_code == 200
        assert b'required' in response.data.lower()
    
    def test_session_updated_after_username_change(self, client, auth, monkeypatch):
        """Session is updated with new username after profile update."""
        import routes.profile as profile_module
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            return None
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        monkeypatch.setattr(profile_module, 'execute_query', lambda *args: None)
        
        with client.session_transaction() as sess:
            assert sess['username'] == 'admin'
        
        client.post('/profile/', data={
            'action': 'update_profile',
            'full_name': 'System Administrator',
            'username': 'updated_admin',
            'email': 'admin@resultportal.com'
        }, follow_redirects=True)
        
        with client.session_transaction() as sess:
            assert sess['username'] == 'updated_admin'


class TestPasswordChange:
    """Test password change functionality."""
    
    def test_change_password_with_correct_current_password(self, client, auth, admin_hash, monkeypatch):
        """Admin can change password with correct current password."""
        import routes.profile as profile_module
        
        updates = []
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            if 'password_hash' in query:
                return {'password_hash': admin_hash}
            return None
        
        def mock_execute(query, params=None):
            updates.append((query, params))
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        monkeypatch.setattr(profile_module, 'execute_query', mock_execute)
        
        response = client.post('/profile/', data={
            'action': 'change_password',
            'current_password': 'admin123',
            'new_password': 'new_password_123',
            'confirm_password': 'new_password_123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Password updated successfully' in response.data
        assert len(updates) == 1
        assert 'UPDATE admins SET password_hash' in updates[0][0]
    
    def test_incorrect_current_password_rejected(self, client, auth, admin_hash, monkeypatch):
        """Password change fails with incorrect current password."""
        import routes.profile as profile_module
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            if 'password_hash' in query:
                return {'password_hash': admin_hash}
            return None
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        
        response = client.post('/profile/', data={
            'action': 'change_password',
            'current_password': 'wrong_password',
            'new_password': 'new_password_123',
            'confirm_password': 'new_password_123'
        })
        
        assert response.status_code == 200
        assert b'Current password is incorrect' in response.data
    
    def test_password_mismatch_rejected(self, client, auth, monkeypatch):
        """Password change fails when new passwords don't match."""
        import routes.profile as profile_module
        monkeypatch.setattr(profile_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'full_name': 'System Administrator',
        })
        
        response = client.post('/profile/', data={
            'action': 'change_password',
            'current_password': 'admin123',
            'new_password': 'new_password_123',
            'confirm_password': 'different_password'
        })
        
        assert response.status_code == 200
        assert b'do not match' in response.data
    
    def test_password_stored_as_hash(self, client, auth, admin_hash, monkeypatch):
        """New password is stored as bcrypt hash, never plaintext."""
        import routes.profile as profile_module
        
        stored_hash = []
        
        def mock_fetch_one(query, params=None):
            if 'SELECT id, username' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'full_name': 'System Administrator',
                }
            if 'password_hash' in query:
                return {'password_hash': admin_hash}
            return None
        
        def mock_execute(query, params=None):
            if params and 'UPDATE admins SET password_hash' in query:
                stored_hash.append(params[0])
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        monkeypatch.setattr(profile_module, 'execute_query', mock_execute)
        
        client.post('/profile/', data={
            'action': 'change_password',
            'current_password': 'admin123',
            'new_password': 'secure_password_456',
            'confirm_password': 'secure_password_456'
        }, follow_redirects=True)
        
        assert len(stored_hash) == 1
        password_hash = stored_hash[0]
        
        # Hash should start with bcrypt identifier
        assert password_hash.startswith('$2b$')
        # Hash should not be the plaintext password
        assert password_hash != 'secure_password_456'
        # Hash should verify correctly
        assert bcrypt.checkpw('secure_password_456'.encode('utf-8'), password_hash.encode('utf-8'))
    
    def test_short_password_rejected(self, client, auth, monkeypatch):
        """Password shorter than 6 characters is rejected."""
        import routes.profile as profile_module
        monkeypatch.setattr(profile_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'full_name': 'System Administrator',
        })
        
        response = client.post('/profile/', data={
            'action': 'change_password',
            'current_password': 'admin123',
            'new_password': '12345',  # Too short
            'confirm_password': '12345'
        })
        
        assert response.status_code == 200
        assert b'at least 6 characters' in response.data


class TestProfileSecurity:
    """Test security aspects of profile feature."""
    
    def test_profile_uses_session_admin_id(self, client, auth, monkeypatch):
        """Profile uses admin_id from session, not form data."""
        import routes.profile as profile_module
        
        fetched_ids = []
        
        def mock_fetch_one(query, params=None):
            if params:
                fetched_ids.append(params[0])
            return {
                'id': 1,
                'username': 'admin',
                'email': 'admin@resultportal.com',
                'full_name': 'System Administrator',
            }
        
        monkeypatch.setattr(profile_module, 'fetch_one', mock_fetch_one)
        monkeypatch.setattr(profile_module, 'execute_query', lambda *args: None)
        
        # Try to inject different admin_id
        client.post('/profile/', data={
            'action': 'update_profile',
            'admin_id': '999',  # Malicious attempt
            'full_name': 'Hacker Name',
            'username': 'admin',
            'email': 'admin@resultportal.com'
        }, follow_redirects=True)
        
        # Should use session admin_id (1), not injected value (999)
        assert 1 in fetched_ids
        assert 999 not in fetched_ids
    
    def test_logout_still_works(self, client, auth):
        """Logout functionality remains working after profile feature."""
        response = client.post('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data
        
        # Verify cannot access profile after logout
        response = client.get('/profile/')
        assert response.status_code == 302
        assert '/login' in response.location
