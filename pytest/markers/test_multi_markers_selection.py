import pytest


# Phase 4 – Markers: combining multiple markers and -m expressions


@pytest.mark.slow
@pytest.mark.api
def test_slow_api():
    assert True


@pytest.mark.api
def test_fast_api():
    assert True


@pytest.mark.db
def test_db_only():
    assert True


@pytest.mark.slow
@pytest.mark.db
def test_slow_db():
    assert True

'''
Output from: pytest -v test_multi_markers_selection.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 5 items

test_multi_markers_selection.py::test_slow_api PASSED
test_multi_markers_selection.py::test_fast_api PASSED
test_multi_markers_selection.py::test_db_only PASSED
test_multi_markers_selection.py::test_slow_db PASSED
test_multi_markers_selection.py::test_unmarked PASSED

==================================================== 5 passed in 0.01s ====================================================
'''


def test_unmarked():
    assert True

