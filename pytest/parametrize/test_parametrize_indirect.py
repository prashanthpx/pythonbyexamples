import pytest


# Phase 5  Parametrization: indirect parametrization via fixtures


@pytest.fixture
def number(request):
    return request.param * 10


@pytest.mark.parametrize(
    "number,expected",
    [
        (1, 10),
        (2, 20),
        (3, 30),
    ],
    indirect=["number"],
)
def test_indirect_parametrization(number, expected):
    assert number == expected



'''
Output from: pytest -v test_parametrize_indirect.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 3 items

test_parametrize_indirect.py::test_indirect_parametrization[1-10] PASSED
test_parametrize_indirect.py::test_indirect_parametrization[2-20] PASSED
test_parametrize_indirect.py::test_indirect_parametrization[3-30] PASSED

==================================================== 3 passed in 0.01s ====================================================
'''
