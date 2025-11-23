import pytest
import calculator


# Phase 5 – Parametrization: combining fixtures with parametrize


@pytest.fixture
def base_number():
    return 10


@pytest.mark.parametrize(
    "delta,expected",
    [
        (1, 11),
        (-5, 5),
    ],
)
def test_add_with_base_and_delta(base_number, delta, expected):
    assert calculator.add(base_number, delta) == expected



'''
Output from: pytest -v test_parametrize_with_fixture.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_parametrize_with_fixture.py::test_add_with_base_and_delta[1-11] PASSED
test_parametrize_with_fixture.py::test_add_with_base_and_delta[-5-5] PASSED

==================================================== 2 passed in 0.01s ====================================================
'''
