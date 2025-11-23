import pytest


def test_add_item_uses_setup_fixture(setup):
    """Uses the shared `setup` fixture defined in conftest.py."""

    print("adding item in second module")


def test_shutdown_fixture(shutdown):
    """Uses the shared `shutdown` fixture defined in conftest.py."""

    print("running shutdown-only test")



output = """\n$ pytest -vs test_conftest_shared_fixtures.py\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ...\ncollected 2 items\n\ntest_conftest_shared_fixtures.py::test_add_item_uses_setup_fixture calling setup...\nlaunch browser\nlogin\nBrowse product\nadding item in second module\nPASSED\n logoff application\nclose browser\n\ntest_conftest_shared_fixtures.py::test_shutdown_fixture calling shutdown...\nlogoff application\nrunning shutdown-only test\nPASSED\n shudown system\n\n\n==================================================== 2 passed in 0.01s =====================================================\n"""
