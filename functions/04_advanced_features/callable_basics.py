"""Basic examples for typing.Callable and ParamSpec.

This module is a beginner-friendly companion to the type hints examples.

It shows:
- Passing a function as a parameter using Callable[[ArgTypes], ReturnType]
- A Go-style mental model for function types
- A slightly more advanced example using ParamSpec to forward *args/**kwargs
"""

from __future__ import annotations

from typing import Callable

try:  # Python 3.10+
    from typing import ParamSpec  # type: ignore[attr-defined]
except ImportError:  # Python < 3.10 fallback so the example still runs
    from typing import TypeVar  # type: ignore

    ParamSpec = TypeVar  # type: ignore[assignment,misc]


# ============================================================================
# 1. Callable[[int], int]  pass a function into another function
# ============================================================================


def apply(f: Callable[[int], int], x: int) -> int:
    """Apply the function ``f`` to ``x`` and return the result.

    In Go you might write: ``func apply(f func(int) int, x int) int``.
    Here we express the *same idea* in Python's type hints.
    """

    return f(x)


def double(n: int) -> int:
    """Return 2 * n.

    Matches the idea of a ``func(int) int`` callback from Go.
    """

    return n * 2


def triple(n: int) -> int:
    """Return 3 * n."""

    return n * 3


# ============================================================================
# 2. Callable[P, bool] with ParamSpec  forwarding *args and **kwargs
# ============================================================================

P = ParamSpec("P")


def wait_until_true(
    condition: Callable[P, bool],
    *args: P.args,
    **kwargs: P.kwargs,
) -> bool:
    """Call ``condition(*args, **kwargs)`` and return its bool result.

    ``Callable[P, bool]`` means: "a function that takes parameters ``P`` and
    returns ``bool``". ``ParamSpec`` lets us forward whatever arguments the
    condition expects while keeping type checking.
    """

    print("Checking condition with:", args, kwargs)
    result = condition(*args, **kwargs)
    print("Condition is", result)
    return result


def is_positive(x: int) -> bool:
    """Return True if x is greater than zero."""

    return x > 0


def has_min_length(text: str, length: int) -> bool:
    """Return True if ``text`` has at least ``length`` characters."""

    return len(text) >= length


if __name__ == "__main__":
    # Demonstrate simple Callable[[int], int]
    print("apply(double, 5)  =", apply(double, 5))
    print("apply(triple, 4)  =", apply(triple, 4))

    # Demonstrate Callable[P, bool] with ParamSpec and *args/**kwargs
    print("\nwait_until_true with is_positive:")
    wait_until_true(is_positive, 10)
    wait_until_true(is_positive, -5)

    print("\nwait_until_true with has_min_length:")
    wait_until_true(has_min_length, "hello", length=3)
    wait_until_true(has_min_length, "hi", length=3)

