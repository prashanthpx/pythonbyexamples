# Pytest Fixtures - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/fixtures/`
> **Test Files**: All fixture-related examples are in this folder

---

## Table of Contents

1. [What are Fixtures?](#1-what-are-fixtures)
2. [Basic Fixtures](#2-basic-fixtures)
3. [Fixture Scopes](#3-fixture-scopes)
4. [How Pytest Discovers and Runs Tests](#4-how-pytest-discovers-and-runs-tests)
5. [Complete Fixture Scopes Example](#5-complete-fixture-scopes-example)
6. [Fixture Dependencies](#6-fixture-dependencies)
7. [Autouse Fixtures](#7-autouse-fixtures)
8. [Built-in Fixtures](#8-built-in-fixtures)

---

## 1. What are Fixtures?

**Fixtures** are pytest's way of providing reusable setup and teardown code for your tests.

### Why use fixtures?

- **Reusability**: Write setup code once, use it in many tests
- **Clarity**: Separate test logic from setup/teardown
- **Dependency injection**: Tests declare what they need via parameters
- **Automatic cleanup**: Teardown happens automatically, even if tests fail

### Real-world use cases

- Setting up database connections
- Creating test files/directories
- Initializing API clients
- Preparing test data
- Mocking external services

---

## 2. Basic Fixtures

### 2.1. Simple Fixture

**File**: `test_fixture.py`

```python
import pytest

@pytest.fixture
def sample_data():
    """Provides sample data for tests."""
    return {"name": "Alice", "age": 30}

def test_using_fixture(sample_data):
    """Test receives fixture via parameter."""
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
```

**How it works:**

1. `@pytest.fixture` decorator marks `sample_data` as a fixture
2. Test function declares `sample_data` as a parameter
3. Pytest automatically calls the fixture and passes the result to the test

### 2.2. Fixture with Setup and Teardown

```python
@pytest.fixture
def database_connection():
    """Fixture with setup and teardown."""
    # Setup: runs before the test
    print("Opening database connection")
    connection = {"connected": True}
    
    yield connection  # Provide the fixture value
    
    # Teardown: runs after the test (even if test fails)
    print("Closing database connection")
    connection["connected"] = False
```

**Key points:**

- Code before `yield` = **setup**
- `yield` provides the value to the test
- Code after `yield` = **teardown** (cleanup)
- Teardown runs even if the test fails

---

## 3. Fixture Scopes

Fixtures can have different **scopes** that control how often they are created and destroyed.

### Available Scopes

| Scope | Created | Destroyed | Use Case |
|-------|---------|-----------|----------|
| `function` | Before each test function | After each test function | Default; fresh state per test |
| `class` | Before first test in class | After last test in class | Shared state within test class |
| `module` | Before first test in module | After last test in module | Expensive setup (DB connection) |
| `package` | Before first test in package | After last test in package | Package-level resources |
| `session` | Before first test in session | After all tests complete | One-time setup (test database) |

### Syntax

```python
@pytest.fixture(scope="function")  # Default
def function_fixture():
    pass

@pytest.fixture(scope="class")
def class_fixture():
    pass

@pytest.fixture(scope="module")
def module_fixture():
    pass

@pytest.fixture(scope="session")
def session_fixture():
    pass
```

---

## 4. How Pytest Discovers and Runs Tests

Before diving into the complete fixture scopes example, it's crucial to understand **how pytest automatically finds and runs your tests**.

### 4.1. Test Discovery (Automatic)

When you run `pytest`, it automatically:

1. **Finds test files**: Looks for files matching `test_*.py` or `*_test.py`
2. **Finds test classes**: Looks for classes named `Test*` (must start with "Test")
3. **Finds test functions**: Looks for functions/methods named `test_*` (must start with "test_")

### 4.2. You Never Instantiate Test Classes

This is a common point of confusion. Consider this code:

```python
class TestFirst:
    def test_a(self):
        assert True
    
    def test_b(self):
        assert True
```

**Question**: Where do we create `TestFirst()` and call the methods?

**Answer**: **You don't!** Pytest does it automatically.

### 4.3. What Happens Behind the Scenes

When pytest finds the above code, it conceptually does this:

```python
# Pytest internally does something like this (simplified):
test_instance_1 = TestFirst()  # Create instance for test_a
test_instance_1.test_a()        # Call test_a

test_instance_2 = TestFirst()  # Create NEW instance for test_b
test_instance_2.test_b()        # Call test_b
```

**Important**: By default, pytest creates a **new instance** of the test class for **each test method**. This ensures test isolation.

### 4.4. Seeing It in Action

You can verify this by adding `__init__`:

```python
class TestExample:
    def __init__(self):
        print("TestExample instance created!")
    
    def test_one(self):
        print("Running test_one")
    
    def test_two(self):
        print("Running test_two")
```

**Output when running `pytest -s`:**
```
TestExample instance created!
Running test_one
.TestExample instance created!
Running test_two
.
```

Notice: **Two instances created** (one per test method)!

### 4.5. Naming Conventions Matter

✅ **These WILL be discovered:**
```python
# File: test_example.py or example_test.py
class TestMyFeature:           # Starts with "Test"
    def test_something(self):  # Starts with "test_"
        pass

def test_standalone():         # Starts with "test_"
    pass
```

❌ **These will NOT be discovered:**
```python
# File: example.py (doesn't match pattern)
class MyTest:                  # Doesn't start with "Test"
    def check_something(self): # Doesn't start with "test_"
        pass
```

### 4.6. Key Takeaway

You **never** need to:
- Import test classes
- Instantiate test classes  
- Call test methods
- Create a main() function

Pytest's **test runner** does all of this automatically by:
1. Scanning files for naming patterns
2. Collecting all tests
3. Instantiating classes and calling methods
4. Managing fixtures and dependencies
5. Reporting results

---

## 5. Complete Fixture Scopes Example

**File**: `test_fixture_scopes_all.py`

This example demonstrates **all five fixture scopes** in action, showing exactly when each fixture is created and destroyed.

### 5.1. The Complete Code

```python
import pytest

# Phase 3 – Fixtures: demonstrating all fixture scopes

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
    """Verify how often each fixture's setup ran in this module."""
    assert call_log.count("function-setup") == 3
    assert call_log.count("class-setup-TestFirst") == 1
    assert call_log.count("class-setup-TestSecond") == 1
    assert call_log.count("module-setup") == 1
    assert call_log.count("package-setup") == 1
    assert call_log.count("session-setup") == 1
```

### 5.2. Understanding the Code

#### Test Organization

- **Two test classes**: `TestFirst` and `TestSecond`
- **Three test methods**: `test_a`, `test_b` (in TestFirst), and `test_c` (in TestSecond)
- **One verification test**: `test_check_scope_setups` (standalone function)

#### Fixture Parameters

Each test method receives **5 fixtures** as parameters:
- `function_scope` - Created/destroyed for **each test function**
- `class_scope` - Created once per **test class**, shared by all tests in that class
- `module_scope` - Created once per **module file**, shared by all tests in the file
- `package_scope` - Created once per **package**, shared across multiple modules
- `session_scope` - Created once per **entire test session**, shared by all tests

### 5.3. Execution Flow

When you run `pytest test_fixture_scopes_all.py -v`, here's what happens:

#### Session Starts
```
1. session_scope fixture created (ONCE for entire test run)
2. package_scope fixture created (ONCE for this package)
3. module_scope fixture created (ONCE for this module)
```

#### TestFirst Class
```
4. class_scope fixture created for TestFirst
5. function_scope fixture created for test_a
6. test_a runs
7. function_scope fixture destroyed
8. function_scope fixture created for test_b
9. test_b runs
10. function_scope fixture destroyed
11. class_scope fixture destroyed for TestFirst
```

#### TestSecond Class
```
12. class_scope fixture created for TestSecond
13. function_scope fixture created for test_c
14. test_c runs
15. function_scope fixture destroyed
16. class_scope fixture destroyed for TestSecond
```

#### Verification Test
```
17. function_scope fixture created for test_check_scope_setups
18. test_check_scope_setups runs (verifies the call_log)
19. function_scope fixture destroyed
```

#### Session Ends
```
20. module_scope fixture destroyed
21. package_scope fixture destroyed
22. session_scope fixture destroyed
```

### 5.4. Detailed Breakdown by Scope

#### `function_scope` (Most Common)
- **Created**: 4 times (once for each test: test_a, test_b, test_c, test_check_scope_setups)
- **Shared**: Not shared; each test gets its own instance
- **Use case**: Fresh state for each test (default behavior)

**Example**:
```python
@pytest.fixture(scope="function")
def fresh_list():
    """Each test gets a new empty list."""
    return []

def test_one(fresh_list):
    fresh_list.append(1)
    assert fresh_list == [1]

def test_two(fresh_list):
    fresh_list.append(2)
    assert fresh_list == [2]  # Still empty at start!
```

#### `class_scope`
- **Created**: 2 times (once for TestFirst, once for TestSecond)
- **Shared**: Between `test_a` and `test_b` (same class), but NOT with `test_c` (different class)
- **Use case**: Shared state within a test class

**Example**:
```python
@pytest.fixture(scope="class")
def shared_counter():
    """Shared counter for all tests in a class."""
    return {"count": 0}

class TestCounter:
    def test_increment_once(self, shared_counter):
        shared_counter["count"] += 1
        assert shared_counter["count"] == 1

    def test_increment_twice(self, shared_counter):
        shared_counter["count"] += 1
        assert shared_counter["count"] == 2  # Remembers previous test!
```

#### `module_scope`
- **Created**: 1 time (when first test in the module runs)
- **Shared**: By all 4 tests in this module
- **Use case**: Expensive setup that can be reused (database connection, API client)

**Example**:
```python
@pytest.fixture(scope="module")
def database_connection():
    """One database connection for the entire module."""
    print("Opening expensive database connection")
    conn = create_connection()
    yield conn
    print("Closing database connection")
    conn.close()
```

#### `package_scope`
- **Created**: 1 time per package
- **Shared**: Across all modules in the same package
- **Use case**: Package-level resources (test database, shared cache)

**Example**:
```python
# In conftest.py at package level
@pytest.fixture(scope="package")
def test_database():
    """One test database for the entire package."""
    db = create_test_database()
    yield db
    db.drop_all_tables()
```

#### `session_scope` (Widest Scope)
- **Created**: 1 time for the entire pytest session
- **Shared**: By absolutely all tests in the entire test run
- **Use case**: One-time expensive setup (Docker containers, test servers)

**Example**:
```python
@pytest.fixture(scope="session")
def docker_container():
    """Start Docker container once for all tests."""
    print("Starting Docker container")
    container = start_container()
    yield container
    print("Stopping Docker container")
    container.stop()
```

### 5.5. The `request` Fixture

Notice the `class_scope` fixture uses a special parameter:

```python
@pytest.fixture(scope="class")
def class_scope(request):
    call_log.append(f"class-setup-{request.cls.__name__}")
    yield
    call_log.append(f"class-teardown-{request.cls.__name__}")
```

**What is `request`?**

- `request` is a **built-in pytest fixture** that provides information about the requesting test
- `request.cls` gives you the test class (e.g., `TestFirst`, `TestSecond`)
- `request.cls.__name__` gives you the class name as a string

**Other useful `request` attributes**:
- `request.function` - The test function object
- `request.module` - The test module
- `request.node` - The test node (full test item)
- `request.param` - Parameter value (used with parametrized fixtures)

### 5.6. Running the Example

From the `pytest/` directory:

```bash
pytest test_fixture_scopes_all.py -v
```

**Output**:
```
test_fixture_scopes_all.py::TestFirst::test_a PASSED
test_fixture_scopes_all.py::TestFirst::test_b PASSED
test_fixture_scopes_all.py::TestSecond::test_c PASSED
test_fixture_scopes_all.py::test_check_scope_setups PASSED

==================================================== 4 passed in 0.01s =====================================================
```

### 5.7. Verification Test Explained

The `test_check_scope_setups` function verifies the fixture behavior:

```python
def test_check_scope_setups():
    """Verify how often each fixture's setup ran in this module."""
    assert call_log.count("function-setup") == 3
    assert call_log.count("class-setup-TestFirst") == 1
    assert call_log.count("class-setup-TestSecond") == 1
    assert call_log.count("module-setup") == 1
    assert call_log.count("package-setup") == 1
    assert call_log.count("session-setup") == 1
```

**Why these counts?**

- `function-setup` appears **3 times**: test_a, test_b, test_c (test_check_scope_setups runs AFTER these)
- `class-setup-TestFirst` appears **1 time**: shared by test_a and test_b
- `class-setup-TestSecond` appears **1 time**: used only by test_c
- `module-setup` appears **1 time**: shared by all tests in the module
- `package-setup` appears **1 time**: shared by all tests in the package
- `session-setup` appears **1 time**: shared by all tests in the session

### 5.8. Key Takeaways

1. **Fixture scopes control lifetime**: Choose the right scope based on setup cost and test isolation needs
2. **Wider scopes = better performance**: But less isolation between tests
3. **Narrower scopes = better isolation**: But more setup/teardown overhead
4. **Default is `function` scope**: Each test gets fresh fixtures
5. **Tests declare dependencies**: Just add fixture names as parameters
6. **Pytest handles everything**: Discovery, instantiation, injection, cleanup

### 5.9. Common Patterns

#### Pattern 1: Expensive Setup with Module Scope
```python
@pytest.fixture(scope="module")
def api_client():
    """Create API client once per module."""
    client = APIClient(base_url="https://api.example.com")
    client.authenticate()
    yield client
    client.logout()
```

#### Pattern 2: Fresh Data with Function Scope
```python
@pytest.fixture(scope="function")
def clean_database():
    """Reset database before each test."""
    db.clear_all_tables()
    db.seed_test_data()
    yield db
    db.clear_all_tables()
```

#### Pattern 3: Session-Wide Test Server
```python
@pytest.fixture(scope="session")
def test_server():
    """Start test server once for all tests."""
    server = TestServer(port=8000)
    server.start()
    yield server
    server.stop()
```

---

## 6. Fixture Dependencies

Fixtures can depend on other fixtures! This creates a **dependency chain** where pytest automatically resolves the order.

### 6.1. Basic Fixture Dependencies

**File**: `test_fixture_dependencies.py`

```python
import pytest

@pytest.fixture
def database():
    """Simulates a database connection."""
    print("\n[SETUP] Connecting to database")
    db = {"connected": True, "data": []}
    yield db
    print("\n[TEARDOWN] Closing database")

@pytest.fixture
def user_data(database):
    """Depends on database fixture."""
    print("[SETUP] Loading user data")
    database["data"].append({"user": "Alice"})
    yield database["data"]
    print("[TEARDOWN] Clearing user data")

def test_user_exists(user_data):
    """Test uses user_data, which depends on database."""
    assert len(user_data) == 1
    assert user_data[0]["user"] == "Alice"
```

**Execution order**:
1. `database` fixture setup
2. `user_data` fixture setup (receives `database`)
3. Test runs (receives `user_data`)
4. `user_data` fixture teardown
5. `database` fixture teardown

### 6.2. Multiple Dependencies

```python
@pytest.fixture
def config():
    return {"api_url": "https://api.example.com"}

@pytest.fixture
def auth_token():
    return "secret-token-123"

@pytest.fixture
def api_client(config, auth_token):
    """Depends on both config and auth_token."""
    client = APIClient(config["api_url"])
    client.set_token(auth_token)
    return client

def test_api_call(api_client):
    """Test receives api_client with all dependencies resolved."""
    response = api_client.get("/users")
    assert response.status_code == 200
```

---

## 7. Autouse Fixtures

Sometimes you want a fixture to run automatically for all tests, without explicitly requesting it.

### 7.1. Basic Autouse

**File**: `test_autouse_fixture.py`

```python
import pytest

@pytest.fixture(autouse=True)
def reset_state():
    """Runs automatically before every test."""
    print("\n[AUTO] Resetting global state")
    global_state.clear()
    yield
    print("[AUTO] Cleanup after test")

def test_one():
    """Doesn't request reset_state, but it still runs."""
    assert len(global_state) == 0

def test_two():
    """Also gets automatic reset."""
    assert len(global_state) == 0
```

### 7.2. Autouse with Scope

```python
@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Runs once at module start, automatically."""
    print("\n[MODULE SETUP] Initializing module resources")
    yield
    print("\n[MODULE TEARDOWN] Cleaning up module resources")
```

**Use cases for autouse**:
- Resetting global state
- Setting up logging
- Initializing test environment
- Cleaning up after tests

---

## 8. Built-in Fixtures

Pytest provides many useful built-in fixtures.

### 8.1. `tmp_path` - Temporary Directory

**File**: `test_tmp_path_fixture.py`

```python
def test_create_file(tmp_path):
    """tmp_path provides a temporary directory unique to this test."""
    # tmp_path is a pathlib.Path object
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, pytest!")

    assert test_file.read_text() == "Hello, pytest!"
    assert test_file.exists()
    # Directory is automatically cleaned up after the test
```

### 8.2. `capsys` - Capture Output

```python
def test_print_output(capsys):
    """capsys captures stdout and stderr."""
    print("Hello, world!")
    print("Error!", file=sys.stderr)

    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"
    assert captured.err == "Error!\n"
```

### 8.3. `monkeypatch` - Modify Objects

```python
def test_environment_variable(monkeypatch):
    """monkeypatch temporarily modifies objects."""
    monkeypatch.setenv("API_KEY", "test-key-123")

    assert os.getenv("API_KEY") == "test-key-123"
    # Automatically restored after test
```

### 8.4. Other Useful Built-in Fixtures

- `request` - Information about the requesting test
- `capfd` - Capture file descriptors
- `caplog` - Capture log messages
- `tmpdir` - Temporary directory (legacy, use `tmp_path`)
- `pytestconfig` - Access to pytest configuration

---

## Summary

### Quick Reference

| Concept | Description | Example |
|---------|-------------|---------|
| **Basic Fixture** | Reusable setup/teardown | `@pytest.fixture` |
| **Scope** | Control fixture lifetime | `scope="function"` (default) |
| **Dependencies** | Fixtures can use other fixtures | `def fixture_b(fixture_a):` |
| **Autouse** | Run automatically | `autouse=True` |
| **Built-in** | Pytest-provided fixtures | `tmp_path`, `capsys`, `monkeypatch` |

### Fixture Scopes Cheat Sheet

```python
@pytest.fixture(scope="function")   # New instance per test (default)
@pytest.fixture(scope="class")      # Shared within test class
@pytest.fixture(scope="module")     # Shared within module file
@pytest.fixture(scope="package")    # Shared within package
@pytest.fixture(scope="session")    # Shared across entire test run
```

### Best Practices

1. **Use descriptive names**: `database_connection` not `db`
2. **Keep fixtures focused**: One responsibility per fixture
3. **Choose appropriate scope**: Balance performance vs. isolation
4. **Use `yield` for cleanup**: Ensures teardown even on failure
5. **Document complex fixtures**: Add docstrings explaining purpose
6. **Avoid fixture overuse**: Don't make everything a fixture

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all fixture tests
pytest fixtures/ -v

# Run a specific test file
pytest fixtures/test_fixture_scopes_all.py -v

# Run with output visible
pytest fixtures/ -v -s
```

---

[← Back to Main Guide](../README.md)

