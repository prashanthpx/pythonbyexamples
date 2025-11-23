import string_utils


# Phase 2 – Testing a small string utilities module


def test_to_upper_and_lower():
    assert string_utils.to_upper("pytest") == "PYTEST"
    assert string_utils.to_lower("PyTeSt") == "pytest"


def test_contains_substring():
    text = "learning pytest is fun"
    assert string_utils.contains_substring(text, "pytest")
    assert string_utils.contains_substring(text, "learn")
    assert not string_utils.contains_substring(text, "django")


def test_is_palindrome_simple():
    assert string_utils.is_palindrome("madam")
    assert string_utils.is_palindrome("racecar")
    assert not string_utils.is_palindrome("python")


def test_is_palindrome_ignores_case_and_outer_spaces():
    assert string_utils.is_palindrome(" Madam ")  # spaces + case
    assert string_utils.is_palindrome("RaceCar")



'''
Output from: pytest test_string_utils.py -v

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ...
collected 4 items

test_string_utils.py::test_to_upper_and_lower PASSED                                                                 [ 25%]
test_string_utils.py::test_contains_substring PASSED                                                                 [ 50%]
test_string_utils.py::test_is_palindrome_simple PASSED                                                               [ 75%]
test_string_utils.py::test_is_palindrome_ignores_case_and_outer_spaces PASSED                                        [100%]

==================================================== 4 passed in 0.01s ====================================================
'''
