import os
import shutil
from numpy import sin, cos, sqrt, pi
import numpy as np
import pathlib
from pathlib import Path

# parameters of grid
scale = [0.2, 0.1, 0.05, 0.025, 0.0125]
grids_num = 1
lamb = [-2, 5]


def transport_function(p):
    r = sqrt(p.x ** 2 + p.y ** 2)
    q = max(abs(p.x), abs(p.y))
    # smooth
    rez_1 = (cos(sqrt(p.x ** 2 + p.y ** 2) * 0.5 * pi)) ** 2 \
        if sqrt(p.x ** 2 + p.y ** 2) < 1 else 0
    rez_1_1 = (cos(sqrt(p.x ** 2) * 0.5 * pi)) ** 2
    # rough
    # cone
    if r >= 0.5:
        rez_2 = 0
    else:
        rez_2 = 1 - 2 * r
    # pyramid
    rez_3 = 1 - q
    # rough derivative
    if q > 0.5:
        rez_4 = 0
    else:
        rez_4 = 1
    return rez_1


class PATHS:
    def __init__(self):
        # Get home directory
        self.dir_path = pathlib.Path.cwd()
        self.exp_path = Path(self.dir_path.parent, 'exp')
        self.rez_path = Path(self.dir_path.parent, 'rez')
        self.files_path = Path(self.dir_path.parent, 'rez', 'files')
        self.pictures_path = Path(self.dir_path.parent, 'rez', 'pictures')
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
