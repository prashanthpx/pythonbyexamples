from .conftest import log


class TestPkgTwo:
    def test_three(self, package_fix):
        log.append("pkg-two-test-three")

