"""Meta-reporting pytest plugin for the training test suite.

This is the same plugin described in the pytest learning notes. It is
kept deliberately small, but it shows how large suites like
`clusterload` use plugins to enrich test output with metadata derived
from markers.

The plugin reads two custom markers defined in ``pytest/pytest.ini``:

* ``@pytest.mark.owner("..."``)
* ``@pytest.mark.component("..."``)

During ``pytest_runtest_setup`` it prints a short line summarizing this
metadata. It does **not** change test outcomes.
"""

from __future__ import annotations

from typing import List, Optional

import pytest


def _format_meta_line(item: pytest.Item) -> Optional[str]:
    """Return a short metadata line based on common markers.

    If neither marker is present, return ``None`` so the caller can do
    nothing.
    """

    owner_marker = item.get_closest_marker("owner")
    component_marker = item.get_closest_marker("component")

    owner = owner_marker.args[0] if owner_marker and owner_marker.args else None
    component = (
        component_marker.args[0] if component_marker and component_marker.args else None
    )

    parts: List[str] = []
    if owner:
        parts.append(f"owner={owner}")
    if component:
        parts.append(f"component={component}")

    if not parts:
        return None

    return f"[meta] {item.nodeid} ({', '.join(parts)})"


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Hook called before each test function is run.

    If the test is marked with ``@pytest.mark.owner`` or
    ``@pytest.mark.component``, emit a small, structured line into the
    terminal output. This mirrors the style of larger suites that add
    metadata about every test case.
    """

    line = _format_meta_line(item)
    if not line:
        return

    terminal_reporter = item.config.pluginmanager.get_plugin("terminalreporter")
    if terminal_reporter is None:
        # This can be the case in some programmatic invocations of pytest.
        return

    terminal_reporter.write_line(line)

