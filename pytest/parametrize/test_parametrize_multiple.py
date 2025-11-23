import pytest
import sys
from pathlib import Path

# Add test_subjects to path so we can import calculator
sys.path.insert(0, str(Path(__file__).parent.parent / "test_subjects"))
import calculator


# Phase 5 – Parametrization: multiple arguments and ids


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (10, 0, 10),
    ],
)
def test_add_multiple_cases(a, b, expected):
    assert calculator.add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),
        (-1, 4, -4),
    ],
    ids=["positive-numbers", "negative-times-positive"],
)
def test_multiply_with_ids(a, b, expected):
    assert calculator.multiply(a, b) == expected



'''
Output from: pytest -v test_parametrize_multiple.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 5 items

test_parametrize_multiple.py::test_add_multiple_cases[2-3-5] PASSED
test_parametrize_multiple.py::test_add_multiple_cases[-1-1-0] PASSED
test_parametrize_multiple.py::test_add_multiple_cases[10-0-10] PASSED
test_parametrize_multiple.py::test_multiply_with_ids[positive-numbers] PASSED
test_parametrize_multiple.py::test_multiply_with_ids[negative-times-positive] PASSED

==================================================== 5 passed in 0.01s ====================================================
'''
