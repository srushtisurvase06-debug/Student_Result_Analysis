"""Import and syntax checks for every backend module.

A syntax error or a bad import in a module that no test touches directly would
otherwise only surface at deploy time. These tests import each module by the
same name production uses, and compile every source file.
"""

import importlib
import py_compile
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent

MODULES = [
    'app',
    'config',
    'routes',
    'utils',
    'utils.db',
    'utils.decorators',
    'utils.helpers',
]


@pytest.mark.parametrize('module_name', MODULES)
def test_module_imports_cleanly(module_name):
    assert importlib.import_module(module_name) is not None


@pytest.mark.parametrize('module_name', MODULES)
def test_module_is_importable_twice(module_name):
    """Re-importing must be side-effect free; the factory is called on import."""
    first = importlib.import_module(module_name)
    assert importlib.import_module(module_name) is first


def test_every_source_file_compiles():
    sources = sorted(
        path for path in BACKEND_DIR.rglob('*.py')
        if '__pycache__' not in path.parts
    )
    assert sources, 'no Python sources found'

    for path in sources:
        py_compile.compile(str(path), doraise=True)


def test_expected_public_names_exist():
    """Guards the contracts later phases and the deployment rely on."""
    app_module = importlib.import_module('app')
    assert callable(app_module.create_app)
    assert app_module.app is not None

    config_module = importlib.import_module('config')
    assert isinstance(config_module.config, dict)

    db_module = importlib.import_module('utils.db')
    for name in ('get_db_connection', 'execute_query', 'fetch_one', 'fetch_all', 'fetch_many'):
        assert callable(getattr(db_module, name)), name

    helpers = importlib.import_module('utils.helpers')
    for name in ('format_date', 'format_datetime', 'get_current_datetime', 'get_current_date'):
        assert callable(getattr(helpers, name)), name

    decorators = importlib.import_module('utils.decorators')
    assert callable(decorators.login_required)
