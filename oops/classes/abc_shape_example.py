"""Small example of abstract base classes and @abstractmethod.

Run from the repo root with:

    python3 oops/classes/abc_shape_example.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class: only meant as a blueprint.

    Subclasses must implement ``area()``.
    """

    @abstractmethod
    def area(self) -> float:
        """Return the area of this shape."""
        raise NotImplementedError


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius * self.radius


class BadShape(Shape):
    """Example of a subclass that *forgets* to implement area()."""

    # No area() implementation here on purpose.
    pass


if __name__ == "__main__":
    shapes: list[Shape] = [Square(2), Circle(3)]

    print("Areas from concrete subclasses:")
    for s in shapes:
        print(f"- {type(s).__name__}: {s.area()}")

    print("\nTrying to instantiate BadShape (should fail):")
    try:
        bad = BadShape()  # type: ignore[abstract]
        print("BadShape instance:", bad)
    except TypeError as e:
        print("Error:", e)

