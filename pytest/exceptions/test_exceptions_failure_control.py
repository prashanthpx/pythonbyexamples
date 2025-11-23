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


'''
Output from: pytest -v test_exceptions_failure_control.py

=================================================== test session starts ====================================================
test_exceptions_failure_control.py::test_zero_division_with_raises PASSED
test_exceptions_failure_control.py::test_value_error_with_message_match PASSED
test_exceptions_failure_control.py::test_forced_failure_with_pytest_fail FAILED
test_exceptions_failure_control.py::test_expected_failure_xfail XFAIL (known bug that we expect to fail)
test_exceptions_failure_control.py::test_unexpected_pass_strict FAILED

========================================================= FAILURES =========================================================
___________________________________________ test_forced_failure_with_pytest_fail ___________________________________________

    def test_forced_failure_with_pytest_fail():
        """Force a failure explicitly with pytest.fail."""
>       pytest.fail("forcing a failure to demonstrate pytest.fail")
E       Failed: forcing a failure to demonstrate pytest.fail

_______________________________________________ test_unexpected_pass_strict ________________________________________________
[XPASS(strict)] bug is actually fixed but marker not updated

================================================= short test summary info ==================================================
FAILED test_exceptions_failure_control.py::test_forced_failure_with_pytest_fail - Failed: forcing a failure
FAILED test_exceptions_failure_control.py::test_unexpected_pass_strict - [XPASS(strict)] bug is actually fixed
========================================== 2 failed, 2 passed, 1 xfailed in 0.05s ==========================================
'''