"""Simple CLI fixture example.

This file introduces a basic pytest fixture that provides a
:class:`~cli_replication.cli_app.FakeCli` instance for each test.

The goal is similar to ``test_rest_client_basic_fixture.py``: show how a
fixture can hide object construction and let tests focus on behaviour.
"""

from __future__ import annotations

import pytest

from .cli_app import FakeCli, FakeCluster


@pytest.fixture
def cli() -> FakeCli:
    """Provide a CLI bound to a single in-memory cluster.

    Each test that uses this fixture receives a *fresh* CLI instance
    pointing at a fresh :class:`FakeCluster`. Tests can modify it freely
    without affecting other tests.
    """

    cluster = FakeCluster(name="primary")
    return FakeCli(cluster)


@pytest.mark.component("cli")
@pytest.mark.owner("training-team")
def test_create_and_list_volumes(cli: FakeCli) -> None:
    """Creating volumes via the CLI is reflected in ``list_volumes``."""

    cli.create_volume("alpha")
    cli.create_volume("beta")

    assert cli.list_volumes() == ["alpha", "beta"]


@pytest.mark.component("cli")
@pytest.mark.intent("clusterload")
@pytest.mark.level("integration")
def test_each_test_gets_isolated_cli(cli: FakeCli) -> None:
    """This test sees a clean cluster despite previous tests creating data.

    When you run the whole file, both tests pass even though
    ``test_create_and_list_volumes`` created volumes. That is because the
    ``cli`` fixture constructs a fresh :class:`FakeCluster` on each
    invocation.
    """

    assert cli.list_volumes() == []

