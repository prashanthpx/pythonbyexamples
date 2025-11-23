import pytest


# pass fixture as an argument to the method
def testAdditemtocart(setup):
	print("item added")

def testRemoveitem(setup):
	print("item removed")


'''
output
pytest -vs test_fixture.py
===================================================================================================================== test session starts =====================================================================================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collected 2 items

test_fixture.py::testAdditemtocart launch browser
login
Browse product
item added
PASSED
test_fixture.py::testRemoveitem item removed
PASSED

====================================================================================================================== 2 passed in 0.01s ======================================================================================================================


'''