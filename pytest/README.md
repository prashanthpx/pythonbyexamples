# Pytest Learning Guide

Welcome to the **Pytest Learning Guide**! This is a comprehensive, example-driven guide to mastering pytest from beginner to advanced level.

## 📚 Documentation Structure

This guide is organized into focused topics. Each topic has its own folder with:
- **README.md**: Comprehensive documentation with examples
- **Test files**: Real, runnable pytest examples

### 📂 Folder Structure

```
pytest/
├── README.md                    # This file - main guide
├── pytest.ini                   # Pytest configuration
├── conftest.py                  # Root-level fixtures
│
├── basics/                      # 🟢 START HERE - Pytest fundamentals
├── fixtures/                    # Fixture patterns and scopes
├── markers/                     # Test organization and selection
├── parametrize/                 # Testing with multiple inputs
├── exceptions/                  # Exception testing and pytest.raises
├── mocking/                     # Mocking with monkeypatch and mocker
├── conftest_patterns/           # Advanced conftest.py usage
└── test_subjects/               # Example code being tested
```

### Core Topics

1. **[Basics](basics/)** - 🟢 **START HERE**
   - Your first test
   - Basic assertions (numbers, strings, lists, booleans)
   - Grouping tests with classes
   - Running tests
   - **14 tests** (2 intentional failures for demonstration)

2. **[Fixtures](fixtures/)** - The heart of pytest
   - Basic fixtures and setup/teardown
   - Fixture scopes (function, class, module, package, session)
   - Fixture dependencies
   - Autouse fixtures
   - Built-in fixtures (tmp_path, etc.)
   - **15 tests** - All pass

3. **[Markers](markers/)** - Organizing and controlling tests
   - Built-in markers (skip, skipif, xfail)
   - Custom markers and registration
   - Selecting tests with `-m`
   - pytestmark for module-level markers
   - Selecting by name with `-k`
   - **13 passed, 3 skipped, 2 xfailed**

4. **[Parametrize](parametrize/)** - Running tests with multiple inputs
   - Basic parametrize with single/multiple parameters
   - Custom IDs for test cases
   - Combining parametrize with fixtures
   - Indirect parametrization
   - Parametrize with markers
   - Parametrized fixtures
   - **18 passed, 1 xfailed**

5. **[Exceptions](exceptions/)** - Testing behavior and errors
   - pytest.raises for exception testing
   - Inspecting exception details
   - Testing exception messages
   - Custom exceptions
   - pytest.fail and pytest.xfail
   - Expected failures
   - **5 passed, 1 xfailed, 2 intentional failures**

6. **[Mocking](mocking/)** - Isolating tests from external dependencies
   - monkeypatch fixture (pytest built-in)
   - pytest-mock (mocker fixture)
   - Mocking functions, methods, and attributes
   - Verifying mock calls
   - **2 passed, 1 skipped**

7. **[Conftest Patterns](conftest_patterns/)** - Sharing fixtures and configuration
   - How conftest.py works
   - Fixture sharing across tests
   - Nested conftest files
   - Package and session scopes
   - **10 tests** - All pass

8. **[Test Subjects](test_subjects/)** - Example code being tested
   - Calculator module with tests
   - String utilities with tests
   - Testing patterns and best practices
   - **14 tests** - All pass

## 🚀 Quick Start

### Running Tests

From the `pytest/` directory:

```bash
# Run all tests in all folders
pytest

# Run tests from a specific topic
pytest basics/ -v
pytest fixtures/ -v
pytest markers/ -v
pytest parametrize/ -v
pytest exceptions/ -v
pytest mocking/ -v
pytest conftest_patterns/ -v
pytest test_subjects/ -v

# Run with verbose output and show print statements
pytest -v -s

# Run a specific file
pytest fixtures/test_fixture_scopes_all.py -v

# Run tests matching a pattern
pytest -k "fixture" -v

# Run tests with a specific marker
pytest -m "slow" -v
```

### Command-Line Cheat Sheet

```bash
# Basic commands
pytest                    # Run all tests
pytest -v                 # Verbose mode (show test names)
pytest -s                 # Show print() output
pytest -v -s              # Both verbose and show prints

# Selection
pytest basics/            # Run all tests in basics folder
pytest -k "pattern"       # Run tests matching pattern
pytest -m "marker"        # Run tests with specific marker

# Failure handling
pytest --lf               # Run last failed tests
pytest --ff               # Run failures first, then others
pytest -x                 # Stop on first failure
pytest --maxfail=3        # Stop after 3 failures

# Information
pytest --fixtures         # List all available fixtures
pytest --markers          # List all available markers
pytest --collect-only     # Show what tests would run
```

## 📖 Learning Path

### 🟢 Beginner (Start Here)

**Week 1: Fundamentals**
1. **[Basics](basics/)** - Your first tests, assertions, grouping
   - Run: `pytest basics/ -v`
   - Time: 30 minutes

2. **[Test Subjects](test_subjects/)** - Testing real code
   - Run: `pytest test_subjects/ -v`
   - Time: 30 minutes

3. **[Fixtures](fixtures/)** - Sections 1-3 (Basic fixtures and setup/teardown)
   - Run: `pytest fixtures/test_fixture.py -v`
   - Time: 1 hour

**Week 2: Organization**
4. **[Markers](markers/)** - Sections 1-4 (skip, skipif, xfail, custom markers)
   - Run: `pytest markers/ -v`
   - Time: 1 hour

5. **[Exceptions](exceptions/)** - Testing errors with pytest.raises
   - Run: `pytest exceptions/ -v`
   - Time: 45 minutes

### 🟡 Intermediate

**Week 3: Advanced Patterns**
6. **[Fixtures](fixtures/)** - Sections 4-7 (Fixture scopes and dependencies)
   - Run: `pytest fixtures/test_fixture_scopes_all.py -v -s`
   - Time: 1.5 hours

7. **[Parametrize](parametrize/)** - Test with multiple inputs
   - Run: `pytest parametrize/ -v`
   - Time: 1.5 hours

8. **[Conftest Patterns](conftest_patterns/)** - Share fixtures across files
   - Run: `pytest conftest_patterns/ -v`
   - Time: 1 hour

### 🔴 Advanced

**Week 4: Professional Testing**
9. **[Mocking](mocking/)** - Isolate external dependencies
   - Run: `pytest mocking/ -v`
   - Time: 2 hours

10. **[Markers](markers/)** - Advanced sections (Complex test selection)
    - Run: `pytest markers/ -m slow -v`
    - Time: 1 hour

11. **Practice**: Combine everything
    - Write tests for your own code
    - Use fixtures, parametrize, mocking together
    - Time: Ongoing

## 🎯 Philosophy

This guide follows a simple principle:

> **Every test file has detailed documentation in its topic folder's README.md**

Each topic folder contains:
- **README.md**: Comprehensive guide with explanations, examples, and best practices
- **Test files**: Real, runnable pytest examples that demonstrate the concepts
- **Code under test**: (in test_subjects/) Actual code being tested

When you explore a topic like `fixtures/`, you'll find:
- Complete documentation in `fixtures/README.md`
- Working test files you can run and modify
- Inline comments explaining what's happening
- Best practices and common patterns
- Links to related topics

## 📊 Test Statistics

Total tests across all folders: **91 tests**

| Folder | Tests | Status |
|--------|-------|--------|
| basics/ | 16 | 14 passed, 2 intentional fails |
| fixtures/ | 15 | All pass |
| markers/ | 18 | 13 passed, 3 skipped, 2 xfailed |
| parametrize/ | 19 | 18 passed, 1 xfailed |
| exceptions/ | 8 | 5 passed, 1 xfailed, 2 intentional fails |
| mocking/ | 3 | 2 passed, 1 skipped |
| conftest_patterns/ | 10 | All pass |
| test_subjects/ | 14 | All pass |

Run all tests: `pytest -v`

## 🎓 Tips for Learning

1. **Run the tests**: Don't just read - run every example
   ```bash
   pytest basics/ -v -s
   ```

2. **Modify and experiment**: Change the code and see what happens
   - What if you remove a fixture?
   - What if you change a marker?
   - What if you add more test cases?

3. **Read the output**: Pytest's output is very informative
   - Look at test names
   - Read failure messages
   - Check the traceback

4. **Follow the learning path**: Start with basics, progress to advanced
   - Don't skip ahead too quickly
   - Master each topic before moving on

5. **Practice with your own code**: Apply what you learn
   - Write tests for your projects
   - Use fixtures to organize setup
   - Use parametrize for multiple cases

## 🔗 External Resources

- [Official Pytest Documentation](https://docs.pytest.org/)
- [Pytest on GitHub](https://github.com/pytest-dev/pytest)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)

---

**Happy Testing! 🧪**

