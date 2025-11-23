import pytest


log = []


@pytest.fixture(autouse=True)
def ui_autouse():
    """Autouse fixture that runs for every test in this package.

    We use it to show how a nested conftest.py can add behavior that only
    applies to tests in this subpackage.
    """
    print("nested_conftest_pkg: ui_autouse setup")
    log.append("ui-autouse-setup")
    yield
    log.append("ui-autouse-teardown")
    print("nested_conftest_pkg: ui_autouse teardown")


@pytest.fixture
def ui_page():
    """Simple fixture local to this package."""
    print("nested_conftest_pkg: creating ui_page")
    return "UI-PAGE"

