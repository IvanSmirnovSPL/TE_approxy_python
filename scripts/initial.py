import analitic
import make_points
import tree
import numpy as np


# init conditions
class IC:
    def __init__(self, l, name='../square.msh', N=51, T = 1):
        self.l = l
        self.N = N
        self.T = T
        self.tau = T / (N - 1)
        self.get_points(name)
        self.make_start()
        self.get_analitic_solve()

    def get_points(self, name):
        # structure of points
        a = make_points.POINTS(name)
        # POINTS is needed only for building tree
        # DOTS is list of points in point.Point format
        self.DOTS = a.dots
        POINTS = a.points
        self.TREE_OF_POINTS = tree.TREE(POINTS, self.DOTS)
        self.x = [p.x for p in self.DOTS]
        self.y = [p.y for p in self.DOTS]

    def func(self, p):
        r = np.sqrt(p.x**2 + p.y**2)
        q = max(abs(p.x), abs(p.y))
        # smooth
        rez_1 = (np.cos(np.sqrt(p.x ** 2 + p.y ** 2) * 0.5 * np.pi)) ** 2 if np.sqrt(p.x ** 2 + p.y ** 2) < 1 else 0
        rez_1_1 = (np.cos(np.sqrt(p.x**2) * 0.5 * np.pi)) ** 2
        # rough
        # cone
        if r >= 0.5:
            rez_2 = 0
        else:
            rez_2 = 1 - 2 * r
        # pyramid
        rez_3 = 1 - q
        #rough derivative
        if q > 0.5:
            rez_4 = 0
        else:
            rez_4 = 1
        return rez_1

    def coord_to_name(self, coord):
        name = str(coord.x) + ' ' + str(coord.y)
        return name

    def make_start(self):
        self.i_data = {}
        for p in self.DOTS:
            self.i_data[self.coord_to_name(p)] = self.func(p)

    def get_analitic_solve(self):
        self.a_data = analitic.get_solve(self.tau, self.N,
                                         self.func, self.DOTS, self.l)

    # make z coordinate from tree
    def make_z(self, d):
        z = []
        for point in self.TREE_OF_POINTS.dots:
            z.append(d[self.coord_to_name(point)])
        return z
