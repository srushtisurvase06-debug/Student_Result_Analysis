"""Application entry point and factory for the Student Result Analysis System.

Phase 3 scope: the Flask application foundation only. No authentication, no
CRUD, no result calculation and no reporting is registered here; those arrive in
Phase 4 and later. Blueprints are registered at the marked point in
create_app() when the phases that own them are built.

Production runs this module through gunicorn as `gunicorn app:app`, so the
module-level `app` object below is part of the deployment contract.
"""

import logging
import os
import sys

import psycopg2
from flask import Flask, jsonify, render_template, request, redirect
from flask.logging import default_handler
from werkzeug.exceptions import HTTPException

# Importing config also loads the .env file. That import must therefore happen
# before anything in this module reads an environment variable. See config.py.
from config import config
from routes.auth import bp as auth_bp, login_required
from routes.dashboard import bp as dashboard_bp
from routes.analysis import bp as analysis_bp
from routes.reports import bp as reports_bp
from routes.students import bp as students_bp
from routes.subjects import bp as subjects_bp
from routes.marks import bp as marks_bp
from routes.results import bp as results_bp
from routes.profile import bp as profile_bp

_LOG_HANDLER_NAME = 'srs-stdout'

# Titles and messages for the status codes that share the generic error page.
# Wording is intentionally generic: no internal detail reaches the user (SEC-039).
_ERROR_PAGES = {
    400: (
        'Bad Request',
        'The request could not be understood. Please check your input and try again.',
    ),
    401: (
        'Sign In Required',
        'You need to sign in before you can view this page.',
    ),
    403: (
        'Access Denied',
        'You do not have permission to view this page.',
    ),
    405: (
        'Action Not Allowed',
        'That action is not supported for this page.',
    ),
    503: (
        'Service Unavailable',
        'The service is temporarily unavailable. Please try again in a few moments.',
    ),
}


def _configure_logging(app):
    """Attach a stdout handler and apply the configured log level.

    Runs in every environment, not just production: development previously had
    no logging configuration at all. Render captures stdout, so a stream handler
    is the correct sink there - a file handler would be lost on each redeploy.
    """
    level_name = str(app.config.get('LOG_LEVEL') or 'INFO').upper()
    level = getattr(logging, level_name, None)
    if not isinstance(level, int):
        level = logging.DEBUG if app.debug else logging.INFO

    app.logger.setLevel(level)

    # Flask installs its own stderr handler on first app.logger access. Leaving
    # it in place would duplicate every line, since ours writes to stdout.
    app.logger.removeHandler(default_handler)

    # Idempotent by design: the test suite calls create_app() many times, and
    # blindly adding a handler each time would duplicate every log line.
    existing = [h for h in app.logger.handlers if h.get_name() == _LOG_HANDLER_NAME]
    if existing:
        for handler in existing:
            handler.setLevel(level)
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.set_name(_LOG_HANDLER_NAME)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s %(module)s:%(lineno)d - %(message)s'
        ))
        app.logger.addHandler(handler)

    # Our own handler is the only sink; propagating would duplicate output via
    # the root logger if anything else calls logging.basicConfig().
    app.logger.propagate = False


def _render_error_page(code):
    """Render the shared error page for a status code."""
    heading, message = _ERROR_PAGES[code]
    return render_template(
        'errors/error.html', code=code, heading=heading, message=message
    ), code


def _register_error_handlers(app):
    """Register handlers for every status code the application can emit.

    User-facing output never contains a traceback, SQL statement, table name,
    file path or configuration value (TRD 17.5, PRD ERR-005). Diagnostic detail
    goes to the log only.
    """

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.warning('400 Bad Request: %s', request.path)
        return _render_error_page(400)

    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.warning('401 Unauthorized: %s', request.path)
        return _render_error_page(401)

    @app.errorhandler(403)
    def forbidden(error):
        app.logger.warning('403 Forbidden: %s', request.path)
        return _render_error_page(403)

    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning('404 Not Found: %s', request.path)
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        app.logger.warning('405 Method Not Allowed: %s %s', request.method, request.path)
        return _render_error_page(405)

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('500 Internal Server Error: %s', request.path, exc_info=error)
        return render_template('errors/500.html'), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        app.logger.error('503 Service Unavailable: %s', request.path)
        return _render_error_page(503)

    @app.errorhandler(psycopg2.OperationalError)
    def database_unavailable(error):
        # Only the exception type is logged. An OperationalError message can
        # embed the connection string, including host and user, which must never
        # reach the log.
        app.logger.error(
            'Database unavailable at %s: %s', request.path, type(error).__name__
        )
        return _render_error_page(503)

    @app.errorhandler(psycopg2.Error)
    def database_error(error):
        # SQLSTATE identifies the fault precisely without exposing any data.
        app.logger.error(
            'Database error at %s: %s (SQLSTATE %s)',
            request.path,
            type(error).__name__,
            getattr(error, 'pgcode', None),
        )
        return render_template('errors/500.html'), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        # Defensive: with TRAP_HTTP_EXCEPTIONS enabled this handler can receive
        # HTTP errors, which must keep their own status rather than becoming 500.
        if isinstance(error, HTTPException):
            return error
        app.logger.error('Unhandled exception at %s', request.path, exc_info=error)
        return render_template('errors/500.html'), 500


def _register_security_headers(app):
    """Add security headers to every response (TR-SEC-020, SEC-041).

    Implemented manually rather than via Flask-Talisman so that Phase 3 adds no
    new dependency. Content-Security-Policy is deferred: a correct policy
    depends on the Chart.js integration decided in Phase 13.
    """

    @app.after_request
    def set_secure_headers(response):
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'DENY')
        response.headers.setdefault('X-XSS-Protection', '1; mode=block')
        response.headers.setdefault(
            'Referrer-Policy', 'strict-origin-when-cross-origin'
        )
        if app.config.get('FLASK_ENV') == 'production':
            response.headers.setdefault(
                'Strict-Transport-Security', 'max-age=31536000; includeSubDomains'
            )
        return response


def create_app(config_name=None):
    """Application factory.

    Args:
        config_name: Optional configuration key ('development', 'testing',
            'production'). Defaults to the FLASK_ENV environment variable, then
            to 'default'. Unrecognised values fall back to the default config
            rather than raising, so a typo cannot crash start-up before any
            error handler exists.
    """
    app = Flask(__name__)

    env = (config_name or os.getenv('FLASK_ENV') or 'development').strip().lower()
    selected_config = config.get(env, config['default'])
    app.config.from_object(selected_config)

    _configure_logging(app)

    # Raises in production when SECRET_KEY or DATABASE_URL is absent; returns
    # warnings elsewhere. Called after logging so warnings are visible.
    for warning in selected_config.validate():
        app.logger.warning('Configuration: %s', warning)

    _register_error_handlers(app)
    _register_security_headers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(marks_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(profile_bp)

    @app.route('/')
    def index():
        """Root endpoint - API status."""
        return jsonify({
            'message': 'Student Result Analysis System API',
            'version': '1.0',
            'status': 'running'
        })

    @app.route('/health')
    def health():
        """Health check endpoint for deployment monitoring.

        Deliberately performs no database query: the platform health check must
        stay fast and must not fail while the database is merely paused.
        """
        return jsonify({'status': 'healthy'}), 200

    @app.route('/result-lookup', methods=['GET'])
    def result_lookup_redirect():
        """Public result lookup page - redirect to results blueprint for consistency."""
        return redirect('/results/lookup')

    app.logger.info('Application initialised in %s mode', app.config.get('FLASK_ENV'))

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
