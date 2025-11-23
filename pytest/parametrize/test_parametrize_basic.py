import pytest


# Phase 5 – Parametrization: single-parameter example


@pytest.mark.parametrize("number", [1, 2, 5, 10])
def test_positive_numbers_are_positive(number):
    assert number > 0



'''
Output from: pytest -v test_parametrize_basic.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 4 items

test_parametrize_basic.py::test_positive_numbers_are_positive[1] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[2] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[5] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[10] PASSED

==================================================== 4 passed in 0.01s ====================================================
'''
