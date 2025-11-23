import pytest


def testLogin():
    print("Login successful")


def testLogoff():
    print("Logged out successfully")


@pytest.mark.assertion
def testCalcs():
    # if 2+2 is 4, assertion will return true and pass
    assert 2 + 2 == 4


@pytest.mark.assertion
def testAssertfail():
    assert 2 * 3 == 9


'''
Output from: pytest test_group.py -v

=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collecting ...
collected 4 items

test_group.py::testLogin PASSED                                                                                      [ 25%]
test_group.py::testLogoff PASSED                                                                                     [ 50%]
test_group.py::testCalcs PASSED                                                                                      [ 75%]
test_group.py::testAssertfail FAILED                                                                                 [100%]

========================================================= FAILURES =========================================================
______________________________________________________ testAssertfail ______________________________________________________

    @pytest.mark.assertion
    def testAssertfail():
>       assert 2 * 3 == 9
E       assert (2 * 3) == 9

test_group.py:20: AssertionError

===================================================== warnings summary =====================================================
test_group.py:12
  /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest/test_group.py:12: PytestUnknownMarkWarning: Unknown pytest.mark.assertion - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.assertion

test_group.py:18
  /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest/test_group.py:18: PytestUnknownMarkWarning: Unknown pytest.mark.assertion - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.assertion

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================= short test summary info ==================================================
FAILED test_group.py::testAssertfail - assert (2 * 3) == 9
========================================= 1 failed, 3 passed, 2 warnings in 0.08s ==========================================
'''
