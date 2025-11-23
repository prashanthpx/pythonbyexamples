import pytest

from .orders import Order, OrderItem
from .payments import PaymentGateway


@pytest.fixture
def simple_order() -> Order:
    """Order with a small, predictable total used in many tests."""

    return Order(items=[OrderItem(name="book", price=10.0, quantity=2)])


@pytest.fixture
def configured_gateway(monkeypatch: pytest.MonkeyPatch) -> PaymentGateway:
    """PaymentGateway instance with a fake API key configured.

    Using monkeypatch here means tests do not depend on any real environment
    variables. Each test that uses this fixture gets a clean configuration.
    """

    monkeypatch.setenv("PAYMENT_API_KEY", "test-key-123")
    return PaymentGateway()


@pytest.fixture(params=[1, 2, 3], ids=["one-item", "two-items", "three-items"])
def variable_size_order(request) -> Order:
    """Parameterized fixture that yields orders of different sizes.

    This lets tests exercise the same behaviour (e.g. checkout) with multiple
    shapes of data without writing separate test functions.
    """

    quantity = request.param
    item = OrderItem(name="widget", price=5.0, quantity=quantity)
    return Order(items=[item])

