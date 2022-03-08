import numpy as np
from scripts.utils.point import Point


class ERROR:
    def __init__(self):
        self.e1 = Point()
        self.e1.x = []
        self.e1.y = []
        self.e2 = Point()
        self.e2.x = []
        self.e2.y = []
        self.e3 = Point()
        self.e3.x = []
        self.e3.y = []

    def calc_error(self, a, b, j):
        error = []
        tmp = min(len(a), len(b))
        for i in range(tmp):
            error.append(abs(a[i] - b[i]))
        e1 = max(error)
        e2 = sum(error) / len(error)
        e3 = np.sqrt(sum(list(map(lambda t: t**2, error)))) / len(error)
        if j == 'x':
            self.e1.x.append(e1)
            self.e2.x.append(e2)
            self.e3.x.append(e3)
        else:
            self.e1.y.append(e1)
            self.e2.y.append(e2)
            self.e3.y.append(e3)

