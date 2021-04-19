from iterative_method import func, func2, tolerance
from math import sin, cos, asin, tan, isclose


# This class stores the coefficients of the lines that bound regions with one solution, with two and without solutions.
# Radius = 1.
# z = a * y + b
class BoundaryLines(object):
    def __init__(self, m):
        self.m = m
        # grazing ray:
        tmp = 1 / (m ** 2 - 1) ** 0.5
        self.a1 = - tmp
        self.b1 = tmp
        # Descartes ray:
        sin_tmp = ((4 - m ** 2) / 3) ** 0.5
        teta = asin(sin_tmp)
        psi = 2 * asin(sin_tmp / m) - teta
        k1 = tan((teta - psi) / 2)
        self.a2 = - 1 / k1
        self.b2 = sin_tmp / k1 - cos(teta)


# check that the point in the sphere
def in_sphere(y, z):
    r2 = y ** 2 + z ** 2
    if r2 <= 1:
        return True
    else:
        return False


# Function for determining in which region a given point is located.
# Returns: "one_root", "two_roots", "no_root", "error"
def region(y2, z2, m, lines):
    if in_sphere(y2, z2):
        if z2 >= 0:
            if m == lines.m:
                z_l1 = lines.a1 * y2 + lines.b1  # grazing ray
                y2_l2 = (z2 - lines.b2) / lines.a2  # Descartes ray
            else:
                print("Error in region() function!")
                return "error"
            if z2 >= z_l1:
                if y2 <= y2_l2:
                    return "two_roots"
                else:
                    return "no_root"
            else:
                return "one_root"
        else:
            return "one_root"
    else:
        print("Error in region() function!")
        return "error"


def in_square(y, z, R):
    if 0 <= y <= R and -R <= z <= 0:
        return True
    else:
        return False


# Function for determining in which region a given point is located (without grazing and Descartes rays).
# Returns: "one_root", "two_roots", "no_root", "error".
def region2(y2, z2, m):
    root_flag, y1, z1 = func(y2, z2, m, y2)
    # root_flag2, y1_2, z1_2 = func2(y2, z2, R, m, 1)
    if root_flag:
        # "one_root"
        root_flag2, y1_2, z1_2 = func(y2, z2, m, 1)
        if root_flag2 and isclose(y1, y1_2, abs_tol=tolerance * 10) and isclose(z1, z1_2, abs_tol=tolerance * 10):
            return "one_root"
        # "two_roots"
        if isclose(y1, y1_2, abs_tol=tolerance) and isclose(z1, z1_2, abs_tol=tolerance):
            if in_square(y1, z1, R):
                return "one_root"
            else:
                return "no_root"
        else:
            if in_square(y1, z1, R) and in_square(y1_2, z1_2, R):
                return "two_roots"
            else:
                return "no_root"
    elif root_flag:
        return "no_root"
    else:
        print("Error in region2() function!")
        return "error"
