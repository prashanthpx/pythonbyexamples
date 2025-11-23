# Pytest Basics - Getting Started

[← Back to Main Guide](../README.md)

> **Location**: `pytest/basics/`  
> **Test Files**: Introductory examples for pytest beginners

---

## Table of Contents

1. [Your First Test](#1-your-first-test)
2. [Basic Assertions](#2-basic-assertions)
3. [Grouping Tests with Classes](#3-grouping-tests-with-classes)
4. [Running Tests](#4-running-tests)

---

## 1. Your First Test

**File**: `test_eg.py`

The simplest pytest test is just a function that starts with `test_`:

```python
def testLogin():
    """A simple test that always passes."""
    assert True
```

### How It Works

1. **File naming**: `test_eg.py` matches the pattern `test_*.py`
2. **Function naming**: `testLogin` starts with `test`
3. **Assertion**: `assert True` is the actual test
4. **Pytest discovers it automatically**: No need to import or call anything

### Running This Test

```bash
# From pytest/ directory
pytest basics/test_eg.py -v
```

**Output**:
```
basics/test_eg.py::testLogin PASSED
```

---

## 2. Basic Assertions

**File**: `test_assertions_basic.py`

Pytest uses Python's built-in `assert` statement for testing. When an assertion fails, pytest provides detailed information about what went wrong.

### 2.1. Number Assertions

```python
def test_numbers_equal():
    """Test that two numbers are equal."""
    result = 2 + 2
    assert result == 4

def test_numbers_not_equal():
    """Test that two numbers are not equal."""
    assert 5 != 3

def test_greater_than():
    """Test greater than comparison."""
    assert 10 > 5

def test_less_than():
    """Test less than comparison."""
    assert 3 < 7
```

### 2.2. String Assertions

```python
def test_string_equality():
    """Test string equality."""
    name = "pytest"
    assert name == "pytest"

def test_string_contains():
    """Test if string contains substring."""
    message = "Hello, pytest!"
    assert "pytest" in message

def test_string_starts_with():
    """Test if string starts with prefix."""
    text = "pytest is awesome"
    assert text.startswith("pytest")

def test_string_ends_with():
    """Test if string ends with suffix."""
    text = "pytest is awesome"
    assert text.endswith("awesome")
```

### 2.3. List Assertions

```python
def test_list_contains():
    """Test if item is in list."""
    fruits = ["apple", "banana", "cherry"]
    assert "banana" in fruits

def test_list_length():
    """Test list length."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5

def test_list_equality():
    """Test list equality."""
    expected = [1, 2, 3]
    actual = [1, 2, 3]
    assert actual == expected
```

### 2.4. Boolean Assertions

```python
def test_true():
    """Test that something is True."""
    is_valid = True
    assert is_valid

def test_false():
    """Test that something is False."""
    is_invalid = False
    assert not is_invalid
```

### 2.5. None Assertions

```python
def test_is_none():
    """Test that value is None."""
    result = None
    assert result is None

def test_is_not_none():
    """Test that value is not None."""
    result = "something"
    assert result is not None
```

### Why Pytest's Assert is Better

Unlike other testing frameworks that require special assertion methods (`assertEqual`, `assertTrue`, etc.), pytest uses plain Python `assert`:

**Other frameworks**:
```python
self.assertEqual(result, 4)
self.assertTrue(is_valid)
self.assertIn("pytest", message)
```

**Pytest**:
```python
assert result == 4
assert is_valid
assert "pytest" in message
```

**Benefits**:
- More readable and Pythonic
- No need to remember special methods
- Better error messages with introspection

### Assertion Failure Messages

When an assertion fails, pytest shows you exactly what went wrong:

```python
def test_example():
    result = 2 + 2
    assert result == 5  # This will fail
```

**Output**:
```
    def test_example():
        result = 2 + 2
>       assert result == 5
E       assert 4 == 5

AssertionError
```

Pytest shows:
- The line that failed
- The actual values (4 == 5)
- Clear indication of the problem

---

## 3. Grouping Tests with Classes

**File**: `test_group.py`

You can organize related tests into classes. This is useful for grouping tests that share a common theme.

### 3.1. Basic Test Class

```python
class TestLogin:
    """Group all login-related tests."""
    
    def test_valid_login(self):
        """Test login with valid credentials."""
        username = "admin"
        password = "secret"
        assert username == "admin"
        assert password == "secret"
    
    def test_invalid_login(self):
        """Test login with invalid credentials."""
        username = "wrong"
        password = "wrong"
        assert username != "admin"
```

### 3.2. Class Naming Rules

- Class name **must** start with `Test` (capital T)
- Methods **must** start with `test_`
- Methods **must** have `self` as first parameter

### 3.3. Why Use Classes?

1. **Organization**: Group related tests together
2. **Shared setup**: Can use class-level fixtures (covered in fixtures section)
3. **Readability**: Clear test structure

### 3.4. Running Class Tests

```bash
# Run all tests in a class
pytest basics/test_group.py::TestLogin -v

# Run a specific test method
pytest basics/test_group.py::TestLogin::test_valid_login -v
```

---

## 4. Running Tests

### 4.1. Basic Commands

```bash
# Run all tests in basics folder
pytest basics/ -v

# Run a specific file
pytest basics/test_eg.py -v

# Run with verbose output and show print statements
pytest basics/ -v -s

# Run tests matching a pattern
pytest basics/ -k "login" -v
```

### 4.2. Understanding Test Output

**Passing test**:
```
basics/test_eg.py::testLogin PASSED                    [100%]
```

**Failing test**:
```
basics/test_assertions_basic.py::test_example FAILED   [100%]
```

**Test symbols**:
- `.` = Test passed
- `F` = Test failed
- `s` = Test skipped
- `x` = Expected failure (xfail)

### 4.3. Useful Options

| Option | Description | Example |
|--------|-------------|---------|
| `-v` | Verbose (show test names) | `pytest -v` |
| `-s` | Show print output | `pytest -s` |
| `-k` | Run tests matching pattern | `pytest -k "login"` |
| `-x` | Stop on first failure | `pytest -x` |
| `--lf` | Run last failed tests | `pytest --lf` |
| `--ff` | Run failures first | `pytest --ff` |

---

## 5. Best Practices for Beginners

### 5.1. Test Naming

✅ **Good names** (descriptive):
```python
def test_user_can_login_with_valid_credentials():
    pass

def test_addition_returns_correct_sum():
    pass
```

❌ **Bad names** (vague):
```python
def test_1():
    pass

def test_stuff():
    pass
```

### 5.2. One Assertion Per Test (Guideline)

While not a strict rule, it's often clearer to test one thing at a time:

✅ **Good** (focused):
```python
def test_addition():
    assert 2 + 2 == 4

def test_subtraction():
    assert 5 - 3 == 2
```

❌ **Less clear** (multiple unrelated assertions):
```python
def test_math():
    assert 2 + 2 == 4
    assert 5 - 3 == 2
    assert 3 * 3 == 9
    assert 10 / 2 == 5
```

### 5.3. Test Independence

Each test should be independent and not rely on other tests:

✅ **Good** (independent):
```python
def test_create_user():
    user = create_user("Alice")
    assert user.name == "Alice"

def test_delete_user():
    user = create_user("Bob")
    delete_user(user)
    assert user_exists("Bob") is False
```

❌ **Bad** (dependent):
```python
# Don't do this - test_delete depends on test_create running first
def test_create_user():
    global user
    user = create_user("Alice")

def test_delete_user():
    delete_user(user)  # Assumes test_create ran first
```

### 5.4. Descriptive Failure Messages

You can add custom messages to assertions:

```python
def test_user_age():
    age = get_user_age("Alice")
    assert age >= 18, f"User must be 18 or older, got {age}"
```

When this fails:
```
AssertionError: User must be 18 or older, got 16
```

---

## 6. Common Patterns

### 6.1. Testing Functions

```python
# Code being tested (in a separate module)
def add(a, b):
    return a + b

# Test
def test_add():
    result = add(2, 3)
    assert result == 5
```

### 6.2. Testing with Multiple Cases

```python
def test_is_even():
    assert is_even(2) is True
    assert is_even(4) is True
    assert is_even(1) is False
    assert is_even(3) is False
```

### 6.3. Testing Exceptions (Preview)

```python
import pytest

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0
```

(More on exceptions in the [exceptions](../exceptions/) section)

---

## Summary

### Key Takeaways

1. **Simple syntax**: Just use `assert` - no special methods needed
2. **Automatic discovery**: Name files `test_*.py` and functions `test_*`
3. **Clear output**: Pytest shows exactly what failed and why
4. **Flexible organization**: Use functions or classes to organize tests
5. **Easy to run**: `pytest` command finds and runs all tests

### What's Next?

Now that you understand the basics, explore:

- **[Fixtures](../fixtures/)** - Reusable setup and teardown
- **[Markers](../markers/)** - Skip tests, mark as slow, etc.
- **[Parametrize](../parametrize/)** - Run same test with different inputs
- **[Exceptions](../exceptions/)** - Test error handling

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all basic tests
pytest basics/ -v

# Run a specific file
pytest basics/test_eg.py -v
pytest basics/test_assertions_basic.py -v
pytest basics/test_group.py -v

# Run with output visible
pytest basics/ -v -s
```

---

[← Back to Main Guide](../README.md)

