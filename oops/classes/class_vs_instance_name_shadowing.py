"""Demonstrate how instance attributes shadow class attributes with the same name.

Run with:

    python3 oops/classes/class_vs_instance_name_shadowing.py
"""

from __future__ import annotations


class User:
    # Class attribute: shared default
    name: str = "class-default"

    def __init__(self, name: str) -> None:
        print("Inside __init__!", name)
        # Instance attribute: unique per object, shadows the class attribute
        self.name = name


if __name__ == "__main__":
    u1 = User("Alice")
    u2 = User("Bob")

    print("u1.name =", u1.name)
    print("u2.name =", u2.name)
    print("User.name =", User.name)

    print("u1.__dict__ =", u1.__dict__)
    print("User.__dict__['name'] =", User.__dict__["name"])

