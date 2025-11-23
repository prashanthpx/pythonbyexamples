import pytest

log = []


@pytest.fixture(scope="package")
def package_fix():
    """Package-scope fixture used by all tests in this directory.

    It will be set up once when the first test in this package runs,
    and torn down once after the last test in this package.
    """
    log.append("package-setup")
    yield
    log.append("package-teardown")

output = """\
=================================================== test session starts ====================================================
platform darwin -- Python 3.10.18, pytest-9.0.1, pluggy-1.6.0 -- /opt/homebrew/opt/python@3.10/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/prkumar/Documents/No Backup/pythonexamples/practice/pytest
configfile: pytest.ini
plugins: langsmith-0.3.5, anyio-3.6.0
collecting ... collected 4 items

package_scope_pkg/test_pkg_one.py::TestPkgOne::test_one PASSED
package_scope_pkg/test_pkg_one.py::TestPkgOne::test_two PASSED
package_scope_pkg/test_pkg_two.py::TestPkgTwo::test_three PASSED
test_package_scope_log.py::test_package_fixture_runs_once_for_package PASSED

==================================================== 4 passed in 0.01s =====================================================
"""
