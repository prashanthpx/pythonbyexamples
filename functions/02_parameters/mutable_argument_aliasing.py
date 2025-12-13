"""Examples: mutable list arguments and aliasing.

This module demonstrates two related ideas:

1. Passing a list into a function does NOT make a copy.
   The parameter becomes another reference (alias) to the same list.
2. Why using a mutable default value (like list = []) is dangerous.

Run this file directly to see the behavior.
"""

from __future__ import annotations

from typing import Optional


def fn_list(lt: list[int] = None) -> list[int]:
    """Modify the incoming list and print its contents.

    NOTE: In the original question, the signature was::

        def fn_list(lt: list = []):

    which uses a mutable default (``[]``). That pattern is dangerous because the
    same list instance would be shared across calls. Here we use ``None`` by
    default to avoid that pitfall and focus on the aliasing behavior.
    """

    if lt is None:
        lt = [1, 2, 3]

    lt[0] = 100
    lt[1] = 200
    lt[2] = 300

    print("Inside fn_list (lt):")
    for i in lt:
        print(f" i {i}")

    return lt


def fn_list_copy_inside(lt: list[int]) -> list[int]:
    """Create a copy inside the function so the caller's list is untouched."""

    copy_lt = lt.copy()  # or list(lt)
    copy_lt[0] = 100
    copy_lt[1] = 200
    copy_lt[2] = 300
    return copy_lt


def demo_aliasing() -> None:
    """Show that modifying lt also modifies the caller's list.

    This mirrors the question:

        l = [1, 2, 3]
        m = fn_list(l)

    Both ``l`` and the parameter ``lt`` point to the *same* list object, so
    modifications via ``lt`` are visible via ``l``.
    """

    l = [1, 2, 3]
    print(f"id(l) before: {id(l)}")

    m = fn_list(l)
    print(f"id(m) after:  {id(m)}")

    print("\nOutside fn_list (l):")
    for i in l:
        print(f" i {i}")

    print("\nSame object?", id(l) == id(m))

    # Show a version that does NOT modify the original list
    print("\n--- copy-inside version ---")
    l2 = [1, 2, 3]
    m2 = fn_list_copy_inside(l2)
    print("l2:", l2)
    print("m2:", m2)


if __name__ == "__main__":
    demo_aliasing()

