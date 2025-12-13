"""Example showing a *constrained* TypeVar for process handles.

We pretend to have two different "process handle" types and restrict
HandleT to be one of them.

Run from the repo root with:

    python3 oops/classes/process_service_constrained_typevar_example.py
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class PopenHandle:
    """Very small stand-in for something like subprocess.Popen[Any]."""

    def __init__(self, cmd: str) -> None:
        self.cmd = cmd

    def terminate(self) -> None:
        print(f"[PopenHandle] terminate {self.cmd!r}")

    def __repr__(self) -> str:  # pragma: no cover - tiny convenience
        return f"PopenHandle(cmd={self.cmd!r})"


class PsutilProcessLike:
    """Very small stand-in for something like psutil.Process."""

    def __init__(self, pid: int) -> None:
        self.pid = pid

    def kill(self) -> None:
        print(f"[PsutilProcessLike] kill pid={self.pid}")

    def __repr__(self) -> str:  # pragma: no cover - tiny convenience
        return f"PsutilProcessLike(pid={self.pid})"


HandleT = TypeVar("HandleT", PopenHandle, PsutilProcessLike)


class ProcessService(ABC, Generic[HandleT]):
    """Generic process service.

    The handle type HandleT is constrained to either PopenHandle or
    PsutilProcessLike. Nothing else is allowed.
    """

    @abstractmethod
    def start(self) -> HandleT:
        ...

    @abstractmethod
    def stop(self, handle: HandleT) -> None:
        ...


class PopenService(ProcessService[PopenHandle]):
    def start(self) -> PopenHandle:
        handle = PopenHandle("sleep 1")
        print("Starting:", handle)
        return handle

    def stop(self, handle: PopenHandle) -> None:
        print("Stopping:", handle)
        handle.terminate()


class PsutilService(ProcessService[PsutilProcessLike]):
    def start(self) -> PsutilProcessLike:
        handle = PsutilProcessLike(1234)
        print("Starting:", handle)
        return handle

    def stop(self, handle: PsutilProcessLike) -> None:
        print("Stopping:", handle)
        handle.kill()


# This would be a type checker error: str is not in {PopenHandle, PsutilProcessLike}.
# class StringService(ProcessService[str]):
#     ...


def demo() -> None:
    print("--- PopenService demo ---")
    popen_service = PopenService()
    h1 = popen_service.start()
    popen_service.stop(h1)

    print("\n--- PsutilService demo ---")
    ps_service = PsutilService()
    h2 = ps_service.start()
    ps_service.stop(h2)


if __name__ == "__main__":
    demo()

