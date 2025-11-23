# Pytest Learning Notes

This document is a **living guide** to the pytest examples in this `practice/pytest` folder. We will:

- Understand the tests you already wrote
- Learn pytest concepts step by step (beginner → intermediate → advanced)
- Add new example tests as you learn (this guide grows with you)

---

## 1. Getting Started with Pytest

### 1.1. How pytest finds and runs tests

Pytest automatically discovers tests using **naming conventions**:

- Files named like `test_*.py` or `*_test.py` (e.g. `test_eg.py`)
- Functions inside those files whose names start with `test_` (e.g. `testLogin`)

To run tests from this folder, from inside `practice/pytest` you can run:

```bash
pytest
```

Pytest will collect all test functions from all matching files and run them.

### 1.2. Useful pytest command-line options

All of these commands are meant to be run **inside** the `practice/pytest` folder.

1. **`pytest`**

   ```bash
   pytest
   ```

   - Runs all discovered tests.
   - Shows a short, minimal output (just dots, F for fail, etc.).

2. **`pytest -v` (verbose)**

   ```bash
   pytest -v
   ```

   - `-v` = **verbose** mode.
   - Shows one line per test function, including the test name, e.g.:
     - `test_eg.py::testLogin PASSED`
     - `test_assertions_basic.py::test_numbers_equal PASSED`
   - Very useful when you want to see **exactly which tests ran**.

3. **`pytest -v -s` (verbose + show print output)**

   ```bash
   pytest -v -s
   ```

   - `-s` tells pytest to **show output** from `print()` and other standard output.
   - Combine with `-v` to both:
     - See each test name, and
     - See the printed messages from tests (like `"Login successful"`).
   - This is especially helpful when you are first learning and want to see your `print` statements.

4. **Run only a specific file**

   ```bash
   pytest test_eg.py
   ```

   - Runs only tests from `test_eg.py`.

   With options:

   ```bash
   pytest -v test_eg.py
   pytest -v -s test_eg.py
   ```

   - Same as above, but verbose and/or showing print output just for that file.

### 1.3. Pytest command cheat sheet

Use this as a quick reference when you forget the exact command:

```bash
# Run all tests in this folder and subfolders
pytest

# Run all tests with verbose output
pytest -v

# Run all tests, verbose, and show print() output
pytest -v -s

# Run tests from a single file
pytest test_eg.py

# Run tests from a single file, verbose, and show print() output
pytest -v -s test_eg.py

# (Bonus) Run only tests whose names contain "login"
pytest -k "login" -v
```

- `-k "login"` runs only tests whose names **contain** the substring `login`.
- You can change `"login"` to any other substring to filter the tests you’re interested in.

---

## 2. Your First Test Files: `test_eg.py` and `test_group.py`

Current contents:

```python
def testLogin():
    print("Login successful")


def testLogoff():
    print("Logged out successfully")


def testCalcs():
    # if 2+2 is 4, assertion will return true and pass
    assert 2 + 2 == 4


def testAssertfail():
    assert 2 + 2 == 5
```

Let’s break down what each test demonstrates.

### 2.1. `testLogin` and `testLogoff`

These tests just **print messages**:

- `testLogin` prints `"Login successful"`
- `testLogoff` prints `"Logged out successfully"`

Because there are **no assertions**, pytest considers these tests **passed** as long as they don’t raise any exceptions.

> In real-world tests, you usually assert something about the behavior (e.g. return values, state changes) instead of only printing.

### 2.2. `testCalcs` – a passing assertion

```python
def testCalcs():
    assert 2 + 2 == 4
```

- `assert` is Python’s built-in assertion statement.
- If the condition is `True`, the test **passes**.
- If the condition is `False`, pytest marks the test as **failed**.

Here, `2 + 2 == 4` is `True`, so the test passes.

### 2.3. Intentional failing tests – `testAssertfail`

```python
def testAssertfail():
    assert 2 + 2 == 5
```

You have **intentional failing tests** in both `test_eg.py` and `test_group.py`:

```python
# in test_eg.py
def testAssertfail():
    assert 2 + 2 == 5

# in test_group.py
@pytest.mark.assertion
def testAssertfail():
    assert 2 * 3 == 9
```

What these show:

- `2 + 2 == 5` is `False`, and `2 * 3 == 9` is also `False`, so the assertions fail.
- Pytest reports these tests as **FAILED** and shows an `AssertionError`.
- You can see in the output:
  - Which test failed (`testAssertfail`)
  - Which file it was in (`test_eg.py` or `test_group.py`)
  - The exact expression that was false (`(2 + 2) == 5` or `(2 * 3) == 9`).

These tests are **kept on purpose** so that when you run `pytest` you can
see how pytest displays failures.

You already captured a sample output in the file comment showing:

- `4 items` collected
- `3 passed, 1 failed`


Example: running only `test_eg.py` in verbose mode:

```bash
pytest -v test_eg.py
```

Expected output (abbreviated):

```text
test_eg.py::testLogin PASSED
test_eg.py::testLogoff PASSED
test_eg.py::testCalcs PASSED
test_eg.py::testAssertfail FAILED
```

---

## 3. Testing real code: calculator and string utilities

In Section 2 you wrote your very first tests using plain `assert` on numbers
and simple functions.

The next step in the fundamentals is to point tests at **real Python code in
modules** instead of only literals. We keep the code tiny so you can focus
on pytest itself, not business logic.

We created two new files in `practice/pytest`:

- `calculator.py` – the code under test
- `test_calculator.py` – the pytest tests for that code

#### 2.1. The `calculator` module (`calculator.py`)

```python
"""Simple calculator module for pytest learning examples."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    """Divide a by b."""
    return a / b
```

Key points:

- Each operation is a **separate function** (`add`, `subtract`, `multiply`, `divide`).
- The functions are intentionally simple so tests are easy to reason about.

#### 2.2. Tests for the calculator (`test_calculator.py`)

```python
import calculator


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
```

What this shows:

- You **import** the module under test: `import calculator`.
- Each test calls one function (`add`, `subtract`, etc.) with sample inputs and asserts on the result.
- Each test checks **more than one case** (e.g. positive/negative, zero).

To run only the calculator tests from inside `practice/pytest`:

```bash
pytest test_calculator.py -v
```

#### 2.3. String utilities module (`string_utils.py`) and tests (`test_string_utils.py`)

We also created a small **string utilities** module and matching tests.

```python
# string_utils.py

def to_upper(text: str) -> str:
    return text.upper()


def to_lower(text: str) -> str:
    return text.lower()


def contains_substring(text: str, substring: str) -> bool:
    return substring in text


def is_palindrome(text: str) -> bool:
    normalized = text.strip().lower()
    return normalized == normalized[::-1]
```

The tests live in `test_string_utils.py`:

```python
import string_utils


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
    assert string_utils.is_palindrome(" Madam ")
    assert string_utils.is_palindrome("RaceCar")
```

To run only these tests from inside `practice/pytest`:

```bash
pytest test_string_utils.py -v
```

You should see output like:

```text
test_string_utils.py::test_to_upper_and_lower PASSED
test_string_utils.py::test_contains_substring PASSED
test_string_utils.py::test_is_palindrome_simple PASSED
test_string_utils.py::test_is_palindrome_ignores_case_and_outer_spaces PASSED

==================================================== 4 passed in 0.01s ====================================================
```


You should see output like:

```text
test_calculator.py::test_add_numbers PASSED
test_calculator.py::test_subtract_numbers PASSED
test_calculator.py::test_multiply_numbers PASSED
test_calculator.py::test_divide_numbers PASSED
test_calculator.py::test_divide_floats_and_negatives PASSED
test_calculator.py::test_add_with_zero_and_large_numbers PASSED
test_calculator.py::test_multiply_by_zero_and_one PASSED

==================================================== 7 passed in 0.01s ====================================================
```

This pattern—**small, focused module + matching `test_*.py` file**—is very common in real projects.

## 4. Fixtures: sharing setup and teardown

So far each test has created its own data inline. As your test suite grows,
that becomes repetitive and harder to change.

Pytest fixtures solve this by letting you **declare reusable setup/teardown
functions** that tests can depend on.

In this section we will:

- Use `@pytest.fixture` to create reusable test data.
- See how fixtures run **before and after** each test.
- Share fixtures across multiple files with `conftest.py`.
- Briefly mention fixture scope (function vs module, etc.).

We will use the existing files in `practice/pytest`.

## 5. Markers and selecting which tests to run

Once you have more tests, you rarely run **all** of them all the time.
Markers let you label tests (slow, api, smoke, etc.) and then select or
skip them from the command line.

In this section we will:

- Use custom markers like `@pytest.mark.slow` and `@pytest.mark.api`.
- Use built-in markers like `@pytest.mark.skip`, `@pytest.mark.skipif`,
  `@pytest.mark.xfail`.
- Select tests with `pytest -m "marker"` and `pytest -k "substring"`.
- See how module-level `pytestmark` works.
- Mention how to register custom markers in `pytest.ini`.

## 6. Parametrization overview

Parametrization lets you cover many input/output cases with fewer tests by
passing a table of values into one test function.

This section is a short **concept overview**. The detailed, runnable examples
are in the next section.

- `@pytest.mark.parametrize` with one parameter.
- Multiple parameters in one test.
- Using `ids=` for readable parameter names.
- Combining parametrization with fixtures.

## 7. Parametrization in practice

### 7.1. Single-parameter tests with `@pytest.mark.parametrize` (`test_parametrize_basic.py`)

The simplest form of parametrization is a **single parameter** with a list of
values. We created `test_parametrize_basic.py`:

```python
import pytest


# Parametrization: single-parameter example


@pytest.mark.parametrize("number", [1, 2, 5, 10])
def test_positive_numbers_are_positive(number):
    assert number > 0
```

Key ideas:

- `@pytest.mark.parametrize("number", [1, 2, 5, 10])` tells pytest to run the
test **once for each value** in the list.
- The generated test names look like:
  - `test_positive_numbers_are_positive[1]`
  - `test_positive_numbers_are_positive[2]`
  - etc.

Run this file with:

```bash
pytest -v test_parametrize_basic.py
```

Example output:

```text
test_parametrize_basic.py::test_positive_numbers_are_positive[1] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[2] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[5] PASSED
test_parametrize_basic.py::test_positive_numbers_are_positive[10] PASSED

==================================================== 4 passed in 0.01s ====================================================
```

The full pytest output is stored at the bottom of
`test_parametrize_basic.py`.

---

### 7.2. Multiple parameters and `ids` (`test_parametrize_multiple.py`)

You can parametrize **multiple arguments** at once by passing a comma-separated
string of parameter names and a list of tuples for the values.

We created `test_parametrize_multiple.py`:

```python
import pytest
import calculator


# Parametrization: multiple arguments and ids


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        (-1, 1, 0),
        (10, 0, 10),
    ],
)
def test_add_multiple_cases(a, b, expected):
    assert calculator.add(a, b) == expected
```

Key ideas:

- The parameter string `"a,b,expected"` maps to each tuple in the list.
- This single test function is run **three times**, once per tuple.

You can add human-friendly IDs using the `ids=` argument. In the same file:

```python
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 6),
        (-1, 4, -4),
    ],
    ids=["positive-numbers", "negative-times-positive"],
)
def test_multiply_with_ids(a, b, expected):
    assert calculator.multiply(a, b) == expected
```

Now the parametrized test names will look like:

- `test_multiply_with_ids[positive-numbers]`
- `test_multiply_with_ids[negative-times-positive]`

Run this file with:

```bash
pytest -v test_parametrize_multiple.py
```

Example output:

```text
test_parametrize_multiple.py::test_add_multiple_cases[2-3-5] PASSED
test_parametrize_multiple.py::test_add_multiple_cases[-1-1-0] PASSED
test_parametrize_multiple.py::test_add_multiple_cases[10-0-10] PASSED
test_parametrize_multiple.py::test_multiply_with_ids[positive-numbers] PASSED
test_parametrize_multiple.py::test_multiply_with_ids[negative-times-positive] PASSED

==================================================== 5 passed in 0.01s ====================================================
```

The full pytest output is stored at the bottom of
`test_parametrize_multiple.py`.

---

### 7.3. Combining parametrization with fixtures (`test_parametrize_with_fixture.py`)

You can freely combine **fixtures** and `@pytest.mark.parametrize` in the same
 test. Fixtures still provide their values, while parametrization provides
additional parameters.

We created `test_parametrize_with_fixture.py`:

```python
import pytest
import calculator


# Parametrization: combining fixtures with parametrize


@pytest.fixture
def base_number():
    return 10


@pytest.mark.parametrize(
    "delta,expected",
    [
        (1, 11),
        (-5, 5),
    ],
)
def test_add_with_base_and_delta(base_number, delta, expected):
    assert calculator.add(base_number, delta) == expected
```

Key ideas:

- `base_number` is a normal fixture that always returns `10`.
- `@pytest.mark.parametrize("delta,expected", [...])` provides the extra
  parameters.
- pytest runs the test **once per (delta, expected) pair**, and each time it
  also resolves `base_number` via the fixture.

Run this file with:

```bash
pytest -v test_parametrize_with_fixture.py
```

Example output:

```text
test_parametrize_with_fixture.py::test_add_with_base_and_delta[1-11] PASSED
test_parametrize_with_fixture.py::test_add_with_base_and_delta[-5-5] PASSED

==================================================== 2 passed in 0.01s ====================================================
```

The full pytest output is stored at the bottom of
`test_parametrize_with_fixture.py`.

---

### 7.4. Row-level marks with `pytest.param` (`test_parametrize_marks.py`)

Sometimes you want **one row** in a parametrized set to be marked differently
(for example, `xfail` or `skip`). You can do this with `pytest.param`.

We created `test_parametrize_marks.py`:

```python
import pytest
import calculator


# Parametrization: row-level marks with pytest.param


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (2, 3, 5),
        pytest.param(
            2,
            2,
            5,
            marks=pytest.mark.xfail(reason="demonstrating xfail for a bad data row"),
        ),
    ],
)
def test_add_with_row_marks(a, b, expected):
    assert calculator.add(a, b) == expected
```

Key ideas:

- The first row `(2, 3, 5)` is a normal passing case.
- The second row is wrapped with `pytest.param(..., marks=...)` and marked as
  `xfail`.
- We deliberately make that row "wrong" (2 + 2 != 5), but pytest does **not**
  count it as a failure because we have declared it as an expected failure.

Run this file with:

```bash
pytest -v test_parametrize_marks.py
```

Example output:

```text
test_parametrize_marks.py::test_add_with_row_marks[2-3-5] PASSED
test_parametrize_marks.py::test_add_with_row_marks[2-2-5] XFAIL (demonstrating xfail for a bad data row)

=============================================== 1 passed, 1 xfailed in 0.03s ===============================================
```

The full pytest output is stored at the bottom of
`test_parametrize_marks.py`.

---

### 7.5. Indirect parametrization with fixtures (`test_parametrize_indirect.py`)

With **indirect parametrization**, you parametrize a _fixture_ instead of a
plain argument. The values in `parametrize` are fed into the fixture via
`request.param`.

We created `test_parametrize_indirect.py`:

```python
import pytest


# Parametrization: indirect parametrization via fixtures


@pytest.fixture
def number(request):
    return request.param * 10


@pytest.mark.parametrize(
    "number,expected",
    [
        (1, 10),
        (2, 20),
        (3, 30),
    ],
    indirect=["number"],
)
def test_indirect_parametrization(number, expected):
    assert number == expected
```

Key ideas:

- The test function takes `number` and `expected`.
- Because `indirect=["number"]`, pytest **does not** pass the raw `number`
  value 1/2/3 into the test. Instead, it passes it into the `number` fixture as
  `request.param`.
- The fixture multiplies that by 10, so the test sees values 10, 20, 30.

Run this file with:

```bash
pytest -v test_parametrize_indirect.py
```

Example output:

```text
test_parametrize_indirect.py::test_indirect_parametrization[1-10] PASSED
test_parametrize_indirect.py::test_indirect_parametrization[2-20] PASSED
test_parametrize_indirect.py::test_indirect_parametrization[3-30] PASSED

==================================================== 3 passed in 0.01s ====================================================
```

The full pytest output is stored at the bottom of
`test_parametrize_indirect.py`.

---



## 9. Exceptions and failure control

In this section you learn how to **test for exceptions** and how to control different
failure types, including expected failures.

We will:
- Use `with pytest.raises(...)` (with and without `match=`) to assert that exceptions are raised.
- Force failures explicitly with `pytest.fail(...)`.
- Use `@pytest.mark.xfail(..., strict=...)` to control how expected failures and unexpected passes are reported.
- Compare how FAILED / XFAIL / XPASS / XPASS(strict) look in real pytest output.

---

#### 6.1. Using `pytest.raises` to test exceptions (`test_exceptions_failure_control.py`)

We created `test_exceptions_failure_control.py` for this section. The first two tests
use `pytest.raises` to assert that specific exceptions are raised.

```python
import pytest


def test_zero_division_with_raises():
    """Use pytest.raises to assert that an exception is raised."""
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_value_error_with_message_match():
    """Use match= to check part of the exception message."""
    with pytest.raises(ValueError, match="invalid literal for int"):
        int("not-an-int")
```

Key ideas:

- `with pytest.raises(SomeError):` asserts that `SomeError` (or a subclass) is raised
  somewhere inside the `with` block.
- If the code does **not** raise that exception, the test **fails**.
- The optional `match="..."` argument lets you check part of the error message.

Run just this file with:

```bash
pytest -v test_exceptions_failure_control.py
```

In the full output (shown at the bottom of `test_exceptions_failure_control.py`)
these two tests show up as **PASSED**.

---

#### 6.2. Forcing failures with `pytest.fail` and xfail vs strict xfail

The same file also demonstrates forcing a failure and the difference between
normal xfail and `strict=True` xfail:

```python
import pytest


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
```

When you run:

```bash
pytest -v test_exceptions_failure_control.py
```

You should see output similar to:

```text
test_exceptions_failure_control.py::test_zero_division_with_raises PASSED
test_exceptions_failure_control.py::test_value_error_with_message_match PASSED
test_exceptions_failure_control.py::test_forced_failure_with_pytest_fail FAILED
test_exceptions_failure_control.py::test_expected_failure_xfail XFAIL (known bug that we expect to fail)
test_exceptions_failure_control.py::test_unexpected_pass_strict FAILED

========================================================= FAILURES =========================================================
___________________________________________ test_forced_failure_with_pytest_fail ___________________________________________
...
_______________________________________________ test_unexpected_pass_strict ________________________________________________
[XPASS(strict)] bug is actually fixed but marker not updated
================================================= short test summary info ==================================================
FAILED test_exceptions_failure_control.py::test_forced_failure_with_pytest_fail - Failed: forcing a failure to demonstrate pytest.fail
FAILED test_exceptions_failure_control.py::test_unexpected_pass_strict - [XPASS(strict)] bug is actually fixed but marker not updated
========================================== 2 failed, 2 passed, 1 xfailed in 0.05s ==========================================
```

What this shows:

- `pytest.fail("message")` **always fails** the test immediately with the given
  message, regardless of assertions.
- A plain `@pytest.mark.xfail` test that really fails is reported as **XFAIL**, not
  FAILED. It does **not** make the whole test run red.
- A test marked with `@pytest.mark.xfail(strict=True)` **must fail**. If it passes,
  pytest reports it as **XPASS(strict)** and treats it as a **failure** in the
  overall test summary. This is useful when you want “unexpected passes” to break
  the build so you remember to update or remove the xfail marker.

The full pytest output is stored in the `output = """..."""` block at the bottom of
`test_exceptions_failure_control.py`.

---

#### 6.3. Testing custom exceptions with `pytest.raises` (`test_exceptions_custom_raises.py`)

Sometimes your code defines its **own exception types** with extra attributes.
You can still use `pytest.raises` and then **inspect the captured exception**.

We created `test_exceptions_custom_raises.py`:

```python
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
```

A test that checks both the **type** and the **attributes** of the exception:

```python
def test_custom_exception_type_and_attributes():
    with pytest.raises(MyCustomError) as excinfo:
        divide_positive(-1, 2)

    err = excinfo.value
    assert isinstance(err, MyCustomError)
    assert "non-negative" in str(err)
    assert err.code == 401
```

Key ideas:

- `with pytest.raises(MyCustomError) as excinfo:` lets you **capture** the
  exception object in `excinfo`.
- `excinfo.value` is the actual exception instance that was raised.
- You can make normal assertions on that object (type, attributes, message,…).

Run this file with:

```bash
pytest -v test_exceptions_custom_raises.py
```

You should see:

```text
test_exceptions_custom_raises.py::test_custom_exception_type_and_attributes PASSED                                   [100%]

==================================================== 1 passed in 0.01s =====================================================
```

The full output is stored at the bottom of
`test_exceptions_custom_raises.py` in the `output = """..."""` block.

---

#### 6.4. Context managers that raise on enter (`test_exceptions_context_manager.py`)

Sometimes the code that **opens a resource** (file, connection, etc.) is
written as a context manager and may raise an exception *before* your
with‑block body runs.

We created `test_exceptions_context_manager.py` to show how `pytest.raises`
handles this.

```python
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

    if should_fail:
        raise ResourceError("failed to open resource")

    try:
        yield "RESOURCE"
    finally:
        # In real code this is where you would close the resource.
        pass
```

The failing path (error on enter) is tested like this:

```python
def test_resource_manager_raises_on_enter():
    """The context manager itself raises before the body runs."""

    with pytest.raises(ResourceError, match="failed to open resource"):
        with resource_manager(should_fail=True):
            # This line is never reached because the error happens on enter.
            pytest.fail("body of with-block should not run")
```

And the success path looks like a normal context‑manager use:

```python
def test_resource_manager_success_path():
    """Normal use: the context manager yields a value and does not raise."""

    with resource_manager(should_fail=False) as resource:
        assert resource == "RESOURCE"
```

Key ideas:

- `pytest.raises` does **not care** whether the exception comes from inside the
  with‑block body or from the context manager’s `__enter__` logic: as long as
  it is raised while evaluating the with‑statement, it is caught.
- You can still use `match="..."` to check the error message.
- It’s good practice to also have a **success-path** test, so you see the
  context manager working when no error is raised.

Run this file with:

```bash
pytest -v test_exceptions_context_manager.py
```

You should see:

```text
test_exceptions_context_manager.py::test_resource_manager_raises_on_enter PASSED                                     [ 50%]
test_exceptions_context_manager.py::test_resource_manager_success_path PASSED                                        [100%]

==================================================== 2 passed in 0.01s =====================================================
```

The full output is stored at the bottom of
`test_exceptions_context_manager.py` in the `output = """..."""` block.

---

## 10. Shared fixtures and `conftest.py`

Fixtures often need to be reused **across many files**. Pytest's special
`conftest.py` files let you define fixtures once and share them with all tests
in a directory tree.

In this section we will:
- See how pytest automatically discovers `conftest.py` files.
- Move common fixtures into `conftest.py` so they are visible to many tests.
- Demonstrate how multiple test modules can share the same fixtures.
- Understand how **nested `conftest.py` files** interact with top-level ones.
- Use **autouse fixtures** in both a single module and a nested package.

---

#### 7.1. A shared UI-style setup fixture in `conftest.py` (`test_fixture.py`)

First, we put some **common setup logic** into `conftest.py` in the
`practice/pytest` directory:

```python
# conftest.py (in practice/pytest)
import pytest


@pytest.fixture
def setup():
    print("calling setup...")
    print("launch browser")
    print("login")
    print("Browse product")
    yield
    print("\n logoff application")
    print("close browser")
```

Any test file under the same directory tree can now use `setup` **without
importing it** explicitly. For example, `test_fixture.py`:

```python
# test_fixture.py
import pytest


# pass fixture as an argument to the method
def testAdditemtocart(setup):
    print("item added")


def testRemoveitem(setup):
    print("item removed")
```

Run this file with:

```bash
pytest -vs test_fixture.py
```

You should see (abbreviated):

```text
test_fixture.py::testAdditemtocart calling setup...
launch browser
login
Browse product
item added
PASSED
 logoff application
close browser

test_fixture.py::testRemoveitem calling setup...
launch browser
login
Browse product
item removed
PASSED
 logoff application
close browser
```

The important points:

- You **never import** `setup` – pytest discovers it automatically from
  `conftest.py` based on the directory structure.
- Both tests in `test_fixture.py` share the same fixture definition.
- The fixture runs once per test (function scope), handling both setup and
  teardown around each test.

The full output of the run is embedded at the bottom of `test_fixture.py` in
its triple-quoted comment block.

---

#### 7.2. Sharing multiple fixtures across modules (`test_conftest_shared_fixtures.py`)

The same `conftest.py` also defines another fixture, `shutdown`:

```python
# conftest.py (continuing)


@pytest.fixture
def shutdown():
    print("calling shutdown...")
    print("logoff application")
    yield
    print("\n shudown system")
```

Now we create a **separate test module** that uses both `setup` and `shutdown`
without importing them explicitly:

```python
# test_conftest_shared_fixtures.py
import pytest


def test_add_item_uses_setup_fixture(setup):
    """Uses the shared `setup` fixture defined in conftest.py."""

    print("adding item in second module")


def test_shutdown_fixture(shutdown):
    """Uses the shared `shutdown` fixture defined in conftest.py."""

    print("running shutdown-only test")
```

Run only this file with:

```bash
pytest -vs test_conftest_shared_fixtures.py
```

You should see output like:

```text
test_conftest_shared_fixtures.py::test_add_item_uses_setup_fixture calling setup...
launch browser
login
Browse product
adding item in second module
PASSED
 logoff application
close browser

test_conftest_shared_fixtures.py::test_shutdown_fixture calling shutdown...
logoff application
running shutdown-only test
PASSED
 shudown system

==================================================== 2 passed in 0.01s =====================================================
```

Key ideas:

- `conftest.py` is **not imported**; pytest finds it by walking up the
  directory tree from each test file.
- All tests under `practice/pytest` can see the fixtures defined in the
  top-level `conftest.py` there.
- You can keep your fixtures **close to where they are used** while still
  sharing them across multiple modules.

The exact output of the run is embedded at the bottom of
#### 7.3. Nested `conftest.py` and autouse fixtures in a subpackage (`nested_conftest_pkg/`)

To see how a **nested `conftest.py`** can add behavior only for a subpackage,
we created a small package directory: `nested_conftest_pkg/`.

Inside it, we have another `conftest.py` with an **autouse fixture**:

```python
# nested_conftest_pkg/conftest.py
import pytest


log = []


@pytest.fixture(autouse=True)
def ui_autouse():
    """Autouse fixture that runs for every test in this package.

    We use it to show how a nested conftest.py can add behavior that only
    applies to tests in this subpackage.
    """
    print("nested_conftest_pkg: ui_autouse setup")
    log.append("ui-autouse-setup")
    yield
    log.append("ui-autouse-teardown")
    print("nested_conftest_pkg: ui_autouse teardown")


@pytest.fixture
def ui_page():
    """Simple fixture local to this package."""
    print("nested_conftest_pkg: creating ui_page")
    return "UI-PAGE"
```

Two tests in the same package use these fixtures. The first one also uses the
**top-level** `setup` fixture from `practice/pytest/conftest.py`:

```python
# nested_conftest_pkg/test_nested_conftest_one.py
import pytest
import nested_conftest_pkg.conftest as nested_shared


def test_uses_top_level_setup_and_nested_autouse(setup, ui_page):
    """Uses top-level `setup` plus the nested autouse fixture.

    - `setup` comes from the top-level practice/pytest/conftest.py.
    - `ui_autouse` comes from nested_conftest_pkg/conftest.py and runs
      automatically for every test in this package.
    """
    print("inside nested_conftest_pkg test one")

    assert ui_page == "UI-PAGE"
    # First test: ui_autouse has run exactly once so far.
    assert nested_shared.log.count("ui-autouse-setup") == 1
```

The second test shows that `ui_autouse` runs even if we **don’t** list it as a
parameter:

```python
# nested_conftest_pkg/test_nested_conftest_two.py
import nested_conftest_pkg.conftest as nested_shared


def test_autouse_runs_without_being_listed():
    """Autouse fixture runs even if we don't list it as a parameter.

    This test does not mention `ui_autouse` or `ui_page`, but the
    autouse fixture still runs around the test body.
    """
    print("inside nested_conftest_pkg test two")

    # After two tests, the autouse fixture has run twice.
    assert nested_shared.log.count("ui-autouse-setup") == 2
```

Run just this package from `practice/pytest` with:

```bash
pytest -vs nested_conftest_pkg
```

You should see output like:

```text
nested_conftest_pkg/test_nested_conftest_one.py::test_uses_top_level_setup_and_nested_autouse nested_conftest_pkg: ui_autouse setup
calling setup...
launch browser
login
Browse product
nested_conftest_pkg: creating ui_page
inside nested_conftest_pkg test one
PASSED
 logoff application
close browser
nested_conftest_pkg: ui_autouse teardown

nested_conftest_pkg/test_nested_conftest_two.py::test_autouse_runs_without_being_listed nested_conftest_pkg: ui_autouse setup
inside nested_conftest_pkg test two
PASSEDnested_conftest_pkg: ui_autouse teardown

==================================================== 2 passed in 0.01s =====================================================
```

Key ideas:

- The **top-level** `conftest.py` and the **nested** one both apply: tests in
  `nested_conftest_pkg/` see fixtures from *both* files.
- `autouse=True` in the nested `conftest.py` makes `ui_autouse` run for **every
  test** in that package, even when the test does not list the fixture name.
- Keeping a small `log` list in the nested `conftest.py` makes it easy to
  assert how many times the autouse fixture ran.

The full `pytest -vs nested_conftest_pkg` output is embedded at the bottom of
`nested_conftest_pkg/test_nested_conftest_two.py` in the
`output = """..."""` block.

---

`test_conftest_shared_fixtures.py` in the `output = """..."""` block.

---

## 11. Mocking with pytest: monkeypatch and mocker

Sometimes you want to test code that talks to **external systems** (random
number generators, environment variables, HTTP services, databases, etc.)
without actually calling those systems.

In this section we will:
- Use pytest's built-in **`monkeypatch`** fixture to patch functions and
environment variables.
- Use the `pytest-mock` plugin's **`mocker`** fixture to patch and spy on
functions and methods.
- Assert that dependencies were called with the expected arguments.

#### 8.1. Deterministic tests with the built-in `monkeypatch` fixture (`test_mock_monkeypatch.py`)

Before using external plugins, Python already gives you powerful tools for mocking:
pytest's built-in **`monkeypatch`** fixture.

We will use it to:

- Patch **functions in other modules** so they return controlled values.
- Set **environment variables** in a reversible way.

First, a tiny module-level function that uses randomness and environment
variables:

```python
# test_mock_monkeypatch.py
import os
import random

import pytest


# Mocking: built-in monkeypatch fixture


def roll_two_dice() -> int:
    """Use random.randint to simulate rolling two dice.

    This function is intentionally non-deterministic so we can see
    how monkeypatch makes tests predictable.
    """
    return random.randint(1, 6) + random.randint(1, 6)


def get_db_url() -> str:
    """Read a DB URL from the environment with a safe default."""
    return os.getenv("DB_URL", "sqlite:///:memory:")
```

Now a test that patches `random.randint` using `monkeypatch.setattr`:

```python
# test_mock_monkeypatch.py

def test_roll_two_dice_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch random.randint so the test is fully deterministic.

    We replace random.randint with a fake that always returns 3,
    so rolling two dice always gives 6.
    """

    calls: list[tuple[int, int]] = []

    def fake_randint(a: int, b: int) -> int:
        calls.append((a, b))
        return 3

    monkeypatch.setattr("random.randint", fake_randint)

    total = roll_two_dice()

    assert total == 6
    assert calls == [(1, 6), (1, 6)]
```

And a test that uses `monkeypatch.setenv` to control environment variables:

```python
# test_mock_monkeypatch.py

def test_get_db_url_with_setenv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use monkeypatch.setenv to control environment variables."""

    monkeypatch.setenv("DB_URL", "postgresql://user@localhost/db")

    assert get_db_url() == "postgresql://user@localhost/db"
```

Run this file from `practice/pytest` with:

```bash
pytest -vs test_mock_monkeypatch.py
```

You should see output like:

```text
test_mock_monkeypatch.py::test_roll_two_dice_with_monkeypatch PASSED
test_mock_monkeypatch.py::test_get_db_url_with_setenv PASSED

==================================================== 2 passed in 0.01s =====================================================
```

The full output of the run is embedded at the bottom of
`test_mock_monkeypatch.py` in the `output = """..."""` block.

---

#### 8.2. Using `pytest-mock`'s `mocker` fixture for patching and spying (`test_mock_mocker.py`)

`pytest-mock` is a popular plugin that adds a **`mocker` fixture** on top of the
standard library's `unittest.mock`.

If `pytest-mock` is not installed, we skip the whole module:

```python
# test_mock_mocker.py
import pytest

import calculator
import string_utils


# Mocking with pytest-mock: the `mocker` fixture

# If pytest-mock (the plugin that provides the `mocker` fixture) is not
# installed, this entire module will be skipped instead of failing.
pytest.importorskip("pytest_mock")
```

A first example: patch `calculator.add` to return a fake value and then assert
how it was called:

```python
# test_mock_mocker.py

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
```

Here `mocker.patch("calculator.add", ...)`:

- Replaces `calculator.add` with a `Mock` object that returns `999`.
- Keeps track of how it was called so we can assert on the call.

A second example uses `mocker.spy` to **observe** a real function without
replacing it:

```python
# test_mock_mocker.py

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
```

Here `mocker.patch("calculator.add", ...)` is patching a *function* by dotted
path. Sometimes you want to patch a **method on a specific object** instead.
That is what `mocker.patch.object` is for.

A small helper class that uses `calculator.add`:

```python
# test_mock_mocker.py

class FakeCalculatorUser:
    """Example class that *uses* calculator.add.

    We will patch its method with mocker.patch.object in tests.
    """

    def compute_sum(self, a: int, b: int) -> int:
        return calculator.add(a, b)
```

Now a test that patches the `compute_sum` method **on a specific instance**:

```python
# test_mock_mocker.py

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
```

Here `mocker.patch.object(user, "compute_sum", ...)` replaces the bound method
**only on that instance**; other instances of `FakeCalculatorUser` (or the class
itself) would still see the original `compute_sum` implementation.
There is also a **class-level** variant that patches a method on the class so
all instances see the patched version:

```python
# test_mock_mocker.py

def test_patch_object_method_on_class(mocker):
    """Use mocker.patch.object to replace a method on the *class*."""

    mock_method = mocker.patch.object(FakeCalculatorUser, "compute_sum", return_value=100)

    user_one = FakeCalculatorUser()
    user_two = FakeCalculatorUser()

    assert user_one.compute_sum(1, 2) == 100
    assert user_two.compute_sum(10, 20) == 100
```

Here `mocker.patch.object(FakeCalculatorUser, "compute_sum", ...)` affects the
attribute on the **class**, so every new instance you create in this test will
use the mocked method.



---

#### 8.3. When to use `monkeypatch` vs `mocker` (summary)

Both `monkeypatch` and `mocker` are built on top of the standard library's
`unittest.mock`, but they shine in slightly different situations:

- **Use `monkeypatch` when...**
  - You want a lightweight, built-in tool with **no extra dependency**.
  - You mainly need to patch **module-level functions** or **environment
    variables**.
  - Examples in this notebook: `test_mock_monkeypatch.py`.

- **Use `mocker` (from pytest-mock) when...**
  - You already depend on `unittest.mock`-style mocks and want a cleaner,
    pytest-friendly API.
  - You like the convenience helpers: `mocker.patch`, `mocker.patch.object`,
    `mocker.spy`, automatic cleanup between tests.
  - You want easy **assertions on mocks and spies** (call counts, arguments,
    etc.).
  - Examples in this notebook: `test_mock_mocker.py`.

In many real projects you will use **both**:

- `monkeypatch` for environment, paths, and simple function patching.
- `mocker` for richer mocking/spying patterns around classes and objects.


Run this module (if you have pytest-mock installed) with:

```bash
pytest -vs test_mock_mocker.py
```

On a machine **without** pytest-mock installed, you should see:

```text
collected 0 items / 1 skipped

==================================================== 1 skipped in 0.01s ====================================================
```

The exact `pytest` output is stored at the bottom of `test_mock_mocker.py` in
its `output = """..."""` block.

In a real project, you would also add pytest-mock to your dependencies (for
example with `pip install pytest-mock`) and enable it in your test
configuration. Here we simply show how to use it when available.

---


## 12. Mini project: putting it all together

As a final step, we build a tiny **checkout mini‑project** inside a
separate package and write tests that use many pytest features together.

In this section you will see, in one place:
- Fixtures
- `conftest.py`
- Parametrization
- Markers and test selection
- Exceptions and failure control
- Mocking with `monkeypatch` / `mocker`


For this mini‑project we build a tiny **checkout example** inside a
separate package and then write tests that use many pytest features
together.

Code lives under `mini_project/`:

- `mini_project/orders.py` – very small `Order` and `OrderItem` models.
- `mini_project/payments.py` – a fake `PaymentGateway`, `PaymentError`, and a
  `checkout(order, gateway)` function that is our main entry point.
- `mini_project/discounts.py` – an extra module that calculates discounts
  on top of an order total.
- `mini_project/conftest.py` – fixtures for reusable orders, a configured
  gateway, and a parametrized `variable_size_order`.
- `mini_project/test_mini_project_checkout.py` – tests that combine
  fixtures, markers, parametrization, exceptions, and mocking around checkout.
- `mini_project/test_mini_project_discounts.py` – tests focused on the
  discount rules module.

You do **not** need any real external API for this; the tests patch the
payment gateway so everything stays local and deterministic.

#### 9.1. Mini‑project domain model (`mini_project/orders.py`)

`mini_project/orders.py` contains a tiny order model:

```python
# mini_project/orders.py

from dataclasses import dataclass
from typing import List


@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int = 1


@dataclass
class Order:
    items: List[OrderItem]

    @property
    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
```

This is intentionally minimal; the point is to have something that looks
like *real code* for tests to exercise.

#### 9.2. Payment gateway and checkout function (`mini_project/payments.py`)

`mini_project/payments.py` fakes out a payment gateway and a small
`checkout` function:

```python
# mini_project/payments.py

class PaymentError(Exception):
    """Raised when the payment gateway reports a failure."""
```

```python
from dataclasses import dataclass


@dataclass
class PaymentResult:
    ok: bool
    transaction_id: str | None = None
```

```python
import os


class PaymentGateway:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("PAYMENT_API_KEY")

    def charge(self, amount: float) -> PaymentResult:
        if not self.api_key:
            raise PaymentError("missing API key")
        if amount <= 0:
            raise ValueError("amount must be positive")
        return PaymentResult(ok=True, transaction_id="TEST-TRANSACTION")
```

```python
from .orders import Order


def checkout(order: Order, gateway: PaymentGateway) -> PaymentResult:
    total = order.total
    if total <= 0:
        raise ValueError("cannot checkout free or empty orders")
    return gateway.charge(total)
```

These pieces give us:

- A **happy path** to test (successful checkout).
- Several **error paths** to test with `pytest.raises`.
- Something that looks like an external dependency (`PaymentGateway`)
  which we can patch or fake in tests.

#### 9.3. Mini‑project fixtures (`mini_project/conftest.py`)

In `mini_project/conftest.py` we define fixtures just for this mini‑project
package:

```python
# mini_project/conftest.py

import pytest

from .orders import Order, OrderItem
from .payments import PaymentGateway
```

```python
@pytest.fixture
def simple_order() -> Order:
    return Order(items=[OrderItem(name="book", price=10.0, quantity=2)])
```

```python
@pytest.fixture
def configured_gateway(monkeypatch: pytest.MonkeyPatch) -> PaymentGateway:
    monkeypatch.setenv("PAYMENT_API_KEY", "test-key-123")
    return PaymentGateway()
```

```python
@pytest.fixture(params=[1, 2, 3], ids=["one-item", "two-items", "three-items"])
def variable_size_order(request) -> Order:
    quantity = request.param
    item = OrderItem(name="widget", price=5.0, quantity=quantity)
    return Order(items=[item])
```

Key ideas:

- This `conftest.py` is *local* to the `mini_project` package.
- Fixtures like `simple_order` and `configured_gateway` are automatically
  available to all tests under `mini_project/` without explicit imports.
- `variable_size_order` is a **parametrized fixture** that yields three
  different orders; any test that uses it will run three times.

#### 9.4. Tests that combine fixtures, markers, parametrization, exceptions, and mocking

The main tests live in `mini_project/test_mini_project_checkout.py`.
Here is a shortened version of each:

```python
# mini_project/test_mini_project_checkout.py

import pytest

from .orders import Order, OrderItem
from .payments import PaymentError, PaymentGateway, checkout
```

**Happy path with fixtures, marker, and monkeypatch:**

```python
@pytest.mark.api
def test_checkout_success_with_patched_gateway(simple_order, configured_gateway, monkeypatch):
    calls: dict[str, float] = {}

    def fake_charge(self, amount: float):
        calls["amount"] = amount
        return type("Result", (), {"ok": True, "transaction_id": "FAKE-123"})()

    monkeypatch.setattr(PaymentGateway, "charge", fake_charge)

    result = checkout(simple_order, configured_gateway)

    assert result.ok is True
    assert result.transaction_id == "FAKE-123"
    assert calls["amount"] == simple_order.total
```

This single test demonstrates:

- Reusing fixtures from `mini_project/conftest.py`.
- Using a **marker** (`@pytest.mark.api`) so we can select just these tests.
- Using `monkeypatch.setattr` to replace `PaymentGateway.charge` so no real
  external call happens.

**Error handling with `pytest.raises` and environment control:**

```python
def test_checkout_raises_payment_error_when_api_key_missing(simple_order, monkeypatch):
    monkeypatch.delenv("PAYMENT_API_KEY", raising=False)
    gateway = PaymentGateway()

    with pytest.raises(PaymentError, match="missing API key"):
        checkout(simple_order, gateway)
```

This test combines:

- Fixture reuse (`simple_order`).
- Environment manipulation with `monkeypatch.delenv`.
- `pytest.raises` with a `match=` string to assert the error message.

**Validation of business rules with exceptions:**

```python
def test_checkout_rejects_free_orders(monkeypatch):
    free_order = Order(items=[OrderItem(name="freebie", price=0.0, quantity=1)])
    gateway = PaymentGateway(api_key="test-key")

    with pytest.raises(ValueError, match="free or empty"):
        checkout(free_order, gateway)
```

Here we build an order directly and assert that our own validation rule is
applied via `ValueError`.

**Parametrized fixture + markers + monkeypatch:**

```python
@pytest.mark.slow
@pytest.mark.api
def test_checkout_works_for_variable_size_orders(variable_size_order, configured_gateway, monkeypatch):
    charged_amounts: list[float] = []

    def fake_charge(self, amount: float):
        charged_amounts.append(amount)
        return type("Result", (), {"ok": True, "transaction_id": "VARIED"})()

    monkeypatch.setattr(PaymentGateway, "charge", fake_charge)

    result = checkout(variable_size_order, configured_gateway)

    assert result.ok is True
    assert charged_amounts[-1] == variable_size_order.total
```

This final test shows:

- Multiple markers (`slow` and `api`) to tag a whole family of tests.
- A **parametrized fixture** `variable_size_order` driving multiple cases.
- Monkeypatch used to capture the amounts our code tries to charge.

#### 9.5. Mini‑project architecture at a glance

You can visualize the mini‑project like this:

```text
          +----------------+
          |  test_*.py    |
          | mini_project  |
          +--------+-------+
                   |
                   |  uses fixtures from
                   v
          +------------------------+
          | mini_project/conftest |
          |  simple_order,        |
          |  configured_gateway,  |
          |  variable_size_order  |
          +-----------+-----------+
                      |
          +-----------+-----------------------------+
          |                                         |
          v                                         v
+----------------------+                +-----------------------+
| mini_project/orders  |                | mini_project/discounts|
|  Order, OrderItem    |                |  DiscountRule,        |
|  Order.total         |                |  calculate_discount,  |
+-----------+----------+                |  total_after_...      |
            |                           +-----------+-----------+
            | uses Order                              |
            v                                         |
+---------------------------+                        |
| mini_project/payments     |                        |
|  PaymentGateway,          | <----------------------+
|  PaymentResult, checkout  |
+---------------------------+
```

- Tests call into `checkout` and the discount helpers.
- Fixtures in `conftest.py` build realistic `Order` and `PaymentGateway`
  instances.
- The domain modules (`orders`, `discounts`, `payments`) stay free of pytest
  imports; only the tests know about pytest.

#### 9.6. End‑to‑end flow of the mini‑project

Here is how the pieces interact in the **checkout** flow:

1. You build an `Order` out of `OrderItem` instances (usually via fixtures
   in `mini_project/conftest.py`).
2. The `Order.total` property computes the pre‑discount total.
3. Optionally, the discounts module (`mini_project/discounts.py`) can compute
   a discount amount and a discounted total.
4. A `PaymentGateway` instance (again often provided via a fixture) reads its
   API key from the constructor or from `PAYMENT_API_KEY`.
5. The `checkout(order, gateway)` function:
   - reads `order.total`,
   - rejects free/empty orders with `ValueError`,
   - then calls `gateway.charge(total)` and returns the resulting
     `PaymentResult`.
6. In tests we usually **patch** `PaymentGateway.charge` so that no real
   external API is touched; we just assert on the amount and the returned
   object.

The **discount** flow is similar but focused on pure computation:

1. An `Order` is created, often directly inside the test.
2. A list of `DiscountRule` objects defines percentage discounts for various
   `min_total` thresholds.
3. `calculate_discount(order, rules)` returns the best discount amount for
   the current total.
4. `total_after_discounts(order, rules)` gives the final total after
   subtracting that discount.

All of these functions are tiny on purpose, so the tests stay readable and
conversation can focus on pytest features.

#### 9.7. Suggested reading order for the mini‑project

If you are new to the code, a good reading order is:

1. `mini_project/orders.py` – the core data model (`OrderItem`, `Order.total`).
2. `mini_project/discounts.py` – pure functions that sit on top of `Order`.
3. `mini_project/payments.py` – `PaymentGateway`, `PaymentResult`, and
   `checkout` using the order total (and conceptually any discounts).
4. `mini_project/conftest.py` – fixtures that create realistic `Order` and
   `PaymentGateway` objects for tests.
5. `mini_project/test_mini_project_checkout.py` – how checkout is tested with
   fixtures, markers, parametrization, exceptions, and monkeypatch.
6. `mini_project/test_mini_project_discounts.py` – how the discount rules are
   tested with parametrization and another marker (`db`).

Once you have walked through that sequence, rerun:

```bash
pytest -vs mini_project
```

and read the test output together with the code to reinforce the mental model.


#### 9.8. Running the mini‑project tests

From inside `practice/pytest` you can exercise everything in several ways.

**1. Run only the checkout tests:**

```bash
pytest -vs mini_project/test_mini_project_checkout.py
```

**2. Run only the discounts tests:**

```bash
pytest -vs mini_project/test_mini_project_discounts.py
```

**3. Run the whole mini‑project package:**

```bash
pytest -vs mini_project
```

**4. Use markers to select subsets (checkout + discounts):**

- All API‑tagged tests (from the checkout module):

  ```bash
  pytest -vs mini_project -m api
  ```

- The slower parametrized API test for checkout only:

  ```bash
  pytest -vs mini_project -m "api and slow"
  ```

- All tests that happen to use the `db` marker (discounts example):

  ```bash
  pytest -vs mini_project -m db
  ```

These commands pull together everything from the previous sections:

- locating tests in a subpackage,
- sharing fixtures via a local `conftest.py`,
- parametrizing both tests and fixtures,
- handling exceptions with `pytest.raises`,
- isolating external calls with `monkeypatch` (or `mocker`, if you prefer),
- and tagging tests with markers so you can run **just the slice you care
  about**.

#### 9.9. Mini‑project recap – pytest concepts used together

The mini‑project is small on purpose, but it ties together many of the
features from earlier sections:

- **Fixtures** – `simple_order`, `configured_gateway`, `variable_size_order`,
  and `default_rules` keep tests readable and DRY.
- **`conftest.py`** – a package‑local `mini_project/conftest.py` that shares
  fixtures across all tests in the mini‑project.
- **Parametrization** – both via `@pytest.mark.parametrize` and via the
  parametrized fixture `variable_size_order`.
- **Markers** – `api`, `slow`, and `db` let you slice the test suite by
  concern.
- **Exceptions** – `pytest.raises` is used to test validation (`ValueError`)
  and integration failures (`PaymentError`).
- **Monkeypatching** – `monkeypatch.setattr`, `setenv`, and `delenv` let you
  isolate the payment gateway and environment from the tests.

If you understand how all of these pieces work together in this miniproject, you have
most of the tools you need to write robust pytest suites for real projects.


---

---


---

## 2. Basic assertions with pytest: `test_assertions_basic.py`

We created a new file: `test_assertions_basic.py`.

To run only this file from inside `practice/pytest`:

```bash
pytest test_assertions_basic.py
```

### 5.1. Numbers: equality and inequality

```python
def test_numbers_equal():
    """Basic numeric equality"""
    assert 2 + 3 == 5
    assert 10 - 4 == 6
```

What this shows:

- Use `==` to check numeric equality.
- You can have **multiple `assert`s in one test**.

```python
def test_numbers_not_equal():
    """Numeric inequality"""
    assert 2 * 3 != 5
    assert 7 / 2 != 4  # 7/2 is 3.5
```

What this shows:

- Use `!=` when you want to ensure two values are **not equal**.
- Pytest will show you both sides of the comparison if an assertion fails.

### 5.2. Number comparisons: `<`, `>`, `<=`, `>=`

```python
def test_number_comparisons():
    """Greater-than and less-than comparisons"""
    value = 10
    assert value > 5
    assert value >= 10
    assert value < 20
```

What this shows:

- You can use all normal comparison operators inside `assert`.
- If any of these comparisons fails, pytest will show exactly which one failed.

### 5.3. Strings: equality, case, and substring checks

```python
def test_string_equality_and_case():
    """String equality and case sensitivity"""
    text = "pytest"
    assert text == "pytest"
    # Case matters in equality
    assert text.upper() == "PYTEST"
```

- String equality is **case-sensitive**.
- You can call methods like `.upper()` inside the `assert` expression.

```python
def test_string_contains():
    """Substring membership in strings"""
    text = "learning pytest is fun"
    assert "pytest" in text
    assert "learn" in text  # substring of "learning"
```

- Use `"sub" in text` to check that a substring appears inside a string.
- This is a very common pattern when testing messages or output.

### 5.4. Lists: membership and length

```python
def test_list_membership_and_length():
    """Basic list checks: membership and length"""
    numbers = [1, 2, 3, 4]
    assert 2 in numbers
    assert 5 not in numbers
    assert len(numbers) == 4
```

- `in` / `not in` checks that a value is (or is not) in a list.
- `len()` is often used in tests to check size or count.

### 5.5. Multiple asserts in a single test

```python
def test_multiple_asserts_in_one_test():
    """A single test can contain multiple asserts"""
    name = "python"
    assert name.startswith("py")
    assert name.endswith("on")
    assert len(name) == 6
```

- One test function can contain **multiple** assertions.
- The test fails on the **first failing assertion**; earlier ones still run.


Example: running only `test_assertions_basic.py` in verbose mode:

```bash
pytest -v test_assertions_basic.py
```

Expected output (abbreviated):

```text
test_assertions_basic.py::test_numbers_equal PASSED
...
test_assertions_basic.py::test_boolean_truthiness PASSED

==================================================== 8 passed in 0.01s ====================================================
```

### 5.6. Truthiness and booleans

```python
def test_boolean_truthiness():
    """Truthiness of values in Python"""
    assert bool("non-empty")  # non-empty string is True
    assert not bool("")  # empty string is False
    assert bool([1])  # non-empty list is True
    assert not bool([])  # empty list is False
```

- In Python, many values have a **truthy** or **falsy** value:
  - Non-empty strings/lists are truthy
  - Empty strings/lists are falsy
- Tests often rely on this behavior when checking conditions.

---

## 8. Fixtures: reusing setup with `@pytest.fixture`

In this section we introduce **fixtures** – small, reusable pieces of setup code
that pytest can inject into your tests by **name**.

### 8.1. A simple calculator fixture (`test_calculator_fixtures.py`)

We created a new file: `test_calculator_fixtures.py`.

```python
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
```

What this shows:

- `@pytest.fixture` marks `calculator_values` as a **fixture**.
- Any test that has a parameter named `calculator_values` will receive the
  dictionary returned by this fixture.
- You avoid repeating the same numbers (`10`, `5`, `-3`, `0`) in every test.

To run only these tests from inside `practice/pytest`:

```bash
pytest -v test_calculator_fixtures.py
```

You should see output like:

```text
test_calculator_fixtures.py::test_add_with_fixture PASSED
test_calculator_fixtures.py::test_subtract_with_fixture PASSED
test_calculator_fixtures.py::test_multiply_with_fixture PASSED

==================================================== 3 passed in 0.01s ====================================================
```

In the file itself, at the bottom, we also embedded the **full pytest output**
from running this file as a triple‑quoted string, so you can review it without
rerunning the tests.

In later examples we will show:

- How to use `yield` inside a fixture for **teardown**.
- How fixture **scopes** work (function, class, module, package, session).
- How to move fixtures into `conftest.py` so they can be reused by many files.

### 8.2. Fixture scopes and teardown with `yield` (`test_fixture_scopes.py`)

To demonstrate **fixture scopes** and `yield`-based teardown, we created
another file: `test_fixture_scopes.py`.

```python
import pytest


# Fixtures: scopes and teardown with `yield`

call_log = []


@pytest.fixture
def function_scope_fixture():
    """Function-scope fixture (default scope).

    Runs once per test that uses it.
    """
    call_log.append("function-setup")
    yield
    call_log.append("function-teardown")


@pytest.fixture(scope="module")
def module_scope_fixture():
    """Module-scope fixture.

    Runs once for the whole module (all tests that use it),
    and tears down once at the end.
    """
    call_log.append("module-setup")
    yield
    call_log.append("module-teardown")


def test_one(function_scope_fixture, module_scope_fixture):
    assert True


def test_two(function_scope_fixture, module_scope_fixture):
    assert True


def test_check_call_log():
    """Verify how many times each fixture ran.

    - module_scope_fixture should run once for setup.
    - function_scope_fixture should run separately for each test that uses it.

    Note: for a `scope="module"` fixture, teardown happens *after* all
    tests in this module finish, so we do **not** see `module-teardown`
    yet while this test is running.
    """
    # module-scope fixture should only run once for setup
    assert call_log.count("module-setup") == 1

    # function-scope fixture runs separately for each test that uses it
    assert call_log.count("function-setup") == 2
    assert call_log.count("function-teardown") == 2
```

Key ideas shown here:

- **Function-scope fixtures** (default): run once per test that uses them.
- **Module-scope fixtures** (`scope="module"`): run once for the whole module
  and tear down once at the end.
- `yield` in a fixture lets you separate **setup** (before `yield`) from
  **teardown** (after `yield`).

Run these tests with:

```bash
pytest -v test_fixture_scopes.py
```

You should see something like:

```text
test_fixture_scopes.py::test_one PASSED
test_fixture_scopes.py::test_two PASSED
test_fixture_scopes.py::test_check_call_log PASSED

==================================================== 3 passed in 0.01s ====================================================
```

As with other examples, the **full pytest output** is also stored at the
bottom of `test_fixture_scopes.py` so you can review it without rerunning
anything.
### 6.3. All fixture scopes in one place (`test_fixture_scopes_all.py`)

So far we have seen **function** and **module** scopes. Pytest also supports
`class`, `package`, and `session` scopes. To make this concrete, we created a
single file that uses *all five* scopes:

```python
import pytest


# Fixtures: demonstrating all fixture scopes

call_log = []


@pytest.fixture(scope="function")
def function_scope():
    call_log.append("function-setup")
    yield
    call_log.append("function-teardown")


@pytest.fixture(scope="class")
def class_scope(request):
    call_log.append(f"class-setup-{request.cls.__name__}")
    yield
    call_log.append(f"class-teardown-{request.cls.__name__}")


@pytest.fixture(scope="module")
def module_scope():
    call_log.append("module-setup")
    yield
    call_log.append("module-teardown")


@pytest.fixture(scope="package")
def package_scope():
    call_log.append("package-setup")
    yield
    call_log.append("package-teardown")


@pytest.fixture(scope="session")
def session_scope():
    call_log.append("session-setup")
    yield
    call_log.append("session-teardown")


class TestFirst:
    def test_a(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True

    def test_b(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True


class TestSecond:
    def test_c(self, function_scope, class_scope, module_scope, package_scope, session_scope):
        assert True


def test_check_scope_setups():
    """Verify how often each fixture's setup ran in this module.

    In this single-module example:
    - function_scope runs once per test that uses it (3 tests).
    - class_scope runs once per *class* that uses it (2 classes).
    - module_scope runs once for this module.
    - package_scope runs once for this test package (here same as module).
    - session_scope runs once for the whole pytest session.
    """

    assert call_log.count("function-setup") == 3
    assert call_log.count("class-setup-TestFirst") == 1
    assert call_log.count("class-setup-TestSecond") == 1
    assert call_log.count("module-setup") == 1
    assert call_log.count("package-setup") == 1
    assert call_log.count("session-setup") == 1
```

Key ideas:

- `scope="function"` (the default): runs once per test that uses the fixture.
- `scope="class"`: one shared instance per test class.
- `scope="module"`: one shared instance for the whole module.
- `scope="package"`: one shared instance per test package (directory).
- `scope="session"`: one shared instance for the entire pytest run.

Run this file by itself:

```bash
pytest -v test_fixture_scopes_all.py
```

You should see output like:

```text
test_fixture_scopes_all.py::TestFirst::test_a PASSED
test_fixture_scopes_all.py::TestFirst::test_b PASSED
test_fixture_scopes_all.py::TestSecond::test_c PASSED
test_fixture_scopes_all.py::test_check_scope_setups PASSED

==================================================== 4 passed in 0.01s ====================================================
```

As with other examples, the full `pytest -v` output is also stored at the
bottom of `test_fixture_scopes_all.py` in a triple-quoted string.

---
### 6.3.1. Package scope across multiple modules (`package_scope_pkg/`)

To really see the difference between **module** and **package** scope, we added
an actual test package directory: `package_scope_pkg/`.

Inside that directory, `conftest.py` defines a `scope="package"` fixture and a
shared `log` list:

```python
# package_scope_pkg/conftest.py
import pytest

log = []


@pytest.fixture(scope="package")
def package_fix():
    """Package-scope fixture used by all tests in this directory.

    It will be set up once when the first test in this package runs,
    and torn down once after the last test in this package.
    """
    log.append("package-setup")
    yield
    log.append("package-teardown")
```

Two test modules in the same package both use this fixture:

```python
# package_scope_pkg/test_pkg_one.py
from .conftest import log


class TestPkgOne:
    def test_one(self, package_fix):
        log.append("pkg-one-test-one")

    def test_two(self, package_fix):
        log.append("pkg-one-test-two")
```

```python
# package_scope_pkg/test_pkg_two.py
from .conftest import log


class TestPkgTwo:
    def test_three(self, package_fix):
        log.append("pkg-two-test-three")
```

Outside the package we have a small test that just checks how many times the
package fixture ran:

```python
# test_package_scope_log.py
from package_scope_pkg.conftest import log


def test_package_fixture_runs_once_for_package():
    assert log.count("package-setup") == 1
    assert log.count("package-teardown") == 1
```

Run them together from `practice/pytest`:

```bash
pytest -v package_scope_pkg test_package_scope_log.py
```

You should see all tests pass, and the important thing is that the
`package_fix` fixture was set up **once** and torn down **once** for the whole
`package_scope_pkg/` directory, even though it served multiple modules.

As usual, the exact `pytest -v` output is stored in
`package_scope_pkg/conftest.py` in a triple-quoted string.

---
### 6.3.2. Session scope across multiple top-level modules (`session_scope_shared.py`)

Finally, here is a small example that makes **session scope** visible across
multiple *top-level* test modules (not in a subpackage).

We put the session-scoped fixture and a simple counter into
`session_scope_shared.py`:

```python
# session_scope_shared.py
import pytest


# Simple module-level counter so we can see how often the session fixture runs.
setup_calls = 0


@pytest.fixture(scope="session")
def session_fix():
    global setup_calls
    setup_calls += 1
    yield
```

Then two separate top-level test modules both use `session_fix` and check the
same counter:

```python
# test_session_scope_one.py
import session_scope_shared as shared


# Fixtures: session scope across multiple top-level modules


def test_session_fixture_seen_in_first_module(session_fix):
    """Session fixture is shared across top-level modules.

    Even though multiple modules use the same fixture name, the underlying
    session-scoped fixture is created only once for the entire pytest run.
    """
    assert shared.setup_calls == 1
```

```python
# test_session_scope_two.py
import session_scope_shared as shared


def test_session_fixture_seen_in_second_module(session_fix):
    # We are in a *different* test module, but the same session fixture has
    # already been created once for the whole test run.
    assert shared.setup_calls == 1
```

Run them together from `practice/pytest`:

```bash
pytest -v test_session_scope_one.py test_session_scope_two.py
```

The important point is that **both** modules see `setup_calls == 1`, showing
that `session_fix` was created only once for the entire test session, even
though multiple independent test files used it.

As usual, the exact `pytest -v` output is stored at the bottom of
`session_scope_shared.py` in a triple-quoted string.

---





---
### 6.3. Fixtures depending on other fixtures (`test_fixture_dependencies.py`)

Fixtures can also **depend on other fixtures**. This lets you build more
complex setup in small, reusable layers.

We created `test_fixture_dependencies.py`:

```python
import pytest
import calculator


# Fixtures: fixtures depending on other fixtures


@pytest.fixture
def base_numbers():
    """Base numbers shared between multiple fixtures."""
    return 2, 3


@pytest.fixture
def product(base_numbers):
    """Fixture that uses another fixture to compute a product."""
    a, b = base_numbers
    return calculator.multiply(a, b)


def test_product_uses_base_numbers(product):
    """The product fixture reuses the base_numbers fixture."""
    assert product == 6


def test_can_use_both_fixtures(base_numbers, product):
    """Tests can mix direct fixture values and dependent fixtures."""
    a, b = base_numbers
    assert a + b == 5
    assert product == a * b == 6
```

Key ideas:

- Fixtures can **take other fixtures as parameters**.
- pytest resolves dependencies for you (here, `product` uses `base_numbers`).
- Tests can use both the "raw" fixture (`base_numbers`) and the derived
  fixture (`product`) together.

Run this file with:

```bash
pytest -v test_fixture_dependencies.py
```

Expected output:

```text
test_fixture_dependencies.py::test_product_uses_base_numbers PASSED
test_fixture_dependencies.py::test_can_use_both_fixtures PASSED

==================================================== 2 passed in 0.01s ====================================================
```

The full pytest output is also stored at the bottom of
`test_fixture_dependencies.py` as a comment block.

---
### 6.4. Autouse fixtures (`test_autouse_fixture.py`)

Sometimes you want a fixture to run for **every test in a module** without
having to list it as a parameter each time. For that, you can use
`autouse=True`.

We created `test_autouse_fixture.py`:

```python
import pytest


# Fixtures: autouse fixture runs for every test in this module


log = []


@pytest.fixture(autouse=True)
def auto_log():
    """Autouse fixture that logs around every test in this module.

    Because autouse=True, we don't need to list it as a parameter
    in each test; it still runs for each test.
    """
    log.append("autouse-setup")
    yield
    log.append("autouse-teardown")


def test_first_uses_autouse():
    # At least one setup should have run before this assertion.
    assert log.count("autouse-setup") >= 1


def test_second_uses_autouse_again():
    # By now, the autouse fixture has run for both tests.
    assert log.count("autouse-setup") >= 2
```

Key ideas:

- `autouse=True` makes the fixture run for **every test in this module**, even
  if the test does not mention the fixture name.
- This is useful for things like logging, small global setup/teardown, etc.

Run this file with:

```bash
pytest -v test_autouse_fixture.py
```

Expected output:

```text
test_autouse_fixture.py::test_first_uses_autouse PASSED
test_autouse_fixture.py::test_second_uses_autouse_again PASSED

==================================================== 2 passed in 0.01s ====================================================
```

The full pytest output is embedded at the bottom of
`test_autouse_fixture.py`.

---

### 6.5. Built-in fixtures: `tmp_path` (`test_tmp_path_fixture.py`)

pytest comes with many **built-in fixtures**. One very useful one is
`tmp_path`, which gives you a temporary directory that is unique per test
and automatically cleaned up.

We created `test_tmp_path_fixture.py`:

```python
import pytest


# Fixtures: using built-in tmp_path fixture


paths = []


def test_write_and_read_tmp_file(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("hello pytest")
    assert file_path.read_text() == "hello pytest"


def test_tmp_path_is_unique_per_test(tmp_path):
    # Record the paths to show that each test gets a different directory.
    paths.append(tmp_path)
    if len(paths) == 2:
        # When the second test runs, both entries should be present and different.
        assert paths[0] != paths[1]
```

Key ideas:

- `tmp_path` is provided by pytest **automatically**.
- Each test that uses `tmp_path` gets its **own temporary directory**.
- pytest cleans up these directories after the test session.

Run this file with:

```bash
pytest -v test_tmp_path_fixture.py
```

Expected output:

```text
test_tmp_path_fixture.py::test_write_and_read_tmp_file PASSED
test_tmp_path_fixture.py::test_tmp_path_is_unique_per_test PASSED

==================================================== 2 passed in 0.01s ====================================================
```

Again, the full pytest output is stored at the bottom of
`test_tmp_path_fixture.py`.

---

### 6.6. Preview: parametrized fixtures (`test_parametrized_fixture.py`)

Full parametrization will be covered later, but here is a **preview** of a
parametrized fixture.

We created `test_parametrized_fixture.py`:

```python
import pytest


# Fixtures: parametrized fixture (preview for parametrization)


@pytest.fixture(params=[1, 2, 3])
def positive_number(request):
    """A parametrized fixture that provides multiple values.

    This single fixture will run the test three times: once for
    each value in params.
    """
    return request.param


def test_positive_number_is_always_positive(positive_number):
    assert positive_number > 0
```

Key ideas:

- `params=[...]` makes pytest run any test that uses this fixture **once per
  parameter value**.
- `request.param` gives you the current value for this run.
- The generated test names include the parameter value (e.g.
  `test_positive_number_is_always_positive[1]`).

Run this file with:

```bash
pytest -v test_parametrized_fixture.py
```

Expected output:

```text
test_parametrized_fixture.py::test_positive_number_is_always_positive[1] PASSED
test_parametrized_fixture.py::test_positive_number_is_always_positive[2] PASSED
test_parametrized_fixture.py::test_positive_number_is_always_positive[3] PASSED

==================================================== 3 passed in 0.01s ====================================================
```

The full pytest output is saved at the bottom of
`test_parametrized_fixture.py`.

---





- In Python, many values have a **truthy** or **falsy** value:
  - Non-empty strings/lists are truthy
  - Empty strings/lists are falsy
- Tests often rely on this behavior when checking conditions.

---

## 6. What’s Next

Now that you’re comfortable with basic assertions on numbers, strings, and lists, the next step is to:

- Write tests for **real functions** instead of only literals.
- Start organizing code into **modules** and **test files**.

Next, you’ll:

- Create a small `calculator` module (e.g. `add`, `subtract`, `multiply`, `divide`).
- Write tests in a file like `test_calculator.py`.
---

## 6. Markers in pytest

Markers let you **tag tests** so that you can:

- Group related tests (e.g. all "assertion" tests)
- Skip certain tests
- Mark tests as "expected to fail" (xfail)
- Select or deselect tests from the command line

### 6.1. Your existing `@pytest.mark.assertion` marker (`test_group.py`)

In `test_group.py` you already use a custom marker on your **grouped assertion tests**:

```python
import pytest


def testLogin():
    print("Login successful")


def testLogoff():
    print("Logged out successfully")


@pytest.mark.assertion
def testCalcs():
    # if 2+2 is 4, assertion will return true and pass
    assert 2 + 2 == 4


@pytest.mark.assertion
def testAssertfail():
    assert 2 * 3 == 9
```

What this gives you:

- Both assertion-style tests are tagged with the marker **`assertion`**.
- You can run **only** these tests from the command line:

```bash
pytest -m assertion -v
```

A typical run of just `test_group.py` looks like:

```text
test_group.py::testLogin PASSED
test_group.py::testLogoff PASSED
test_group.py::testCalcs PASSED
test_group.py::testAssertfail FAILED
```

So when you run all tests, you should **expect**:

- 3 passing tests (`testLogin`, `testLogoff`, `testCalcs`).
- 1 intentionally failing test (`testAssertfail`), to show how pytest displays failures.

### 6.2. Built‑in markers: `skip` and `xfail`

We also created `test_markers.py` to demonstrate some common built‑in markers:

```python
import pytest


@pytest.mark.slow
def test_slow_example():
    """A dummy 'slow' test, marked just for selection."""
    assert 1 + 1 == 2


@pytest.mark.skip(reason="demonstration of a skipped test")
def test_skipped_example():
    """This test is always skipped."""
    assert 1 == 2  # would fail if it ran, but it is skipped


@pytest.mark.xfail(reason="demonstration of expected failure")
def test_expected_failure_example():
    """This test is expected to fail (xfail)."""
    assert 2 + 2 == 5  # xfail instead of fail
```

From inside `practice/pytest` you can run:

```bash
pytest test_markers.py -v
```

You should see something like:

```text
test_markers.py::test_slow_example PASSED
test_markers.py::test_skipped_example SKIPPED
test_markers.py::test_expected_failure_example XFAIL
```

- `@pytest.mark.skip` means pytest **does not run the test at all**. It is reported as **SKIPPED**.
- `@pytest.mark.xfail` means pytest **expects the test to fail**. When it fails, pytest reports it as **XFAIL** instead of FAILED.

This is useful when:

- You know a feature is not implemented yet, but you still want to write a test.
- There is a known bug and you dont want it to make the whole test run red.

### 6.3. Custom markers like `slow`
### 6.4. Module-level markers with `pytestmark` (`test_module_markers.py`)

So far, we have marked **individual tests** with decorators. Pytest also lets
you apply a marker to **all tests in a module** using the special variable
`pytestmark`.

We created `test_module_markers.py`:

```python
import pytest


# Markers: module-level markers with pytestmark


pytestmark = pytest.mark.slow


def test_module_level_marker_one():
    """This test inherits the module-level 'slow' marker."""
    assert 1 + 1 == 2


def test_module_level_marker_two():
    """This test also inherits the 'slow' marker."""
    assert "py" in "pytest"
```

Key ideas:

- `pytestmark = pytest.mark.slow` applies the `slow` marker to **every test** in
  this module.
- You don’t need to decorate each function individually.

Run this file with:

```bash
pytest -v test_module_markers.py
```

Expected output:

```text
test_module_markers.py::test_module_level_marker_one PASSED
test_module_markers.py::test_module_level_marker_two PASSED

==================================================== 2 passed in 0.01s ====================================================
```

The full pytest output is at the bottom of
`test_module_markers.py`.

---

### 6.5. Conditional skipping with `skipif` (`test_skipif.py`)

Sometimes you want to **skip tests only under certain conditions** (for
example, on a specific OS or when an environment flag is not enabled).

We created `test_skipif.py`:

```python
import sys
import pytest


# Markers: conditional skipping with skipif


RUN_EXPENSIVE = False


@pytest.mark.skipif(sys.platform.startswith("win"), reason="skip on Windows")
def test_not_on_windows():
    """This test will be skipped on Windows, but run elsewhere."""
    assert True


@pytest.mark.skipif(not RUN_EXPENSIVE, reason="expensive test disabled")
def test_expensive_operation():
    """Example of using a flag to disable an expensive test."""
    assert 2 * 3 == 6
```

Key ideas:

- `@pytest.mark.skipif(condition, reason=...)` evaluates `condition` at
  **collection time**.
- If the condition is `True`, the test is **SKIPPED**.
- If the condition is `False`, the test runs normally.

Run this file with:

```bash
pytest -v test_skipif.py
```

On a non-Windows system with `RUN_EXPENSIVE = False`, you should see:

```text
test_skipif.py::test_not_on_windows PASSED
test_skipif.py::test_expensive_operation SKIPPED (expensive test disabled)

=============================================== 1 passed, 1 skipped in 0.01s ===============================================
```

The full pytest output is stored at the bottom of `test_skipif.py`.

---

### 6.6. Runtime skipping and xfail (`test_runtime_skip_xfail.py`)

Sometimes you don’t know whether to skip/xfail a test until **runtime** (inside
the test body itself). Pytest provides functions for that:

- `pytest.skip("reason")`
- `pytest.xfail("reason")`

We created `test_runtime_skip_xfail.py`:

```python
import os
import pytest


# Markers: runtime skip and xfail inside tests


def test_runtime_skip_if_env_not_set():
    """Use pytest.skip() at runtime if a condition is not met."""
    if "MY_FEATURE_FLAG" not in os.environ:
        pytest.skip("MY_FEATURE_FLAG not set")
    assert True


def test_runtime_xfail_inside_test():
    """Use pytest.xfail() at runtime to mark a known bug."""
    pytest.xfail("demonstration of runtime xfail")
    assert 2 + 2 == 5  # would fail, but reported as XFAIL
```

Key ideas:

- `pytest.skip(...)` and `pytest.xfail(...)` can be called from **inside tests**.
- This is useful when the decision depends on runtime state (env vars, network,
  database availability, etc.).

Run this file with:

```bash
pytest -v test_runtime_skip_xfail.py
```

Expected output on a typical run (without `MY_FEATURE_FLAG` set):

```text
test_runtime_skip_xfail.py::test_runtime_skip_if_env_not_set SKIPPED (MY_FEATURE_FLAG not set)
test_runtime_skip_xfail.py::test_runtime_xfail_inside_test XFAIL (demonstration of runtime xfail)

============================================== 1 skipped, 1 xfailed in 0.03s ===============================================
```

The full pytest output is captured at the bottom of
`test_runtime_skip_xfail.py`.

---

### 6.7. Registering markers in `pytest.ini`

Pytest warns when you use **custom markers** that are not registered.
We created a small `pytest.ini` configuration file to register the
custom markers we use:

```ini
[pytest]
markers =
    assertion: tests that exercise basic assertion behavior
    slow: tests that are slow or optional
    api: tests that call external or HTTP APIs
    db: tests that touch the database or persistence layer
```

This removes the `PytestUnknownMarkWarning` for `@pytest.mark.slow`, your
`@pytest.mark.assertion` marker in `test_group.py`, and the new `api` / `db`
markers used in the markers examples above.

Now you can safely use:

```bash
pytest -m slow -v
pytest -m assertion -v
pytest -m api -v
pytest -m db -v
```

without marker warning noise.

---

### 6.8. Combining multiple markers and `-m` expressions (`test_multi_markers_selection.py`)

So far we have used simple marker selection like `-m slow`. Pytest also lets
you combine markers with **boolean expressions**.

We created `test_multi_markers_selection.py`:

```python
import pytest


@pytest.mark.slow
@pytest.mark.api
def test_slow_api():
    assert True


@pytest.mark.api
def test_fast_api():
    assert True


@pytest.mark.db
def test_db_only():
    assert True


@pytest.mark.slow
@pytest.mark.db
def test_slow_db():
    assert True


def test_unmarked():
    assert True
```

Key ideas:

- A test can have **multiple markers** (e.g. `slow` and `api`).
- You can then select tests based on marker **expressions**:

```bash
# Only tests marked "slow"
pytest -m slow -v test_multi_markers_selection.py

# Only tests that are slow *and* API tests
pytest -m "slow and api" -v test_multi_markers_selection.py

# Tests that are API tests but not slow
pytest -m "api and not slow" -v test_multi_markers_selection.py

# Only database tests (slow or not)
pytest -m db -v test_multi_markers_selection.py
```

On your machine, running all tests in this file with:

```bash
pytest -v test_multi_markers_selection.py
```

produced (abbreviated):

```text
test_multi_markers_selection.py::test_slow_api PASSED
test_multi_markers_selection.py::test_fast_api PASSED
test_multi_markers_selection.py::test_db_only PASSED
test_multi_markers_selection.py::test_slow_db PASSED
test_multi_markers_selection.py::test_unmarked PASSED

==================================================== 5 passed in 0.01s ====================================================
```

The full pytest output is embedded at the bottom of
`test_multi_markers_selection.py`.

---

### 6.9. Selecting tests by name with `-k` (`test_selection_k.py`)

Markers are great when you plan ahead, but sometimes you just want to **run
all tests whose names match a pattern**. That is what `-k` is for.

We created `test_selection_k.py`:

```python
def test_login_success():
    assert True


def test_login_failure():
    assert True


def test_logout():
    assert True


def test_profile_update():
    assert True
```

You can now run subsets of these tests without changing the code:

```bash
# Run all tests whose names contain "login"
pytest -k "login" -v test_selection_k.py

# Run tests whose names contain either "login" or "logout"
pytest -k "login or logout" -v test_selection_k.py

# Run tests whose names contain "login" but not "failure"
pytest -k "login and not failure" -v test_selection_k.py
```

On your machine, running the whole file with:

```bash
pytest -v test_selection_k.py
```

produced:

```text
test_selection_k.py::test_login_success PASSED
test_selection_k.py::test_login_failure PASSED
test_selection_k.py::test_logout PASSED
test_selection_k.py::test_profile_update PASSED

==================================================== 4 passed in 0.01s ====================================================
```

The full pytest output is stored at the bottom of `test_selection_k.py`.

---

- Explain how to run just that module’s tests and how to read failures.

When you’re ready, tell me and we’ll design the `calculator` module and its tests together.