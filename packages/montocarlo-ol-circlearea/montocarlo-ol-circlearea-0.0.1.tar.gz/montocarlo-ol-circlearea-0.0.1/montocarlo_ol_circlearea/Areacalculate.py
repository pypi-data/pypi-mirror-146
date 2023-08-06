import math
import numpy as np


class Overlapped_2_circles:
    """
    Area of overlapped region between 2 Circle will be calculated using MontoCarlo method (Random Points)
    :param _c1: circle1[center c1, center c2, radius r1]
    :type _c1: list
    :param _c2: circle2[center c1, center c2, radius r2]
    :type _c2: list
    :param _N: Number of Random Points
    :type _N: int
    """
    def __init__(self, _c1, _c2, _N):
        self._c1 = _c1
        self._c2 = _c2
        self._N = _N

    def area(self):
        # circle c1
        x1 = self._c1[0]
        y1 = self._c1[1]
        r1 = self._c1[2]
        # circle c2
        x2 = self._c2[0]
        y2 = self._c2[1]
        r2 = self._c2[2]

        Random_points = self._N

        if math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)) >= (r1 + r2):
            # no intersection (Area of overlapped region is zero)
            Area = 0
        else:
            a_min = x1 - r1 - 2 * r2
            a_max = x1 + r1 + 2 * r2
            b_min = y1 - r1 - 2 * r2
            b_max = y1 + r1 + 2 * r2

            # Monte Carlo algorithm
            count = 0
            for x in range(Random_points):
                rand_x = (a_max - a_min) * np.random.rand() + a_min
                rand_y = (b_max - b_min) * np.random.rand() + b_min
                if (math.sqrt((rand_x - x1) ** 2 + (rand_y - y1) ** 2) < r1) and (
                        math.sqrt((rand_x - x2) ** 2 + (rand_y - y2) ** 2) < r2):
                    count = count + 1
            Area = ((a_max - a_min) * (b_max - b_min)) * count / Random_points

        return Area

