import math


# Phase 1 – Basic assertions: numbers, strings, lists, booleans


def test_numbers_equal():
    """Basic numeric equality"""
    assert 2 + 3 == 5
    assert 10 - 4 == 6


def test_numbers_not_equal():
    """Numeric inequality"""
    assert 2 * 3 != 5
    assert 7 / 2 != 4  # 7/2 is 3.5


def test_number_comparisons():
    """Greater-than and less-than comparisons"""
    value = 10
    assert value > 5
    assert value >= 10
    assert value < 20


def test_string_equality_and_case():
    """String equality and case sensitivity"""
    text = "pytest"
    assert text == "pytest"
    # Case matters in equality
    assert text.upper() == "PYTEST"


def test_string_contains():
    """Substring membership in strings"""
    text = "learning pytest is fun"
    assert "pytest" in text
    assert "learn" in text  # substring of "learning"


def test_list_membership_and_length():
    """Basic list checks: membership and length"""
    numbers = [1, 2, 3, 4]
    assert 2 in numbers
    assert 5 not in numbers
    assert len(numbers) == 4


def test_multiple_asserts_in_one_test():
    """A single test can contain multiple asserts"""
    name = "python"
    assert name.startswith("py")
    assert name.endswith("on")
    assert len(name) == 6


def test_boolean_truthiness():
    """Truthiness of values in Python"""
    assert bool("non-empty")  # non-empty string is True
    assert not bool("")  # empty string is False
    assert bool([1])  # non-empty list is True
    assert not bool([])  # empty list is False


'''
Output from: pytest test_assertions_basic.py -v

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ...
collected 8 items

test_assertions_basic.py::test_numbers_equal PASSED                                                                  [ 12%]
test_assertions_basic.py::test_numbers_not_equal PASSED                                                              [ 25%]
test_assertions_basic.py::test_number_comparisons PASSED                                                             [ 37%]
test_assertions_basic.py::test_string_equality_and_case PASSED                                                       [ 50%]
test_assertions_basic.py::test_string_contains PASSED                                                                [ 62%]
test_assertions_basic.py::test_list_membership_and_length PASSED                                                     [ 75%]
test_assertions_basic.py::test_multiple_asserts_in_one_test PASSED                                                   [ 87%]
test_assertions_basic.py::test_boolean_truthiness PASSED                                                             [100%]

==================================================== 8 passed in 0.01s ====================================================
'''
