import pytest


# Phase 3  Fixtures: parametrized fixture (preview for Phase 5)


@pytest.fixture(params=[1, 2, 3])
def positive_number(request):
    """A parametrized fixture that provides multiple values.

    This single fixture will run the test three times: once for
    each value in params.
    """
    return request.param


def test_positive_number_is_always_positive(positive_number):
    assert positive_number > 0



'''
Output from: pytest -v test_parametrized_fixture.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 3 items

test_parametrized_fixture.py::test_positive_number_is_always_positive[1] PASSED
test_parametrized_fixture.py::test_positive_number_is_always_positive[2] PASSED
test_parametrized_fixture.py::test_positive_number_is_always_positive[3] PASSED

==================================================== 3 passed in 0.01s ====================================================
'''
