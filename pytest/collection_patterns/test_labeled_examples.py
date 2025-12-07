"""Tests that demonstrate label-based custom collection.

We reuse the existing ``component`` marker as our "label" source and
show how the options added in :mod:`collection_patterns.conftest` affect
which tests are selected.
"""

from __future__ import annotations

import pytest


@pytest.mark.component("rest")
@pytest.mark.intent("docs")
@pytest.mark.level("smoke")
def test_rest_smoke() -> None:
    assert True


@pytest.mark.component("cli")
@pytest.mark.intent("docs")
@pytest.mark.level("smoke")
def test_cli_smoke() -> None:
    assert True


@pytest.mark.component("rest")
@pytest.mark.intent("slow-suite")
@pytest.mark.slow
def test_rest_slow() -> None:
    assert True


@pytest.mark.component("misc")
def test_unlabeled_misc() -> None:
    """This test has a component that we will not select in examples."""

    assert True

