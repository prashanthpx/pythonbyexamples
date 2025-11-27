def testassert():
	assert 2+2 == 4

def testNoassert():
	assert not 2+3 == 6

def test_assert_msg():
	assert 2 == 3, f"2 is not equal to 3"

