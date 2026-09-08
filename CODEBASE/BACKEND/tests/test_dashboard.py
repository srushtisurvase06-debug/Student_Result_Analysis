"""Tests for dashboard routes.

Phase 6: Admin dashboard statistics and charts.
"""

import pytest
from unittest.mock import patch


# Mock data for testing without database
MOCK_STATS = {
    'total_students': 50,
    'total_subjects': 5,
    'students_with_results': 45,
    'pass_percentage': 85.5,
    'fail_percentage': 14.5,
    'class_average': 72.3,
    'grade_distribution': {'A': 10, 'B': 12, 'C': 15, 'D': 8, 'F': 5},
    'pass_fail_count': {'pass': 45, 'fail': 5},
    'top_students': [
        {'name': 'Alice', 'roll_number': 'S001', 'percentage': 95.5},
        {'name': 'Bob', 'roll_number': 'S002', 'percentage': 92.0},
        {'name': 'Charlie', 'roll_number': 'S003', 'percentage': 89.5},
        {'name': 'Diana', 'roll_number': 'S004', 'percentage': 87.0},
        {'name': 'Eve', 'roll_number': 'S005', 'percentage': 85.5},
    ],
}


class TestDashboardRoute:
    """Test dashboard route protection and access."""

    def test_dashboard_requires_login(self, client):
        """Unauthenticated users are redirected to login."""
        response = client.get('/dashboard/')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']


class TestDashboardStats:
    """Test dashboard statistics display."""

    def test_dashboard_shows_total_students(self, client, admin_hash, monkeypatch):
        """Dashboard displays total student count."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        # Mock the entire calculate_dashboard_stats function
        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Total Students' in response.data
            assert b'<p class="stat-card__value stat-card__value--primary">50</p>' in response.data

    def test_dashboard_shows_total_subjects(self, client, admin_hash, monkeypatch):
        """Dashboard displays total subject count."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Total Subjects' in response.data
            assert b'<p class="stat-card__value stat-card__value--primary">5</p>' in response.data

    def test_dashboard_shows_results_count(self, client, admin_hash, monkeypatch):
        """Dashboard displays results generated count."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Results Generated' in response.data
            assert b'<p class="stat-card__value stat-card__value--info">45</p>' in response.data

    def test_dashboard_shows_pass_percentage(self, client, admin_hash, monkeypatch):
        """Dashboard displays pass percentage."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Pass %' in response.data
            assert b'<p class="stat-card__value stat-card__value--success">85.5%</p>' in response.data

    def test_dashboard_shows_fail_percentage(self, client, admin_hash, monkeypatch):
        """Dashboard displays fail percentage."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Fail %' in response.data
            assert b'<p class="stat-card__value stat-card__value--danger">14.5%</p>' in response.data

    def test_dashboard_shows_class_average(self, client, admin_hash, monkeypatch):
        """Dashboard displays class average percentage."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Class Average' in response.data
            assert b'<p class="stat-card__value stat-card__value--warning">72.3%</p>' in response.data


class TestDashboardCharts:
    """Test dashboard chart rendering."""

    def test_dashboard_has_grade_distribution_chart(self, client, admin_hash, monkeypatch):
        """Dashboard has grade distribution bar chart."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Grade Distribution' in response.data
            assert b'gradeChart' in response.data

    def test_dashboard_has_pass_fail_chart(self, client, admin_hash, monkeypatch):
        """Dashboard has pass/fail pie chart."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Pass vs Fail Ratio' in response.data
            assert b'passFailChart' in response.data

    def test_dashboard_loads_chart_js_from_cdn(self, client, admin_hash, monkeypatch):
        """Dashboard loads Chart.js from CDN."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'cdn.jsdelivr.net/npm/chart.js' in response.data


class TestDashboardTopStudents:
    """Test top students table display."""

    def test_dashboard_shows_top_students_section(self, client, admin_hash, monkeypatch):
        """Dashboard has top 5 students section."""
        import routes.auth as auth_module
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=MOCK_STATS):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'Top 5 Students' in response.data
            assert b'Alice' in response.data

    def test_dashboard_shows_no_students_when_empty(self, client, admin_hash, monkeypatch):
        """Dashboard shows empty state with no students."""
        import routes.auth as auth_module
        
        empty_stats = MOCK_STATS.copy()
        empty_stats['top_students'] = []
        
        monkeypatch.setattr(auth_module, 'fetch_one', lambda query, params=None: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@resultportal.com',
            'password_hash': admin_hash,
            'full_name': 'System Administrator',
        })
        monkeypatch.setattr(auth_module, 'execute_query', lambda *args, **kwargs: None)

        with patch('routes.dashboard.calculate_dashboard_stats', return_value=empty_stats):
            client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
            response = client.get('/dashboard/')
            assert response.status_code == 200
            assert b'No student data available' in response.data or b'Rank' in response.data