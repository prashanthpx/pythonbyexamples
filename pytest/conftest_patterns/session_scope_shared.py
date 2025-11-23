import pytest


# Simple module-level counters so we can see how often the session fixture runs.
setup_calls = 0


@pytest.fixture(scope="session")
def session_fix():
    global setup_calls
    setup_calls += 1
    yield


output = """\
$ pytest -v test_session_scope_one.py test_session_scope_two.py
=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_session_scope_one.py::test_session_fixture_seen_in_first_module PASSED                                          [ 50%]
test_session_scope_two.py::test_session_fixture_seen_in_second_module PASSED                                         [100%]

==================================================== 2 passed in 0.01s ====================================================
"""
