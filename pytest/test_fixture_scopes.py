import pytest


# Phase 3 – Fixtures: scopes and teardown with `yield`

call_log = []


@pytest.fixture
def function_scope_fixture():
    """Function-scope fixture (default scope).

    Runs once per test that uses it.
    """
    call_log.append("function-setup")
    yield
    call_log.append("function-teardown")


@pytest.fixture(scope="module")
def module_scope_fixture():
    """Module-scope fixture.

    Runs once for the whole module (all tests that use it),
    and tears down once at the end.
    """
    call_log.append("module-setup")
    yield
    call_log.append("module-teardown")


def test_one(function_scope_fixture, module_scope_fixture):
    assert True


def test_two(function_scope_fixture, module_scope_fixture):
    assert True


def test_check_call_log():
    """Verify how many times each fixture ran.

    - module_scope_fixture should run once for setup.
    - function_scope_fixture should run separately for each test that uses it.

    Note: for a `scope="module"` fixture, teardown happens *after* all
    tests in this module finish, so we do **not** see `module-teardown`
    yet while this test is running.
    """
    # module-scope fixture should only run once for setup
    assert call_log.count("module-setup") == 1

    # function-scope fixture runs separately for each test that uses it
    assert call_log.count("function-setup") == 2
    assert call_log.count("function-teardown") == 2


'''
Output from: pytest -v test_fixture_scopes.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 3 items

test_fixture_scopes.py::test_one PASSED
test_fixture_scopes.py::test_two PASSED
test_fixture_scopes.py::test_check_call_log PASSED

==================================================== 3 passed in 0.01s ====================================================
'''

