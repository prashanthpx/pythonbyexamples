from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    """A simple task in an automation system."""

    id: int
    description: str


class TaskHandler:
    """Base class for handling tasks.

    Subclasses override `handle()` to do something specific. Code that calls
    `handle()` can work with `TaskHandler` without caring which subclass it is.
    This is classic runtime polymorphism.
    """

    def handle(self, task: Task) -> None:  # pragma: no cover - interface only
        raise NotImplementedError


class EmailTaskHandler(TaskHandler):
    """Send task notifications by email.

    The concrete implementation detail (email address) is encapsulated inside
    this class via the `_email` attribute.
    """

    def __init__(self, email: str) -> None:
        self._email = email  # leading underscore: internal detail

    def handle(self, task: Task) -> None:
        print(f"[EMAIL] Sending '{task.description}' to {self._email}")


class SlackTaskHandler(TaskHandler):
    """Send task notifications to a Slack channel (simulated)."""

    def __init__(self, channel: str) -> None:
        self._channel = channel

    def handle(self, task: Task) -> None:
        print(f"[SLACK] Posting '{task.description}' to channel {self._channel}")


def process_task_with_all_handlers(handlers: List[TaskHandler], task: Task) -> None:
    """Call `handle()` on each handler.

    Thanks to inheritance + polymorphism, this function doesn't need to know
    *which* concrete handler it is calling; it just calls `handle()`.
    """

    for handler in handlers:
        handler.handle(task)


if __name__ == "__main__":  # pragma: no cover - manual run example
    task = Task(id=1, description="Deploy new version")

    handlers: List[TaskHandler] = [
        EmailTaskHandler("dev-team@example.com"),
        SlackTaskHandler("#deployments"),
    ]

    process_task_with_all_handlers(handlers, task)


# Captured output from running: python3 inheritance_polymorphism_example.py
output = """[EMAIL] Sending 'Deploy new version' to dev-team@example.com
[SLACK] Posting 'Deploy new version' to channel #deployments
"""

