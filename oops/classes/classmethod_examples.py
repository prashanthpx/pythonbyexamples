"""Examples showing when to use @classmethod instead of instance methods.

Run from the repository root with:

    python oops/classes/classmethod_examples.py

or from inside ``oops/classes`` with:

    python classmethod_examples.py
"""

from __future__ import annotations


class CounterInstanceStyle:
    """Uses an *instance* method, even though it only needs class data.

    This is legal Python but not great design: you must create an object even
    though the method never touches ``self``.
    """

    class_count: int = 0

    def print_class_count(self) -> None:
        # ``self`` is not used; we reach for the class directly.
        print(f"[instance] class_count = {CounterInstanceStyle.class_count}")


class CounterClassMethod:
    """Uses a proper ``@classmethod``.

    Here the method clearly belongs to the *class*, not to any single
    instance. No object needs to be created just to call it.
    """

    class_count: int = 0

    @classmethod
    def print_class_count(cls) -> None:
        print(f"[classmethod] {cls.__name__}.class_count = {cls.class_count}")


class SubCounter(CounterClassMethod):
    """Subclass that overrides the class attribute.

    Calling ``SubCounter.print_class_count()`` uses ``SubCounter.class_count``,
    because ``cls`` in the classmethod is the subclass.
    """

    class_count: int = 10


class UserWithAltConstructor:
    """Shows the most common real use of ``@classmethod``: alternate constructors."""

    def __init__(self, full_name: str) -> None:
        self.full_name = full_name

    @classmethod
    def from_first_last(cls, first: str, last: str) -> "UserWithAltConstructor":
        """Alternate constructor that builds the full name from parts."""

        return cls(f"{first} {last}")


if __name__ == "__main__":
    # Instance-style: you must create an object just to call the method.
    one = CounterInstanceStyle()
    one.print_class_count()

    # Classmethod: call directly on the class, no instance required.
    CounterClassMethod.print_class_count()

    # Inheritance: ``cls`` is ``SubCounter``, so we see the overridden value.
    SubCounter.print_class_count()

    # Alternate constructor using a classmethod.
    user = UserWithAltConstructor.from_first_last("Ada", "Lovelace")
    print(f"[alt ctor] full_name = {user.full_name}")


output = """\
$ python oops/classes/classmethod_examples.py
[instance] class_count = 0
[classmethod] CounterClassMethod.class_count = 0
[classmethod] SubCounter.class_count = 10
[alt ctor] full_name = Ada Lovelace
"""
