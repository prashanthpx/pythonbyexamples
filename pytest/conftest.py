import pytest
# pytest_plugins = ["session_scope_shared"]  # Moved to conftest_patterns/



# @pytest.fixture(autouse=True)
@pytest.fixture
def setup():
	print("calling setup...")
	print("launch browser")
	print("login")
	print("Browse product")
	yield
	print("\n logoff application")
	print("close browser")


# if we have multiple methods with autouse=True, all will be
# executed from top to bottom order
# @pytest.fixture(autouse=True)
@pytest.fixture
def shutdown():
	print("calling shutdown...")
	print("logoff application")
	yield
	print("\n shudown system")