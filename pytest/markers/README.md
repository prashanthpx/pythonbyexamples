# Pytest Markers - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/markers/`  
> **Test Files**: All marker-related examples are in this folder

---

## Table of Contents

1. [What are Markers?](#1-what-are-markers)
2. [Built-in Markers](#2-built-in-markers)
3. [Custom Markers](#3-custom-markers)
4. [Selecting Tests with Markers](#4-selecting-tests-with-markers)
5. [Module-Level Markers](#5-module-level-markers)
6. [Combining Markers](#6-combining-markers)
7. [Selecting by Name with -k](#7-selecting-by-name-with--k)

---

## 1. What are Markers?

**Markers** are pytest's way of tagging tests with metadata. They allow you to:

- **Skip tests** conditionally or unconditionally
- **Mark tests as expected to fail** (xfail)
- **Tag tests** for selective execution (slow, fast, api, db, etc.)
- **Parametrize tests** (covered in parametrize section)
- **Add custom metadata** to tests

### Why Use Markers?

1. **Selective test execution**: Run only fast tests in development, all tests in CI
2. **Organize tests**: Group related tests (api tests, database tests, etc.)
3. **Skip problematic tests**: Temporarily skip broken tests without deleting them
4. **Document test characteristics**: Mark slow tests, flaky tests, etc.

---

## 2. Built-in Markers

Pytest provides several built-in markers out of the box.

### 2.1. `@pytest.mark.skip` - Skip Unconditionally

**File**: `test_markers.py`

```python
import pytest

@pytest.mark.skip(reason="demonstration of a skipped test")
def test_skipped_example():
    """This test is always skipped."""
    assert 1 == 2  # would fail if it ran, but it is skipped
```

**When to use**:
- Feature not implemented yet
- Test is broken and you need to fix it later
- Test only works on certain platforms

**Running**:
```bash
pytest markers/test_markers.py -v
```

**Output**:
```
markers/test_markers.py::test_skipped_example SKIPPED (demonstration of a skipped test)
```

### 2.2. `@pytest.mark.skipif` - Skip Conditionally

**File**: `test_skipif.py`

```python
import sys
import pytest

@pytest.mark.skipif(sys.platform == "win32", reason="does not run on Windows")
def test_linux_only():
    """This test only runs on non-Windows platforms."""
    assert True

@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8+")
def test_requires_python38():
    """This test requires Python 3.8 or higher."""
    assert True
```

**Common conditions**:
```python
# Skip based on platform
@pytest.mark.skipif(sys.platform == "darwin", reason="not for macOS")

# Skip based on Python version
@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10+")

# Skip based on environment variable
@pytest.mark.skipif(os.getenv("CI") is None, reason="only runs in CI")

# Skip based on module availability
@pytest.mark.skipif(not HAS_REDIS, reason="requires redis")
```

### 2.3. `@pytest.mark.xfail` - Expected to Fail

**File**: `test_markers.py`

```python
@pytest.mark.xfail(reason="demonstration of expected failure")
def test_expected_failure_example():
    """This test is expected to fail (xfail)."""
    assert 2 + 2 == 5  # xfail instead of fail
```

**When to use**:
- Known bug that hasn't been fixed yet
- Feature partially implemented
- Test documents desired behavior not yet achieved

**Output**:
```
markers/test_markers.py::test_expected_failure_example XFAIL (demonstration of expected failure)
```

**Difference from skip**:
- `skip`: Test doesn't run at all
- `xfail`: Test runs, but failure is expected and doesn't fail the test suite

### 2.4. Runtime Skip and XFail

**File**: `test_runtime_skip_xfail.py`

You can also skip or xfail tests at runtime (inside the test function):

```python
import pytest

def test_runtime_skip():
    """Skip test at runtime based on condition."""
    if not has_database_connection():
        pytest.skip("database not available")
    # Test continues only if database is available
    assert query_database() is not None

def test_runtime_xfail():
    """Mark test as xfail at runtime."""
    if is_known_bug():
        pytest.xfail("known bug #123")
    assert some_function() == expected_value
```

**When to use runtime skip/xfail**:
- Condition can't be determined until test runs
- Need to check resource availability
- Complex conditions that can't be expressed in decorator

---

## 3. Custom Markers

You can create your own markers to tag and organize tests.

### 3.1. Defining Custom Markers

Custom markers must be registered in `pytest.ini`:

**File**: `pytest.ini` (at root level)

```ini
[pytest]
markers =
    assertion: tests that exercise basic assertion behavior
    slow: tests that are slow or optional
    api: tests that call external or HTTP APIs
    db: tests that touch the database or persistence layer
```

### 3.2. Using Custom Markers

**File**: `test_markers.py`

```python
import pytest

@pytest.mark.slow
def test_slow_example():
    """A dummy 'slow' test, marked just for selection."""
    assert 1 + 1 == 2

@pytest.mark.api
def test_api_call():
    """Test that makes an API call."""
    response = make_api_request()
    assert response.status_code == 200

@pytest.mark.db
def test_database_query():
    """Test that queries the database."""
    result = db.query("SELECT * FROM users")
    assert len(result) > 0
```

### 3.3. Why Register Markers?

If you don't register markers in `pytest.ini`, pytest will show warnings:

```
PytestUnknownMarkWarning: Unknown pytest.mark.slow
```

Registering markers:
- Prevents typos (pytest warns about unregistered markers)
- Documents available markers
- Makes markers discoverable with `pytest --markers`

### 3.4. Listing Available Markers

```bash
pytest --markers
```

Shows all available markers including built-in and custom ones.

---

## 4. Selecting Tests with Markers

The real power of markers is selective test execution using `-m`.

### 4.1. Basic Selection

**File**: `test_multi_markers_selection.py`

```python
import pytest

@pytest.mark.slow
@pytest.mark.api
def test_slow_api():
    """Slow API test."""
    assert True

@pytest.mark.api
def test_fast_api():
    """Fast API test."""
    assert True

@pytest.mark.db
def test_db_only():
    """Database test."""
    assert True

@pytest.mark.slow
@pytest.mark.db
def test_slow_db():
    """Slow database test."""
    assert True

def test_unmarked():
    """Test with no markers."""
    assert True
```

### 4.2. Selection Examples

```bash
# Run only slow tests
pytest markers/ -m slow -v

# Run only API tests
pytest markers/ -m api -v

# Run only database tests
pytest markers/ -m db -v
```

### 4.3. Boolean Expressions

You can combine markers with boolean logic:

```bash
# Run tests marked as slow OR api
pytest markers/ -m "slow or api" -v

# Run tests marked as slow AND api (both markers)
pytest markers/ -m "slow and api" -v

# Run API tests that are NOT slow
pytest markers/ -m "api and not slow" -v

# Run everything except slow tests
pytest markers/ -m "not slow" -v
```

### 4.4. Real-World Example

```bash
# Development: Run only fast tests
pytest -m "not slow" -v

# CI: Run all tests including slow ones
pytest -v

# Integration testing: Run only API and DB tests
pytest -m "api or db" -v

# Smoke tests: Run fast, critical tests
pytest -m "smoke and not slow" -v
```

---

## 5. Module-Level Markers

You can apply markers to all tests in a module using `pytestmark`.

### 5.1. Single Module Marker

**File**: `test_module_markers.py`

```python
import pytest

# Apply 'api' marker to ALL tests in this module
pytestmark = pytest.mark.api

def test_endpoint_one():
    """Automatically has @pytest.mark.api."""
    assert True

def test_endpoint_two():
    """Also automatically has @pytest.mark.api."""
    assert True
```

**Running**:
```bash
pytest markers/ -m api -v
```

Both tests will run because they inherit the module-level marker.

### 5.2. Multiple Module Markers

```python
import pytest

# Apply multiple markers to all tests in this module
pytestmark = [pytest.mark.api, pytest.mark.slow]

def test_slow_api_one():
    """Has both 'api' and 'slow' markers."""
    assert True

def test_slow_api_two():
    """Also has both 'api' and 'slow' markers."""
    assert True
```

### 5.3. When to Use Module Markers

- All tests in a file test the same component (e.g., all API tests)
- All tests in a file are slow
- All tests in a file require the same setup (database, external service)

---

## 6. Combining Markers

Tests can have multiple markers for fine-grained control.

### 6.1. Multiple Markers on One Test

```python
import pytest

@pytest.mark.slow
@pytest.mark.api
@pytest.mark.integration
def test_complex_api_workflow():
    """This test has three markers."""
    assert True
```

### 6.2. Selection with Multiple Markers

```bash
# Run tests that are BOTH slow AND api
pytest -m "slow and api" -v

# Run tests that are slow OR api (or both)
pytest -m "slow or api" -v

# Run integration tests that are NOT slow
pytest -m "integration and not slow" -v
```

### 6.3. Practical Example

```python
import pytest

@pytest.mark.api
@pytest.mark.smoke  # Critical test
def test_api_health_check():
    """Quick health check - runs in smoke tests."""
    assert api.is_alive()

@pytest.mark.api
@pytest.mark.slow
def test_api_full_workflow():
    """Complete workflow - skipped in smoke tests."""
    result = api.complete_workflow()
    assert result.success

@pytest.mark.db
@pytest.mark.smoke
def test_db_connection():
    """Quick DB check - runs in smoke tests."""
    assert db.can_connect()

@pytest.mark.db
@pytest.mark.slow
def test_db_migration():
    """Full migration - skipped in smoke tests."""
    db.run_migration()
    assert db.schema_version == "latest"
```

**Usage**:
```bash
# Quick smoke tests (fast, critical tests)
pytest -m smoke -v

# Full test suite
pytest -v

# Only slow tests
pytest -m slow -v

# API tests excluding slow ones
pytest -m "api and not slow" -v
```

---

## 7. Selecting by Name with -k

The `-k` option lets you select tests by name pattern (not markers).

### 7.1. Basic Name Selection

**File**: `test_selection_k.py`

```python
def test_login_valid_credentials():
    """Test login with valid credentials."""
    assert True

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    assert True

def test_logout_after_login():
    """Test logout functionality."""
    assert True

def test_signup_new_user():
    """Test user signup."""
    assert True
```

### 7.2. Selection Examples

```bash
# Run all tests with "login" in the name
pytest markers/test_selection_k.py -k login -v

# Output:
# test_login_valid_credentials PASSED
# test_login_invalid_credentials PASSED
# test_logout_after_login PASSED  (contains "login")

# Run tests with "valid" in the name
pytest markers/test_selection_k.py -k valid -v

# Output:
# test_login_valid_credentials PASSED

# Run tests with "login" but NOT "invalid"
pytest markers/test_selection_k.py -k "login and not invalid" -v

# Output:
# test_login_valid_credentials PASSED
# test_logout_after_login PASSED
```

### 7.3. -k vs -m

| Feature | `-k` (keyword) | `-m` (marker) |
|---------|----------------|---------------|
| Selects by | Test name pattern | Marker tags |
| Requires setup | No | Yes (register in pytest.ini) |
| Boolean logic | Yes (`and`, `or`, `not`) | Yes (`and`, `or`, `not`) |
| Use case | Quick filtering by name | Organized test categorization |

### 7.4. Combining -k and -m

You can use both together:

```bash
# Run API tests with "login" in the name
pytest -m api -k login -v

# Run slow tests excluding "database"
pytest -m slow -k "not database" -v
```

### 7.5. When to Use -k

✅ **Good use cases**:
- Quick ad-hoc filtering during development
- Running all tests for a specific feature
- Excluding specific test names

❌ **Not ideal for**:
- Permanent test organization (use markers instead)
- Complex categorization (use markers instead)

---

## 8. Complete Example: Organizing a Test Suite

Let's see how to organize a real test suite with markers.

### 8.1. pytest.ini Configuration

```ini
[pytest]
markers =
    smoke: quick smoke tests that run on every commit
    slow: tests that take more than 1 second
    api: tests that call external APIs
    db: tests that require database
    integration: integration tests
    unit: unit tests
```

### 8.2. Test Files with Markers

**File**: `test_user_api.py`

```python
import pytest

pytestmark = pytest.mark.api  # All tests in this file are API tests

@pytest.mark.smoke
def test_api_health():
    """Quick health check."""
    assert api.ping() == "pong"

@pytest.mark.slow
def test_create_user_workflow():
    """Full user creation workflow."""
    user = api.create_user("Alice")
    assert user.id is not None
    assert api.get_user(user.id).name == "Alice"
```

**File**: `test_database.py`

```python
import pytest

pytestmark = pytest.mark.db  # All tests in this file are DB tests

@pytest.mark.smoke
def test_db_connection():
    """Quick DB connection check."""
    assert db.can_connect()

@pytest.mark.slow
def test_db_migration():
    """Full database migration."""
    db.migrate()
    assert db.version == "latest"
```

### 8.3. Running Different Test Suites

```bash
# Pre-commit: Run only smoke tests (fast)
pytest -m smoke -v

# Development: Run all tests except slow ones
pytest -m "not slow" -v

# CI: Run all tests
pytest -v

# Integration testing: Run API and DB tests
pytest -m "api or db" -v

# Unit tests only
pytest -m unit -v

# Slow tests only (run overnight)
pytest -m slow -v
```

---

## 9. Best Practices

### 9.1. Marker Naming Conventions

✅ **Good names** (clear, descriptive):
```python
@pytest.mark.slow
@pytest.mark.api
@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.requires_database
```

❌ **Bad names** (vague, unclear):
```python
@pytest.mark.test1
@pytest.mark.important
@pytest.mark.misc
```

### 9.2. Don't Over-Mark

❌ **Too many markers** (confusing):
```python
@pytest.mark.slow
@pytest.mark.api
@pytest.mark.integration
@pytest.mark.external
@pytest.mark.http
@pytest.mark.network
@pytest.mark.critical
def test_something():
    pass
```

✅ **Just enough markers** (clear):
```python
@pytest.mark.api
@pytest.mark.slow
def test_something():
    pass
```

### 9.3. Document Your Markers

Always register markers in `pytest.ini` with descriptions:

```ini
[pytest]
markers =
    slow: tests that take more than 1 second to run
    api: tests that make HTTP requests to external APIs
    db: tests that require database connection
    smoke: critical tests that run on every commit
    integration: tests that test multiple components together
    unit: isolated unit tests with no external dependencies
```

### 9.4. Consistent Marker Usage

Establish team conventions:

```python
# Convention: All API tests go in test_api_*.py files
# and have @pytest.mark.api

# Convention: All slow tests must be marked with @pytest.mark.slow
# so they can be skipped in development

# Convention: Smoke tests are fast, critical tests that always run
```

---

## 10. Summary

### Key Takeaways

1. **Built-in markers**: `skip`, `skipif`, `xfail` for controlling test execution
2. **Custom markers**: Tag tests for organization and selective execution
3. **Selection with -m**: Run specific subsets of tests
4. **Module markers**: Apply markers to all tests in a file with `pytestmark`
5. **Boolean logic**: Combine markers with `and`, `or`, `not`
6. **Selection with -k**: Filter tests by name pattern
7. **Register markers**: Always register custom markers in `pytest.ini`

### Common Workflows

```bash
# Development: Fast tests only
pytest -m "not slow"

# CI: All tests
pytest

# Smoke tests: Critical, fast tests
pytest -m smoke

# Integration: API and DB tests
pytest -m "api or db"

# Specific feature: Use -k
pytest -k "login"
```

### What's Next?

- **[Parametrize](../parametrize/)** - Run same test with different inputs
- **[Exceptions](../exceptions/)** - Test error handling with pytest.raises
- **[Fixtures](../fixtures/)** - Reusable setup and teardown

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all marker tests
pytest markers/ -v

# Run only slow tests
pytest markers/ -m slow -v

# Run only API tests
pytest markers/ -m api -v

# Run tests with "skip" in the name
pytest markers/ -k skip -v

# List all available markers
pytest --markers
```

---

[← Back to Main Guide](../README.md)

