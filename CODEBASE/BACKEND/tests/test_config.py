"""Tests for configuration loading and validation."""

import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pytest

from config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    config,
)

BACKEND_DIR = Path(__file__).resolve().parent.parent


class TestConfigRegistry:
    def test_importing_config_never_raises_even_in_production(self):
        """Validation must live in validate(), not in a class body.

        A class-body raise would make `import config` fail whenever a secret is
        absent, breaking development, CI and test collection alike. This runs in
        a subprocess so the parent interpreter's already-imported module and
        environment cannot mask the result.
        """
        env = {
            key: value for key, value in os.environ.items()
            if key not in ('SECRET_KEY', 'DATABASE_URL')
        }
        env['FLASK_ENV'] = 'production'

        result = subprocess.run(
            [sys.executable, '-c', 'import config; print("imported")'],
            cwd=str(BACKEND_DIR),
            capture_output=True,
            text=True,
            env=env,
        )

        assert result.returncode == 0, result.stderr
        assert 'imported' in result.stdout

    def test_all_expected_keys_present(self):
        assert set(config) == {'development', 'testing', 'production', 'default'}

    def test_default_is_development(self):
        assert config['default'] is DevelopmentConfig

    def test_each_key_maps_to_a_config_class(self):
        for name, cls in config.items():
            assert issubclass(cls, Config), name


class TestRequiredKeys:
    @pytest.mark.parametrize('cls', [DevelopmentConfig, TestingConfig, ProductionConfig])
    def test_database_url_key_exists(self, cls):
        """TR-ENV-009: DATABASE_URL must be part of the configuration surface."""
        assert hasattr(cls, 'DATABASE_URL')

    @pytest.mark.parametrize('cls', [DevelopmentConfig, TestingConfig, ProductionConfig])
    def test_log_level_key_exists(self, cls):
        assert hasattr(cls, 'LOG_LEVEL')

    def test_log_level_defaults_to_a_valid_name(self):
        assert Config.LOG_LEVEL.upper() in {
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
        }


class TestEnvironmentValues:
    def test_debug_enabled_in_development(self):
        assert DevelopmentConfig.DEBUG is True

    def test_debug_disabled_in_production(self):
        """PRD SEC-038: the Werkzeug debugger must never run in production."""
        assert ProductionConfig.DEBUG is False

    def test_debug_disabled_in_testing(self):
        assert TestingConfig.DEBUG is False

    def test_session_cookie_secure_only_in_production(self):
        assert ProductionConfig.SESSION_COOKIE_SECURE is True
        assert DevelopmentConfig.SESSION_COOKIE_SECURE is False
        assert TestingConfig.SESSION_COOKIE_SECURE is False

    def test_session_cookie_hardening_shared(self):
        for cls in (DevelopmentConfig, TestingConfig, ProductionConfig):
            assert cls.SESSION_COOKIE_HTTPONLY is True
            assert cls.SESSION_COOKIE_SAMESITE == 'Lax'

    def test_session_lifetime_is_thirty_minutes(self):
        assert Config.PERMANENT_SESSION_LIFETIME == timedelta(minutes=30)


class TestProductionValidation:
    def test_raises_when_secret_key_missing(self, monkeypatch):
        monkeypatch.setattr(ProductionConfig, 'SECRET_KEY', None)
        monkeypatch.setattr(ProductionConfig, 'DATABASE_URL', 'postgresql://localhost/x')

        with pytest.raises(ValueError, match='SECRET_KEY'):
            ProductionConfig.validate()

    def test_raises_when_database_url_missing(self, monkeypatch):
        monkeypatch.setattr(ProductionConfig, 'SECRET_KEY', 'test-only-value')
        monkeypatch.setattr(ProductionConfig, 'DATABASE_URL', None)

        with pytest.raises(ValueError, match='DATABASE_URL'):
            ProductionConfig.validate()

    def test_passes_when_both_present(self, monkeypatch):
        monkeypatch.setattr(ProductionConfig, 'SECRET_KEY', 'test-only-value')
        monkeypatch.setattr(ProductionConfig, 'DATABASE_URL', 'postgresql://localhost/x')

        assert ProductionConfig.validate() == []

    def test_error_message_does_not_contain_secret_values(self, monkeypatch):
        monkeypatch.setattr(ProductionConfig, 'SECRET_KEY', None)
        monkeypatch.setattr(ProductionConfig, 'DATABASE_URL', 'postgresql://u:p@h/db')

        with pytest.raises(ValueError) as exc_info:
            ProductionConfig.validate()

        message = str(exc_info.value)
        assert 'postgresql://' not in message
        assert 'DATABASE_URL' in message or 'SECRET_KEY' in message

    def test_development_validation_warns_instead_of_raising(self, monkeypatch):
        monkeypatch.setattr(DevelopmentConfig, 'DATABASE_URL', None)
        warnings = DevelopmentConfig.validate()
        assert any('DATABASE_URL' in warning for warning in warnings)

    def test_testing_validation_is_silent_without_a_database(self, monkeypatch):
        monkeypatch.setattr(TestingConfig, 'DATABASE_URL', None)
        assert TestingConfig.validate() == []


class TestSecretHandling:
    def test_production_defines_no_secret_key_default(self):
        """SEC-030: ProductionConfig must inherit from the environment only.

        Defining its own value - or inheriting a hardcoded base default - would
        let a deploy run on a publicly known key.
        """
        assert 'SECRET_KEY' not in ProductionConfig.__dict__

    def test_base_secret_key_comes_from_the_environment(self):
        assert Config.SECRET_KEY == os.environ.get('SECRET_KEY')

    def test_development_defines_its_own_secret_key_fallback(self):
        assert 'SECRET_KEY' in DevelopmentConfig.__dict__

    def test_no_config_class_carries_the_old_insecure_default(self):
        for cls in (Config, DevelopmentConfig, TestingConfig, ProductionConfig):
            assert getattr(cls, 'SECRET_KEY', None) != 'dev-secret-key-change-in-production'

    def test_source_contains_no_hardcoded_production_secret(self):
        """Guards against a future edit reintroducing a shared fallback."""
        source = (BACKEND_DIR / 'config.py').read_text(encoding='utf-8')
        assert "SECRET_KEY = os.getenv('SECRET_KEY')" in source
        assert 'dev-secret-key-change-in-production' not in source
