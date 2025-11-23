import pytest


# Phase 3  Fixtures: using built-in tmp_path fixture


paths = []


def test_write_and_read_tmp_file(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("hello pytest")
    assert file_path.read_text() == "hello pytest"


def test_tmp_path_is_unique_per_test(tmp_path):
    # Record the paths to show that each test gets a different directory.
    paths.append(tmp_path)
    if len(paths) == 2:
        # When the second test runs, both entries should be present and different.
        assert paths[0] != paths[1]


'''
Output from: pytest -v test_tmp_path_fixture.py

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ... collected 2 items

test_tmp_path_fixture.py::test_write_and_read_tmp_file PASSED
test_tmp_path_fixture.py::test_tmp_path_is_unique_per_test PASSED

==================================================== 2 passed in 0.01s ====================================================
'''

