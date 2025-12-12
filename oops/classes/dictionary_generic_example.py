"""Example of a generic Dictionary[K, V] class.

Shows that K is the key type and V is the value type, chosen when you
instantiate the class.

Run from the repo root with:

    python3 oops/classes/dictionary_generic_example.py
"""

from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Dictionary(Generic[K, V]):
    """A tiny generic dictionary mapping keys of type K to values of type V."""

    def __init__(self) -> None:
        self.data: dict[K, V] = {}

    def add(self, key: K, value: V) -> None:
        print(f"Adding {key!r} -> {value!r}")
        self.data[key] = value

    def get(self, key: K) -> V:
        print(f"Getting value for {key!r}")
        return self.data[key]


def demo_str_int() -> None:
    print("\n--- Dictionary[str, int] demo ---")
    d: Dictionary[str, int] = Dictionary()
    d.add("age", 25)
    d.add("height", 180)
    value = d.get("age")
    print("age =", value)
    # d.add("age", "hello")  # type checker error: value must be int


def demo_int_str() -> None:
    print("\n--- Dictionary[int, str] demo ---")
    d: Dictionary[int, str] = Dictionary()
    d.add(1, "apple")
    d.add(2, "banana")
    value = d.get(2)
    print("key 2 =", value)
    # d.add("one", "apple")  # type checker error: key must be int


def demo_str_list_int() -> None:
    print("\n--- Dictionary[str, list[int]] demo ---")
    d: Dictionary[str, list[int]] = Dictionary()
    d.add("scores", [10, 20, 30])
    value = d.get("scores")
    print("scores =", value)
    # d.add("scores", "not a list")  # type checker error: value must be list[int]


if __name__ == "__main__":
    demo_str_int()
    demo_int_str()
    demo_str_list_int()

