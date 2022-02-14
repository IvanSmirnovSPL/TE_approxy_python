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

    def upgrade_error(self, n, N, f1, f2):
        a_x, c_x, a_y, c_y = check(f1, f2, n)
        self.err.calc_error(a_x, c_x, 'x')
        self.err.calc_error(a_y, c_y, 'y')
        self.err_f.write2file(str("{:10.4e}".format((n) / (N - 1))) + ' x '
                                  + str("{:10.4e}".format(self.err.e1.x[-1])) + ' '
                                  + str("{:10.4e}".format(self.err.e2.x[-1])) + ' '
                                  + str("{:10.4e}".format(self.err.e3.x[-1])) + '\n')
        self.err_f.write2file(str("{:10.4e}".format((n) / (N - 1))) + ' y '
                                  + str("{:10.4e}".format(self.err.e1.y[-1])) + ' '
                                  + str("{:10.4e}".format(self.err.e2.y[-1])) + ' '
                                  + str("{:10.4e}".format(self.err.e3.y[-1])) + '\n')


def start_end(f1, f2, num):
    f1 = open(f1, 'r')
    f2 = open(f2, 'r')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    f1.close()
    f2.close()
    pattern1 = 'Slice №' + str(num) + ' _x_ '
    pattern2 = 'Slice №' + str(num) + ' _y_ '
    start1 = 0
    finish1 = 0
    start2 = 0
    finish2 = 0
    for j in range(len(lines1)):
        if pattern1 in lines1[j]:
            start1 = j + 1
        if pattern2 in lines1[j]:
            finish1 = j - 1
            start2 = j + 1
        finish2 = start2 + finish1 - start1
    return start1, finish1, start2, finish2


def check(f1, f2, num):
    start1, finish1, start2, finish2 = start_end(f1, f2, num)
    f1 = open(f1, 'r')
    f2 = open(f2, 'r')
    lines1 = f1.readlines()
    lines2 = f2.readlines()
    a_x = [float(lines1[j].split()[-1]) for j in range(start1, finish1 + 1)]
    c_x = [float(lines2[j].split()[-1]) for j in range(start1, finish1 + 1)]
    a_y = [float(lines1[j].split()[-1]) for j in range(start2, finish2 + 1)]
    c_y = [float(lines2[j].split()[-1]) for j in range(start2, finish2 + 1)]
    f1.close()
    f2.close()

    return a_x, c_x, a_y, c_y
