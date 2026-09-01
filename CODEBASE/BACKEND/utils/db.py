import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask import current_app


def get_db_connection():
    """Get database connection with RealDictCursor for dict-like row access"""
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor,
            sslmode='require',
            connect_timeout=10
        )
        return conn
    except psycopg2.OperationalError as e:
        current_app.logger.error(f'Database connection failed: {e}')
        raise


def execute_query(query, params=None):
    """Execute a query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f'Query execution failed: {e}')
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
        current_app.logger.error(f'Fetch one failed: {e}')
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
        current_app.logger.error(f'Fetch all failed: {e}')
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
        current_app.logger.error(f'Fetch many failed: {e}')
        raise
    finally:
        cursor.close()
        conn.close()
