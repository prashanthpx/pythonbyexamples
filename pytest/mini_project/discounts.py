from __future__ import annotations

"""Discount calculation helpers for the Phase 9 mini project.

This module is intentionally small but realistic enough to show how a second
piece of domain logic can grow around the existing order + payment code.
"""

from dataclasses import dataclass

from .orders import Order


@dataclass(frozen=True)
class DiscountRule:
    """Simple rule: if order total >= ``min_total``, apply ``percent_off``.

    ``percent_off`` is expressed as a percentage (e.g. 10.0 for 10%%).
    """

    name: str
    min_total: float
    percent_off: float


def calculate_discount(order: Order, rules: list[DiscountRule]) -> float:
    """Return the discount amount for an order under a set of rules.

    The highest matching ``percent_off`` wins. The result is rounded to 2
    decimal places to look like a currency value.
    """

    total = order.total
    applicable_percents = [r.percent_off for r in rules if total >= r.min_total]
    if not applicable_percents:
        return 0.0

    best_percent = max(applicable_percents)
    return round(total * best_percent / 100.0, 2)


def total_after_discounts(order: Order, rules: list[DiscountRule]) -> float:
    """Return the order total *after* subtracting any discount.

    This does **not** mutate the order; it just computes a derived total.
    """

    return round(order.total - calculate_discount(order, rules), 2)

