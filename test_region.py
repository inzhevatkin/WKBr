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
        m = 1.1
        assert region2(0.5, 0.5, m) == "one_root"
        assert region2(0.5, -0.5, m) == "one_root"
        assert region2(0, 0, m) == "one_root"
        assert region2(0, -1, m) == "one_root"
        assert region2(0, 1, m) == "one_root"
        assert region2(0.78, 0.5, m) == "two_roots"
        assert region2(0.8, 0.5, m) == "no_root"
        assert region2(0.9, 0.9, m) == "error"
        assert region2(0.8295857402818346, 0.36895316611247475, m) == "one_root"
        assert region2(0.7879568729508031, 0.4927658178691825, m) == "two_roots"

        # read from Mathematica test data:
        f = open("C:/Users/konstantin/PycharmProjects/WKBr2/m=1.1.dat", 'r')
        while True:
            numbers = f.readline()
            if len(numbers) == 0:  # EOF
                break
            numbers = numbers.split()
            y1 = float(numbers[0])
            z1 = float(numbers[1])
            n = float(numbers[2])
            if n == 0:
                assert region2(y1, z1, m) == "no_root"
            elif n == 1:
                assert region2(y1, z1, m) == "one_root"
            elif n == 2:
                assert region2(y1, z1, m) == "two_roots"
            else:
                print("Error in test_region2() function! Undefined parameter n.")
        f.close()

