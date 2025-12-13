"""Comparison of list parameter defaults for fn_list.

Demonstrates the difference between:

1. def fn_list_required(lt: list[int]) -> list[int]
2. def fn_list_mutable_default(lt: list[int] = []) -> list[int]
3. def fn_list_safe(lt: list[int] | None = None) -> list[int]

Run this file directly to see how mutable default arguments behave.
"""

from __future__ import annotations

from typing import Any


def fn_list_required(lt: list[int]) -> list[int]:
    """Version where the caller MUST pass a list.

    Safe: there is no default list, so no hidden shared state.
    """

    lt.append(100)
    return lt


def fn_list_mutable_default(lt: list[int] = []) -> list[int]:  # noqa: B006
    """WRONG: uses a mutable default list.

    The same list instance is reused across calls that don't pass ``lt``.
    This mirrors the classic mutable-default-argument pitfall.
    """

    lt.append(100)
    return lt


def fn_list_safe(lt: list[int] | None = None) -> list[int]:
    """CORRECT: uses ``None`` as default and creates a new list per call.

    This is the recommended pattern when you want an optional list parameter
    with a default empty list.
    """

    if lt is None:
        lt = []
    lt.append(100)
    return lt


def demo() -> None:
    print("REQUIRED VERSION (no default):")
    print("fn_list_required([1, 2, 3]) ->", fn_list_required([1, 2, 3]))

    print("\nMUTABLE DEFAULT VERSION (shared list):")
    print("First call fn_list_mutable_default() ->", fn_list_mutable_default())
    print("Second call fn_list_mutable_default() ->", fn_list_mutable_default())
    print("Third call fn_list_mutable_default() ->", fn_list_mutable_default())

    print("\nSAFE NONE VERSION (fresh list each call):")
    print("First call fn_list_safe() ->", fn_list_safe())
    print("Second call fn_list_safe() ->", fn_list_safe())
    print("Third call fn_list_safe() ->", fn_list_safe())


if __name__ == "__main__":
    demo()

