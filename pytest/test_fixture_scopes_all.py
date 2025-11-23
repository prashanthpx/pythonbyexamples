import pytest


# Phase 3 – Fixtures: demonstrating all fixture scopes

call_log = []


@pytest.fixture(scope="function")
def function_scope():
    call_log.append("function-setup")
    yield
    call_log.append("function-teardown")


@pytest.fixture(scope="class")
def class_scope(request):
    call_log.append(f"class-setup-{request.cls.__name__}")
    yield
    call_log.append(f"class-teardown-{request.cls.__name__}")


@pytest.fixture(scope="module")
def module_scope():
    call_log.append("module-setup")
    yield
    call_log.append("module-teardown")


@pytest.fixture(scope="package")
def package_scope():
    call_log.append("package-setup")
    yield
    call_log.append("package-teardown")


@pytest.fixture(scope="session")
def session_scope():
    call_log.append("session-setup")
    yield
    call_log.append("session-teardown")


class TestFirst:
    def test_a(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True

    def test_b(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True


class TestSecond:
    def test_c(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True


def test_check_scope_setups():
    """Verify how often each fixture's setup ran in this module.

    In this single-module example:
    - function_scope runs once per test that uses it (3 tests).
    - class_scope runs once per *class* that uses it (2 classes).
    - module_scope runs once for this module.
    - package_scope runs once for this test package (here same as module).
    - session_scope runs once for the whole pytest session.
    """

    assert call_log.count("function-setup") == 3
    assert call_log.count("class-setup-TestFirst") == 1
    assert call_log.count("class-setup-TestSecond") == 1
    assert call_log.count("module-setup") == 1
    assert call_log.count("package-setup") == 1
    assert call_log.count("session-setup") == 1


output = """\
=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 4 items

test_fixture_scopes_all.py::TestFirst::test_a PASSED
test_fixture_scopes_all.py::TestFirst::test_b PASSED
test_fixture_scopes_all.py::TestSecond::test_c PASSED
test_fixture_scopes_all.py::test_check_scope_setups PASSED

==================================================== 4 passed in 0.01s =====================================================
"""
