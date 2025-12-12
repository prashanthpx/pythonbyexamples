"""Example of combining ABC with Generic[HandleT] for service-style classes.

Run from the repo root with:

    python3 oops/classes/service_generic_example.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


HandleT = TypeVar("HandleT")


class Service(ABC, Generic[HandleT]):
    """Abstract generic service managing some kind of handle.

    - ``HandleT`` represents the *handle type* (file path, connection object,
      instance ID, ...).
    - Subclasses choose the concrete type when they inherit from ``Service``.
    """

    @abstractmethod
    def start(self) -> HandleT:
        """Start the service and return a handle."""

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        """Stop the service using the given handle."""

    def restart(self) -> HandleT:
        """Concrete method built on top of the abstract ones.

        In a real system this might do a graceful restart.
        """

        print("Restarting service…")
        handle = self.start()
        self.stop(handle)
        return self.start()


# ---------------------------------------------------------------------------
# File-based service: HandleT = str
# ---------------------------------------------------------------------------


class FileService(Service[str]):
    """Service whose handle is a ``str`` (e.g. file path).

    In a real project you would return an actual file object or descriptor.
    """

    def start(self) -> str:
        print("Opening file…")
        handle = "/tmp/app.log"  # pretend we opened a file
        return handle

    def stop(self, handle: str) -> None:
        print(f"Closing file {handle}")


# ---------------------------------------------------------------------------
# Database-based service: HandleT = DBConnection
# ---------------------------------------------------------------------------


class DBConnection:
    """Very small stand-in for a real database connection object."""

    def __init__(self, host: str) -> None:
        self.host = host


class DatabaseService(Service[DBConnection]):
    """Service whose handle is a ``DBConnection`` object."""

    def start(self) -> DBConnection:
        print("Connecting to DB…")
        return DBConnection("localhost")

    def stop(self, handle: DBConnection) -> None:
        print(f"Closing DB connection to {handle.host}")


if __name__ == "__main__":
    # FileService demo
    print("\n--- FileService demo ---")
    file_service = FileService()
    file_handle = file_service.start()
    file_service.stop(file_handle)

    # DatabaseService demo
    print("\n--- DatabaseService demo ---")
    db_service = DatabaseService()
    db_handle = db_service.start()
    db_service.stop(db_handle)

    # Restart uses the generic logic from the base Service class
    print("\n--- DatabaseService restart() demo ---")
    db_service.restart()

