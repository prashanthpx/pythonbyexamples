# Phase 4 – Selection: using -k to select tests by name


def test_login_success():
    assert True


def test_login_failure():
    assert True


def test_logout():
    assert True


def test_profile_update():
    assert True

'''
Output from: pytest -v test_selection_k.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 4 items

test_selection_k.py::test_login_success PASSED
test_selection_k.py::test_login_failure PASSED
test_selection_k.py::test_logout PASSED
test_selection_k.py::test_profile_update PASSED

==================================================== 4 passed in 0.01s ====================================================
'''
