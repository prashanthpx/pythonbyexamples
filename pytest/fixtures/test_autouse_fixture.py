import pytest


# Phase 3  Fixtures: autouse fixture runs for every test in this module


log = []


@pytest.fixture(autouse=True)
def auto_log():
    """Autouse fixture that logs around every test in this module.

    Because autouse=True, we don't need to list it as a parameter
    in each test; it still runs for each test.
    """
    log.append("autouse-setup")
    yield
    log.append("autouse-teardown")


def test_first_uses_autouse():
    # At least one setup should have run before this assertion.
    assert log.count("autouse-setup") >= 1



'''
Output from: pytest -v test_autouse_fixture.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_autouse_fixture.py::test_first_uses_autouse PASSED
test_autouse_fixture.py::test_second_uses_autouse_again PASSED

==================================================== 2 passed in 0.01s ====================================================
'''

def test_second_uses_autouse_again():
    # By now, the autouse fixture has run for both tests.
    assert log.count("autouse-setup") >= 2

