# Conftest.py Patterns - Complete Guide

[← Back to Main Guide](../README.md)

> **Location**: `pytest/conftest_patterns/`  
> **Test Files**: All conftest.py pattern examples are in this folder

---

## Table of Contents

1. [What is conftest.py?](#1-what-is-conftestpy)
2. [Basic conftest.py](#2-basic-conftestpy)
3. [Fixture Scopes in conftest.py](#3-fixture-scopes-in-conftestpy)
4. [Nested conftest.py Files](#4-nested-conftestpy-files)
5. [Package-Scoped Fixtures](#5-package-scoped-fixtures)
6. [Session-Scoped Fixtures](#6-session-scoped-fixtures)
7. [Sharing Fixtures Across Tests](#7-sharing-fixtures-across-tests)
8. [conftest.py Best Practices](#8-conftestpy-best-practices)

---

## 1. What is conftest.py?

**conftest.py** is a special pytest file that:

- **Shares fixtures** across multiple test files
- **Configures pytest** behavior for a directory and its subdirectories
- **Defines hooks** to customize test execution
- **Registers plugins** and custom markers
- **Is automatically discovered** by pytest (no need to import)

### Key Features

✅ **Automatic discovery**: Pytest finds and loads conftest.py automatically  
✅ **Hierarchical**: Can have multiple conftest.py files at different levels  
✅ **Scope control**: Fixtures can have different scopes (function, class, module, package, session)  
✅ **No imports needed**: Fixtures are available without importing  

### When to Use conftest.py

Use conftest.py when you need to:
- Share fixtures across multiple test files
- Set up test environment (database, API clients, etc.)
- Configure pytest for a specific directory
- Define custom markers or hooks
- Avoid duplicating fixture code

---

## 2. Basic conftest.py

### 2.1. Simple Shared Fixture

**File**: `conftest.py`

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"name": "Alice", "age": 30}
```

**File**: `test_user.py`

```python
def test_user_name(sample_data):
    """Test using shared fixture from conftest.py."""
    assert sample_data["name"] == "Alice"

def test_user_age(sample_data):
    """Test using shared fixture from conftest.py."""
    assert sample_data["age"] == 30
```

**File**: `test_profile.py`

```python
def test_profile_data(sample_data):
    """Another test file using the same fixture."""
    assert "name" in sample_data
    assert "age" in sample_data
```

### 2.2. Multiple Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def database():
    """Provide database connection."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def api_client():
    """Provide API client."""
    client = APIClient()
    yield client
    client.close()

@pytest.fixture
def test_user(database):
    """Create test user (depends on database fixture)."""
    user = database.create_user("testuser")
    yield user
    database.delete_user(user.id)
```

---

## 3. Fixture Scopes in conftest.py

Fixtures in conftest.py can have different scopes:

| Scope | Lifetime | Use Case |
|-------|----------|----------|
| `function` | Each test function (default) | Test-specific data |
| `class` | Each test class | Shared within class |
| `module` | Each test module (file) | Shared within file |
| `package` | Each test package (directory) | Shared within directory |
| `session` | Entire test session | Expensive setup (database, server) |

### 3.1. Function Scope (Default)

```python
# conftest.py
import pytest

@pytest.fixture  # scope="function" is default
def temp_file():
    """Create temporary file for each test."""
    file = create_temp_file()
    yield file
    file.delete()

# Each test gets its own temp_file
```

### 3.2. Module Scope

```python
# conftest.py
import pytest

@pytest.fixture(scope="module")
def database_connection():
    """Create database connection once per test file."""
    db = Database()
    db.connect()
    print("\n[SETUP] Database connected")
    yield db
    print("\n[TEARDOWN] Database disconnected")
    db.disconnect()

# Connection is created once per test file, shared by all tests in that file
```

### 3.3. Session Scope

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def test_server():
    """Start test server once for entire test session."""
    server = TestServer()
    server.start()
    print("\n[SETUP] Server started")
    yield server
    print("\n[TEARDOWN] Server stopped")
    server.stop()

# Server starts once at beginning, stops at end of all tests
```

---

## 4. Nested conftest.py Files

You can have multiple conftest.py files at different directory levels. Pytest loads them hierarchically.

### 4.1. Directory Structure

```
pytest/
├── conftest.py              # Root conftest (session-wide)
├── test_root.py
├── api/
│   ├── conftest.py          # API-specific conftest
│   ├── test_users.py
│   └── test_posts.py
└── database/
    ├── conftest.py          # Database-specific conftest
    └── test_queries.py
```

### 4.2. Root conftest.py

```python
# pytest/conftest.py
import pytest

@pytest.fixture(scope="session")
def config():
    """Global configuration for all tests."""
    return {
        "api_url": "http://localhost:8000",
        "db_url": "sqlite:///:memory:"
    }
```

### 4.3. Subdirectory conftest.py

```python
# pytest/api/conftest.py
import pytest

@pytest.fixture
def api_client(config):
    """API client for API tests (uses config from root conftest)."""
    client = APIClient(config["api_url"])
    yield client
    client.close()
```

### 4.4. Fixture Override

Child conftest.py can override parent fixtures:

```python
# pytest/conftest.py (root)
import pytest

@pytest.fixture
def database_url():
    """Default database URL."""
    return "sqlite:///:memory:"

# pytest/integration/conftest.py (subdirectory)
import pytest

@pytest.fixture
def database_url():
    """Override with real database for integration tests."""
    return "postgresql://localhost/test_db"
```

**File**: `nested_conftest_pkg/` - Complete example of nested conftest files

---

## 5. Package-Scoped Fixtures

Package scope creates fixtures once per directory (package).

### 5.1. Package Scope Example

```python
# conftest.py
import pytest

@pytest.fixture(scope="package")
def package_logger():
    """Logger shared across all tests in this package."""
    logger = Logger("test_package")
    logger.info("Package tests starting")
    yield logger
    logger.info("Package tests complete")
    logger.close()
```

### 5.2. When to Use Package Scope

Use package scope when:
- Setting up resources for a specific test directory
- Creating test data for a module
- Initializing package-specific configuration

**File**: `package_scope_pkg/` - Complete example of package-scoped fixtures

---

## 6. Session-Scoped Fixtures

Session scope creates fixtures once for the entire test run.

### 6.1. Session Scope Example

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def test_database():
    """Database connection for entire test session."""
    db = Database()
    db.connect()
    db.create_test_schema()
    print("\n[SESSION SETUP] Database ready")

    yield db

    print("\n[SESSION TEARDOWN] Cleaning up database")
    db.drop_test_schema()
    db.disconnect()
```

### 6.2. Sharing Session Fixtures

Session fixtures can be shared across all test files:

**File**: `session_scope_shared.py`

```python
# session_scope_shared.py
import pytest

@pytest.fixture(scope="session")
def shared_resource():
    """Expensive resource created once."""
    print("\n[SETUP] Creating expensive resource")
    resource = ExpensiveResource()
    resource.initialize()
    yield resource
    print("\n[TEARDOWN] Destroying expensive resource")
    resource.cleanup()
```

**File**: `test_session_scope_one.py`

```python
def test_first_use(shared_resource):
    """First test using shared resource."""
    assert shared_resource.is_ready()
```

**File**: `test_session_scope_two.py`

```python
def test_second_use(shared_resource):
    """Second test using same shared resource."""
    assert shared_resource.is_ready()
```

Both tests use the same `shared_resource` instance!

---

## 7. Sharing Fixtures Across Tests

### 7.1. Simple Sharing

**File**: `conftest.py`

```python
import pytest

@pytest.fixture
def user_data():
    """User data available to all tests."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "role": "admin"
    }
```

**File**: `test_conftest_shared_fixtures.py`

```python
def test_username(user_data):
    """Test using shared fixture."""
    assert user_data["username"] == "testuser"

def test_email(user_data):
    """Another test using shared fixture."""
    assert "@" in user_data["email"]
```

### 7.2. Fixture Dependencies

Fixtures can depend on other fixtures:

```python
# conftest.py
import pytest

@pytest.fixture
def database():
    """Database connection."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repository(database):
    """User repository (depends on database)."""
    return UserRepository(database)

@pytest.fixture
def test_user(user_repository):
    """Test user (depends on user_repository)."""
    user = user_repository.create(username="testuser")
    yield user
    user_repository.delete(user.id)
```

### 7.3. Autouse Fixtures

Autouse fixtures run automatically for all tests:

```python
# conftest.py
import pytest

@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test (runs automatically)."""
    database.reset()
    yield
    # Cleanup if needed

@pytest.fixture(autouse=True, scope="session")
def setup_logging():
    """Setup logging for entire session (runs once)."""
    logging.basicConfig(level=logging.DEBUG)
    yield
    logging.shutdown()
```

---

## 8. conftest.py Best Practices

### 8.1. Organize by Scope

Keep fixtures organized by scope:

```python
# conftest.py
import pytest

# ============================================================================
# SESSION-SCOPED FIXTURES (created once for entire test run)
# ============================================================================

@pytest.fixture(scope="session")
def test_server():
    """Test server for all tests."""
    server = TestServer()
    server.start()
    yield server
    server.stop()

# ============================================================================
# MODULE-SCOPED FIXTURES (created once per test file)
# ============================================================================

@pytest.fixture(scope="module")
def database_connection():
    """Database connection per test file."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# ============================================================================
# FUNCTION-SCOPED FIXTURES (created for each test)
# ============================================================================

@pytest.fixture
def temp_user(database_connection):
    """Temporary user for each test."""
    user = database_connection.create_user("temp")
    yield user
    database_connection.delete_user(user.id)
```

### 8.2. Use Descriptive Names

✅ **Good**:
```python
@pytest.fixture
def authenticated_api_client():
    """API client with authentication."""
    pass

@pytest.fixture
def empty_database():
    """Clean database with no data."""
    pass
```

❌ **Bad**:
```python
@pytest.fixture
def client():  # Too generic
    pass

@pytest.fixture
def db():  # Unclear what state
    pass
```

### 8.3. Document Fixtures

Always add docstrings:

```python
@pytest.fixture(scope="session")
def test_config():
    """
    Test configuration for entire session.

    Provides:
        - API URL
        - Database URL
        - Test credentials

    Scope: session (created once)
    """
    return {
        "api_url": "http://localhost:8000",
        "db_url": "sqlite:///:memory:",
        "username": "testuser",
        "password": "testpass"
    }
```

### 8.4. Avoid Global State

❌ **Bad** (global state):
```python
# conftest.py
DATABASE = None  # Global variable

@pytest.fixture
def database():
    global DATABASE
    if DATABASE is None:
        DATABASE = Database()
    return DATABASE
```

✅ **Good** (use session scope):
```python
# conftest.py
@pytest.fixture(scope="session")
def database():
    """Database connection (session-scoped)."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```

### 8.5. One conftest.py per Directory

Structure your conftest files logically:

```
pytest/
├── conftest.py              # Shared across all tests
├── unit/
│   ├── conftest.py          # Unit test fixtures
│   └── test_*.py
├── integration/
│   ├── conftest.py          # Integration test fixtures
│   └── test_*.py
└── e2e/
    ├── conftest.py          # E2E test fixtures
    └── test_*.py
```

### 8.6. Keep It Simple

Don't put too much logic in conftest.py:

✅ **Good**:
```python
@pytest.fixture
def api_client():
    """Simple API client fixture."""
    client = APIClient()
    yield client
    client.close()
```

❌ **Bad**:
```python
@pytest.fixture
def api_client():
    """Overly complex fixture."""
    # Too much logic in fixture
    if os.getenv("USE_MOCK"):
        client = MockAPIClient()
    else:
        client = RealAPIClient()

    client.configure(...)
    client.authenticate(...)
    client.setup_logging(...)
    # ... 50 more lines

    yield client
    # ... complex cleanup
```

---

## 9. Real-World Examples

### 9.1. Web Application Testing

```python
# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def browser():
    """Browser instance for entire test session."""
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_user(browser):
    """User logged into the application."""
    browser.get("http://localhost:8000/login")
    browser.find_element_by_id("username").send_keys("testuser")
    browser.find_element_by_id("password").send_keys("testpass")
    browser.find_element_by_id("submit").click()
    yield browser
    # Logout
    browser.get("http://localhost:8000/logout")
```

### 9.2. API Testing

```python
# conftest.py
import pytest
import requests

@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for API."""
    return "http://localhost:8000/api"

@pytest.fixture
def api_client(api_base_url):
    """API client with authentication."""
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer test_token"})
    session.base_url = api_base_url
    yield session
    session.close()

@pytest.fixture
def test_user(api_client):
    """Create test user via API."""
    response = api_client.post("/users", json={"username": "testuser"})
    user = response.json()
    yield user
    # Cleanup
    api_client.delete(f"/users/{user['id']}")
```

### 9.3. Database Testing

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def database_engine():
    """Database engine for entire session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(database_engine):
    """Database session for each test."""
    Session = sessionmaker(bind=database_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    """Create sample user in database."""
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    yield user
    # Cleanup handled by session rollback
```

---

## 10. Advanced Patterns

### 10.1. Parametrized Fixtures in conftest.py

```python
# conftest.py
import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """Test with multiple database types."""
    return request.param

@pytest.fixture
def database(database_type):
    """Database connection based on type."""
    if database_type == "sqlite":
        db = SQLiteDatabase()
    elif database_type == "postgresql":
        db = PostgreSQLDatabase()
    else:
        db = MySQLDatabase()

    db.connect()
    yield db
    db.disconnect()
```

### 10.2. Conditional Fixtures

```python
# conftest.py
import pytest
import os

@pytest.fixture
def api_client():
    """API client (real or mock based on environment)."""
    if os.getenv("USE_MOCK_API") == "true":
        client = MockAPIClient()
    else:
        client = RealAPIClient()

    yield client
    client.close()
```

### 10.3. Fixture Factories

```python
# conftest.py
import pytest

@pytest.fixture
def user_factory(db_session):
    """Factory to create multiple users."""
    created_users = []

    def create_user(username, email):
        user = User(username=username, email=email)
        db_session.add(user)
        db_session.commit()
        created_users.append(user)
        return user

    yield create_user

    # Cleanup all created users
    for user in created_users:
        db_session.delete(user)
    db_session.commit()

# Usage in test
def test_multiple_users(user_factory):
    user1 = user_factory("alice", "alice@example.com")
    user2 = user_factory("bob", "bob@example.com")
    assert user1.id != user2.id
```

### 10.4. Fixture Caching

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def expensive_computation():
    """Expensive computation cached for session."""
    print("\n[COMPUTING] This takes 10 seconds...")
    result = perform_expensive_computation()
    print("[DONE] Computation complete")
    return result

# All tests share the same result
```

---

## 11. Debugging conftest.py

### 11.1. Print Fixture Execution

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def debug_fixture():
    """Fixture with debug output."""
    print("\n[SETUP] Session fixture created")
    yield "data"
    print("\n[TEARDOWN] Session fixture destroyed")
```

Run with `-s` to see output:
```bash
pytest -s -v
```

### 11.2. List Available Fixtures

```bash
# Show all fixtures
pytest --fixtures

# Show fixtures from specific file
pytest --fixtures test_file.py

# Show only custom fixtures (not built-in)
pytest --fixtures -v
```

### 11.3. Fixture Execution Order

```python
# conftest.py
import pytest

@pytest.fixture(scope="session", autouse=True)
def session_fixture():
    print("\n1. Session fixture setup")
    yield
    print("\n6. Session fixture teardown")

@pytest.fixture(scope="module", autouse=True)
def module_fixture():
    print("\n2. Module fixture setup")
    yield
    print("\n5. Module fixture teardown")

@pytest.fixture(autouse=True)
def function_fixture():
    print("\n3. Function fixture setup")
    yield
    print("\n4. Function fixture teardown")
```

---

## 12. Summary

### Key Takeaways

1. **conftest.py**: Special file for sharing fixtures and configuration
2. **Automatic discovery**: No imports needed, pytest finds it automatically
3. **Hierarchical**: Can have multiple conftest.py files at different levels
4. **Scopes**: function, class, module, package, session
5. **Fixture override**: Child conftest can override parent fixtures
6. **Autouse**: Fixtures that run automatically
7. **Best practices**: Organize by scope, use descriptive names, document well

### Common Patterns

```python
# Basic shared fixture
@pytest.fixture
def shared_data():
    return {"key": "value"}

# Session-scoped (expensive setup)
@pytest.fixture(scope="session")
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# Autouse (runs automatically)
@pytest.fixture(autouse=True)
def reset_state():
    reset()
    yield

# Fixture dependency
@pytest.fixture
def user(database):
    return database.create_user("test")
```

### Directory Structure

```
pytest/
├── conftest.py              # Root-level fixtures
├── test_*.py
├── api/
│   ├── conftest.py          # API-specific fixtures
│   └── test_*.py
└── database/
    ├── conftest.py          # Database-specific fixtures
    └── test_*.py
```

### What's Next?

- **[Fixtures](../fixtures/)** - Deep dive into fixtures
- **[Mocking](../mocking/)** - Mock objects in tests
- **[Basics](../basics/)** - Pytest fundamentals

---

## Running the Examples

From the `pytest/` directory:

```bash
# Run all conftest pattern tests
pytest conftest_patterns/ -v

# Run with output visible (see fixture setup/teardown)
pytest conftest_patterns/ -v -s

# List all available fixtures
pytest conftest_patterns/ --fixtures

# Run specific example
pytest conftest_patterns/nested_conftest_pkg/ -v
pytest conftest_patterns/package_scope_pkg/ -v
```

---

[← Back to Main Guide](../README.md)

