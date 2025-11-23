import pytest


# Phase 6 – Exceptions and failure control


def test_zero_division_with_raises():
    """Use pytest.raises to assert that an exception is raised."""
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_value_error_with_message_match():
    """Use match= to check part of the exception message."""
    with pytest.raises(ValueError, match="invalid literal for int"):
        int("not-an-int")


def test_forced_failure_with_pytest_fail():
    """Force a failure explicitly with pytest.fail."""
    pytest.fail("forcing a failure to demonstrate pytest.fail")


@pytest.mark.xfail(reason="known bug that we expect to fail")
def test_expected_failure_xfail():
    """This test is expected to fail and is reported as XFAIL, not FAILED."""
    assert 2 + 2 == 5


@pytest.mark.xfail(reason="bug is actually fixed but marker not updated", strict=True)
def test_unexpected_pass_strict():
    """This passes even though it is marked xfail(strict=True) -> XPASS(strict)."""
    assert 1 + 1 == 2



output = """\n$ pytest -v test_exceptions_failure_control.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ... \ncollected 5 items\n\ntest_exceptions_failure_control.py::test_zero_division_with_raises PASSED                                            [ 20%]\ntest_exceptions_failure_control.py::test_value_error_with_message_match PASSED                                       [ 40%]\ntest_exceptions_failure_control.py::test_forced_failure_with_pytest_fail FAILED                                      [ 60%]\ntest_exceptions_failure_control.py::test_expected_failure_xfail XFAIL (known bug that we expect to fail)             [ 80%]\ntest_exceptions_failure_control.py::test_unexpected_pass_strict FAILED                                               [100%]\n\n========================================================= FAILURES =========================================================\n___________________________________________ test_forced_failure_with_pytest_fail ___________________________________________\n\n    def test_forced_failure_with_pytest_fail():\n        """Force a failure explicitly with pytest.fail."""\n>       pytest.fail("forcing a failure to demonstrate pytest.fail")\nE       Failed: forcing a failure to demonstrate pytest.fail\n\n...\n\n_______________________________________________ test_unexpected_pass_strict ________________________________________________\n[XPASS(strict)] bug is actually fixed but marker not updated\n================================================= short test summary info ==================================================\nFAILED test_exceptions_failure_control.py::test_forced_failure_with_pytest_fail - Failed: forcing a failure to demonstrate pytest.fail\nFAILED test_exceptions_failure_control.py::test_unexpected_pass_strict - [XPASS(strict)] bug is actually fixed but marker not updated\n========================================== 2 failed, 2 passed, 1 xfailed in 0.05s ==========================================\n"""