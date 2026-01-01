# Pytest Parametrize - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/parametrize/`  
> **Test Files**: All parametrize-related examples are in this folder

---

## Table of Contents

1. [What is Parametrize?](#1-what-is-parametrize)
2. [Basic Parametrize](#2-basic-parametrize)
3. [Multiple Parameters](#3-multiple-parameters)
4. [Parametrize with IDs](#4-parametrize-with-ids)
5. [Parametrize with Fixtures](#5-parametrize-with-fixtures)
6. [Indirect Parametrization](#6-indirect-parametrization)
7. [Parametrize with Markers](#7-parametrize-with-markers)
8. [Parametrized Fixtures](#8-parametrized-fixtures)

---

## 1. What is Parametrize?

**Parametrize** allows you to run the same test function with different input values. Instead of writing multiple similar tests, you write one test and provide multiple sets of inputs.

### Why Use Parametrize?

**Without parametrize** (repetitive):
```python
def test_add_2_and_3():
    assert add(2, 3) == 5

def test_add_5_and_7():
    assert add(5, 7) == 12

def test_add_10_and_20():
    assert add(10, 20) == 30
```

**With parametrize** (DRY - Don't Repeat Yourself):
```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (5, 7, 12),
    (10, 20, 30),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Benefits

1. **Less code**: Write one test instead of many
2. **Easy to add cases**: Just add a new tuple to the list
3. **Clear test output**: Each parameter set shows as a separate test
4. **Better coverage**: Encourages testing more cases

### How It Works Under the Hood

When you use `@pytest.mark.parametrize`, pytest automatically runs the test
function **multiple times** — once for each set of parameter values you define.

**You write one test function**, but **pytest runs it N times**:

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (5, 7, 12),
    (10, 20, 30),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

| Run | `a` | `b` | `expected` | What pytest checks |
|-----|-----|-----|------------|-------------------|
| 1 | 2 | 3 | 5 | `add(2, 3) == 5` ✅ |
| 2 | 5 | 7 | 12 | `add(5, 7) == 12` ✅ |
| 3 | 10 | 20 | 30 | `add(10, 20) == 30` ✅ |

If you run it with verbose output (`pytest -v`), you'll see:

```
test_add.py::test_add[2-3-5] PASSED
test_add.py::test_add[5-7-12] PASSED
test_add.py::test_add[10-20-30] PASSED
```

Each parameter combination becomes a **separate test case**.

#### Key Insight

Even though you call `test_add()` once in your code, pytest:

1. Reads the parameter list from `@pytest.mark.parametrize`
2. Creates a separate test run for each tuple
3. Injects the values (`a`, `b`, `expected`) into the function for each run
4. Reports each run as an independent test result

This is why one failing parameter set doesn't stop the others from running —
they are truly separate test executions.

---

## 2. Basic Parametrize

**File**: `test_parametrize_basic.py`

### 2.1. Single Parameter

```python
import pytest

@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_is_positive(number):
    """Test that numbers are positive."""
    assert number > 0
```

**Running**:
```bash
pytest parametrize/test_parametrize_basic.py::test_is_positive -v
```

**Output**:
```
test_parametrize_basic.py::test_is_positive[1] PASSED
test_parametrize_basic.py::test_is_positive[2] PASSED
test_parametrize_basic.py::test_is_positive[3] PASSED
test_parametrize_basic.py::test_is_positive[4] PASSED
test_parametrize_basic.py::test_is_positive[5] PASSED
```

Each value becomes a separate test case!

### 2.2. Multiple Parameters (Input and Expected Output)

```python
@pytest.mark.parametrize("input_value, expected", [
    (2, 4),      # 2 * 2 = 4
    (3, 9),      # 3 * 3 = 9
    (4, 16),     # 4 * 4 = 16
    (5, 25),     # 5 * 5 = 25
])
def test_square(input_value, expected):
    """Test squaring numbers."""
    assert input_value ** 2 == expected
```

**Output**:
```
test_parametrize_basic.py::test_square[2-4] PASSED
test_parametrize_basic.py::test_square[3-9] PASSED
test_parametrize_basic.py::test_square[4-16] PASSED
test_parametrize_basic.py::test_square[5-25] PASSED
```

### 2.3. String Parameters

```python
@pytest.mark.parametrize("text", [
    "hello",
    "pytest",
    "parametrize",
])
def test_string_length(text):
    """Test that strings have length > 0."""
    assert len(text) > 0
```

### 2.4. Testing Edge Cases

```python
@pytest.mark.parametrize("value, expected", [
    (0, True),       # Zero is even
    (1, False),      # One is odd
    (2, True),       # Two is even
    (-1, False),     # Negative odd
    (-2, True),      # Negative even
    (100, True),     # Large even
    (999, False),    # Large odd
])
def test_is_even(value, expected):
    """Test is_even function with various inputs."""
    assert is_even(value) == expected
```

This tests:
- Positive numbers
- Negative numbers
- Zero
- Large numbers
- Edge cases

---

## 3. Multiple Parameters

**File**: `test_parametrize_multiple.py`

You can parametrize multiple arguments at once.

### 3.1. Three Parameters

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (10, -5, 5),
    (0, 0, 0),
    (-3, -7, -10),
])
def test_addition(a, b, expected):
    """Test addition with multiple parameter sets."""
    assert a + b == expected
```

### 3.2. Complex Data Types

```python
@pytest.mark.parametrize("input_list, expected_sum", [
    ([1, 2, 3], 6),
    ([10, 20, 30], 60),
    ([], 0),
    ([5], 5),
    ([-1, 1], 0),
])
def test_sum_list(input_list, expected_sum):
    """Test summing lists."""
    assert sum(input_list) == expected_sum
```

### 3.3. Dictionary Parameters

```python
@pytest.mark.parametrize("user_data, is_valid", [
    ({"name": "Alice", "age": 25}, True),
    ({"name": "Bob", "age": 17}, False),  # Too young
    ({"name": "", "age": 30}, False),     # Empty name
    ({"name": "Charlie", "age": -5}, False),  # Invalid age
])
def test_user_validation(user_data, is_valid):
    """Test user data validation."""
    assert validate_user(user_data) == is_valid
```

---

## 4. Parametrize with IDs

You can provide custom IDs to make test output more readable.

### 4.1. Using the `ids` Parameter

**File**: `test_parametrize_basic.py`

```python
@pytest.mark.parametrize("input_value, expected", [
    (2, 4),
    (3, 9),
    (4, 16),
], ids=["two_squared", "three_squared", "four_squared"])
def test_square_with_ids(input_value, expected):
    """Test with custom IDs."""
    assert input_value ** 2 == expected
```

**Output**:
```
test_parametrize_basic.py::test_square_with_ids[two_squared] PASSED
test_parametrize_basic.py::test_square_with_ids[three_squared] PASSED
test_parametrize_basic.py::test_square_with_ids[four_squared] PASSED
```

Much more readable than `[2-4]`, `[3-9]`, `[4-16]`!

### 4.2. Automatic IDs from Strings

When parameters are strings, pytest uses them as IDs automatically:

```python
@pytest.mark.parametrize("operation", ["add", "subtract", "multiply"])
def test_operations(operation):
    """Test different operations."""
    assert operation in ["add", "subtract", "multiply", "divide"]
```

**Output**:
```
test_parametrize_basic.py::test_operations[add] PASSED
test_parametrize_basic.py::test_operations[subtract] PASSED
test_parametrize_basic.py::test_operations[multiply] PASSED
```

### 4.3. ID Function

You can use a function to generate IDs:

```python
def id_func(param):
    """Generate custom ID from parameter."""
    if isinstance(param, dict):
        return f"user_{param.get('name', 'unknown')}"
    return str(param)

@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
], ids=id_func)
def test_user(user):
    """Test with ID function."""
    assert user["age"] > 0
```

**Output**:
```
test_parametrize_basic.py::test_user[user_Alice] PASSED
test_parametrize_basic.py::test_user[user_Bob] PASSED
```

---

## 5. Parametrize with Fixtures

You can combine parametrize with fixtures.

**File**: `test_parametrize_with_fixture.py`

### 5.1. Fixture + Parametrize

```python
import pytest

@pytest.fixture
def database():
    """Fixture that provides a database connection."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
])
def test_get_user(database, user_id, expected_name):
    """Test getting users from database."""
    user = database.get_user(user_id)
    assert user.name == expected_name
```

**How it works**:
1. Fixture `database` runs for each parameter set
2. Each test gets a fresh database connection
3. Test runs with different `user_id` and `expected_name`

### 5.2. Multiple Fixtures + Parametrize

```python
@pytest.fixture
def api_client():
    """Fixture for API client."""
    return APIClient()

@pytest.fixture
def auth_token():
    """Fixture for authentication token."""
    return "test-token-123"

@pytest.mark.parametrize("endpoint, expected_status", [
    ("/users", 200),
    ("/posts", 200),
    ("/invalid", 404),
])
def test_api_endpoints(api_client, auth_token, endpoint, expected_status):
    """Test API endpoints with fixtures."""
    response = api_client.get(endpoint, token=auth_token)
    assert response.status_code == expected_status
```

---

## 6. Indirect Parametrization

**Indirect parametrization** passes parameter values to fixtures instead of directly to the test.

**File**: `test_parametrize_indirect.py`

### 6.1. Basic Indirect

```python
import pytest

@pytest.fixture
def user(request):
    """Fixture that creates a user based on parameter."""
    user_data = request.param  # Get the parameter value
    return User(name=user_data["name"], age=user_data["age"])

@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
], indirect=True)  # Pass parameters to fixture, not test
def test_user_creation(user):
    """Test user creation via fixture."""
    assert user.name in ["Alice", "Bob"]
    assert user.age > 0
```

**How it works**:
1. `indirect=True` tells pytest to pass parameters to the `user` fixture
2. Fixture receives parameter via `request.param`
3. Fixture creates and returns the user object
4. Test receives the user object from fixture

### 6.2. Why Use Indirect?

**Without indirect** (setup in test):
```python
@pytest.mark.parametrize("user_data", [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
])
def test_user(user_data):
    # Setup code repeated in every test
    user = User(name=user_data["name"], age=user_data["age"])
    db.save(user)

    # Actual test
    assert user.is_valid()

    # Teardown code repeated in every test
    db.delete(user)
```

**With indirect** (setup in fixture):
```python
@pytest.fixture
def user(request):
    user_data = request.param
    user = User(name=user_data["name"], age=user_data["age"])
    db.save(user)
    yield user
    db.delete(user)  # Automatic cleanup

@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
], indirect=True)
def test_user(user):
    # Just the test logic - setup/teardown in fixture
    assert user.is_valid()
```

### 6.3. Partial Indirect

You can make only some parameters indirect:

```python
@pytest.fixture
def database(request):
    """Fixture for database."""
    db_name = request.param
    db = Database(db_name)
    db.connect()
    yield db
    db.disconnect()

@pytest.mark.parametrize("database, query, expected", [
    ("test_db", "SELECT * FROM users", 5),
    ("prod_db", "SELECT * FROM users", 100),
], indirect=["database"])  # Only 'database' is indirect
def test_query(database, query, expected):
    """Test database queries."""
    result = database.execute(query)
    assert len(result) == expected
```

Here:
- `database` parameter goes to the fixture
- `query` and `expected` go directly to the test

---

## 7. Parametrize with Markers

You can apply markers to specific parameter sets.

**File**: `test_parametrize_marks.py`

### 7.1. Marking Individual Parameters

```python
import pytest

@pytest.mark.parametrize("value, expected", [
    (2, 4),
    (3, 9),
    pytest.param(4, 16, marks=pytest.mark.slow),  # Mark this case as slow
    pytest.param(5, 25, marks=pytest.mark.slow),
])
def test_square_with_marks(value, expected):
    """Test with some cases marked as slow."""
    assert value ** 2 == expected
```

**Running**:
```bash
# Run all tests
pytest parametrize/test_parametrize_marks.py -v

# Skip slow tests
pytest parametrize/test_parametrize_marks.py -m "not slow" -v
```

### 7.2. Skip Specific Parameters

```python
@pytest.mark.parametrize("platform, command", [
    ("linux", "ls"),
    ("mac", "ls"),
    pytest.param("windows", "dir", marks=pytest.mark.skip(reason="Windows not supported")),
])
def test_platform_command(platform, command):
    """Test platform-specific commands."""
    assert command in ["ls", "dir"]
```

### 7.3. XFail Specific Parameters

```python
@pytest.mark.parametrize("value, expected", [
    (2, 4),
    (3, 9),
    pytest.param(4, 15, marks=pytest.mark.xfail(reason="known bug")),  # Expected to fail
])
def test_with_xfail(value, expected):
    """Test with one case expected to fail."""
    assert value ** 2 == expected
```

### 7.4. Multiple Markers on Parameters

```python
@pytest.mark.parametrize("test_input, expected", [
    (1, 2),
    pytest.param(10, 20, marks=[pytest.mark.slow, pytest.mark.integration]),
    pytest.param(100, 200, marks=[pytest.mark.slow, pytest.mark.skip(reason="too slow")]),
])
def test_with_multiple_marks(test_input, expected):
    """Test with multiple markers on parameters."""
    assert test_input * 2 == expected
```

---

## 8. Parametrized Fixtures

You can parametrize fixtures themselves to create multiple versions of a fixture.

**File**: `test_parametrized_fixture.py`

### 8.1. Basic Parametrized Fixture

```python
import pytest

@pytest.fixture(params=["chrome", "firefox", "safari"])
def browser(request):
    """Fixture that provides different browsers."""
    browser_name = request.param
    print(f"\nSetting up {browser_name} browser")

    # Setup browser
    browser_instance = Browser(browser_name)

    yield browser_instance

    # Teardown
    print(f"\nTearing down {browser_name} browser")
    browser_instance.quit()

def test_website_loads(browser):
    """This test runs 3 times - once for each browser."""
    browser.get("https://example.com")
    assert browser.title == "Example Domain"
```

**Output**:
```
test_parametrized_fixture.py::test_website_loads[chrome] PASSED
test_parametrized_fixture.py::test_website_loads[firefox] PASSED
test_parametrized_fixture.py::test_website_loads[safari] PASSED
```

**How it works**:
1. Fixture has `params=["chrome", "firefox", "safari"]`
2. Pytest runs the test 3 times, once for each parameter
3. Each time, `request.param` has a different value
4. Test automatically runs with all browser variations

### 8.2. Parametrized Fixture with Complex Data

```python
@pytest.fixture(params=[
    {"db": "sqlite", "host": "localhost"},
    {"db": "postgres", "host": "db.example.com"},
    {"db": "mysql", "host": "mysql.example.com"},
])
def database(request):
    """Fixture providing different database configurations."""
    config = request.param
    db = Database(config["db"], config["host"])
    db.connect()
    yield db
    db.disconnect()

def test_database_query(database):
    """Test runs 3 times with different databases."""
    result = database.query("SELECT 1")
    assert result is not None
```

### 8.3. Parametrized Fixture with IDs

```python
@pytest.fixture(params=[
    "small_dataset",
    "medium_dataset",
    "large_dataset",
], ids=["small", "medium", "large"])
def dataset(request):
    """Fixture providing different dataset sizes."""
    size = request.param
    return load_dataset(size)

def test_data_processing(dataset):
    """Test with different dataset sizes."""
    result = process(dataset)
    assert result.is_valid()
```

**Output**:
```
test_parametrized_fixture.py::test_data_processing[small] PASSED
test_parametrized_fixture.py::test_data_processing[medium] PASSED
test_parametrized_fixture.py::test_data_processing[large] PASSED
```

### 8.4. When to Use Parametrized Fixtures

✅ **Good use cases**:
- Testing across multiple browsers
- Testing with different database backends
- Testing with different configurations
- Cross-platform testing

**Example**: Test suite that should work with multiple databases:
```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db(request):
    """All tests run against all databases."""
    return setup_database(request.param)

def test_create_user(db):
    """Runs 3 times - once per database."""
    user = db.create_user("Alice")
    assert user.id is not None

def test_delete_user(db):
    """Also runs 3 times - once per database."""
    user = db.create_user("Bob")
    db.delete_user(user.id)
    assert db.get_user(user.id) is None
```

Both tests run 3 times each (6 total test runs).

### 8.5. Parametrized Fixture vs Parametrize Decorator

| Feature | Parametrized Fixture | @pytest.mark.parametrize |
|---------|---------------------|--------------------------|
| Scope | All tests using fixture | Single test function |
| Setup/Teardown | Yes (in fixture) | No (unless using indirect) |
| Reusability | High (many tests can use it) | Low (per test) |
| Use case | Cross-cutting concerns | Test-specific variations |

**Parametrized Fixture** (affects all tests using it):
```python
@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    return Browser(request.param)

def test_login(browser):  # Runs 2 times
    pass

def test_logout(browser):  # Runs 2 times
    pass

# Total: 4 test runs
```

**Parametrize Decorator** (affects only decorated test):
```python
@pytest.fixture
def browser():
    return Browser("chrome")

@pytest.mark.parametrize("username", ["alice", "bob"])
def test_login(browser, username):  # Runs 2 times
    pass

def test_logout(browser):  # Runs 1 time
    pass

# Total: 3 test runs
```

---

## 9. Combining Multiple Parametrizations

You can stack multiple `@pytest.mark.parametrize` decorators.

### 9.1. Cartesian Product

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_multiply(x, y):
    """Test runs 4 times: (1,3), (1,4), (2,3), (2,4)."""
    result = x * y
    assert result > 0
```

**Output**:
```
test_parametrize_multiple.py::test_multiply[3-1] PASSED
test_parametrize_multiple.py::test_multiply[3-2] PASSED
test_parametrize_multiple.py::test_multiply[4-1] PASSED
test_parametrize_multiple.py::test_multiply[4-2] PASSED
```

This creates a **cartesian product**: all combinations of x and y.

### 9.2. Real-World Example: Cross-Browser Testing

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
@pytest.mark.parametrize("viewport", ["mobile", "tablet", "desktop"])
def test_responsive_design(browser, viewport):
    """Test runs 9 times: 3 browsers × 3 viewports."""
    driver = setup_browser(browser, viewport)
    driver.get("https://example.com")
    assert driver.is_responsive()
```

**Output**: 9 test runs (3 × 3)

### 9.3. Combining with Parametrized Fixture

```python
@pytest.fixture(params=["sqlite", "postgres"])
def database(request):
    return Database(request.param)

@pytest.mark.parametrize("operation", ["insert", "update", "delete"])
def test_database_operations(database, operation):
    """Test runs 6 times: 2 databases × 3 operations."""
    result = database.execute(operation)
    assert result.success
```

**Output**: 6 test runs (2 × 3)

---

## 10. Best Practices

### 10.1. Keep Parameter Sets Readable

✅ **Good** (readable):
```python
@pytest.mark.parametrize("input_value, expected", [
    (2, 4),       # 2^2 = 4
    (3, 9),       # 3^2 = 9
    (4, 16),      # 4^2 = 16
])
def test_square(input_value, expected):
    assert input_value ** 2 == expected
```

❌ **Bad** (hard to read):
```python
@pytest.mark.parametrize("a,b", [(2,4),(3,9),(4,16)])
def test_square(a,b):
    assert a**2==b
```

### 10.2. Use Descriptive IDs

✅ **Good**:
```python
@pytest.mark.parametrize("user, is_admin", [
    ("alice", True),
    ("bob", False),
], ids=["admin_user", "regular_user"])
```

❌ **Bad**:
```python
@pytest.mark.parametrize("user, is_admin", [
    ("alice", True),
    ("bob", False),
], ids=["1", "2"])
```

### 10.3. Don't Over-Parametrize

❌ **Too many combinations** (hard to debug):
```python
@pytest.mark.parametrize("a", range(100))
@pytest.mark.parametrize("b", range(100))
@pytest.mark.parametrize("c", range(100))
def test_something(a, b, c):
    # 1,000,000 test runs!
    pass
```

✅ **Focused test cases**:
```python
@pytest.mark.parametrize("a, b, c", [
    (1, 2, 3),
    (10, 20, 30),
    (0, 0, 0),
    (-1, -2, -3),
])
def test_something(a, b, c):
    # 4 meaningful test runs
    pass
```

### 10.4. Use Indirect for Complex Setup

When setup is complex, use `indirect=True`:

✅ **Good** (complex setup in fixture):
```python
@pytest.fixture
def user(request):
    user_data = request.param
    user = create_user(user_data)
    db.save(user)
    send_welcome_email(user)
    yield user
    db.delete(user)

@pytest.mark.parametrize("user", [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
], indirect=True)
def test_user(user):
    assert user.is_active()
```

❌ **Bad** (setup repeated in test):
```python
@pytest.mark.parametrize("user_data", [
    {"name": "Alice", "role": "admin"},
    {"name": "Bob", "role": "user"},
])
def test_user(user_data):
    user = create_user(user_data)
    db.save(user)
    send_welcome_email(user)

    assert user.is_active()

    db.delete(user)  # Cleanup
```

---

## 11. Summary

### Key Takeaways

1. **Basic parametrize**: Run same test with different inputs
2. **Multiple parameters**: Test with combinations of inputs
3. **Custom IDs**: Make test output readable
4. **With fixtures**: Combine parametrize with fixtures
5. **Indirect**: Pass parameters to fixtures for complex setup
6. **With markers**: Mark specific parameter sets (skip, xfail, slow)
7. **Parametrized fixtures**: Create multiple versions of a fixture
8. **Stacking**: Combine multiple parametrizations for cartesian product

### Common Patterns

```bash
# Basic parametrize
@pytest.mark.parametrize("input, expected", [(1, 2), (3, 4)])

# With IDs
@pytest.mark.parametrize("value", [1, 2], ids=["first", "second"])

# Indirect
@pytest.mark.parametrize("fixture_name", [data1, data2], indirect=True)

# With markers
pytest.param(value, marks=pytest.mark.slow)

# Parametrized fixture
@pytest.fixture(params=[1, 2, 3])

# Stacking
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
```

### What's Next?

- **[Exceptions](../exceptions/)** - Test error handling with pytest.raises
- **[Mocking](../mocking/)** - Mock objects and monkeypatch
- **[Fixtures](../fixtures/)** - Advanced fixture patterns

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all parametrize tests
pytest parametrize/ -v

# Run a specific file
pytest parametrize/test_parametrize_basic.py -v

# Run with output visible
pytest parametrize/ -v -s

# Skip slow parametrized tests
pytest parametrize/ -m "not slow" -v
```

---

[← Back to Main Guide](../README.md)

