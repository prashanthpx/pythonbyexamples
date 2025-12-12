"""Example showing that @override is only checked by type checkers.

Run from the repo root with:

    python3 oops/classes/override_typo_example.py

At runtime, Python does *not* enforce @override. A static type checker like
mypy or pyright would catch the typo in ``languag`` below.
"""

from __future__ import annotations

try:  # Python 3.12+
    from typing import override  # type: ignore[attr-defined]
except ImportError:  # Older Python versions: provide a no-op fallback
    def override(func):  # type: ignore[misc]
        return func


class User:
    def language(self, name: str) -> None:
        print("[User.language] setting lang to", name)
        self.lang = name

    def printlanguage(self) -> None:
        print("Current lang:", self.lang)


class Person(User):
    @override
    def languag(self, name: str) -> None:  # NOTE: typo, does *not* override
        print("[Person.languag] setting lang to", "Mr " + name)
        self.lang = "Mr " + name


if __name__ == "__main__":
    p = Person()

    # This calls User.language, not Person.languag, because the method name
    # does not match. The @override decorator is ignored at runtime.
    p.language("pk")
    p.printlanguage()

    print("Has attribute 'languag' on Person?", hasattr(p, "languag"))

