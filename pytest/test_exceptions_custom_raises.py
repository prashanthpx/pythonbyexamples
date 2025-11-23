import pytest


class MyCustomError(Exception):
    """Simple custom exception with an error code attribute."""

    def __init__(self, message: str, *, code: int) -> None:
        super().__init__(message)
        self.code = code


def divide_positive(number: int, divisor: int) -> float:
    """Divide only non-negative numbers and non-zero divisors.

    This function raises MyCustomError with different codes depending on what
    went wrong. We will test those exceptions with pytest.raises.
    """

    if divisor == 0:
        raise MyCustomError("divisor must not be zero", code=400)
    if number < 0:
        raise MyCustomError("number must be non-negative", code=401)
    return number / divisor


def test_custom_exception_type_and_attributes():
    """Use pytest.raises as a context manager and inspect the exception."""

    with pytest.raises(MyCustomError) as excinfo:
        divide_positive(-1, 2)

    err = excinfo.value
    assert isinstance(err, MyCustomError)
    assert "non-negative" in str(err)
    assert err.code == 401


output = """\n$ pytest -v test_exceptions_custom_raises.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ... \ncollected 1 item\n\ntest_exceptions_custom_raises.py::test_custom_exception_type_and_attributes PASSED                                   [100%]\n\n==================================================== 1 passed in 0.01s =====================================================\n"""
