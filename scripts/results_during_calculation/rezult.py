from scripts.results_during_calculation import error
import matplotlib.pyplot as plt
from scripts.utils.point import FILE
from pathlib import Path


class REZULT:

    def __init__(self, num, PATHS):
        self.num = num
        self.PATHS = PATHS
        self.doc = FILE(Path(self.PATHS.files_path, 'doc' + str(self.num) + '.txt'))
        self.err_f = FILE(Path(self.PATHS.files_path, 'err_f' + str(self.num) + '.txt'))
        self.err_f.write2file('time e1 e2 e3' + '\n')
        self.err = error.ERROR()

    def draw(self, x, y, z1, z2, n, N):
        # z1 - numeric, z2 - analytic
        # T - period of saving
        T = 10
        if n % T == 0:
            for j in range(2):
                abscissa = x if j == 0 else y
                name = 'x' if j == 0 else 'y'
                plt.scatter(abscissa, z1, label='numeric in '
                                                + str('%.4f' % (n / (N - 1))) + ' seconds')
                plt.scatter(abscissa, z2, label='analytic in '
                                                + str('%.4f' % (n / (N - 1))) + ' seconds')
                plt.xlabel(name)
                plt.ylabel('function')
                plt.grid(True)
                plt.legend()
                plt.savefig(Path(self.PATHS.grid_path[self.num], name + '_'
                            + str(self.num) + '_' + str(n // T) + '.png'))
                plt.close()

    def upgrade_error(self, n, N, a, b, j):
        abscissa = j
        self.err.calc_error(a, b)
        self.err_f.write2file(abscissa + '\n')
        self.err_f.write2file(str("{:10.4e}".format((n - 1) / (N - 1))) + ' '
                         + str("{:10.4e}".format(self.err.e1[-1])) + ' '
                         + str("{:10.4e}".format(self.err.e2[-1])) + ' '
                         + str("{:10.4e}".format(self.err.e3[-1])) + '\n')

