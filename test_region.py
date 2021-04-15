from unittest import TestCase
from Region import region, region2, BoundaryLines


class TestRegion(TestCase):
    def test_region(self):
        m = 1.1
        lines = BoundaryLines(m)
        assert region(0.5, 0.5, m, lines) == "one_root"
        assert region(0.5, -0.5, m, lines) == "one_root"
        assert region(0, 0, m, lines) == "one_root"
        assert region(0, -1, m, lines) == "one_root"
        assert region(0, 1, m, lines) == "one_root"
        assert region(0.78, 0.5, m, lines) == "two_roots"
        assert region(0.8, 0.5, m, lines) == "no_root"
        assert region(0.9, 0.9, m, lines) == "error"

    def test_region2(self):
        assert region2(0.5, 0.5, 1, 1.1) == "one_root"
        assert region2(0.78, 0.5, 1, 1.1) == "two_roots"
        assert region2(0.8, 0.5, 1, 1.1) == "no_root"
