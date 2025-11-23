import pytest

import calculator
import string_utils


# Phase 8 – Mocking with pytest-mock: the `mocker` fixture

# If pytest-mock (the plugin that provides the `mocker` fixture) is not
# installed, this entire module will be skipped instead of failing.
pytest.importorskip("pytest_mock")


def test_patch_calculator_add_with_mocker(mocker):
    """Patch calculator.add so we can control its behavior.

    - The real add(2, 3) would return 5.
    - We patch it so it returns 999 instead.
    - Then we assert the mock was called with the expected arguments.
    """

    mock_add = mocker.patch("calculator.add", return_value=999)

    result = calculator.add(2, 3)

    assert result == 999
    mock_add.assert_called_once_with(2, 3)


def test_spy_on_string_utils_to_upper(mocker):
    """Use mocker.spy to assert how a real function was called.

    Here we do *not* replace string_utils.to_upper; we just wrap it with a
    spy so we can make assertions about how many times it was called and
    with which arguments.
    """

    spy = mocker.spy(string_utils, "to_upper")

    result = string_utils.to_upper("pytest")

    assert result == "PYTEST"
    spy.assert_called_once_with("pytest")


class FakeCalculatorUser:
    """Example class that *uses* calculator.add.

    We will patch its method with mocker.patch.object in tests.
    """

    def compute_sum(self, a: int, b: int) -> int:
        return calculator.add(a, b)


def test_patch_object_method_on_instance(mocker):
    """Use mocker.patch.object to replace a method on an *instance*.

    We patch FakeCalculatorUser.compute_sum on a specific instance so that it
    returns a constant without calling the real calculator.add.
    """

    user = FakeCalculatorUser()

    mock_method = mocker.patch.object(user, "compute_sum", return_value=42)

    result = user.compute_sum(10, 20)

    assert result == 42
    mock_method.assert_called_once_with(10, 20)



def test_patch_object_method_on_class(mocker):
    """Use mocker.patch.object to replace a method on the *class*.

    Here we patch FakeCalculatorUser.compute_sum on the class, so *all* new
    instances see the patched method.
    """

    mock_method = mocker.patch.object(FakeCalculatorUser, "compute_sum", return_value=100)

    user_one = FakeCalculatorUser()
    user_two = FakeCalculatorUser()

    assert user_one.compute_sum(1, 2) == 100
    assert user_two.compute_sum(10, 20) == 100

    mock_method.assert_has_calls([
        mocker.call(user_one, 1, 2),
        mocker.call(user_two, 10, 20),
    ])


output = """\n$ pytest -vs test_mock_mocker.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ... collected 0 items / 1 skipped\n\n==================================================== 1 skipped in 0.01s ====================================================\n"""