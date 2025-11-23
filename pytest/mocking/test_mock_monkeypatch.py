import os
import random

import pytest


# Phase 8 – Mocking: built-in monkeypatch fixture


def roll_two_dice() -> int:
    """Use random.randint to simulate rolling two dice.

    This function is intentionally non-deterministic so we can see
    how monkeypatch makes tests predictable.
    """
    return random.randint(1, 6) + random.randint(1, 6)


def get_db_url() -> str:
    """Read a DB URL from the environment with a safe default."""
    return os.getenv("DB_URL", "sqlite:///:memory:")


def test_roll_two_dice_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch random.randint so the test is fully deterministic.

    We replace random.randint with a fake that always returns 3,
    so rolling two dice always gives 6.
    """

    calls: list[tuple[int, int]] = []

    def fake_randint(a: int, b: int) -> int:
        calls.append((a, b))
        return 3

    monkeypatch.setattr("random.randint", fake_randint)

    total = roll_two_dice()

    assert total == 6
    assert calls == [(1, 6), (1, 6)]


def test_get_db_url_with_setenv(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use monkeypatch.setenv to control environment variables."""

    monkeypatch.setenv("DB_URL", "postgresql://user@localhost/db")

    assert get_db_url() == "postgresql://user@localhost/db"




output = """\n$ pytest -vs test_mock_monkeypatch.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ... collected 2 items\n\ntest_mock_monkeypatch.py::test_roll_two_dice_with_monkeypatch PASSED\ntest_mock_monkeypatch.py::test_get_db_url_with_setenv PASSED\n\n==================================================== 2 passed in 0.01s =====================================================\n"""