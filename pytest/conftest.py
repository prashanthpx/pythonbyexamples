import pathlib
import sys

import pytest

# Ensure the repository root (one level above this "pytest" folder) is on
# ``sys.path`` so that our small training plugin package can be imported
# reliably, even when pytest chooses a different working directory.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Enable a small example plugin that demonstrates how large projects
# use pytest plugins to enrich test behavior and reporting.
#
# The plugin implementation lives in
# ``pytest/training_pytest_plugins/meta_report_plugin.py`` and is loaded
# here via its module name.
pytest_plugins = ["training_pytest_plugins.meta_report_plugin"]

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