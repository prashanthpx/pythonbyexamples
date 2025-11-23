import os
import pytest


# Phase 4  Markers: runtime skip and xfail inside tests


def test_runtime_skip_if_env_not_set():
    """Use pytest.skip() at runtime if a condition is not met."""
    if "MY_FEATURE_FLAG" not in os.environ:
        pytest.skip("MY_FEATURE_FLAG not set")
    assert True


def test_runtime_xfail_inside_test():
    """Use pytest.xfail() at runtime to mark a known bug."""
    pytest.xfail("demonstration of runtime xfail")
    assert 2 + 2 == 5  # would fail, but reported as XFAIL



'''
Output from: pytest -v test_runtime_skip_xfail.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.0
collecting ... collected 2 items

test_runtime_skip_xfail.py::test_runtime_skip_if_env_not_set SKIPPED (MY_FEATURE_FLAG not set)
test_runtime_skip_xfail.py::test_runtime_xfail_inside_test XFAIL (demonstration of runtime xfail)

============================================== 1 skipped, 1 xfailed in 0.03s ===============================================
'''
