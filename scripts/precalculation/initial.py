from scripts.precalculation import tree, make_points, analytic
from scripts.utils.preliminary_preparation import lamb
from scripts.utils.point import FILE
from pathlib import Path
import numpy as np


# init conditions
class IC:
    def __init__(self, name, PATHS, num, N=51, T=1):
        self.num = num
        self.PATHS = PATHS
        self.lamb = lamb
        self.N = N
        self.T = T
        self.tau = T / (N - 1)
        self.get_points(name)
        self.make_start()
        self.get_analytic_solve()

    # generate x and y parts of grid from grid.msh file
    def get_points(self, name):
        # structure of points
        a = make_points.POINTS(name)
        # POINTS is needed only for building tree
        # DOTS is list of points in scripts.utils.point.Point format
        self.DOTS = a.dots
        POINTS = a.points
        self.TREE_OF_POINTS = tree.TREE(POINTS, self.DOTS)
        self.x = [p.x for p in self.DOTS]
        self.y = [p.y for p in self.DOTS]

    def coord_to_name(self, coord):
        name = str(coord.x) + ' ' + str(coord.y)
        return name

    # make zero slice of time
    def make_start(self):
        self.i_data = {}
        for p in self.DOTS:
            self.i_data[self.coord_to_name(p)] = self.PATHS.transport_function(p)

    def get_analytic_solve(self):
        self.dots_for_calc = self.DOTS
        q = FILE(Path(self.PATHS.grid_file_path[self.num], 'dots_for_calc' + str(self.num) + '.txt'))
        for j in self.dots_for_calc:
            q.write2file(str(j.x) + ' ' + str(j.y) + '\n')
        self.a_data = analytic.get_solve(self.tau, self.N,
                                         self.PATHS.transport_function, self.DOTS, self.lamb, self.PATHS, self.num)

    # make z coordinate from tree
    def make_z(self, d):
        z = []
        for point in self.TREE_OF_POINTS.dots:
            z.append(d[self.coord_to_name(point)])
        return z
