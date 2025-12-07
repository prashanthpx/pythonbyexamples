"""Parametrized REST client fixtures with versioned schemas.

This example builds on :mod:`test_rest_client_basic_fixture` and shows
how to:

* parametrize a fixture over multiple API versions, and
* dynamically import per-version schema modules based on that version.

It is loosely inspired by the ``rest1_client/conftest.py`` file in the
Purity ``clusterload`` test suite, but kept intentionally small.
"""

from __future__ import annotations

import importlib
from types import ModuleType

import pytest

from .rest_client import RestClient


@pytest.fixture(params=["v1", "v2"], ids=["rest-v1", "rest-v2"])
def api_version(request: pytest.FixtureRequest) -> str:
    """Parametrized API version shared by all fixtures in this module.

    Pytest will run each test in this file **twice**: once with
    ``api_version == "v1"`` and once with ``api_version == "v2"``.
    The ``ids`` argument controls how the cases appear in test output.
    """

    return str(request.param)


@pytest.fixture
def schema_module(api_version: str) -> ModuleType:
    """Dynamically import the schema module for the given API version.

    This mirrors the way large projects import ``v1`` / ``v2`` specific
    schema helpers. The important pytest idea is that fixtures can
    depend on *other* fixtures (here: ``api_version``) and use their
    values when doing setup work.

    We purposely use a **relative import** here (``.schemas_v1``,
    ``.schemas_v2``) so that this example behaves the same regardless of
    how your project is laid out on disk.
    """

    # ``__package__`` will be ``"rest_versioning"`` when this test
    # module is imported. Using a leading dot asks Python to look for the
    # schema modules inside the same package as this file.
    return importlib.import_module(f".schemas_{api_version}", package=__package__)


@pytest.fixture
def rest_client(api_version: str) -> RestClient:
    """Create a client for the current API version."""

    return RestClient(
        base_url="https://storage.example.test",
        api_version=api_version,
    )


@pytest.mark.component("rest")
@pytest.mark.level("integration")
def test_schema_required_fields_change_with_version(
    api_version: str, schema_module: ModuleType
) -> None:
    """The required fields differ slightly between ``v1`` and ``v2``.

    ``schemas_v1.REQUIRED_FIELDS`` and ``schemas_v2.REQUIRED_FIELDS`` are
    tiny on purpose so that it is easy to see how parametrization causes
    the same test to run twice with different expectations.
    """

    assert "name" in schema_module.REQUIRED_FIELDS
    assert "size_gb" in schema_module.REQUIRED_FIELDS

    if api_version == "v1":
        assert "compression" not in schema_module.REQUIRED_FIELDS
    else:
        assert "compression" in schema_module.REQUIRED_FIELDS


@pytest.mark.component("rest")
@pytest.mark.intent("clusterload")
@pytest.mark.level("integration")
def test_list_volumes_includes_api_version(
    api_version: str, rest_client: RestClient
) -> None:
    """The client uses ``api_version`` when building its payload.

    Because ``api_version`` is parametrized, this single test produces
    **two** test cases: one for ``v1`` and one for ``v2``. You will see
    both in the pytest output.
    """

    payload = rest_client.list_volumes()

    assert payload["api_version"] == api_version

