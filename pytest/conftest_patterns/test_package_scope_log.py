from package_scope_pkg.conftest import log


# Phase 3 – Fixtures: demonstrating package scope across multiple modules


def test_package_fixture_runs_once_for_package():
    # The tests in package_scope_pkg will be collected and run first
    # when we run this file with -k.
    # We don't assert on the exact test-log entries, only on the
    # package-level setup/teardown markers.
    assert log.count("package-setup") == 1
    assert log.count("package-teardown") == 1

