import calculator


# Phase 2 – Testing a small calculator module


def test_add_numbers():
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0


def test_subtract_numbers():
    assert calculator.subtract(10, 3) == 7
    assert calculator.subtract(0, 5) == -5


def test_multiply_numbers():
    assert calculator.multiply(4, 5) == 20
    assert calculator.multiply(-2, 3) == -6


def test_divide_numbers():
    assert calculator.divide(10, 2) == 5
    assert calculator.divide(9, 3) == 3

def test_divide_floats_and_negatives():
    # Floats
    assert calculator.divide(7.5, 2.5) == 3.0
    # Negative numbers
    assert calculator.divide(-9, 3) == -3
    assert calculator.divide(9, -3) == -3
    assert calculator.divide(-9, -3) == 3


def test_add_with_zero_and_large_numbers():
    # Zero
    assert calculator.add(0, 5) == 5
    assert calculator.add(0, 0) == 0
    # Larger values
    assert calculator.add(1_000_000, 2_000_000) == 3_000_000


def test_multiply_by_zero_and_one():
    assert calculator.multiply(0, 10) == 0
    assert calculator.multiply(10, 0) == 0
    assert calculator.multiply(1, 99) == 99
    assert calculator.multiply(-1, 99) == -99



'''
Output from: pytest test_calculator.py -v

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ...
collected 7 items

test_calculator.py::test_add_numbers PASSED                                                                          [ 14%]
test_calculator.py::test_subtract_numbers PASSED                                                                     [ 28%]
test_calculator.py::test_multiply_numbers PASSED                                                                     [ 42%]
test_calculator.py::test_divide_numbers PASSED                                                                       [ 57%]
test_calculator.py::test_divide_floats_and_negatives PASSED                                                          [ 71%]
test_calculator.py::test_add_with_zero_and_large_numbers PASSED                                                      [ 85%]
test_calculator.py::test_multiply_by_zero_and_one PASSED                                                             [100%]

==================================================== 7 passed in 0.01s ====================================================
'''
