import sys
import pytest


# Phase 4  Markers: conditional skipping with skipif


RUN_EXPENSIVE = False


@pytest.mark.skipif(sys.platform.startswith("win"), reason="skip on Windows")
def test_not_on_windows():
    """This test will be skipped on Windows, but run elsewhere."""
    assert True


@pytest.mark.skipif(not RUN_EXPENSIVE, reason="expensive test disabled")
def test_expensive_operation():
    """Example of using a flag to disable an expensive test."""
    assert 2 * 3 == 6

'''
Output from: pytest -v test_skipif.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.0
collecting ... collected 2 items

test_skipif.py::test_not_on_windows PASSED
test_skipif.py::test_expensive_operation SKIPPED (expensive test disabled)

=============================================== 1 passed, 1 skipped in 0.01s ===============================================
'''


