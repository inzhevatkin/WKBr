from math import sin, cos, asin, tan

# Данный класс будет хранить коэффициенты линий, который ограничивают области с одним решением, с двумя и без решений.
class BoundaryLines(object):
    def __init__(self, m, R):
        sin_tmp = 1 / m
        self.a1 = - sin_tmp / (1 - sin_tmp ** 2) ** 0.5
        self.b1 = R * (1 - self.a1)
        psi = asin(((4 - m ** 2) / 3) ** 0.5)
        theta = 2 * asin(sin(psi) / m) - psi
        self.a2 = 1 / tan((theta - psi) / 2.)
        self.b2 = R * (1 + cos(theta) - self.a2 * sin(theta))
        self.m = m
        self.R = R


# Function for determining in which region a given point is located.
# Returns: "one_root", "two_roots", "no_root"
def region(y2, z2, R, m, lines):
    if 0 <= y2 <= R and 0 <= z2 <= 2 * R:
        if z2 > R:
            if R == lines.R and m == lines.m:
                z_l1 = lines.a1 * y2 + lines.b1
                y2_l2 = (z2 - lines.b2) / lines.a2
            else:
                print("Error in region() function!")
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