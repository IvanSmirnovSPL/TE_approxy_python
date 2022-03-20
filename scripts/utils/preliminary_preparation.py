import os
import shutil
from numpy import sin, cos, sqrt, pi, exp
import numpy as np
import pathlib
from pathlib import Path

# parameters of grid
scale = [0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625]
grids_num = 6
lamb = [-2, 5]


class PATHS:
    def __init__(self, figure):
        # Get home directory
        self.figure = figure
        self.dir_path = pathlib.Path.cwd()
        self.exp_path = Path(self.dir_path.parent, 'exp')
        self.rez_path = Path(self.dir_path.parent, 'rez_' + figure)
        self.files_path = Path(self.dir_path.parent, 'rez_' + figure, 'files')
        self.pictures_path = Path(self.dir_path.parent, 'rez_' + figure, 'pictures')
        self.meshes_path = []
        for j in range(grids_num):
            self.meshes_path.append(Path(self.dir_path.parent,
                                         'exp', 'mesh_' + str(j) + '.msh'))
        # make directory for saving results
        shutil.rmtree(self.rez_path, ignore_errors=True)
        os.mkdir(self.rez_path)
        os.mkdir(self.pictures_path)
        self.grid_pic_path = []
        self.grid_file_path = []
        self.grid_vtk_path = []
        for j in range(grids_num):
            os.mkdir(Path(self.pictures_path, 'grid_' + str(j)))
            self.grid_pic_path.append(Path(self.pictures_path, 'grid_' + str(j)))
        os.mkdir(self.files_path)
        for j in range(grids_num):
            os.mkdir(Path(self.files_path, 'grid_' + str(j)))
            self.grid_file_path.append(Path(self.files_path, 'grid_' + str(j)))
            os.mkdir(Path(self.files_path, 'grid_' + str(j), 'vtk'))
            self.grid_vtk_path.append(Path(self.files_path, 'grid_' + str(j), 'vtk'))

    def transport_function(self, p):
        if self.figure == 'wave':
            return (cos(sqrt(p.x ** 2 + p.y ** 2) * 0.5 * pi)) ** 2 \
                if sqrt(p.x ** 2 + p.y ** 2) < 1 else 0
        elif self.figure == 'cone':
            r = sqrt(p.x ** 2 + p.y ** 2)
            if r >= 0.5:
                tmp = 0
            else:
                tmp = 1 - 2 * r
            return tmp
        elif self.figure == 'cube':
            q = max(abs(p.x), abs(p.y))
            if q > 0.5:
                tmp = 0
            else:
                tmp = 1
            return tmp
        elif self.figure == 'fig_1':
            return (cos(p.x * pi / 2) * cos(p.y * pi / 2)) ** 4
        elif self.figure == 'fig_2':
            if -0.2 < p.x < 0.2 and -0.2 < p.y < 0.2:
                tmp = exp(- 84 * (p.x ** 2 + p.y ** 2))
            else:
                tmp = 0
            return tmp
        elif self.figure == 'fig_3':
            if -0.2 < p.x < 0.2 and -0.2 < p.y < 0.2:
                tmp = (1 - 5 * abs(p.x)) * (1 - 5 * abs(p.y))
            else:
                tmp = 0
            return tmp
        elif self.figure == 'fig_4':
            if -0.2 < p.x < 0.2 and -0.2 < p.y < 0.2:
                tmp = sqrt((1 - 25 * p.x ** 2) * (1 - 25 * p.y ** 2))
            else:
                tmp = 0
            return tmp
        else:
            print('Bad figure')
            return 0
