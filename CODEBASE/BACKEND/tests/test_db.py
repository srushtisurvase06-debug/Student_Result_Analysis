"""Tests for the database utilities.

The whole suite runs offline: psycopg2.connect is replaced with a fake so that
connection parameters, transaction handling and the query contract can be
verified without a live database. The one test that needs a real connection is
marked `integration` and skips itself when DATABASE_URL is unset.
"""

import logging
import os

import psycopg2
import pytest
from psycopg2.extras import RealDictCursor

from app import create_app
from utils import db


class FakeCursor:
    def __init__(self, description=None, rows=None, rowcount=0, raise_on_execute=None):
        self.description = description
        self.rowcount = rowcount
        self.closed = False
        self.executed = []
        self._rows = rows if rows is not None else []
        self._raise_on_execute = raise_on_execute

    def execute(self, query, params=None):
        self.executed.append((query, params))
        if self._raise_on_execute is not None:
            raise self._raise_on_execute

    def fetchall(self):
        return list(self._rows)

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def fetchmany(self, size):
        return list(self._rows[:size])

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class FakeDatabase:
    """Records how psycopg2.connect was called and hands back the fake objects."""

    def __init__(self):
        self.dsn = None
        self.kwargs = None
        self.cursor = FakeCursor()
        self.connection = None
        self.connect_error = None

    def connect(self, dsn=None, **kwargs):
        self.dsn = dsn
        self.kwargs = kwargs
        if self.connect_error is not None:
            raise self.connect_error
        self.connection = FakeConnection(self.cursor)
        return self.connection


@pytest.fixture
def fake_db(monkeypatch):
    fake = FakeDatabase()
    monkeypatch.setattr(db.psycopg2, 'connect', fake.connect)
    return fake


@pytest.fixture
def db_app(app):
    """Testing app with a database URL present in configuration."""
    app.config['DATABASE_URL'] = 'postgresql://config-user@config-host/config-db'
    return app


class TestConnectionParameters:
    def test_uses_required_driver_settings(self, fake_db, db_app):
        with db_app.app_context():
            db.get_db_connection()

        assert fake_db.kwargs['cursor_factory'] is RealDictCursor
        assert fake_db.kwargs['sslmode'] == 'require'
        assert fake_db.kwargs['connect_timeout'] == 10

    def test_prefers_the_url_from_flask_config(self, fake_db, db_app, monkeypatch):
        monkeypatch.setenv('DATABASE_URL', 'postgresql://env-host/env-db')

        with db_app.app_context():
            db.get_db_connection()

        assert fake_db.dsn == 'postgresql://config-user@config-host/config-db'

    def test_falls_back_to_the_environment_outside_an_app_context(
        self, fake_db, monkeypatch
    ):
        monkeypatch.setenv('DATABASE_URL', 'postgresql://env-host/env-db')

        db.get_db_connection()

        assert fake_db.dsn == 'postgresql://env-host/env-db'

    def test_raises_a_clear_error_when_no_url_is_configured(self, fake_db, monkeypatch):
        monkeypatch.delenv('DATABASE_URL', raising=False)

        with pytest.raises(RuntimeError, match='DATABASE_URL'):
            db.get_db_connection()

    def test_operational_error_is_reraised(self, fake_db, monkeypatch):
        monkeypatch.setenv('DATABASE_URL', 'postgresql://env-host/env-db')
        fake_db.connect_error = psycopg2.OperationalError('boom')

        with pytest.raises(psycopg2.OperationalError):
            db.get_db_connection()


class TestExecuteQuery:
    """The Phase 1 implementation returned a cursor that the finally block had
    already closed, so every caller received an unusable object."""

    def test_returns_rows_for_a_returning_statement(self, fake_db, db_app):
        fake_db.cursor.description = [('id',)]
        fake_db.cursor._rows = [{'id': 7}]

        with db_app.app_context():
            result = db.execute_query(
                'INSERT INTO students (roll_number) VALUES (%s) RETURNING id',
                ('2024099',),
            )

        assert result == [{'id': 7}]

    def test_returns_rowcount_for_a_plain_write(self, fake_db, db_app):
        fake_db.cursor.description = None
        fake_db.cursor.rowcount = 3

        with db_app.app_context():
            result = db.execute_query('DELETE FROM marks WHERE student_id = %s', (1,))

        assert result == 3

    def test_result_is_not_a_closed_cursor(self, fake_db, db_app):
        fake_db.cursor.description = None
        fake_db.cursor.rowcount = 1

        with db_app.app_context():
            result = db.execute_query('UPDATE students SET name = %s', ('x',))

        assert not hasattr(result, 'closed')

    def test_commits_and_closes_on_success(self, fake_db, db_app):
        with db_app.app_context():
            db.execute_query('UPDATE students SET name = %s', ('x',))

        assert fake_db.connection.committed is True
        assert fake_db.connection.closed is True
        assert fake_db.cursor.closed is True

    def test_rolls_back_and_closes_on_failure(self, fake_db, db_app):
        fake_db.cursor._raise_on_execute = psycopg2.IntegrityError('duplicate key')

        with db_app.app_context():
            with pytest.raises(psycopg2.IntegrityError):
                db.execute_query('INSERT INTO students VALUES (%s)', ('dup',))

        assert fake_db.connection.rolled_back is True
        assert fake_db.connection.committed is False
        assert fake_db.connection.closed is True
        assert fake_db.cursor.closed is True


class TestFetchHelpers:
    def test_fetch_one_returns_a_single_row(self, fake_db, db_app):
        fake_db.cursor._rows = [{'id': 1}, {'id': 2}]

        with db_app.app_context():
            assert db.fetch_one('SELECT id FROM students') == {'id': 1}

    def test_fetch_all_returns_every_row(self, fake_db, db_app):
        fake_db.cursor._rows = [{'id': 1}, {'id': 2}]

        with db_app.app_context():
            assert db.fetch_all('SELECT id FROM students') == [{'id': 1}, {'id': 2}]

    def test_fetch_many_respects_size(self, fake_db, db_app):
        fake_db.cursor._rows = [{'id': 1}, {'id': 2}, {'id': 3}]

        with db_app.app_context():
            assert db.fetch_many('SELECT id FROM students', 2) == [{'id': 1}, {'id': 2}]

    def test_helpers_close_their_resources(self, fake_db, db_app):
        with db_app.app_context():
            db.fetch_all('SELECT 1')

        assert fake_db.cursor.closed is True
        assert fake_db.connection.closed is True


class TestSqlInjectionProtection:
    @pytest.mark.parametrize(
        'call',
        [
            lambda: db.fetch_one('SELECT * FROM students WHERE roll_number = %s', ('x',)),
            lambda: db.fetch_all('SELECT * FROM students WHERE roll_number = %s', ('x',)),
            lambda: db.execute_query('DELETE FROM students WHERE roll_number = %s', ('x',)),
        ],
    )
    def test_parameters_are_passed_separately_from_the_statement(
        self, fake_db, db_app, call
    ):
        """SEC-036: the driver must do the escaping, never string formatting."""
        fake_db.cursor.description = None

        with db_app.app_context():
            call()

        query, params = fake_db.cursor.executed[-1]
        assert '%s' in query
        assert params == ('x',)
        # The value must never have been interpolated into the statement.
        assert "'x'" not in query

    def test_a_malicious_value_stays_a_parameter(self, fake_db, db_app):
        payload = "1; DROP TABLE students; --"

        with db_app.app_context():
            db.fetch_all('SELECT * FROM students WHERE roll_number = %s', (payload,))

        query, params = fake_db.cursor.executed[-1]
        assert 'DROP TABLE' not in query
        assert params == (payload,)


class TestLoggingSafety:
    def test_logging_works_outside_an_application_context(
        self, fake_db, monkeypatch, caplog
    ):
        """current_app would raise 'Working outside of application context' and
        mask the real database error."""
        monkeypatch.setenv('DATABASE_URL', 'postgresql://env-host/env-db')
        fake_db.cursor._raise_on_execute = psycopg2.ProgrammingError('bad sql')

        with caplog.at_level(logging.ERROR, logger='utils.db'):
            with pytest.raises(psycopg2.ProgrammingError):
                db.fetch_all('SELECT * FROM missing_table')

        assert 'Fetch all failed' in caplog.text
        assert 'ProgrammingError' in caplog.text

    def test_connection_failure_log_omits_the_connection_string(
        self, fake_db, monkeypatch, caplog
    ):
        secret_dsn = 'postgresql://dbuser:dbpassword@db.example.com:5432/results'
        monkeypatch.setenv('DATABASE_URL', secret_dsn)
        fake_db.connect_error = psycopg2.OperationalError(
            'connection to server at "db.example.com", user "dbuser" failed'
        )

        with caplog.at_level(logging.ERROR, logger='utils.db'):
            with pytest.raises(psycopg2.OperationalError):
                db.get_db_connection()

        assert 'dbpassword' not in caplog.text
        assert 'db.example.com' not in caplog.text
        assert 'OperationalError' in caplog.text

    def test_query_parameters_are_never_logged(self, fake_db, monkeypatch, caplog):
        monkeypatch.setenv('DATABASE_URL', 'postgresql://env-host/env-db')
        fake_db.cursor._raise_on_execute = psycopg2.DataError('bad value')

        with caplog.at_level(logging.ERROR, logger='utils.db'):
            with pytest.raises(psycopg2.DataError):
                db.fetch_one(
                    'SELECT * FROM students WHERE contact_number = %s',
                    ('9876543210',),
                )

        # The statement template is safe to log; the values are not.
        assert 'contact_number' in caplog.text
        assert '9876543210' not in caplog.text

    def test_statement_is_truncated_in_logs(self):
        long_statement = 'SELECT ' + ('x' * 500)
        summary = db._summarise(long_statement)
        assert len(summary) <= db._MAX_LOGGED_STATEMENT + 3
        assert summary.endswith('...')

    def test_summarise_collapses_whitespace(self):
        assert db._summarise('SELECT\n  1\n  FROM   students') == 'SELECT 1 FROM students'


class TestLiveDatabase:
    @pytest.mark.integration
    def test_can_reach_the_phase_2_schema(self):
        """Read-only. Skipped unless DATABASE_URL points at a real database."""
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            pytest.skip('DATABASE_URL is not set; skipping live database check')
        if 'placeholder' in db_url:
            pytest.skip('DATABASE_URL is placeholder; skipping live database check')

        application = create_app('development')
        with application.app_context():
            assert db.fetch_one('SELECT 1 AS ok')['ok'] == 1
