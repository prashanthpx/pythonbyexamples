import pytest

from .orders import Order, OrderItem
from .payments import PaymentError, PaymentGateway, checkout


# Phase 9 – Putting it all together: mini checkout project


@pytest.mark.api
def test_checkout_success_with_patched_gateway(simple_order, configured_gateway, monkeypatch):
    """Happy-path checkout using fixtures, a marker, and monkeypatch.

    - ``simple_order`` and ``configured_gateway`` come from mini_project/conftest.py
    - We patch ``PaymentGateway.charge`` so no real external call happens.
    """

    calls: dict[str, float] = {}

    def fake_charge(self, amount: float):  # type: ignore[override]
        calls["amount"] = amount
        # Simple object with the attributes the test cares about.
        return type("Result", (), {"ok": True, "transaction_id": "FAKE-123"})()

    monkeypatch.setattr(PaymentGateway, "charge", fake_charge)

    result = checkout(simple_order, configured_gateway)

    assert result.ok is True
    assert result.transaction_id == "FAKE-123"
    assert calls["amount"] == simple_order.total


def test_checkout_raises_payment_error_when_api_key_missing(simple_order, monkeypatch):
    """Missing API key -> our code should raise a custom PaymentError.

    This shows how to combine fixtures, environment manipulation, and
    ``pytest.raises`` to test error paths.
    """

    monkeypatch.delenv("PAYMENT_API_KEY", raising=False)
    gateway = PaymentGateway()  # will now see no API key at all

    with pytest.raises(PaymentError, match="missing API key"):
        checkout(simple_order, gateway)


def test_checkout_rejects_free_orders(monkeypatch):
    """Orders with a non-positive total are rejected with ValueError."""

    free_order = Order(items=[OrderItem(name="freebie", price=0.0, quantity=1)])
    gateway = PaymentGateway(api_key="test-key")

    with pytest.raises(ValueError, match="free or empty"):
        checkout(free_order, gateway)


@pytest.mark.slow
@pytest.mark.api
def test_checkout_works_for_variable_size_orders(variable_size_order, configured_gateway, monkeypatch):
    """Use a parametrized fixture to run the same test for many order shapes.

    The ``variable_size_order`` fixture in ``mini_project/conftest.py`` yields
    three different orders. Because this test uses that fixture, it runs once
    for each of them, but the test body stays clean.
    """

    charged_amounts: list[float] = []

    def fake_charge(self, amount: float):  # type: ignore[override]
        charged_amounts.append(amount)
        return type("Result", (), {"ok": True, "transaction_id": "VARIED"})()

    monkeypatch.setattr(PaymentGateway, "charge", fake_charge)

    result = checkout(variable_size_order, configured_gateway)

    assert result.ok is True
    # Check that we charged exactly the order total for each parametrized case.
    assert charged_amounts[-1] == variable_size_order.total


output = """\
$ pytest -vs mini_project/test_mini_project_checkout.py
=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 6 items

mini_project/test_mini_project_checkout.py::test_checkout_success_with_patched_gateway PASSED
mini_project/test_mini_project_checkout.py::test_checkout_raises_payment_error_when_api_key_missing PASSED
mini_project/test_mini_project_checkout.py::test_checkout_rejects_free_orders PASSED
mini_project/test_mini_project_checkout.py::test_checkout_works_for_variable_size_orders[one-item] PASSED
mini_project/test_mini_project_checkout.py::test_checkout_works_for_variable_size_orders[two-items] PASSED
mini_project/test_mini_project_checkout.py::test_checkout_works_for_variable_size_orders[three-items] PASSED

==================================================== 6 passed in 0.01s ====================================================
"""

