import pytest

from .orders import Order, OrderItem
from .discounts import DiscountRule, calculate_discount, total_after_discounts


# Extra Phase 9 module – discounts on top of orders


@pytest.fixture
def default_rules() -> list[DiscountRule]:
    """Two simple discount tiers used in multiple tests.

    - 10% off for orders >= 100
    - 15% off for orders >= 500
    """

    return [
        DiscountRule(name="10%-over-100", min_total=100.0, percent_off=10.0),
        DiscountRule(name="15%-over-500", min_total=500.0, percent_off=15.0),
    ]


@pytest.mark.parametrize(
    "total, expected_discount",
    [
        (50.0, 0.0),
        (150.0, 15.0),   # 10% of 150
        (600.0, 90.0),   # 15% of 600 (better than 10%)
    ],
    ids=["no-discount", "ten-percent", "fifteen-percent"],
)
def test_calculate_discount_for_various_totals(total, expected_discount, default_rules):
    """Parametrized test that drives the discount logic with simple orders."""

    order = Order(items=[OrderItem(name="item", price=total, quantity=1)])
    assert calculate_discount(order, default_rules) == expected_discount


@pytest.mark.db
@pytest.mark.parametrize(
    "total, expected_final",
    [
        (50.0, 50.0),     # no discount
        (150.0, 135.0),   # 10% off
        (600.0, 510.0),   # 15% off
    ],
    ids=["no-discount", "ten-percent", "fifteen-percent"],
)
def test_total_after_discounts(total, expected_final, default_rules):
    """Show how total_after_discounts composes with the order model.

    We mark this test with ``db`` just to demonstrate another marker from
    ``pytest.ini``.
    """

    order = Order(items=[OrderItem(name="item", price=total, quantity=1)])
    assert total_after_discounts(order, default_rules) == expected_final


output = """\
$ pytest -vs mini_project/test_mini_project_discounts.py
=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 6 items

mini_project/test_mini_project_discounts.py::test_calculate_discount_for_various_totals[no-discount] PASSED
mini_project/test_mini_project_discounts.py::test_calculate_discount_for_various_totals[ten-percent] PASSED
mini_project/test_mini_project_discounts.py::test_calculate_discount_for_various_totals[fifteen-percent] PASSED
mini_project/test_mini_project_discounts.py::test_total_after_discounts[no-discount] PASSED
mini_project/test_mini_project_discounts.py::test_total_after_discounts[ten-percent] PASSED
mini_project/test_mini_project_discounts.py::test_total_after_discounts[fifteen-percent] PASSED

==================================================== 6 passed in 0.01s ====================================================
"""

