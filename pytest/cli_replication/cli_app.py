"""Tiny fake CLI and replication domain used by pytest fixture examples.

The goal is to have just enough structure that fixtures and tests feel
"real" without bringing in any external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set


@dataclass
class FakeCluster:
    """Very small in-memory representation of a storage cluster."""

    name: str
    volumes: Set[str] = field(default_factory=set)


@dataclass
class ReplicationLink:
    """Tracks which volumes have been replicated between two clusters."""

    source: FakeCluster
    target: FakeCluster
    replicated: Set[str] = field(default_factory=set)


class FakeCli:
    """CLI-like façade that operates on a :class:`FakeCluster`.

    It exposes just enough behaviour for the tests to exercise:

    * creating volumes, and
    * listing existing volumes.
    """

    def __init__(self, cluster: FakeCluster) -> None:
        self.cluster = cluster

    def create_volume(self, name: str) -> None:
        """Create a new volume on this cluster."""

        self.cluster.volumes.add(name)

    def list_volumes(self) -> List[str]:
        """Return all volume names in sorted order."""

        return sorted(self.cluster.volumes)


@dataclass
class ReplicationTestbed:
    """Bundle together two clusters and a replication link.

    This object gives tests a single handle that exposes both the
    *environment* (primary/secondary clusters and their CLIs) and a
    tiny bit of replication logic.
    """

    primary: FakeCluster
    secondary: FakeCluster
    primary_cli: FakeCli
    secondary_cli: FakeCli
    link: ReplicationLink

    def replicate(self, volume: str) -> None:
        """Simulate replicating a volume from primary to secondary."""

        if volume not in self.primary.volumes:
            raise ValueError(f"volume {volume!r} does not exist on primary")

        self.secondary.volumes.add(volume)
        self.link.replicated.add(volume)

    def is_replicated(self, volume: str) -> bool:
        """Return ``True`` if the given volume was replicated."""

        return volume in self.link.replicated

