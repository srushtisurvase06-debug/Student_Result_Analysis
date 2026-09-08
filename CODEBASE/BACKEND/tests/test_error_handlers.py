"""Tests for the error handlers and for information leakage in error responses."""

import psycopg2
import pytest
from flask import abort

from app import create_app


@pytest.fixture
def error_client():
    """A client whose app exposes routes that deliberately fail.

    The routes are registered before the first request, which Flask requires,
    and are prefixed with __ so they cannot collide with real application URLs.
    """
    application = create_app('testing')

    @application.route('/__abort/<int:code>')
    def _abort(code):
        abort(code)

    @application.route('/__raise')
    def _raise():
        raise RuntimeError('deliberate failure with sensitive detail')

    @application.route('/__db-down')
    def _db_down():
        raise psycopg2.OperationalError(
            'connection to server at "db.internal.example.com", user "admin" failed'
        )

    @application.route('/__db-error')
    def _db_error():
        raise psycopg2.ProgrammingError('relation "students" does not exist')

    return application.test_client()


class TestHttpErrorHandlers:
    def test_unknown_url_returns_404_page(self, client):
        response = client.get('/definitely-not-a-real-page')
        assert response.status_code == 404
        assert b'Page Not Found' in response.data

    def test_wrong_method_returns_405(self, client):
        response = client.post('/health')
        assert response.status_code == 405
        assert b'Action Not Allowed' in response.data

    @pytest.mark.parametrize(
        'code,expected_text',
        [
            (400, b'Bad Request'),
            (401, b'Sign In Required'),
            (403, b'Access Denied'),
            (503, b'Service Unavailable'),
        ],
    )
    def test_generic_error_pages_render(self, error_client, code, expected_text):
        response = error_client.get('/__abort/{}'.format(code))
        assert response.status_code == code
        assert expected_text in response.data

    def test_aborted_500_returns_error_page(self, error_client):
        response = error_client.get('/__abort/500')
        assert response.status_code == 500
        assert b'Something Went Wrong' in response.data

    def test_unhandled_exception_returns_500_page(self, error_client):
        response = error_client.get('/__raise')
        assert response.status_code == 500
        assert b'Something Went Wrong' in response.data


class TestDatabaseErrorHandlers:
    def test_operational_error_becomes_503(self, error_client):
        """TR-ERR-008: an unreachable database is a service-availability fault."""
        response = error_client.get('/__db-down')
        assert response.status_code == 503
        assert b'Service Unavailable' in response.data

    def test_other_database_errors_become_500(self, error_client):
        response = error_client.get('/__db-error')
        assert response.status_code == 500
        assert b'Something Went Wrong' in response.data


class TestNoInformationLeakage:
    LEAK_MARKERS = [
        b'Traceback',
        b'RuntimeError',
        b'psycopg2',
        b'SECRET_KEY',
        b'DATABASE_URL',
        b'postgresql://',
        b'db.internal.example.com',
        b'sensitive detail',
        b'relation "students"',
        b'.py",',
        b'site-packages',
    ]

    @pytest.mark.parametrize(
        'path',
        ['/__raise', '/__db-down', '/__db-error', '/__abort/403', '/__abort/500'],
    )
    def test_response_body_reveals_nothing_internal(self, error_client, path):
        """TRD 17.5 / PRD ERR-005: no internal detail may reach the user."""
        body = error_client.get(path).data
        for marker in self.LEAK_MARKERS:
            assert marker not in body, marker

    def test_404_body_reveals_nothing_internal(self, client):
        body = client.get('/secret-admin-path').data
        for marker in self.LEAK_MARKERS:
            assert marker not in body, marker

    def test_error_response_does_not_echo_the_requested_path(self, client):
        """Reflecting the URL back would give a stored-XSS foothold."""
        body = client.get('/<script>alert(1)</script>').data
        assert b'<script>alert(1)</script>' not in body


class TestErrorPagesUseTemplateInheritance:
    @pytest.mark.parametrize('path', ['/no-such-page', '/__abort/403'])
    def test_pages_are_complete_documents_from_base(self, error_client, path):
        body = error_client.get(path).data
        assert body.startswith(b'<!DOCTYPE html>')
        assert b'css/main.css' in body
        assert b'css/print.css' in body

    @pytest.mark.parametrize('path', ['/no-such-page', '/__abort/403'])
    def test_pages_carry_no_inline_styles(self, error_client, path):
        """Styling belongs in main.css, not duplicated into each template."""
        assert b'<style' not in error_client.get(path).data
