import pytest
import calculator


# Fixtures: reusing a calculator instance


@pytest.fixture
def calculator_values():
    """Common input values for calculator tests.

    This fixture returns a small dictionary so multiple tests can
    reuse the same numbers without repeating them.
    """
    return {
        "a": 10,
        "b": 5,
        "negative": -3,
        "zero": 0,
    }


def test_add_with_fixture(calculator_values):
    values = calculator_values
    assert calculator.add(values["a"], values["b"]) == 15
    assert calculator.add(values["negative"], values["b"]) == 2


def test_subtract_with_fixture(calculator_values):
    values = calculator_values
    assert calculator.subtract(values["a"], values["b"]) == 5
    assert calculator.subtract(values["b"], values["a"]) == -5


def test_multiply_with_fixture(calculator_values):
    values = calculator_values
    assert calculator.multiply(values["a"], values["zero"]) == 0
    assert calculator.multiply(values["negative"], values["b"]) == -15


# NOTE: A real teardown example using `yield` will be shown in a later
# fixture example or when we introduce resources that need cleanup.


'''
Output from: pytest -v test_calculator_fixtures.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 3 items

test_calculator_fixtures.py::test_add_with_fixture PASSED
test_calculator_fixtures.py::test_subtract_with_fixture PASSED
test_calculator_fixtures.py::test_multiply_with_fixture PASSED

==================================================== 3 passed in 0.01s ====================================================
'''
