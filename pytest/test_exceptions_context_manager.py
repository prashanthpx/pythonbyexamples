import pytest
from contextlib import contextmanager


class ResourceError(Exception):
    """Custom error used by the resource_manager context manager."""


@contextmanager
def resource_manager(should_fail: bool):
    """Simple context manager that may raise when entering the with-block.

    If should_fail is True, we raise ResourceError *before* yielding, so the
    body of the with-block is never executed.
    """

    # In a real program, this might open a file or network connection.
    # Here we just simulate a possible failure on enter.
    if should_fail:
        raise ResourceError("failed to open resource")

    try:
        yield "RESOURCE"
    finally:
        # In real code this is where you would close the resource.
        pass


def test_resource_manager_raises_on_enter():
    """The context manager itself raises before the body runs."""

    with pytest.raises(ResourceError, match="failed to open resource"):
        with resource_manager(should_fail=True):
            # This line is never reached because the error happens on enter.
            pytest.fail("body of with-block should not run")


def test_resource_manager_success_path():
    """Normal use: the context manager yields a value and does not raise."""

    with resource_manager(should_fail=False) as resource:
        assert resource == "RESOURCE"


output = """\n$ pytest -v test_exceptions_context_manager.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ...\ncollected 2 items\n\ntest_exceptions_context_manager.py::test_resource_manager_raises_on_enter PASSED                                     [ 50%]\ntest_exceptions_context_manager.py::test_resource_manager_success_path PASSED                                        [100%]\n\n==================================================== 2 passed in 0.01s =====================================================\n"""
