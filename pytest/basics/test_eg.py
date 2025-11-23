def testLogin():
    print("Login successful")

def testLogoff():
    print("Logged out successfully")

def testCalcs():
    # if 2+2 is 4, assertion will return true and pass
    assert 2+2 == 4

def testAssertfail():
    assert 2+2 == 5


'''
Output
prkumar@prkumar--MacBookPro18 pytest % pytest test_eg.py
====================================================== test session starts =======================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
plugins: langsmith-0.3.5, anyio-3.6.2
collected 4 items                                                                                                                

test_eg.py ...F                                                                                                            [100%]

============================================================ FAILURES ============================================================
_________________________________________________________ testAssertfail _________________________________________________________

    def testAssertfail():
>       assert 2+2 == 5
E       assert (2 + 2) == 5

test_eg.py:12: AssertionError
==================================================== short test summary info =====================================================
FAILED test_eg.py::testAssertfail - assert (2 + 2) == 5
================================================== 1 failed, 3 passed in 0.05s ==================================================                                                                                                          [100%]

'''