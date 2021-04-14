from unittest import TestCase
from Region import region2


class TestRegion(TestCase):
    def test_region2(self):
        assert region2(0.5, 0.5, 1, 1.1) == "one_root"
        assert region2(0.78, 0.5, 1, 1.1) == "two_roots"
        assert region2(0.8, 0.5, 1, 1.1) == "no_root"
