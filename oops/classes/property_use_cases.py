"""Small examples showing practical uses of @property.

Run from the repo root with:

    python3 oops/classes/property_use_cases.py
"""

from __future__ import annotations


class Rectangle:
    """Computed property: expose `area` like an attribute.

    We never store `area` on the instance; we compute it from width * height.
    """

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        print("[Rectangle] computing area")
        return self.width * self.height


class UserFullName:
    """Hide implementation while exposing attribute-style full_name."""

    def __init__(self, first: str, last: str) -> None:
        self.first = first
        self.last = last

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"


class Data:
    """Lazy / cached property for an expensive computation."""

    def __init__(self) -> None:
        self._expensive_result: int | None = None

    @property
    def expensive_result(self) -> int:
        if self._expensive_result is None:
            print("[Data] computing expensive_result...")
            # In real code this could be a DB query, API call, or heavy math.
            self._expensive_result = 42
        return self._expensive_result


class UserEmail:
    """Validation on assignment via a property setter."""

    def __init__(self, email: str) -> None:
        # This will go through the property setter.
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid email address")
        self._email = value


if __name__ == "__main__":
    rect = Rectangle(3, 4)
    print("area =", rect.area)
    print("area again =", rect.area)  # still computed, but cheap in this example

    user = UserFullName("Ada", "Lovelace")
    print("full_name =", user.full_name)

    data = Data()
    print("first access =", data.expensive_result)
    print("second access =", data.expensive_result)  # uses cached value

    user_email = UserEmail("test@example.com")
    print("email =", user_email.email)
    try:
        user_email.email = "not-an-email"
    except ValueError as e:
        print("validation failed:", e)

