"""Tests for the application factory, foundation routes and security headers."""

import logging

from flask import Flask

from app import create_app


class TestApplicationFactory:
    def test_create_app_returns_flask_instance(self, app):
        assert isinstance(app, Flask)

    def test_create_app_applies_testing_config(self, app):
        assert app.config['TESTING'] is True
        assert app.config['FLASK_ENV'] == 'testing'

    def test_create_app_defaults_to_development(self, monkeypatch):
        monkeypatch.delenv('FLASK_ENV', raising=False)
        application = create_app()
        assert application.config['FLASK_ENV'] == 'development'

    def test_create_app_honours_flask_env(self, monkeypatch):
        monkeypatch.setenv('FLASK_ENV', 'testing')
        assert create_app().config['FLASK_ENV'] == 'testing'

    def test_explicit_name_overrides_environment(self, monkeypatch):
        monkeypatch.setenv('FLASK_ENV', 'production')
        assert create_app('testing').config['FLASK_ENV'] == 'testing'

    def test_unknown_environment_falls_back_without_raising(self, monkeypatch):
        monkeypatch.setenv('FLASK_ENV', 'not-a-real-environment')
        # Must not raise KeyError; must land on the default configuration.
        assert create_app().config['FLASK_ENV'] == 'development'

    def test_module_level_app_exists_for_gunicorn(self):
        # Deployment runs `gunicorn app:app`, so this attribute is a contract.
        import app as app_module

        assert isinstance(app_module.app, Flask)


class TestFoundationRoutes:
    def test_index_returns_status_payload(self, client):
        response = client.get('/')
        assert response.status_code == 200

        payload = response.get_json()
        assert payload['message'] == 'Student Result Analysis System API'
        assert payload['version'] == '1.0'
        assert payload['status'] == 'running'

    def test_health_returns_healthy(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'healthy'}

    def test_only_foundation_routes_are_registered(self, app):
        """Phase 4 adds auth routes, Phase 6 adds dashboard routes, Phase 7 adds students routes, Phase 8 adds subjects routes, Phase 9 adds marks routes, Phase 10 adds result calculation engine, Phase 11 adds results view, Phase 12 adds public result lookup, Phase 13 adds performance analytics, Phase 14 adds reports routes, Admin Profile feature adds profile routes."""
        rules = {rule.rule for rule in app.url_map.iter_rules()}
        expected = {
            '/', '/health', '/dashboard/', '/analysis/', '/analysis/subject/<int:subject_id>',
            '/reports/', '/reports/individual', '/reports/class', '/reports/class-rank',
            '/reports/grade-distribution', '/reports/subject',
            '/login', '/logout', '/static/<path:filename>',
            '/students/', '/students/add', '/students/<int:student_id>/edit',
            '/students/<int:student_id>/delete', '/students/confirm-delete',
            '/subjects/', '/subjects/add', '/subjects/<int:subject_id>/edit',
            '/subjects/<int:subject_id>/delete',
            '/marks/', '/marks/add', '/marks/<int:marks_id>/edit',
            '/marks/<int:marks_id>/delete',
            '/results/', '/results/lookup', '/results/<int:student_id>',
            '/result-lookup', '/profile/'
        }
        assert rules == expected

    def test_no_blueprints_registered(self, app):
        assert 'auth' in app.blueprints
        assert 'dashboard' in app.blueprints
        assert 'analysis' in app.blueprints
        assert 'reports' in app.blueprints
        assert 'students' in app.blueprints
        assert 'subjects' in app.blueprints
        assert 'marks' in app.blueprints
        assert 'results' in app.blueprints
        assert 'profile' in app.blueprints
        assert set(app.blueprints) == {'auth', 'dashboard', 'analysis', 'reports', 'students', 'subjects', 'marks', 'results', 'profile'}


class TestSecurityHeaders:
    def test_headers_present_on_success(self, client):
        headers = client.get('/').headers
        assert headers['X-Content-Type-Options'] == 'nosniff'
        assert headers['X-Frame-Options'] == 'DENY'
        assert headers['X-XSS-Protection'] == '1; mode=block'
        assert headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'

    def test_headers_present_on_error_response(self, client):
        headers = client.get('/no-such-page').headers
        assert headers['X-Content-Type-Options'] == 'nosniff'
        assert headers['X-Frame-Options'] == 'DENY'

    def test_hsts_absent_outside_production(self, client):
        assert 'Strict-Transport-Security' not in client.get('/').headers

    def test_hsts_present_in_production(self, monkeypatch):
        from config import ProductionConfig

        # Satisfy production validation without reading or printing real secrets.
        monkeypatch.setattr(ProductionConfig, 'SECRET_KEY', 'test-only-value')
        monkeypatch.setattr(ProductionConfig, 'DATABASE_URL', 'postgresql://localhost/test')

        response = create_app('production').test_client().get('/')
        assert response.headers['Strict-Transport-Security'] == (
            'max-age=31536000; includeSubDomains'
        )


class TestLogging:
    def test_logger_has_stdout_handler(self, app):
        assert any(
            handler.get_name() == 'srs-stdout' for handler in app.logger.handlers
        )

    def test_flask_default_stderr_handler_is_removed(self, app):
        """Leaving it attached would duplicate every log line."""
        from flask.logging import default_handler

        assert default_handler not in app.logger.handlers

    def test_logger_does_not_propagate_to_root(self, app):
        assert app.logger.propagate is False

    def test_repeated_factory_calls_do_not_duplicate_handlers(self):
        first = create_app('testing')
        baseline = len(
            [h for h in first.logger.handlers if h.get_name() == 'srs-stdout']
        )

        for _ in range(3):
            create_app('testing')

        # Flask apps created from the same module share a logger name, so a
        # non-idempotent setup would stack handlers and duplicate every line.
        latest = create_app('testing')
        current = len(
            [h for h in latest.logger.handlers if h.get_name() == 'srs-stdout']
        )
        assert current == baseline == 1

    def test_log_level_follows_configuration(self, app):
        assert app.logger.level in {
            logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, logging.CRITICAL,
        }
