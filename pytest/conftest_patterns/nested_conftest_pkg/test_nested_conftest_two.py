import nested_conftest_pkg.conftest as nested_shared


def test_autouse_runs_without_being_listed():
    """Autouse fixture runs even if we don't list it as a parameter.

    This test does not mention `ui_autouse` or `ui_page`, but the
    autouse fixture still runs around the test body.
    """
    print("inside nested_conftest_pkg test two")

    # After two tests, the autouse fixture has run twice.
    assert nested_shared.log.count("ui-autouse-setup") == 2



output = """\n$ pytest -vs nested_conftest_pkg\n=================================================== test session starts ====================================================\nplatform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10\ncachedir: .pytest_cache\nrootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest\nconfigfile: pytest.ini\nplugins: langsmith-0.3.5, anyio-3.6.2\ncollecting ...\ncollected 2 items\n\nnested_conftest_pkg/test_nested_conftest_one.py::test_uses_top_level_setup_and_nested_autouse nested_conftest_pkg: ui_autouse setup\ncalling setup...\nlaunch browser\nlogin\nBrowse product\nnested_conftest_pkg: creating ui_page\ninside nested_conftest_pkg test one\nPASSED\n logoff application\nclose browser\nnested_conftest_pkg: ui_autouse teardown\n\nnested_conftest_pkg/test_nested_conftest_two.py::test_autouse_runs_without_being_listed nested_conftest_pkg: ui_autouse setup\ninside nested_conftest_pkg test two\nPASSEDnested_conftest_pkg: ui_autouse teardown\n\n\n==================================================== 2 passed in 0.01s =====================================================\n"""
