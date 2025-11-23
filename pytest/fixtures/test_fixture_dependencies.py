import pytest
import sys
from pathlib import Path

# Add test_subjects to path so we can import calculator
sys.path.insert(0, str(Path(__file__).parent.parent / "test_subjects"))
import calculator


# Phase 3 – Fixtures: fixtures depending on other fixtures


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


'''
Output from: pytest -v test_fixture_dependencies.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_fixture_dependencies.py::test_product_uses_base_numbers PASSED
test_fixture_dependencies.py::test_can_use_both_fixtures PASSED

==================================================== 2 passed in 0.01s ====================================================
'''


def test_can_use_both_fixtures(base_numbers, product):
    """Tests can mix direct fixture values and dependent fixtures."""
    a, b = base_numbers
    assert a + b == 5
    assert product == a * b == 6

