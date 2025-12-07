"""Replication and compatibility-layer fixtures.

This module builds on :mod:`test_cli_basic_fixture` and shows how to:

* model a tiny *replication testbed* with two clusters and a link, and
* add a **compatibility fixture** that adapts the testbed for legacy
  tests that expect different attribute names.

The patterns are inspired by the real ``cli`` fixtures in the
``clusterload`` suite, but kept intentionally small and readable.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from .cli_app import FakeCli, FakeCluster, ReplicationLink, ReplicationTestbed


@pytest.fixture
def clusters() -> tuple[FakeCluster, FakeCluster]:
    """Provide a pair of clusters used in replication tests."""

    primary = FakeCluster(name="primary")
    secondary = FakeCluster(name="secondary")
    return primary, secondary


@pytest.fixture
def replication_testbed(clusters: tuple[FakeCluster, FakeCluster]) -> ReplicationTestbed:
    """Yield a :class:`ReplicationTestbed` with setup/teardown logging.

    Using ``yield`` in a fixture lets you express both *setup* and
    *teardown* in one place. Run this file with ``-s`` to see the
    printed messages in order.
    """

    primary, secondary = clusters
    testbed = ReplicationTestbed(
        primary=primary,
        secondary=secondary,
        primary_cli=FakeCli(primary),
        secondary_cli=FakeCli(secondary),
        link=ReplicationLink(source=primary, target=secondary),
    )

    print(f"[setup] created replication testbed {primary.name}->{secondary.name}")
    yield testbed
    print("[teardown] clearing replication state")

    primary.volumes.clear()
    secondary.volumes.clear()
    testbed.link.replicated.clear()


@dataclass
class LegacyReplicationView:
    """Compatibility wrapper exposing legacy attribute names.

    Imagine that older tests expect attributes called ``src_cli`` and
    ``dst_cli`` instead of the newer ``primary_cli`` / ``secondary_cli``.
    Rather than changing all those tests at once, you can add a small
    compatibility layer that presents the same underlying testbed with a
    different surface.
    """

    src_cli: FakeCli
    dst_cli: FakeCli
    testbed: ReplicationTestbed


@pytest.fixture
def legacy_replication_testbed(replication_testbed: ReplicationTestbed) -> LegacyReplicationView:
    """Adapt :class:`ReplicationTestbed` for legacy tests.

    This fixture wraps the modern testbed in a :class:`LegacyReplicationView`
    so that older tests can keep using ``src_cli`` / ``dst_cli`` while new
    tests adopt the clearer attribute names.
    """

    print("[compat] adapting ReplicationTestbed to LegacyReplicationView")
    return LegacyReplicationView(
        src_cli=replication_testbed.primary_cli,
        dst_cli=replication_testbed.secondary_cli,
        testbed=replication_testbed,
    )


@pytest.mark.component("cli")
@pytest.mark.level("integration")
def test_replication_flow_uses_yield_fixture(
    replication_testbed: ReplicationTestbed,
) -> None:
    """Replicating a volume affects both clusters and the link object."""

    replication_testbed.primary_cli.create_volume("data-vol")
    replication_testbed.replicate("data-vol")

    assert replication_testbed.primary_cli.list_volumes() == ["data-vol"]
    assert replication_testbed.secondary_cli.list_volumes() == ["data-vol"]
    assert replication_testbed.is_replicated("data-vol") is True


@pytest.mark.component("cli")
@pytest.mark.intent("clusterload")
@pytest.mark.level("system")
def test_legacy_view_uses_compat_fixture(
    legacy_replication_testbed: LegacyReplicationView,
) -> None:
    """Legacy-style tests can keep using ``src_cli`` / ``dst_cli``.

    Both this test and :func:`test_replication_flow_uses_yield_fixture`
    share the same underlying :class:`ReplicationTestbed` fixture. The
    compatibility layer allows different calling conventions without
    duplicating setup logic.
    """

    legacy_replication_testbed.src_cli.create_volume("legacy-vol")
    legacy_replication_testbed.testbed.replicate("legacy-vol")

    assert legacy_replication_testbed.dst_cli.list_volumes() == ["legacy-vol"]

