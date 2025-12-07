"""Custom collection hooks demonstrating simple "labels".

This module adds command-line options used only for tests in this
folder:

* ``--label NAME`` (can be given multiple times) to only run tests whose
  ``component(NAME)`` marker matches one of the provided names.
* ``--list-labels`` to list which component labels exist for these tests
  and exit without running them.
* ``--skip-label NAME`` to **skip** tests with a matching ``component``
  label at runtime.
* ``--xfail-label NAME`` to **xfail** (expected-fail) tests with a
  matching ``component`` label at runtime.

This is a small, concrete version of the more sophisticated collection
and label handling used in the real `clusterload` suite.
"""

from __future__ import annotations

from typing import Iterable, List, Optional

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register collection-related command-line options.

    These options are scoped to the ``collection_patterns`` examples but
    work like any other pytest CLI flag.
    """

    group = parser.getgroup("collection-patterns")
    group.addoption(
        "--label",
        action="append",
        dest="_collection_labels",
        default=[],
        metavar="NAME",
        help=(
            "Only run tests in pytest/collection_patterns whose component "
            "marker matches one of the given labels."
        ),
    )
    group.addoption(
        "--list-labels",
        action="store_true",
        dest="_collection_list_labels",
        help=(
            "List component labels used by tests in pytest/collection_patterns "
            "and exit without running them."
        ),
    )
    group.addoption(
        "--skip-label",
        action="append",
        dest="_collection_skip_labels",
        default=[],
        metavar="NAME",
        help=(
            "Skip tests in pytest/collection_patterns whose component "
            "marker matches one of the given labels."
        ),
    )
    group.addoption(
        "--xfail-label",
        action="append",
        dest="_collection_xfail_labels",
        default=[],
        metavar="NAME",
        help=(
            "Xfail tests in pytest/collection_patterns whose component "
            "marker matches one of the given labels."
        ),
    )


def _component_label(item: pytest.Item) -> Optional[str]:
    """Return the value of the ``component`` marker, if present.

    For this example we treat the first argument to ``@pytest.mark.component``
    as the test's **label**.
    """

    marker = item.get_closest_marker("component")
    if marker and marker.args:
        return str(marker.args[0])
    return None


def _filter_items_by_labels(
    items: List[pytest.Item], labels: Iterable[str]
) -> List[pytest.Item]:
    wanted = {str(label) for label in labels}
    if not wanted:
        return list(items)

    selected: List[pytest.Item] = []
    for item in items:
        label = _component_label(item)
        if label is None:
            continue
        if label in wanted:
            selected.append(item)
    return selected


def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    """Filter or inspect items based on component "labels".

    This hook runs after pytest has collected all tests under
    ``pytest/collection_patterns``. We then:

    * optionally **list** all component labels and exit early, or
    * **filter** the item list in-place based on ``--label`` arguments.
    """

    labels: List[str] = config.getoption("_collection_labels") or []
    list_only: bool = bool(config.getoption("_collection_list_labels"))

    # If neither option is used, do nothing and run all tests as normal.
    if not labels and not list_only:
        return

    # Compute the set of labels that appear on tests in this folder.
    seen_labels = {lbl for lbl in (_component_label(i) for i in items) if lbl}

    terminal_reporter = config.pluginmanager.get_plugin("terminalreporter")

    if list_only:
        # Print one line per label and then clear the item list so pytest
        # will exit without actually running any tests.
        if terminal_reporter is not None:
            for lbl in sorted(seen_labels):
                terminal_reporter.write_line(f"[label] {lbl}")
        items[:] = []
        return

    # Otherwise filter items in-place based on the requested labels.
    selected = _filter_items_by_labels(items, labels)
    if terminal_reporter is not None:
        terminal_reporter.write_line(
            f"[collection] selected {len(selected)}/{len(items)} tests "
            f"matching labels: {', '.join(labels)}"
        )
    items[:] = selected


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Apply skip/xfail at runtime based on component labels.

    This is intentionally **separate** from collection filtering above:

    * ``--skip-label`` and ``--xfail-label`` work at **run time**, so the
      tests are still collected and reported, but marked as SKIPPED or
      XFAILED.
    * This mirrors patterns you might see in large suites where certain
      components are temporarily skipped or expected to fail.
    """

    config = item.config
    skip_labels = set(config.getoption("_collection_skip_labels") or [])
    xfail_labels = set(config.getoption("_collection_xfail_labels") or [])

    if not skip_labels and not xfail_labels:
        return

    label = _component_label(item)
    if label is None:
        return

    if label in skip_labels:
        pytest.skip(f"Skipping component '{label}' via --skip-label")

    if label in xfail_labels:
        pytest.xfail(f"Xfailing component '{label}' via --xfail-label")

