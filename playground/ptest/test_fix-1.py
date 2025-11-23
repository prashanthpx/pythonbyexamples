import pytest

@pytest.fixture
def calc_values():
	return {"a": 10, "b": 5, "negative": -5, "zero": 0}


def test_calc_fixtures(calc_values):
	values = calc_values
	for val in values:
		print(f"{val}")
