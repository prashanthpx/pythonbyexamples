import pytest
import nested_conftest_pkg.conftest as nested_shared


def test_uses_top_level_setup_and_nested_autouse(setup, ui_page):
    """Uses top-level `setup` plus the nested autouse fixture.

    - `setup` comes from the top-level practice/pytest/conftest.py.
    - `ui_autouse` comes from nested_conftest_pkg/conftest.py and runs
      automatically for every test in this package.
    """
    print("inside nested_conftest_pkg test one")

    assert ui_page == "UI-PAGE"
    # First test: ui_autouse has run exactly once so far.
    assert nested_shared.log.count("ui-autouse-setup") == 1

