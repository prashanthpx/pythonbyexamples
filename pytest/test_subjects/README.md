# Test Subjects - Code Under Test

[← Back to Main Guide](../README.md)

> **Location**: `pytest/test_subjects/`  
> **Purpose**: Contains the actual code being tested and their test files

---

## Table of Contents

1. [What is This Folder?](#1-what-is-this-folder)
2. [Calculator Module](#2-calculator-module)
3. [String Utils Module](#3-string-utils-module)
4. [Testing Patterns](#4-testing-patterns)

---

## 1. What is This Folder?

This folder contains **code under test** (also called "subject code" or "system under test") along with their test files.

### Purpose

In real projects, you typically have:
- **Source code**: The actual application code (e.g., `src/`, `app/`, `lib/`)
- **Test code**: Tests for the source code (e.g., `tests/`, `test_*/`)

For learning pytest, we keep simple example modules here along with their tests to demonstrate:
- How to structure tests for real code
- Different testing approaches (basic tests vs. fixture-based tests)
- How to test different types of functions

### Files in This Folder

| File | Type | Description |
|------|------|-------------|
| `calculator.py` | Source | Simple calculator with add, subtract, multiply, divide |
| `test_calculator.py` | Tests | Basic tests for calculator |
| `test_calculator_fixtures.py` | Tests | Calculator tests using fixtures |
| `string_utils.py` | Source | String utility functions |
| `test_string_utils.py` | Tests | Tests for string utilities |

---

## 2. Calculator Module

### 2.1. The Code

**File**: `calculator.py`

```python
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    return a / b
```

### 2.2. Basic Tests

**File**: `test_calculator.py`

Simple, straightforward tests:

```python
from calculator import add, subtract, multiply, divide

def test_add():
    """Test addition."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    """Test subtraction."""
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    """Test multiplication."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    """Test division."""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
```

### 2.3. Fixture-Based Tests

**File**: `test_calculator_fixtures.py`

Same tests but using fixtures for test data:

```python
import pytest
from calculator import add, subtract, multiply, divide

@pytest.fixture
def numbers():
    """Provide test numbers."""
    return {"a": 10, "b": 5}

def test_add_with_fixture(numbers):
    """Test addition using fixture."""
    result = add(numbers["a"], numbers["b"])
    assert result == 15

def test_subtract_with_fixture(numbers):
    """Test subtraction using fixture."""
    result = subtract(numbers["a"], numbers["b"])
    assert result == 5

def test_multiply_with_fixture(numbers):
    """Test multiplication using fixture."""
    result = multiply(numbers["a"], numbers["b"])
    assert result == 50

def test_divide_with_fixture(numbers):
    """Test division using fixture."""
    result = divide(numbers["a"], numbers["b"])
    assert result == 2.0
```

### 2.4. Comparison: Basic vs Fixture

| Approach | Pros | Cons |
|----------|------|------|
| **Basic** | Simple, direct, easy to read | Duplicates test data |
| **Fixture** | Reusable data, DRY principle | Slightly more complex |

**When to use each:**
- **Basic tests**: For simple, one-off tests
- **Fixture tests**: When you need the same data in multiple tests

---

## 3. String Utils Module

### 3.1. The Code

**File**: `string_utils.py`

```python
def to_upper(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()

def to_lower(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()

def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome."""
    normalized = text.strip().lower()
    return normalized == normalized[::-1]

def contains_substring(text: str, sub: str) -> bool:
    """Check if text contains substring."""
    return sub in text
```

### 3.2. Tests

**File**: `test_string_utils.py`

```python
from string_utils import to_upper, to_lower, is_palindrome, contains_substring

def test_to_upper():
    """Test uppercase conversion."""
    assert to_upper("hello") == "HELLO"
    assert to_upper("Hello World") == "HELLO WORLD"

def test_to_lower():
    """Test lowercase conversion."""
    assert to_lower("HELLO") == "hello"
    assert to_lower("Hello World") == "hello world"

def test_is_palindrome():
    """Test palindrome detection."""
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("A man a plan a canal Panama") is False  # Has spaces
    assert is_palindrome("  racecar  ") is True  # Strips spaces

def test_contains_substring():
    """Test substring detection."""
    assert contains_substring("hello world", "world") is True
    assert contains_substring("hello world", "foo") is False
```

---

## 4. Testing Patterns

### 4.1. Arrange-Act-Assert (AAA)

Most tests follow the AAA pattern:

```python
def test_example():
    # ARRANGE: Set up test data
    a = 10
    b = 5

    # ACT: Call the function being tested
    result = add(a, b)

    # ASSERT: Verify the result
    assert result == 15
```

### 4.2. Multiple Assertions

You can have multiple assertions in one test:

```python
def test_add_multiple_cases():
    """Test addition with multiple cases."""
    # Positive numbers
    assert add(2, 3) == 5

    # Negative numbers
    assert add(-1, -1) == -2

    # Mixed
    assert add(-5, 10) == 5

    # Zero
    assert add(0, 0) == 0
```

**Pros**: Fewer test functions
**Cons**: If one assertion fails, the rest don't run

### 4.3. Parametrize for Multiple Cases

Better approach for multiple test cases:

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, -1, -2),
    (-5, 10, 5),
    (0, 0, 0),
])
def test_add_parametrized(a, b, expected):
    """Test addition with parametrize."""
    assert add(a, b) == expected
```

**Pros**: Each case runs independently, clear test output
**Cons**: Slightly more complex syntax

### 4.4. Testing Edge Cases

Always test edge cases:

```python
def test_divide_edge_cases():
    """Test division edge cases."""
    # Normal case
    assert divide(10, 2) == 5

    # Division by 1
    assert divide(10, 1) == 10

    # Negative numbers
    assert divide(-10, 2) == -5

    # Floating point
    assert divide(7, 2) == 3.5

def test_divide_by_zero():
    """Test that division by zero raises error."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### 4.5. Testing String Functions

String tests often check:
- Empty strings
- Single characters
- Special characters
- Unicode
- Whitespace

```python
def test_to_upper_edge_cases():
    """Test uppercase conversion edge cases."""
    # Empty string
    assert to_upper("") == ""

    # Already uppercase
    assert to_upper("HELLO") == "HELLO"

    # Numbers and symbols
    assert to_upper("hello123!") == "HELLO123!"

    # Unicode
    assert to_upper("café") == "CAFÉ"
```

---

## 5. Real-World Testing Tips

### 5.1. Test One Thing at a Time

✅ **Good** (focused test):
```python
def test_add_positive_numbers():
    """Test adding positive numbers."""
    assert add(2, 3) == 5

def test_add_negative_numbers():
    """Test adding negative numbers."""
    assert add(-2, -3) == -5
```

❌ **Bad** (testing too much):
```python
def test_all_calculator_functions():
    """Test everything."""
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(2, 3) == 6
    assert divide(6, 2) == 3
```

### 5.2. Use Descriptive Test Names

✅ **Good**:
```python
def test_add_returns_sum_of_two_positive_numbers():
    assert add(2, 3) == 5

def test_divide_raises_error_when_divisor_is_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

❌ **Bad**:
```python
def test_1():
    assert add(2, 3) == 5

def test_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### 5.3. Test Both Success and Failure

Always test both paths:

```python
# Success path
def test_is_palindrome_returns_true_for_palindrome():
    assert is_palindrome("racecar") is True

# Failure path
def test_is_palindrome_returns_false_for_non_palindrome():
    assert is_palindrome("hello") is False
```

### 5.4. Don't Test Implementation Details

✅ **Good** (test behavior):
```python
def test_is_palindrome_ignores_case():
    """Test that palindrome check is case-insensitive."""
    assert is_palindrome("Racecar") is True
```

❌ **Bad** (test implementation):
```python
def test_is_palindrome_calls_lower():
    """Don't test internal implementation."""
    # This is too coupled to implementation
    pass
```

### 5.5. Keep Tests Independent

Each test should be able to run alone:

✅ **Good**:
```python
def test_add():
    result = add(2, 3)
    assert result == 5

def test_subtract():
    result = subtract(5, 2)
    assert result == 3
```

❌ **Bad**:
```python
result = None

def test_add():
    global result
    result = add(2, 3)
    assert result == 5

def test_use_previous_result():
    # Depends on test_add running first!
    assert result == 5
```

---

## 6. Summary

### Key Takeaways

1. **Test subjects**: The actual code being tested
2. **Test files**: Start with `test_` and test the subject code
3. **AAA pattern**: Arrange, Act, Assert
4. **Edge cases**: Always test boundary conditions
5. **Independence**: Tests should not depend on each other
6. **Descriptive names**: Test names should describe what they test
7. **One thing**: Each test should test one specific behavior

### Testing Checklist

When writing tests, ask yourself:

- [ ] Does the test have a clear, descriptive name?
- [ ] Does it test one specific behavior?
- [ ] Does it follow the AAA pattern?
- [ ] Have I tested edge cases?
- [ ] Have I tested both success and failure paths?
- [ ] Is the test independent of other tests?
- [ ] Would someone else understand what this test does?

### What's Next?

- **[Parametrize](../parametrize/)** - Test multiple cases efficiently
- **[Exceptions](../exceptions/)** - Test error handling
- **[Fixtures](../fixtures/)** - Reusable test setup

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all test_subjects tests
pytest test_subjects/ -v

# Run specific test file
pytest test_subjects/test_calculator.py -v
pytest test_subjects/test_calculator_fixtures.py -v
pytest test_subjects/test_string_utils.py -v

# Run with output visible
pytest test_subjects/ -v -s
```

---

[← Back to Main Guide](../README.md)

