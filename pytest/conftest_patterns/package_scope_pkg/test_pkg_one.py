from .conftest import log


class TestPkgOne:
    def test_one(self, package_fix):
        log.append("pkg-one-test-one")

    def test_two(self, package_fix):
        log.append("pkg-one-test-two")

