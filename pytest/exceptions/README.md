# Pytest Exceptions - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/exceptions/`  
> **Test Files**: All exception-related examples are in this folder

---

## Table of Contents

1. [Testing Exceptions with pytest.raises](#1-testing-exceptions-with-pytestRaises)
2. [Basic Exception Testing](#2-basic-exception-testing)
3. [Inspecting Exception Details](#3-inspecting-exception-details)
4. [Testing Exception Messages](#4-testing-exception-messages)
5. [Custom Exceptions](#5-custom-exceptions)
6. [pytest.fail and pytest.xfail](#6-pytestfail-and-pytestxfail)
7. [Expected Failures](#7-expected-failures)

---

## 1. Testing Exceptions with pytest.raises

In Python, exceptions are a normal part of code flow. Good tests verify that your code raises the **right exceptions** at the **right times**.

### Why Test Exceptions?

1. **Validate error handling**: Ensure your code fails gracefully
2. **Document expected behavior**: Show what inputs are invalid
3. **Prevent regressions**: Ensure error handling doesn't break
4. **API contracts**: Define what exceptions callers should expect

### The pytest.raises Context Manager

Pytest provides `pytest.raises()` to test that code raises an exception:

```python
import pytest

def test_division_by_zero():
    """Test that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0
```

**How it works**:
1. Code inside the `with` block is expected to raise the specified exception
2. If the exception is raised, the test **passes**
3. If no exception is raised, the test **fails**
4. If a different exception is raised, the test **fails**

---

## 2. Basic Exception Testing

**File**: `test_exceptions_context_manager.py`

### 2.1. Testing Built-in Exceptions

```python
import pytest

def test_zero_division():
    """Test ZeroDivisionError is raised."""
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_type_error():
    """Test TypeError is raised."""
    with pytest.raises(TypeError):
        "string" + 123  # Can't add string and int

def test_value_error():
    """Test ValueError is raised."""
    with pytest.raises(ValueError):
        int("not a number")

def test_key_error():
    """Test KeyError is raised."""
    with pytest.raises(KeyError):
        d = {"a": 1}
        value = d["b"]  # Key doesn't exist

def test_index_error():
    """Test IndexError is raised."""
    with pytest.raises(IndexError):
        lst = [1, 2, 3]
        value = lst[10]  # Index out of range
```

### 2.2. Testing Function Exceptions

```python
def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero_raises_value_error():
    """Test that divide() raises ValueError for zero divisor."""
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_normal_case():
    """Test that divide() works normally."""
    result = divide(10, 2)
    assert result == 5
```

### 2.3. What Happens if Exception is NOT Raised?

```python
def test_expecting_exception_but_none_raised():
    """This test will FAIL because no exception is raised."""
    with pytest.raises(ValueError):
        result = 2 + 2  # No exception here!
```

**Output**:
```
Failed: DID NOT RAISE <class 'ValueError'>
```

---

## 3. Inspecting Exception Details

You can capture the exception object to inspect its details.

**File**: `test_exceptions_context_manager.py`

### 3.1. Capturing Exception Info

```python
import pytest

def test_exception_info():
    """Capture exception to inspect its details."""
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("Something went wrong")
    
    # exc_info.value is the actual exception object
    assert str(exc_info.value) == "Something went wrong"
    assert exc_info.type == ValueError
```

### 3.2. Accessing Exception Attributes

```python
class CustomError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

def test_custom_exception_attributes():
    """Test custom exception attributes."""
    with pytest.raises(CustomError) as exc_info:
        raise CustomError("Error occurred", code=404)
    
    # Access custom attributes
    assert exc_info.value.code == 404
    assert str(exc_info.value) == "Error occurred"
```

### 3.3. Inspecting Traceback

```python
def test_exception_traceback():
    """Inspect exception traceback."""
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("Test error")
    
    # exc_info.traceback contains traceback information
    assert exc_info.traceback is not None
```

---

## 4. Testing Exception Messages

Often you want to verify not just that an exception is raised, but also that it has the correct message.

**File**: `test_exceptions_custom_raises.py`

### 4.1. Exact Message Match

```python
import pytest

def validate_age(age):
    """Validate age is positive."""
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age cannot exceed 150")
    return age

def test_negative_age_message():
    """Test exact error message for negative age."""
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    
    assert str(exc_info.value) == "Age cannot be negative"

def test_excessive_age_message():
    """Test exact error message for excessive age."""
    with pytest.raises(ValueError) as exc_info:
        validate_age(200)
    
    assert str(exc_info.value) == "Age cannot exceed 150"
```

### 4.2. Partial Message Match

Sometimes you only care that the message contains certain text:

```python
def test_error_message_contains_text():
    """Test that error message contains specific text."""
    with pytest.raises(ValueError) as exc_info:
        validate_age(-10)

    # Check message contains "negative"
    assert "negative" in str(exc_info.value)
```

### 4.3. Using match Parameter

Pytest provides a `match` parameter for regex matching:

```python
def test_error_message_with_match():
    """Test error message using regex match."""
    with pytest.raises(ValueError, match="Age cannot be negative"):
        validate_age(-5)

def test_error_message_regex():
    """Test error message with regex pattern."""
    with pytest.raises(ValueError, match=r"Age cannot (be negative|exceed 150)"):
        validate_age(-5)
```

**Benefits of `match`**:
- More concise than capturing and asserting
- Uses regex for flexible matching
- Fails immediately if message doesn't match

### 4.4. Case-Insensitive Match

```python
def test_case_insensitive_match():
    """Test error message case-insensitively."""
    with pytest.raises(ValueError, match=r"(?i)age"):  # (?i) = case-insensitive
        validate_age(-5)
```

---

## 5. Custom Exceptions

Testing custom exceptions works the same way as built-in exceptions.

**File**: `test_exceptions_custom_raises.py`

### 5.1. Simple Custom Exception

```python
import pytest

class InvalidUserError(Exception):
    """Raised when user data is invalid."""
    pass

def create_user(name, age):
    """Create a user with validation."""
    if not name:
        raise InvalidUserError("Name cannot be empty")
    if age < 18:
        raise InvalidUserError("User must be 18 or older")
    return {"name": name, "age": age}

def test_empty_name_raises_invalid_user_error():
    """Test that empty name raises InvalidUserError."""
    with pytest.raises(InvalidUserError):
        create_user("", 25)

def test_underage_raises_invalid_user_error():
    """Test that underage raises InvalidUserError."""
    with pytest.raises(InvalidUserError, match="must be 18 or older"):
        create_user("Alice", 16)
```

### 5.2. Custom Exception with Attributes

```python
class ValidationError(Exception):
    """Exception with additional context."""
    def __init__(self, message, field, value):
        super().__init__(message)
        self.field = field
        self.value = value

def validate_email(email):
    """Validate email format."""
    if "@" not in email:
        raise ValidationError(
            "Invalid email format",
            field="email",
            value=email
        )
    return email

def test_invalid_email_exception():
    """Test invalid email raises ValidationError with correct attributes."""
    with pytest.raises(ValidationError) as exc_info:
        validate_email("invalid-email")

    # Check exception attributes
    assert exc_info.value.field == "email"
    assert exc_info.value.value == "invalid-email"
    assert "Invalid email format" in str(exc_info.value)
```

### 5.3. Exception Hierarchy

```python
class DatabaseError(Exception):
    """Base exception for database errors."""
    pass

class ConnectionError(DatabaseError):
    """Database connection failed."""
    pass

class QueryError(DatabaseError):
    """Database query failed."""
    pass

def test_specific_exception():
    """Test for specific exception type."""
    with pytest.raises(ConnectionError):
        raise ConnectionError("Cannot connect to database")

def test_base_exception_catches_subclass():
    """Test that base exception catches subclass."""
    with pytest.raises(DatabaseError):  # Catches any DatabaseError subclass
        raise ConnectionError("Cannot connect")
```

---

## 6. pytest.fail and pytest.xfail

Pytest provides functions to explicitly fail or mark tests as expected failures.

**File**: `test_exceptions_failure_control.py`

### 6.1. pytest.fail - Explicitly Fail a Test

```python
import pytest

def test_explicit_failure():
    """Explicitly fail a test with a message."""
    if some_condition():
        pytest.fail("This condition should not be true")

def test_conditional_failure():
    """Fail test based on runtime condition."""
    result = complex_calculation()
    if result < 0:
        pytest.fail(f"Result should be positive, got {result}")
```

**When to use `pytest.fail`**:
- Complex validation that can't be expressed as simple assertion
- Want to provide detailed failure message
- Conditional failure based on runtime state

### 6.2. pytest.xfail - Mark Test as Expected Failure

```python
def test_known_bug():
    """Test for known bug - expected to fail."""
    if is_known_bug_present():
        pytest.xfail("Known bug #123 - fix in progress")

    # Test continues only if bug is fixed
    assert buggy_function() == expected_value

def test_feature_not_implemented():
    """Test for feature not yet implemented."""
    pytest.xfail("Feature not implemented yet")
    assert new_feature() == expected_result
```

**Difference between decorator and function**:

```python
# Decorator: Always marks test as xfail
@pytest.mark.xfail(reason="known bug")
def test_with_decorator():
    assert buggy_function() == expected

# Function: Conditionally marks as xfail at runtime
def test_with_function():
    if condition:
        pytest.xfail("reason")
    assert something()
```

### 6.3. pytest.fail vs assert

```python
# Using assert (preferred for simple checks)
def test_with_assert():
    result = calculate()
    assert result > 0, f"Result should be positive, got {result}"

# Using pytest.fail (for complex logic)
def test_with_fail():
    result = calculate()
    if result <= 0:
        pytest.fail(f"Result should be positive, got {result}")

    # More complex validation
    if result > 100:
        pytest.fail(f"Result too large: {result}")
```

**Guideline**: Use `assert` for simple checks, `pytest.fail` for complex conditional failures.

---

## 7. Expected Failures

Understanding the difference between skip, xfail, and fail.

### 7.1. Test Outcomes

| Outcome | Meaning | How to Achieve |
|---------|---------|----------------|
| **PASSED** | Test succeeded | Assertions pass |
| **FAILED** | Test failed | Assertion fails or exception raised |
| **SKIPPED** | Test didn't run | `@pytest.mark.skip` or `pytest.skip()` |
| **XFAIL** | Expected to fail, and did fail | `@pytest.mark.xfail` or `pytest.xfail()` |
| **XPASS** | Expected to fail, but passed | Test marked xfail but passed |

### 7.2. When to Use Each

**SKIP**: Test can't run in current environment
```python
@pytest.mark.skip(reason="requires database")
def test_database_query():
    pass
```

**XFAIL**: Test documents known bug or unfinished feature
```python
@pytest.mark.xfail(reason="known bug #123")
def test_buggy_feature():
    assert buggy_function() == expected
```

**FAIL**: Test found a real problem
```python
def test_something():
    assert actual == expected  # Fails if not equal
```

### 7.3. Strict XFail

You can make xfail strict - if test passes when expected to fail, it fails:

```python
@pytest.mark.xfail(strict=True, reason="must fail")
def test_strict_xfail():
    """If this passes, the test suite fails."""
    assert False  # Expected to fail
```

**Use case**: Ensure you remove xfail marker once bug is fixed.

---

## 8. Advanced Exception Testing

### 8.1. Multiple Exceptions

Test that code can raise different exceptions:

```python
def process_data(data):
    """Process data with multiple validation checks."""
    if data is None:
        raise ValueError("Data cannot be None")
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    if "id" not in data:
        raise KeyError("Data must have 'id' field")
    return data

def test_none_data():
    """Test ValueError for None data."""
    with pytest.raises(ValueError, match="cannot be None"):
        process_data(None)

def test_wrong_type():
    """Test TypeError for wrong data type."""
    with pytest.raises(TypeError, match="must be a dictionary"):
        process_data("not a dict")

def test_missing_field():
    """Test KeyError for missing field."""
    with pytest.raises(KeyError, match="must have 'id'"):
        process_data({"name": "Alice"})
```

### 8.2. Exception Chaining

Test exception chains (Python 3's `raise ... from ...`):

```python
def outer_function():
    """Function that catches and re-raises."""
    try:
        inner_function()
    except ValueError as e:
        raise RuntimeError("Outer error") from e

def inner_function():
    """Function that raises original error."""
    raise ValueError("Inner error")

def test_exception_chain():
    """Test exception chaining."""
    with pytest.raises(RuntimeError) as exc_info:
        outer_function()

    # Check the raised exception
    assert str(exc_info.value) == "Outer error"

    # Check the original exception
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ValueError)
    assert str(exc_info.value.__cause__) == "Inner error"
```

### 8.3. Testing Exception in Loops

```python
def test_multiple_exceptions_in_loop():
    """Test that each iteration raises exception."""
    invalid_inputs = ["", None, 123, []]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            validate_string(invalid_input)
```

**Better approach with parametrize**:
```python
@pytest.mark.parametrize("invalid_input", ["", None, 123, []])
def test_invalid_inputs_raise_error(invalid_input):
    """Test each invalid input separately."""
    with pytest.raises(ValueError):
        validate_string(invalid_input)
```

---

## 9. Common Patterns and Best Practices

### 9.1. Test Both Success and Failure

Always test both the happy path and error cases:

```python
def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Test success case
def test_divide_success():
    """Test normal division."""
    assert divide(10, 2) == 5

# Test failure case
def test_divide_by_zero():
    """Test division by zero raises error."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### 9.2. Specific Exception Types

Always test for the most specific exception type:

✅ **Good** (specific):
```python
def test_specific_exception():
    with pytest.raises(ValueError):  # Specific exception
        int("not a number")
```

❌ **Bad** (too broad):
```python
def test_broad_exception():
    with pytest.raises(Exception):  # Too broad!
        int("not a number")
```

### 9.3. Test Exception Messages

Test exception messages to ensure good error reporting:

```python
def test_exception_with_helpful_message():
    """Test that exception has helpful message."""
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)

    # Ensure message is helpful
    message = str(exc_info.value)
    assert "negative" in message.lower()
    assert "-5" in message  # Includes the actual value
```

### 9.4. Don't Catch Too Much Code

Keep the `with pytest.raises()` block minimal:

✅ **Good** (minimal code in block):
```python
def test_exception_minimal():
    # Setup outside the block
    user = create_user("Alice", 25)

    # Only the code that should raise exception
    with pytest.raises(ValueError):
        user.set_age(-5)

    # Verification outside the block
    assert user.age == 25  # Age unchanged
```

❌ **Bad** (too much code in block):
```python
def test_exception_too_much():
    with pytest.raises(ValueError):
        user = create_user("Alice", 25)  # Might raise unexpected exception
        user.set_age(-5)
        # If exception raised here, we don't know which line caused it
```

### 9.5. Use match for Better Errors

Using `match` gives better error messages:

```python
# Without match - less clear
def test_without_match():
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    assert "negative" in str(exc_info.value)

# With match - clearer and more concise
def test_with_match():
    with pytest.raises(ValueError, match="negative"):
        validate_age(-5)
```

If the message doesn't match, pytest shows:
```
AssertionError: Pattern 'negative' does not match 'Age must be positive'
```

---

## 10. Real-World Examples

### 10.1. API Validation

```python
class APIError(Exception):
    """Base exception for API errors."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

class NotFoundError(APIError):
    """Resource not found."""
    def __init__(self, resource):
        super().__init__(f"{resource} not found", 404)
        self.resource = resource

class UnauthorizedError(APIError):
    """Unauthorized access."""
    def __init__(self):
        super().__init__("Unauthorized", 401)

def get_user(user_id, token):
    """Get user by ID."""
    if not token:
        raise UnauthorizedError()
    if user_id not in database:
        raise NotFoundError(f"User {user_id}")
    return database[user_id]

def test_get_user_unauthorized():
    """Test that missing token raises UnauthorizedError."""
    with pytest.raises(UnauthorizedError) as exc_info:
        get_user(123, token=None)

    assert exc_info.value.status_code == 401

def test_get_user_not_found():
    """Test that invalid user ID raises NotFoundError."""
    with pytest.raises(NotFoundError) as exc_info:
        get_user(999, token="valid-token")

    assert exc_info.value.status_code == 404
    assert exc_info.value.resource == "User 999"
```

### 10.2. File Operations

```python
def read_config(filename):
    """Read configuration file."""
    if not filename.endswith('.json'):
        raise ValueError("Config file must be JSON")

    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {filename}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filename}: {e}")

def test_config_wrong_extension():
    """Test that non-JSON file raises ValueError."""
    with pytest.raises(ValueError, match="must be JSON"):
        read_config("config.txt")

def test_config_file_not_found():
    """Test that missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="not found"):
        read_config("nonexistent.json")

def test_config_invalid_json(tmp_path):
    """Test that invalid JSON raises ValueError."""
    # Create invalid JSON file
    config_file = tmp_path / "config.json"
    config_file.write_text("{invalid json}")

    with pytest.raises(ValueError, match="Invalid JSON"):
        read_config(str(config_file))
```

### 10.3. Database Operations

```python
class DatabaseError(Exception):
    """Database operation failed."""
    pass

def save_user(user, db):
    """Save user to database."""
    if not user.get("id"):
        raise ValueError("User must have an ID")

    if not db.is_connected():
        raise DatabaseError("Database not connected")

    try:
        db.insert("users", user)
    except Exception as e:
        raise DatabaseError(f"Failed to save user: {e}")

def test_save_user_no_id():
    """Test that user without ID raises ValueError."""
    with pytest.raises(ValueError, match="must have an ID"):
        save_user({"name": "Alice"}, db=mock_db)

def test_save_user_db_not_connected():
    """Test that disconnected DB raises DatabaseError."""
    db = MockDatabase(connected=False)

    with pytest.raises(DatabaseError, match="not connected"):
        save_user({"id": 1, "name": "Alice"}, db)
```

---

## 11. Summary

### Key Takeaways

1. **pytest.raises**: Context manager to test that code raises exceptions
2. **Capture exception**: Use `as exc_info` to inspect exception details
3. **Match messages**: Use `match` parameter for regex matching
4. **Custom exceptions**: Test custom exceptions the same way as built-in ones
5. **pytest.fail**: Explicitly fail a test with a message
6. **pytest.xfail**: Mark test as expected to fail
7. **Be specific**: Test for specific exception types, not broad ones
8. **Test messages**: Verify exception messages are helpful
9. **Minimal blocks**: Keep code in `with pytest.raises()` minimal

### Common Patterns

```python
# Basic exception test
with pytest.raises(ValueError):
    function_that_raises()

# With message matching
with pytest.raises(ValueError, match="specific message"):
    function_that_raises()

# Capture and inspect
with pytest.raises(ValueError) as exc_info:
    function_that_raises()
assert exc_info.value.code == 404

# Explicit failure
if condition:
    pytest.fail("Reason for failure")

# Expected failure
pytest.xfail("Known bug #123")
```

### What's Next?

- **[Mocking](../mocking/)** - Mock objects and monkeypatch
- **[Fixtures](../fixtures/)** - Advanced fixture patterns
- **[Parametrize](../parametrize/)** - Test with multiple inputs

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all exception tests
pytest exceptions/ -v

# Run a specific file
pytest exceptions/test_exceptions_context_manager.py -v

# Run with output visible
pytest exceptions/ -v -s
```

---

[← Back to Main Guide](../README.md)
