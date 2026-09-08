"""Configuration for the Student Result Analysis System.

Environment variables are loaded in this module, at import time, because the
configuration classes below read them in their class bodies. Loading them from
app.py would be too late: importing this module already evaluates the classes,
so `from config import config` must not run before the .env file is read.

Validation lives in a `validate()` classmethod rather than in a class body so
that importing this module can never raise, in any environment. A class-body
`raise` would break every development import and every test collection.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# config.py lives at CODEBASE/BACKEND/config.py, so the repository root - where
# .env is kept - is three levels up. An explicit path keeps loading independent
# of the current working directory; the fallback preserves python-dotenv's
# upward search for unusual layouts.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _REPO_ROOT / '.env'

if _ENV_FILE.is_file():
    load_dotenv(_ENV_FILE)
else:
    load_dotenv()


class Config:
    """Base configuration shared by every environment."""

    # Secrets come from the environment only. There is deliberately no
    # hardcoded fallback here: a shared default would be inherited by
    # ProductionConfig and silently weaken production sessions (SEC-030).
    SECRET_KEY = os.getenv('SECRET_KEY')

    DATABASE_URL = os.getenv('DATABASE_URL')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    @classmethod
    def validate(cls):
        """Check required settings.

        Returns a list of human-readable warning strings for non-fatal problems.
        Subclasses raise ValueError instead when a missing value is fatal.
        Never include a secret value in a returned message.
        """
        warnings = []
        if not cls.SECRET_KEY:
            warnings.append(
                'SECRET_KEY is not set; sessions will not be stable across restarts.'
            )
        if not cls.DATABASE_URL:
            warnings.append(
                'DATABASE_URL is not set; database-backed features are unavailable.'
            )
        return warnings


class DevelopmentConfig(Config):
    """Local development configuration."""

    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_COOKIE_SECURE = False

    # Clearly labelled, development-only. Overridden by SECRET_KEY when set.
    SECRET_KEY = os.getenv('SECRET_KEY') or 'development-only-not-for-production'


class TestingConfig(Config):
    """Configuration for the automated test suite.

    The suite substitutes a fake database driver, so DATABASE_URL is optional
    and its absence must not produce warnings or failures.
    """

    TESTING = True
    DEBUG = False
    FLASK_ENV = 'testing'
    SESSION_COOKIE_SECURE = False

    SECRET_KEY = os.getenv('SECRET_KEY') or 'testing-only-not-for-production'

    @classmethod
    def validate(cls):
        return []


class ProductionConfig(Config):
    """Production configuration.

    Refuses to start when a required secret is absent. Failing loudly at
    start-up is safer than running on a weak or absent key (SEC-030, SEC-038).
    """

    DEBUG = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True

    @classmethod
    def validate(cls):
        missing = [
            name for name in ('SECRET_KEY', 'DATABASE_URL')
            if not getattr(cls, name, None)
        ]
        if missing:
            raise ValueError(
                'Missing required production environment variable(s): '
                + ', '.join(missing)
                + '. Set them in the deployment environment before starting the '
                'application.'
            )
        return []


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
