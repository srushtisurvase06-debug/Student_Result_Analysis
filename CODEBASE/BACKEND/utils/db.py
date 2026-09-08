"""Database access utilities.

Every helper opens a connection, runs one statement and closes the connection.
Queries are always parameterised: the SQL string and its parameters are passed
to psycopg2 separately, so the driver handles escaping and SQL injection is not
possible through these functions (SEC-036, TR-DB-004).

Logging rule enforced throughout this module: the SQL statement may be logged
because it is a static template containing only placeholders, never data. Query
parameters, connection strings and credentials are never logged.
"""

import logging
import os
import re

import psycopg2
from flask import current_app, has_app_context
from psycopg2.extras import RealDictCursor

_module_logger = logging.getLogger(__name__)

_MAX_LOGGED_STATEMENT = 200


def _logger():
    """Return the Flask app logger inside an app context, else a module logger.

    These helpers are also called from one-off scripts and from the test suite,
    where current_app would raise 'Working outside of application context' and
    mask the real database error.
    """
    if has_app_context():
        return current_app.logger
    return _module_logger


def _summarise(statement):
    """Collapse a SQL statement to a single truncated line for logging."""
    collapsed = re.sub(r'\s+', ' ', str(statement)).strip()
    if len(collapsed) > _MAX_LOGGED_STATEMENT:
        return collapsed[:_MAX_LOGGED_STATEMENT] + '...'
    return collapsed


def _log_error(message, exc, query=None):
    """Log a database failure without leaking data or credentials."""
    detail = '{}: {}'.format(message, type(exc).__name__)

    pgcode = getattr(exc, 'pgcode', None)
    if pgcode:
        detail += ' (SQLSTATE {})'.format(pgcode)

    if query is not None:
        detail += ' | statement: {}'.format(_summarise(query))

    _logger().error(detail)


def _database_url():
    """Resolve the database URL from Flask config, falling back to the environment."""
    url = None
    if has_app_context():
        url = current_app.config.get('DATABASE_URL')
    if not url:
        url = os.getenv('DATABASE_URL')
    if not url:
        # Without this check psycopg2 would receive None, fall back to libpq
        # defaults and fail with an unrelated message about a local socket.
        raise RuntimeError(
            'DATABASE_URL is not configured. Set it in the environment or .env file.'
        )
    return url


def get_db_connection():
    """Get database connection with RealDictCursor for dict-like row access"""
    try:
        conn = psycopg2.connect(
            _database_url(),
            cursor_factory=RealDictCursor,
            sslmode='require',
            connect_timeout=10
        )
        return conn
    except psycopg2.OperationalError as e:
        # The message is omitted deliberately: it can contain the connection
        # string, including host and user.
        _logger().error(
            'Database connection failed: %s', type(e).__name__
        )
        raise


def execute_query(query, params=None):
    """Execute a write query and return its result.

    Returns:
        A list of rows when the statement produces rows, for example
        ``INSERT ... RETURNING id``; otherwise the number of affected rows.

    The result is materialised before the cursor is closed. Returning the cursor
    itself would hand the caller an already-closed object, because the finally
    block below closes both the cursor and the connection.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall() if cursor.description else cursor.rowcount
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        _log_error('Query execution failed', e, query)
        raise
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, params=None):
    """Fetch a single row from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except Exception as e:
        _log_error('Fetch one failed', e, query)
        raise
    finally:
        cursor.close()
        conn.close()


def fetch_all(query, params=None):
    """Fetch all rows from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        _log_error('Fetch all failed', e, query)
        raise
    finally:
        cursor.close()
        conn.close()


def fetch_many(query, size, params=None):
    """Fetch specified number of rows from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchmany(size)
    except Exception as e:
        _log_error('Fetch many failed', e, query)
        raise
    finally:
        cursor.close()
        conn.close()
