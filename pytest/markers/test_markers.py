import pytest


# Examples to demonstrate pytest markers


@pytest.mark.slow
def test_slow_example():
    """A dummy 'slow' test, marked just for selection."""
    assert 1 + 1 == 2


@pytest.mark.skip(reason="demonstration of a skipped test")
def test_skipped_example():
    """This test is always skipped."""
    assert 1 == 2  # would fail if it ran, but it is skipped


@pytest.mark.xfail(reason="demonstration of expected failure")
def test_expected_failure_example():
    """This test is expected to fail (xfail)."""
    assert 2 + 2 == 5  # xfail instead of fail


'''
Output from: pytest test_markers.py -v

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ...
collected 3 items

test_markers.py::test_slow_example PASSED                                                                            [ 33%]
test_markers.py::test_skipped_example SKIPPED (demonstration of a skipped test)                                      [ 66%]
test_markers.py::test_expected_failure_example XFAIL (demonstration of expected failure)                             [100%]

===================================================== warnings summary =====================================================
test_markers.py:7
  /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest/test_markers.py:7: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.slow

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
==================================== 1 passed, 1 skipped, 1 xfailed, 1 warning in 0.04s ====================================
'''
