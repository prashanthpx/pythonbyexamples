from dataclasses import dataclass
from typing import List


@dataclass
class OrderItem:
    """A single line item in an order."""

    name: str
    price: float
    quantity: int = 1


@dataclass
class Order:
    """A very small order model used in the Phase 9 mini project."""

    items: List[OrderItem]

    @property
    def total(self) -> float:
        """Compute the total value of the order."""

        return sum(item.price * item.quantity for item in self.items)

