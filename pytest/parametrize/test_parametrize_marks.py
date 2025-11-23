import pytest
import sys
from pathlib import Path

# Add test_subjects to path so we can import calculator
sys.path.insert(0, str(Path(__file__).parent.parent / "test_subjects"))
import calculator


# Phase 5  Parametrization: row-level marks with pytest.param


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        pytest.param(
            2,
            2,
            5,
            marks=pytest.mark.xfail(reason="demonstrating xfail for a bad data row"),
        ),
    ],
)
def test_add_with_row_marks(a, b, expected):
    assert calculator.add(a, b) == expected



'''
Output from: pytest -v test_parametrize_marks.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_parametrize_marks.py::test_add_with_row_marks[2-3-5] PASSED
test_parametrize_marks.py::test_add_with_row_marks[2-2-5] XFAIL (demonstrating xfail for a bad data row)

=============================================== 1 passed, 1 xfailed in 0.03s ===============================================
'''
