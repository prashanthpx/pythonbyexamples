from __future__ import annotations

import os
from dataclasses import dataclass

from .orders import Order


class PaymentError(Exception):
    """Raised when the payment gateway reports a failure."""


@dataclass
class PaymentResult:
    """Tiny result object returned from the payment gateway."""

    ok: bool
    transaction_id: str | None = None


class PaymentGateway:
    """Very small fake payment gateway for the mini project.

    In real life this would talk to an external HTTP API. For the tests we
    patch or fake out the :meth:`charge` method to control behaviour.
    """

    def __init__(self, api_key: str | None = None) -> None:
        # Allow explicit api_key or read from environment to show monkeypatch.
        self.api_key = api_key or os.getenv("PAYMENT_API_KEY")

    def charge(self, amount: float) -> PaymentResult:
        """Charge the given amount.

        This implementation is intentionally tiny; the interesting part is how we
        *test* code that calls it.
        """

        if not self.api_key:
            raise PaymentError("missing API key")

        if amount <= 0:
            raise ValueError("amount must be positive")

        # Pretend we went out to an API and got back a transaction id.
        return PaymentResult(ok=True, transaction_id="TEST-TRANSACTION")


def checkout(order: Order, gateway: PaymentGateway) -> PaymentResult:
    """Perform a checkout for an order using the given gateway.

    This function is the main entry point the tests exercise.
    """

    total = order.total
    if total <= 0:
        raise ValueError("cannot checkout free or empty orders")

    return gateway.charge(total)

