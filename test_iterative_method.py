from unittest import TestCase
from pytest import approx
from iterative_method import func, func2, tolerance


class TestIterMethod(TestCase):
    def test_func(self):
        # one solution
        y2 = 0.5
        z2 = 0.5
        m = 1.1
        root_flag, y1, z1 = func(y2, z2, m, y2)
        assert root_flag is True
        assert y1 == approx(0.58404, 1e-4)
        assert z1 == approx(-(1 - y1 ** 2) ** 0.5, 1e-4)
        root_flag, y1, z1 = func(y2, z2, m, 1)
        assert root_flag is True
        assert y1 == approx(0.58404, 1e-4)
        assert z1 == approx(-(1 - y1 ** 2) ** 0.5, 1e-4)

        # two solution
        y2 = 0.78
        z2 = 0.5
        m = 1.1
        root_flag, y1, z1 = func(y2, z2, m, y2)
        assert root_flag is True
        assert y1 == approx(0.958827, 1e-4)
        assert z1 == approx(-(1 - y1 ** 2) ** 0.5, 1e-4)
        root_flag, y1, z1 = func2(y2, z2, m, 1)
        assert root_flag is True
        assert y1 == approx(0.997381, 1e-4)
        assert z1 == approx(-(1 - y1 ** 2) ** 0.5, 1e-4)

        # no solution
        y2 = 0.8
        z2 = 0.5
        m = 1.1
        root_flag, y1, z1 = func(y2, z2, m, y2)
        assert root_flag is False
        root_flag, y1, z1 = func(y2, z2, m, 1)
        assert root_flag is False
        root_flag, y1, z1 = func2(y2, z2, m, 1)
        assert root_flag is False
