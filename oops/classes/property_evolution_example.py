"""Before/after style example: evolve a public attribute into a property.

Run from the repo root with:

    python3 oops/classes/property_evolution_example.py
"""


class UserV1:
    """Initial version: plain public attribute.

    In real projects you might start with something this simple.
    """

    def __init__(self, age: int) -> None:
        self.age = age  # direct public attribute


class UserV2:
    """Evolved version: "age" becomes a property with validation.

    Callers still write ``user.age`` and ``user.age = value``.
    """

    def __init__(self, age: int) -> None:
        self._age = 0
        # This goes through the property setter below:
        self.age = age

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value


if __name__ == "__main__":
    u1 = UserV1(30)
    print("[UserV1] age =", u1.age)

    u2 = UserV2(30)
    print("[UserV2] age =", u2.age)

    # Existing code keeps using attribute-style access:
    u2.age = 40
    print("[UserV2] updated age =", u2.age)

    try:
        u2.age = -5
    except ValueError as e:
        print("[UserV2] validation error:", e)

