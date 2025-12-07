"""Examples that show how pytest.ini markers and a simple plugin work together.

These tests are intentionally trivial from a *business logic* point of view.
The focus is on:

* Using rich markers declared in pytest/pytest.ini (component, owner, intent,
  require_feature_flags, level).
* Letting the example plugin (pytest_example_plugin) print structured
  metadata based on the owner/component markers for each test.

Run just these tests with::

    pytest pytest/conftest_patterns/test_global_config_effects.py -vv

and watch the extra ``[meta]`` lines the plugin prints before each test.
"""

from __future__ import annotations

import pytest


@pytest.mark.owner("storage-team")
@pytest.mark.component("rest")
@pytest.mark.level("integration")
def test_rest_component_example() -> None:
    """A fake REST-style integration test.

    In a real suite this would exercise a REST API client, but here we only
    care that the test is richly annotated so tools and humans can quickly
    see what it belongs to.
    """

    assert 1 + 1 == 2


@pytest.mark.slow
@pytest.mark.owner("infra-team")
@pytest.mark.intent("clusterload")
@pytest.mark.level("system")
def test_slow_cluster_intent() -> None:
    """A pretend long-running test tagged as "slow" and "clusterload".

    The important part is *how* it is labelled. In large suites, selectors
    like ``-m 'slow and clusterload'`` are used to carve out focused runs.
    """

    assert "cluster".startswith("clu")


@pytest.mark.require_feature_flags("new-ui", "beta-mode")
@pytest.mark.owner("ui-team")
@pytest.mark.component("ui")
def test_requires_feature_flags() -> None:
    """Example of a test that documents required feature flags.

    In your real system you would pair this with logic in fixtures or plugins
    that enables or skips tests based on which flags are active. Here we only
    demonstrate the *shape* of such a marker so the pattern is easy to copy.
    """

    assert sorted({"new-ui", "beta-mode"}) == ["beta-mode", "new-ui"]

