# Pytest Mocking - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/mocking/`  
> **Test Files**: All mocking-related examples are in this folder

---

## Table of Contents

1. [What is Mocking?](#1-what-is-mocking)
2. [Monkeypatch - Pytest's Built-in Mocking](#2-monkeypatch---pytests-built-in-mocking)
3. [pytest-mock (mocker fixture)](#3-pytest-mock-mocker-fixture)
4. [Mocking Functions](#4-mocking-functions)
5. [Mocking Classes and Methods](#5-mocking-classes-and-methods)
6. [Mocking Environment Variables](#6-mocking-environment-variables)
7. [Mocking Attributes](#7-mocking-attributes)
8. [Verifying Mock Calls](#8-verifying-mock-calls)

---

## 1. What is Mocking?

**Mocking** is the practice of replacing real objects with fake ones during testing. This allows you to:

- **Isolate code under test**: Test one component without depending on others
- **Control behavior**: Make external dependencies return specific values
- **Avoid side effects**: Don't send real emails, make real API calls, or modify databases
- **Speed up tests**: Skip slow operations like network calls or file I/O
- **Test error conditions**: Simulate failures that are hard to reproduce

### When to Use Mocking

✅ **Good use cases**:
- External API calls
- Database operations
- File system operations
- Email sending
- Time-dependent code
- Random number generation

❌ **Don't mock**:
- Simple functions you control
- Data structures (lists, dicts)
- Your own business logic (test it for real!)

### Two Approaches in Pytest

1. **monkeypatch**: Pytest's built-in fixture for simple mocking
2. **mocker**: From pytest-mock plugin, provides full Mock functionality

---

## 2. Monkeypatch - Pytest's Built-in Mocking

**Monkeypatch** is a pytest fixture that allows you to modify or replace objects during testing.

**File**: `test_mock_monkeypatch.py`

### 2.1. Basic Monkeypatch

```python
import pytest

def get_username():
    """Get username from environment."""
    import os
    return os.getenv("USER", "unknown")

def test_get_username_with_monkeypatch(monkeypatch):
    """Test with mocked environment variable."""
    # Set environment variable for this test only
    monkeypatch.setenv("USER", "testuser")
    
    assert get_username() == "testuser"
    
# After test, environment is restored automatically
```

### 2.2. Monkeypatch Methods

| Method | Description | Example |
|--------|-------------|---------|
| `setattr(obj, name, value)` | Set attribute | `monkeypatch.setattr(module, "func", mock_func)` |
| `delattr(obj, name)` | Delete attribute | `monkeypatch.delattr(module, "func")` |
| `setitem(dict, key, value)` | Set dictionary item | `monkeypatch.setitem(os.environ, "KEY", "value")` |
| `delitem(dict, key)` | Delete dictionary item | `monkeypatch.delitem(os.environ, "KEY")` |
| `setenv(name, value)` | Set environment variable | `monkeypatch.setenv("PATH", "/usr/bin")` |
| `delenv(name)` | Delete environment variable | `monkeypatch.delenv("DEBUG")` |
| `syspath_prepend(path)` | Prepend to sys.path | `monkeypatch.syspath_prepend("/tmp")` |
| `chdir(path)` | Change directory | `monkeypatch.chdir("/tmp")` |

### 2.3. Mocking Functions

```python
# Module: api.py
def fetch_data():
    """Fetch data from external API."""
    import requests
    response = requests.get("https://api.example.com/data")
    return response.json()

# Test
def test_fetch_data_mocked(monkeypatch):
    """Test with mocked API call."""
    def mock_fetch():
        return {"status": "success", "data": [1, 2, 3]}
    
    # Replace the real function with mock
    monkeypatch.setattr("api.fetch_data", mock_fetch)
    
    result = fetch_data()
    assert result["status"] == "success"
    assert result["data"] == [1, 2, 3]
```

### 2.4. Mocking Methods

```python
class Database:
    def connect(self):
        """Connect to real database."""
        # Expensive operation
        return "real_connection"
    
    def query(self, sql):
        """Execute SQL query."""
        # Would hit real database
        return []

def test_database_mocked(monkeypatch):
    """Test with mocked database methods."""
    def mock_connect(self):
        return "mock_connection"
    
    def mock_query(self, sql):
        return [{"id": 1, "name": "Alice"}]
    
    # Mock the methods
    monkeypatch.setattr(Database, "connect", mock_connect)
    monkeypatch.setattr(Database, "query", mock_query)
    
    db = Database()
    assert db.connect() == "mock_connection"
    assert db.query("SELECT * FROM users") == [{"id": 1, "name": "Alice"}]
```

### 2.5. Mocking Imports

```python
# Module: weather.py
import requests

def get_weather(city):
    """Get weather for a city."""
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()

# Test
def test_get_weather_mocked(monkeypatch):
    """Test with mocked requests.get."""
    class MockResponse:
        def json(self):
            return {"temp": 72, "condition": "sunny"}
    
    def mock_get(url):
        return MockResponse()
    
    # Mock requests.get
    monkeypatch.setattr("requests.get", mock_get)
    
    result = get_weather("Boston")
    assert result["temp"] == 72
    assert result["condition"] == "sunny"
```

### 2.6. Automatic Cleanup

Monkeypatch automatically restores everything after the test:

```python
import os

def test_env_var_cleanup(monkeypatch):
    """Test that monkeypatch cleans up after test."""
    original_value = os.getenv("MY_VAR")
    
    # Set for this test
    monkeypatch.setenv("MY_VAR", "test_value")
    assert os.getenv("MY_VAR") == "test_value"
    
# After test, MY_VAR is restored to original_value automatically
```

---

## 3. pytest-mock (mocker fixture)

**pytest-mock** is a plugin that provides the `mocker` fixture, which wraps Python's `unittest.mock` library.

**Installation**:
```bash
pip install pytest-mock
```

**File**: `test_mock_mocker.py`

### 3.1. Basic Mocker Usage

```python
import pytest

def get_data():
    """Get data from external source."""
    import requests
    return requests.get("https://api.example.com").json()

def test_get_data_with_mocker(mocker):
    """Test with mocker fixture."""
    # Create a mock for requests.get
    mock_get = mocker.patch("requests.get")

    # Configure what the mock returns
    mock_get.return_value.json.return_value = {"status": "ok"}

    result = get_data()
    assert result == {"status": "ok"}

    # Verify the mock was called
    mock_get.assert_called_once()
```

### 3.2. mocker.patch

The most common mocker method is `patch()`:

```python
def test_with_patch(mocker):
    """Test using mocker.patch."""
    # Patch a function
    mock_func = mocker.patch("module.function_name")

    # Set return value
    mock_func.return_value = "mocked result"

    # Call code that uses the function
    result = module.function_name()

    assert result == "mocked result"
    mock_func.assert_called_once()
```

### 3.3. Return Values

```python
def test_mock_return_values(mocker):
    """Test different return value configurations."""
    mock = mocker.patch("module.func")

    # Simple return value
    mock.return_value = 42
    assert module.func() == 42

    # Different values for multiple calls
    mock.side_effect = [1, 2, 3]
    assert module.func() == 1
    assert module.func() == 2
    assert module.func() == 3

    # Raise exception
    mock.side_effect = ValueError("error")
    with pytest.raises(ValueError):
        module.func()
```

### 3.4. Mocking Class Methods

```python
class UserService:
    def get_user(self, user_id):
        """Get user from database."""
        # Real database call
        return database.query(f"SELECT * FROM users WHERE id={user_id}")

    def create_user(self, name):
        """Create new user."""
        # Real database insert
        return database.insert("users", {"name": name})

def test_user_service_mocked(mocker):
    """Test UserService with mocked methods."""
    # Mock the get_user method
    mock_get = mocker.patch.object(UserService, "get_user")
    mock_get.return_value = {"id": 1, "name": "Alice"}

    service = UserService()
    user = service.get_user(1)

    assert user["name"] == "Alice"
    mock_get.assert_called_once_with(1)
```

### 3.5. Mocking Entire Classes

```python
def test_mock_entire_class(mocker):
    """Test with entire class mocked."""
    # Mock the entire Database class
    MockDatabase = mocker.patch("module.Database")

    # Configure the mock instance
    mock_instance = MockDatabase.return_value
    mock_instance.query.return_value = [{"id": 1}]

    # Code that creates Database instance
    db = Database()
    result = db.query("SELECT * FROM users")

    assert result == [{"id": 1}]
    MockDatabase.assert_called_once()
    mock_instance.query.assert_called_once_with("SELECT * FROM users")
```

### 3.6. Spy - Partial Mocking

Sometimes you want to call the real function but also track calls:

```python
def real_function(x):
    """Real function that does actual work."""
    return x * 2

def test_spy_on_function(mocker):
    """Test using spy to track real function calls."""
    # Spy on the function (calls real function but tracks calls)
    spy = mocker.spy(module, "real_function")

    result = real_function(5)

    # Real function was called
    assert result == 10

    # But we can verify it was called
    spy.assert_called_once_with(5)
```

---

## 4. Mocking Functions

### 4.1. Mocking Built-in Functions

```python
import time

def wait_and_return():
    """Wait 5 seconds and return."""
    time.sleep(5)
    return "done"

def test_mock_sleep(mocker):
    """Test without actually sleeping."""
    mock_sleep = mocker.patch("time.sleep")

    result = wait_and_return()

    assert result == "done"
    mock_sleep.assert_called_once_with(5)
    # Test runs instantly!
```

### 4.2. Mocking datetime

```python
from datetime import datetime

def get_current_year():
    """Get current year."""
    return datetime.now().year

def test_mock_datetime(mocker):
    """Test with mocked datetime."""
    # Mock datetime.now()
    mock_now = mocker.patch("datetime.datetime")
    mock_now.now.return_value = datetime(2025, 1, 1)

    result = get_current_year()
    assert result == 2025
```

### 4.3. Mocking Random

```python
import random

def get_random_choice():
    """Get random choice from list."""
    return random.choice(["a", "b", "c"])

def test_mock_random(mocker):
    """Test with predictable random."""
    mock_choice = mocker.patch("random.choice")
    mock_choice.return_value = "b"

    result = get_random_choice()
    assert result == "b"
```

---

## 5. Mocking Classes and Methods

### 5.1. Mocking Instance Methods

```python
class EmailService:
    def send_email(self, to, subject, body):
        """Send email via SMTP."""
        # Real email sending
        smtp.send(to, subject, body)
        return True

def test_email_service_mocked(mocker):
    """Test without sending real emails."""
    mock_send = mocker.patch.object(EmailService, "send_email")
    mock_send.return_value = True

    service = EmailService()
    result = service.send_email("test@example.com", "Hello", "Body")

    assert result is True
    mock_send.assert_called_once_with("test@example.com", "Hello", "Body")
```

### 5.2. Mocking Class Attributes

```python
class Config:
    DEBUG = False
    DATABASE_URL = "postgres://prod"

def test_mock_class_attributes(mocker):
    """Test with mocked class attributes."""
    mocker.patch.object(Config, "DEBUG", True)
    mocker.patch.object(Config, "DATABASE_URL", "sqlite://test")

    assert Config.DEBUG is True
    assert Config.DATABASE_URL == "sqlite://test"
```

### 5.3. Mocking Property

```python
class User:
    @property
    def is_admin(self):
        """Check if user is admin (expensive check)."""
        return database.check_admin(self.id)

def test_mock_property(mocker):
    """Test with mocked property."""
    mock_is_admin = mocker.patch.object(
        User, "is_admin",
        new_callable=mocker.PropertyMock
    )
    mock_is_admin.return_value = True

    user = User()
    assert user.is_admin is True
```

---

## 6. Mocking Environment Variables

### 6.1. With Monkeypatch

```python
import os

def get_api_key():
    """Get API key from environment."""
    return os.getenv("API_KEY", "default_key")

def test_api_key_with_monkeypatch(monkeypatch):
    """Test with mocked environment variable."""
    monkeypatch.setenv("API_KEY", "test_key_123")

    assert get_api_key() == "test_key_123"
```

### 6.2. With Mocker

```python
def test_api_key_with_mocker(mocker):
    """Test with mocker."""
    mocker.patch.dict(os.environ, {"API_KEY": "test_key_456"})

    assert get_api_key() == "test_key_456"
```

### 6.3. Removing Environment Variables

```python
def test_missing_env_var(monkeypatch):
    """Test when environment variable is missing."""
    # Remove the variable if it exists
    monkeypatch.delenv("API_KEY", raising=False)

    assert get_api_key() == "default_key"
```

---

## 7. Mocking Attributes

### 7.1. Mocking Module-Level Variables

```python
# config.py
DEBUG = False
MAX_RETRIES = 3

# test
def test_mock_module_variables(monkeypatch):
    """Test with mocked module variables."""
    monkeypatch.setattr("config.DEBUG", True)
    monkeypatch.setattr("config.MAX_RETRIES", 10)

    import config
    assert config.DEBUG is True
    assert config.MAX_RETRIES == 10
```

### 7.2. Mocking Object Attributes

```python
class Database:
    def __init__(self):
        self.connected = False
        self.host = "localhost"

def test_mock_object_attributes(monkeypatch):
    """Test with mocked object attributes."""
    db = Database()

    monkeypatch.setattr(db, "connected", True)
    monkeypatch.setattr(db, "host", "testhost")

    assert db.connected is True
    assert db.host == "testhost"
```

---

## 8. Verifying Mock Calls

### 8.1. Assert Called

```python
def test_assert_called(mocker):
    """Test that mock was called."""
    mock = mocker.patch("module.func")

    module.func()

    # Verify it was called
    mock.assert_called()
    mock.assert_called_once()
```

### 8.2. Assert Called With

```python
def test_assert_called_with(mocker):
    """Test that mock was called with specific arguments."""
    mock = mocker.patch("module.func")

    module.func(1, 2, key="value")

    # Verify arguments
    mock.assert_called_with(1, 2, key="value")
    mock.assert_called_once_with(1, 2, key="value")
```

### 8.3. Assert Any Call

```python
def test_assert_any_call(mocker):
    """Test that mock was called with specific args at least once."""
    mock = mocker.patch("module.func")

    module.func(1)
    module.func(2)
    module.func(3)

    # Verify it was called with 2 at some point
    mock.assert_any_call(2)
```

### 8.4. Call Count

```python
def test_call_count(mocker):
    """Test number of times mock was called."""
    mock = mocker.patch("module.func")

    module.func()
    module.func()
    module.func()

    assert mock.call_count == 3
```

### 8.5. Call Args

```python
def test_call_args(mocker):
    """Test arguments of mock calls."""
    mock = mocker.patch("module.func")

    module.func(1, 2, key="value")

    # Get last call arguments
    args, kwargs = mock.call_args
    assert args == (1, 2)
    assert kwargs == {"key": "value"}

    # Or use call_args_list for all calls
    module.func(3, 4)
    assert len(mock.call_args_list) == 2
```

### 8.6. Not Called

```python
def test_not_called(mocker):
    """Test that mock was not called."""
    mock = mocker.patch("module.func")

    # Don't call the function

    mock.assert_not_called()
```

---

## 9. Advanced Mocking Patterns

### 9.1. Context Manager Mocking

```python
class FileHandler:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self):
        return "file contents"

def test_mock_context_manager(mocker):
    """Test mocking a context manager."""
    mock_handler = mocker.MagicMock()
    mock_handler.__enter__.return_value.read.return_value = "mocked contents"

    mocker.patch("module.FileHandler", return_value=mock_handler)

    with FileHandler() as f:
        contents = f.read()

    assert contents == "mocked contents"
```

### 9.2. Chained Calls

```python
def test_chained_calls(mocker):
    """Test mocking chained method calls."""
    mock = mocker.patch("module.api")

    # Mock: api.get_client().get_user(1).name
    mock.get_client.return_value.get_user.return_value.name = "Alice"

    result = api.get_client().get_user(1).name
    assert result == "Alice"
```

### 9.3. Multiple Return Values

```python
def test_multiple_return_values(mocker):
    """Test mock returning different values on each call."""
    mock = mocker.patch("module.func")

    # First call returns 1, second returns 2, third returns 3
    mock.side_effect = [1, 2, 3]

    assert module.func() == 1
    assert module.func() == 2
    assert module.func() == 3
```

### 9.4. Conditional Mocking

```python
def test_conditional_mock(mocker):
    """Test mock that behaves differently based on input."""
    mock = mocker.patch("module.func")

    def side_effect(arg):
        if arg > 0:
            return "positive"
        else:
            return "negative"

    mock.side_effect = side_effect

    assert module.func(5) == "positive"
    assert module.func(-3) == "negative"
```

### 9.5. Mocking Exceptions

```python
def test_mock_exception(mocker):
    """Test that mock raises exception."""
    mock = mocker.patch("module.func")
    mock.side_effect = ValueError("error message")

    with pytest.raises(ValueError, match="error message"):
        module.func()
```

---

## 10. Best Practices

### 10.1. Mock at the Right Level

✅ **Good** (mock at the boundary):
```python
# Mock external dependency
def test_good_mocking(mocker):
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.json.return_value = {"data": "test"}

    result = my_function_that_uses_requests()
    assert result == {"data": "test"}
```

❌ **Bad** (mock internal logic):
```python
# Don't mock your own business logic
def test_bad_mocking(mocker):
    mock_my_function = mocker.patch("module.my_business_logic")
    mock_my_function.return_value = "expected"

    # This doesn't test anything!
    result = my_business_logic()
    assert result == "expected"
```

### 10.2. Don't Over-Mock

✅ **Good** (test real code):
```python
def test_minimal_mocking(mocker):
    # Only mock external API
    mock_api = mocker.patch("external_api.fetch")
    mock_api.return_value = {"status": "ok"}

    # Test real business logic
    result = process_data()
    assert result.is_valid()
```

❌ **Bad** (mock everything):
```python
def test_over_mocking(mocker):
    # Mocking too much - not testing real code
    mocker.patch("module.func1")
    mocker.patch("module.func2")
    mocker.patch("module.func3")
    mocker.patch("module.func4")
    # ...
```

### 10.3. Use Descriptive Names

✅ **Good**:
```python
def test_with_descriptive_names(mocker):
    mock_database_query = mocker.patch("database.query")
    mock_email_send = mocker.patch("email.send")

    # Clear what each mock does
```

❌ **Bad**:
```python
def test_with_bad_names(mocker):
    m1 = mocker.patch("database.query")
    m2 = mocker.patch("email.send")

    # Unclear what m1 and m2 are
```

### 10.4. Verify Important Calls

Always verify that important functions were called:

```python
def test_verify_calls(mocker):
    """Test that critical operations were performed."""
    mock_send_email = mocker.patch("email.send")
    mock_log = mocker.patch("logger.info")

    process_order(order_id=123)

    # Verify email was sent
    mock_send_email.assert_called_once()

    # Verify logging happened
    mock_log.assert_called()
```

### 10.5. Clean Test Data

Use realistic test data in mocks:

✅ **Good**:
```python
def test_realistic_data(mocker):
    mock_api = mocker.patch("api.get_user")
    mock_api.return_value = {
        "id": 123,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "created_at": "2024-01-01T00:00:00Z"
    }
```

❌ **Bad**:
```python
def test_unrealistic_data(mocker):
    mock_api = mocker.patch("api.get_user")
    mock_api.return_value = {"x": 1, "y": 2}  # Doesn't match real API
```

---

## 11. Monkeypatch vs Mocker

### When to Use Each

| Feature | Monkeypatch | Mocker |
|---------|-------------|--------|
| **Simplicity** | ✅ Simpler for basic cases | More complex API |
| **Built-in** | ✅ No installation needed | Requires pytest-mock |
| **Environment vars** | ✅ Easy with setenv() | Possible but verbose |
| **Verification** | ❌ Can't verify calls | ✅ Full call verification |
| **Return values** | ❌ Manual setup | ✅ Easy with return_value |
| **Side effects** | ❌ Manual | ✅ Built-in side_effect |
| **Spying** | ❌ Not supported | ✅ mocker.spy() |

### Recommendation

- **Use monkeypatch** for:
  - Environment variables
  - Simple attribute replacement
  - Quick and dirty mocking

- **Use mocker** for:
  - Complex mocking scenarios
  - Need to verify calls
  - Multiple return values
  - Raising exceptions
  - Spying on real functions

---

## 12. Summary

### Key Takeaways

1. **Mocking isolates tests**: Test one component without dependencies
2. **Monkeypatch**: Pytest's built-in, simple mocking
3. **Mocker**: Full-featured mocking from pytest-mock
4. **Mock at boundaries**: Mock external dependencies, not your own logic
5. **Verify calls**: Use assert_called_* to verify behavior
6. **Return values**: Use return_value and side_effect
7. **Don't over-mock**: Test real code when possible

### Common Patterns

```python
# Monkeypatch
def test_with_monkeypatch(monkeypatch):
    monkeypatch.setattr("module.func", lambda: "mocked")
    monkeypatch.setenv("VAR", "value")

# Mocker - basic
def test_with_mocker(mocker):
    mock = mocker.patch("module.func")
    mock.return_value = "result"
    mock.assert_called_once()

# Mocker - side effect
def test_side_effect(mocker):
    mock = mocker.patch("module.func")
    mock.side_effect = [1, 2, 3]  # Different values
    mock.side_effect = ValueError()  # Raise exception

# Mocker - spy
def test_spy(mocker):
    spy = mocker.spy(module, "func")
    module.func()  # Calls real function
    spy.assert_called_once()
```

### What's Next?

- **[Conftest Patterns](../conftest_patterns/)** - Advanced conftest.py usage
- **[Fixtures](../fixtures/)** - Reusable test setup
- **[Mini Project](../mini_project/)** - Complete example project

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all mocking tests
pytest mocking/ -v

# Run a specific file
pytest mocking/test_mock_monkeypatch.py -v
pytest mocking/test_mock_mocker.py -v

# Run with output visible
pytest mocking/ -v -s
```

---

[← Back to Main Guide](../README.md)

