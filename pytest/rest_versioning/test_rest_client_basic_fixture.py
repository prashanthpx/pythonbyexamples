"""Simple REST client fixture example.

This file introduces the idea of using a pytest fixture to construct
and share a tiny REST client object across tests. It mirrors the
*shape* of real code (client object + tests) but keeps behaviour very
small so the focus stays on pytest concepts.
"""

from __future__ import annotations

import pytest

from .rest_client import RestClient


@pytest.fixture
def api_version() -> str:
    """Return the default API version used in the simplest examples.

    In real projects this might come from configuration or the command
    line. Here we hard-code ``"v1"`` so you can see the basic fixture
    pattern without any parametrization yet.
    """

    return "v1"


@pytest.fixture
def rest_client(api_version: str) -> RestClient:
    """Create a :class:`RestClient` bound to a specific API version.

    Any test that accepts a ``rest_client`` parameter will receive this
    object. If we later change how the client is constructed, we only
    need to update this fixture in one place.
    """

    return RestClient(
        base_url="https://storage.example.test",
        api_version=api_version,
    )


@pytest.mark.component("rest")
@pytest.mark.owner("training-team")
def test_client_exposes_version_and_url(rest_client: RestClient) -> None:
    """The basic fixture gives tests a ready-to-use client instance.

    This test demonstrates that the object created by the fixture has
    the expected attributes.
    """

    assert rest_client.api_version == "v1"
    assert rest_client.base_url == "https://storage.example.test"


@pytest.mark.component("rest")
@pytest.mark.intent("clusterload")
@pytest.mark.level("integration")
def test_list_volumes_includes_version(rest_client: RestClient) -> None:
    """The ``list_volumes`` method includes the API version in its payload."""

    payload = rest_client.list_volumes()

    assert payload["api_version"] == "v1"
    assert payload["volumes"] == []

