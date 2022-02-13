import numpy as np


class ERROR:
    def __init__(self):
        self.e1 = []
        self.e2 = []
        self.e3 = []

    def calc_error(self, a, b):
        error = []
        tmp = min(len(a), len(b))
        for i in range(tmp):
            error.append(abs(a[i] - b[i]))
        e1 = max(error)
        e2 = sum(error)
        e3 = np.sqrt(sum(list(map(lambda t: t**2, error))))
        self.e1.append(e1)
        self.e2.append(e2)
        self.e3.append(e3)
