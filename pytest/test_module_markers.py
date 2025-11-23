import pytest


# Phase 4  Markers: module-level markers with pytestmark


pytestmark = pytest.mark.slow


def test_module_level_marker_one():
    """This test inherits the module-level 'slow' marker."""
    assert 1 + 1 == 2


def test_module_level_marker_two():
    """This test also inherits the 'slow' marker."""

'''
Output from: pytest -v test_module_markers.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.0
collecting ... collected 2 items

test_module_markers.py::test_module_level_marker_one PASSED
test_module_markers.py::test_module_level_marker_two PASSED

==================================================== 2 passed in 0.01s ====================================================
'''

