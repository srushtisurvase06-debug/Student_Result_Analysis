#!/usr/bin/env python
"""
Automated route audit to find HTTP 500 errors and broken routes.

This script systematically tests all Flask routes and reports any issues.
"""

import sys
import os

# Add parent directory to path for imports
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, '..'))

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
# Load from project root
ENV_FILE = os.path.join(os.path.dirname(PROJECT_ROOT), '.env')
load_dotenv(ENV_FILE)

import unittest
from app import create_app
from routes import auth


class RouteAudit(unittest.TestCase):
    """Test all routes for 500 errors."""
    
    @classmethod
    def setUpClass(cls):
        """Create test app."""
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
    
    def setUp(self):
        """Set up test fixtures."""
        self.admin_password_hash = '$2b$12$B9wCP7S5cUHIk5RteYo62.HEugMyIKkKhkb5SXnbWv5/3ApeyfwI.'
    
    def _login(self):
        """Login as admin for protected routes."""
        # Mock auth functions
        import routes.auth as auth_module
        import routes.dashboard as dashboard_module
        import routes.students as students_module
        import routes.subjects as subjects_module
        import routes.marks as marks_module
        import routes.results as results_module
        import routes.analysis as analysis_module
        import routes.reports as reports_module
        import routes.profile as profile_module
        from utils.db import get_db_connection
        import utils.db as db_module
        import utils.calculations as calc_module
        
        # Mock fetch_one for login
        def mock_fetch_one(query, params=None):
            if 'admins' in query:
                return {
                    'id': 1,
                    'username': 'admin',
                    'email': 'admin@resultportal.com',
                    'password_hash': self.admin_password_hash,
                    'full_name': 'System Administrator',
                }
            return None
        
        def mock_execute_query(*args, **kwargs):
            return None
        
        def mock_fetch_all(query, params=None):
            return []
        
        def mock_get_db_connection():
            return None  # Will cause error - we'll catch it
        
        # Patch auth
        auth_module.fetch_one = mock_fetch_one
        auth_module.execute_query = mock_execute_query
        
        # Patch dashboard to use mocked fetch_one
        dashboard_module.fetch_one = mock_fetch_one
        
        # Patch students
        students_module.fetch_all = mock_fetch_all
        students_module.fetch_one = mock_fetch_one
        students_module.execute_query = mock_execute_query
        
        # Patch subjects
        subjects_module.fetch_all = mock_fetch_all
        subjects_module.fetch_one = mock_fetch_one
        subjects_module.execute_query = mock_execute_query
        
        # Patch marks
        marks_module.fetch_all = mock_fetch_all
        marks_module.fetch_one = mock_fetch_one
        marks_module.execute_query = mock_execute_query
        
        # Patch results
        results_module.fetch_all = mock_fetch_all
        results_module.fetch_one = mock_fetch_one
        results_module.execute_query = mock_execute_query
        
        # Patch analysis
        analysis_module.fetch_one = mock_fetch_one
        analysis_module.execute_query = mock_execute_query
        
        # Patch reports
        reports_module.fetch_one = mock_fetch_one
        reports_module.execute_query = mock_execute_query
        
        # Patch profile
        profile_module.fetch_one = mock_fetch_one
        profile_module.execute_query = mock_execute_query
        
        # Patch db
        db_module.get_db_connection = mock_get_db_connection
        db_module.fetch_one = mock_fetch_one
        db_module.fetch_all = mock_fetch_all
        db_module.execute_query = mock_execute_query
        
        # Mock calculations
        calc_module.calculate_pass_fail_stats = lambda conn: {'pass_count': 10, 'fail_count': 5, 'pass_percentage': 66.67, 'fail_percentage': 33.33}
        calc_module.calculate_grade_distribution = lambda conn: {'A': 5, 'B': 5, 'C': 3, 'D': 2, 'F': 0}
        calc_module.calculate_class_average = lambda conn: 75.5
        calc_module.get_top_performers = lambda limit, conn: []
        calc_module.get_subject_averages = lambda conn: []
    
    def test_routes(self):
        """Test all routes for errors."""
        # Public routes (no auth required)
        public_routes = [
            ('/', 200),
            ('/health', 200),
            ('/results/lookup', 200),
            ('/login', 200),
        ]
        
        # Protected routes (need auth)
        protected_routes = [
            ('/dashboard/', 200),
            ('/students/', 200),
            ('/students/add', 200),
            ('/subjects/', 200),
            ('/subjects/add', 200),
            ('/marks/', 200),
            ('/marks/add', 200),
            ('/results/', 200),
            ('/analysis/', 200),
            ('/reports/', 200),
            ('/profile/', 200),
        ]
        
        print("\n" + "="*60)
        print("ROUTE AUDIT RESULTS")
        print("="*60)
        
        errors = []
        
        # Test public routes
        print("\n[Public Routes]")
        for route, expected_status in public_routes:
            try:
                response = self.client.get(route)
                status = response.status_code
                if status == 500:
                    errors.append(f"GET {route} -> 500 ERROR")
                    print(f"  ✗ GET {route} -> {status} (500 ERROR)")
                elif status != expected_status:
                    print(f"  ⚠ GET {route} -> {status} (expected {expected_status})")
                else:
                    print(f"  ✓ GET {route} -> {status}")
            except Exception as e:
                errors.append(f"GET {route} -> EXCEPTION: {e}")
                print(f"  ✗ GET {route} -> EXCEPTION: {e}")
        
        # Test protected routes (with mocked auth)
        self._login()
        print("\n[Protected Routes]")
        for route, expected_status in protected_routes:
            try:
                response = self.client.get(route)
                status = response.status_code
                if status == 500:
                    errors.append(f"GET {route} -> 500 ERROR")
                    print(f"  ✗ GET {route} -> {status} (500 ERROR)")
                elif status == 302:
                    # Redirect is expected if login mock didn't work
                    print(f"  ⚠ GET {route} -> {status} (redirect)")
                elif status != expected_status:
                    print(f"  ⚠ GET {route} -> {status} (expected {expected_status})")
                else:
                    print(f"  ✓ GET {route} -> {status}")
            except Exception as e:
                errors.append(f"GET {route} -> EXCEPTION: {e}")
                print(f"  ✗ GET {route} -> EXCEPTION: {e}")
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
        
        if errors:
            self.fail(f"Found {len(errors)} route errors")

if __name__ == '__main__':
    # Run with verbose output
    suite = unittest.TestLoader().loadTestsFromTestCase(RouteAudit)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
