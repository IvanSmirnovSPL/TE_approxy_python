import scipy as sp
import numpy as np
import time
import matplotlib.pyplot as plt
from pathlib import Path
from scripts.utils.point import residual
from scripts.utils.point import FILE


class Showing_results:

    def __init__(self, scale, PATHS):
        self.main_rez = FILE(Path(PATHS.files_path, 'main_rez.txt'))
        self.r = residual()
        self.h_dots = []
        self.h_dots_scale = []
        self.scale = scale
        self.PATHS = PATHS

    def new_grid(self, num):
        self.num = num
        print('Grid №', self.num)
        self.main_rez.write2file(str(self.num) + ' scale: '
                                 + str(self.scale[self.num]) + ' ')
        self.start_time = time.time()

    def add_grid(self, tmp):
        self.main_rez.write2file('dots: ' + str(tmp[-1]) + ' step: '
                                 + str("{:10.4e}".format(1 / np.sqrt(tmp[1]))) + ' ')
        self.r.e1.x.append(np.log(tmp[0]))
        self.r.e2.x.append(np.log(tmp[1]))
        self.r.e3.x.append(np.log(tmp[2]))
        self.r.e1.y.append(np.log(tmp[3]))
        self.r.e2.y.append(np.log(tmp[4]))
        self.r.e3.y.append(np.log(tmp[5]))
        self.h_dots_scale.append(np.log(self.scale[self.num]))
        self.h_dots.append(np.log(1 / np.sqrt(tmp[-1])))
        self.main_rez.write2file('time: '
                                 + "%.4f" % (time.time() - self.start_time) + '\n')

    # generate approximation functions and write them on file
    def get_func(self, discrepancy, num, bar):
        fp, residuals, rank, sv, rcond = np.polyfit(self.h_dots,
                                                    discrepancy, 1, full=True)
        func1 = sp.poly1d(fp)
        self.main_rez.write2file('=====================e ' + bar + ' '
                                 + str(num + 1) + '=======================')
        self.main_rez.write2file('\n' + 'function_(1 / sqrt(dots)): '
                                 + str(func1) + '\n')
        fp, residuals, rank, sv, rcond = np.polyfit(self.h_dots_scale,
                                                    discrepancy, 1, full=True)
        func2 = sp.poly1d(fp)
        self.main_rez.write2file('\n' + 'function_(scale): ' + str(func2) + '\n')
        return func1, func2

    # chose suitable error norm
    @staticmethod
    def switch_residual_norm(residual_norm, real_residual, j):
        if residual_norm == 0:
            discrepancy = real_residual.e1.x if j == 0 else real_residual.e1.y
            res_name = 'main_rez_e1_x.png' if j == 0 else 'main_rez_e1_y.png'
        elif residual_norm == 1:
            discrepancy = real_residual.e2.x if j == 0 else real_residual.e2.y
            res_name = 'main_rez_e2_x.png' if j == 0 else 'main_rez_e2_y.png'
        elif residual_norm == 2:
            discrepancy = real_residual.e3.x if j == 0 else real_residual.e3.y
            res_name = 'main_rez_e3_x.png' if j == 0 else 'main_rez_e3_y.png'
        return discrepancy, res_name

    # show results
    def show_main_graphics(self):
        for i in range(3):
            for j in range(2):
                bar = 'x' if j == 0 else 'y'
                residual, name = self.switch_residual_norm(i, self.r, j)
                plt.clf()
                func_1, func_2 = self.get_func(residual, i, bar)

                plt.scatter(self.h_dots, residual, c='b', label=r'$\frac{1}{\sqrt{dots}}$')
                plt.scatter(self.h_dots_scale, residual, c='g', label=r'$\frac{1}{scale}$')
                plt.plot(self.h_dots, list(map(lambda t: t * func_1[1] + func_1[0],
                                               self.h_dots)), '--', c='b', label=func_1)
                plt.plot(self.h_dots_scale,
                         list(map(lambda t: t * func_2[1] + func_2[0],
                                  self.h_dots_scale)), '--', c='g', label=func_2)
                plt.legend()
                plt.xlabel(r'$\ln h_{dots}$')
                plt.ylabel(r'$\ln r$')
                plt.grid(True)
                plt.savefig(Path(self.PATHS.pictures_path, name), dpi=1000)
