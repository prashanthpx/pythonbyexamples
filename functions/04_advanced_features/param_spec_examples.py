"""Examples demonstrating Callable with ParamSpec and TypeVar.

This file is a companion to the Callable / ParamSpec documentation in
functions/functions.md. It shows:

1. call_twice(f, *args, **kwargs) -> tuple[R, R]
   - Generic helper using Callable[P, R], ParamSpec P and TypeVar R.
2. wait_until(condition, timeout_sec, *args, **kwargs)
   - More realistic timeout-based helper that keeps checking a condition.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar

try:  # Python 3.10+
    from typing import ParamSpec  # type: ignore[attr-defined]
except ImportError:  # Python < 3.10 fallback to keep example runnable
    from typing import TypeVar as ParamSpec  # type: ignore[misc]
import time


# ---------------------------------------------------------------------------
# 1. call_twice: call any function twice with the same arguments
# ---------------------------------------------------------------------------

P = ParamSpec("P")
R = TypeVar("R")


def call_twice(
    f: Callable[P, R],
    *args: P.args,
    **kwargs: P.kwargs,
) -> tuple[R, R]:
    """Call ``f`` twice with the same arguments and return both results.

    In type-hint form:
    - ``Callable[P, R]``: a function that takes parameters ``P`` and returns ``R``
    - ``*args: P.args, **kwargs: P.kwargs``: forward whatever arguments
      ``f`` expects
    - return type ``tuple[R, R]``: two results of the same type
    """

    first = f(*args, **kwargs)
    second = f(*args, **kwargs)
    return first, second


def greet(name: str, punctuation: str = "!") -> str:
    """Simple greeting function to use with call_twice."""

    return f"Hello, {name}{punctuation}"


# ---------------------------------------------------------------------------
# 2. wait_until: check a condition until timeout
# ---------------------------------------------------------------------------

P2 = ParamSpec("P2")


def wait_until(
    condition: Callable[P2, bool],
    timeout_sec: float,
    *args: P2.args,
    **kwargs: P2.kwargs,
) -> None:
    """Wait until ``condition(*args, **kwargs)`` becomes True or timeout.

    - ``Callable[P2, bool]``: condition function that returns ``bool``
    - ``timeout_sec``: maximum time to wait in seconds
    - ``*args`` / ``**kwargs``: forwarded to ``condition`` on each check
    """

    print(f"Waiting up to {timeout_sec} seconds...")
    end = time.time() + timeout_sec
    while time.time() < end:
        if condition(*args, **kwargs):
            print("Condition became True")
            return
        print("Condition still False, sleeping...")
        time.sleep(1)
    raise TimeoutError("Condition did not become True in time")


def is_even_after_increment(n: int, increments: int) -> bool:
    """Example condition: (n + increments) must be even."""

    return (n + increments) % 2 == 0


# ---------------------------------------------------------------------------
# 3. Class-based wrapper: wait_until_running vs _wait_until
# ---------------------------------------------------------------------------

P3 = ParamSpec("P3")


class Service:
    """Demonstrate a thin wrapper using Any and a core helper using ParamSpec.

    This mirrors the pattern discussed in the documentation:

    - ``wait_until_running`` is a public wrapper that accepts ``Any``.
    - ``_wait_until`` is the strongly typed core helper using ``Callable[P3, bool]``.
    """

    def __init__(self) -> None:
        self._checks = 0

    def is_running(self, target: str, min_checks: int = 1) -> bool:
        """Pretend to check whether *target* is running."""

        self._checks += 1
        print(
            f"  [is_running] check {self._checks} for {target!r}, "
            f"min_checks={min_checks}",
        )
        return self._checks >= min_checks

    def _wait_until(
        self,
        condition: Callable[P3, bool],
        action: str,
        timeout_sec: float | None = None,
        *args: P3.args,
        **kwargs: P3.kwargs,
    ) -> None:
        """Core helper: strongly typed using Callable[P3, bool]."""

        if timeout_sec is None:
            timeout_sec = 5.0
        print(f"Waiting to {action!r} for up to {timeout_sec} seconds...")
        end = time.time() + timeout_sec
        while time.time() < end:
            if condition(*args, **kwargs):
                print(f"Action {action!r} succeeded")
                return
            print("Still not ready, sleeping...")
            time.sleep(1.0)
        raise TimeoutError(f"{action!r} did not complete in time")

    def wait_until_running(
        self,
        *args: Any,
        timeout_sec: float | None = None,
        **kwargs: Any,
    ) -> None:
        """Thin wrapper: forwards args/kwargs to _wait_until(self.is_running, ...)."""

        return self._wait_until(
            self.is_running,
            "start",
            timeout_sec,
            *args,
            **kwargs,
        )


if __name__ == "__main__":
    # Demo 1: call_twice with greet
    print("call_twice(greet, 'Prashanth', punctuation='!'):")
    result1, result2 = call_twice(greet, "Prashanth", punctuation="!")
    print("  ", result1)
    print("  ", result2)

    # Demo 2: wait_until with is_even_after_increment
    # Note: may take a few seconds due to sleep(1) loop.
    print("\nwait_until(is_even_after_increment, 5, 3, increments=1):")
    try:
        wait_until(is_even_after_increment, 5, 3, increments=1)
    except TimeoutError as exc:
        print("TimeoutError:", exc)

    # Demo 3: class-based wait_until_running wrapper
    print("\nService().wait_until_running('demo', timeout_sec=3, min_checks=2):")
    service = Service()
    try:
        service.wait_until_running("demo", timeout_sec=3.0, min_checks=2)
    except TimeoutError as exc:
        print("TimeoutError:", exc)

