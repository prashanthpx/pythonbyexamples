"""Examples showing:

1. Naming TypeVars (HandleT vs PHandle etc.).
2. Difference between using Any vs TypeVar in a service and in a Box.

Run from the repo root with:

    python3 oops/classes/typevar_vs_any_example.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


# ---------------------------------------------------------------------------
# 1. Naming TypeVars
# ---------------------------------------------------------------------------

HandleT = TypeVar("HandleT")  # common convention: "handle type"
PHandle = TypeVar("PHandle")  # also valid, just a different name
ItemT = TypeVar("ItemT")      # typical container type parameter


# ---------------------------------------------------------------------------
# 2. AnyService vs generic Service[HandleT]
# ---------------------------------------------------------------------------


class AnyService(ABC):
    """Service using Any everywhere: type checker cannot help you."""

    @abstractmethod
    def start(self) -> Any:
        ...

    @abstractmethod
    def stop(self, handle: Any) -> None:
        ...


class AnyFileService(AnyService):
    def start(self) -> Any:
        print("[AnyFileService] Opening file…")
        return "/tmp/app.log"  # could also return something else, type checker won't mind

    def stop(self, handle: Any) -> None:
        print(f"[AnyFileService] Closing file handle={handle!r}")


class Service(ABC, Generic[HandleT]):
    """Generic service: start/stop are tied to the same handle type."""

    @abstractmethod
    def start(self) -> HandleT:
        ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        ...


class FileService(Service[str]):
    def start(self) -> str:
        print("[FileService] Opening file…")
        return "/tmp/app.log"

    def stop(self, handle: str) -> None:
        print(f"[FileService] Closing file {handle}")


# ---------------------------------------------------------------------------
# 3. Box[Any] vs Box[ItemT]
# ---------------------------------------------------------------------------


class AnyBox:
    """Box using Any: can store anything, no type safety."""

    def __init__(self) -> None:
        self._item: Any | None = None

    def put(self, item: Any) -> None:
        print(f"[AnyBox] putting {item!r}")
        self._item = item

    def get(self) -> Any | None:
        print(f"[AnyBox] getting {self._item!r}")
        return self._item


class Box(Generic[ItemT]):
    """Generic box: logically holds exactly one ItemT value."""

    def __init__(self) -> None:
        self._item: ItemT | None = None

    def put(self, item: ItemT) -> None:
        print(f"[Box[{ItemT.__name__}]] putting {item!r}")
        self._item = item

    def get(self) -> ItemT | None:
        print(f"[Box[{ItemT.__name__}]] getting {self._item!r}")
        return self._item


if __name__ == "__main__":
    print("\n--- AnyService demo ---")
    any_service = AnyFileService()
    h_any = any_service.start()
    any_service.stop(h_any)
    any_service.stop(12345)  # type checker would not complain, but this is probably a bug

    print("\n--- Generic Service[HandleT] demo ---")
    file_service = FileService()
    h_str = file_service.start()
    file_service.stop(h_str)
    file_service.stop("/tmp/other.log")
    # file_service.stop(12345)  # type checker (mypy/pyright) would flag this

    print("\n--- AnyBox demo ---")
    any_box = AnyBox()
    any_box.put(10)
    any_box.put("hello")
    any_box.put([1, 2, 3])
    any_box.get()

    print("\n--- Box[ItemT] demo (conceptual type safety) ---")
    int_box: Box[int] = Box()
    int_box.put(42)
    int_box.get()
    # int_box.put("oops")  # type checker would flag this as an error

