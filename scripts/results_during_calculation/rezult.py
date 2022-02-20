from scripts.results_during_calculation import error
import matplotlib.pyplot as plt
from scripts.utils.point import FILE
from scripts.utils.point import Point
from pathlib import Path


class REZULT:

    def __init__(self, num, PATHS):
        self.num = num
        self.PATHS = PATHS
        self.der = FILE(Path(PATHS.grid_file_path[num], 'derivative' + str(num) + '.txt'))
        self.doc = FILE(Path(self.PATHS.grid_file_path[num], 'doc' + str(self.num) + '.txt'))
        self.err_f = FILE(Path(self.PATHS.grid_file_path[num], 'err_f' + str(self.num) + '.txt'))
        self.err_f.write2file('time e1 e2 e3' + '\n')
        self.err = error.ERROR()
        self.der_slices = Point()
        self.der_slices.x = []
        self.der_slices.y = []
        self.avg_der_answer = Point()
        self.avg_der_answer.x = []
        self.avg_der_answer.y = []

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
                plt.savefig(Path(self.PATHS.grid_pic_path[self.num], name + '_'
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

    def new_der_slice(self):
        self.der_slices.x.append(derivative(1e10, 0))
        self.der_slices.y.append(derivative(1e10, 0))
        self.avg_ratio = Point()
        self.avg_ratio.x = []
        self.avg_ratio.y = []
        self.avg_der_answer.x.append(0)
        self.avg_der_answer.y.append(0)

    def update_slice(self, d1_x, d2_x, d1_y, d2_y):
        cur_der_x = derivative(d1_x, d2_x)
        cur_der_y = derivative(d1_y, d2_y)
        self.der_slices.x[-1].d1 = min(cur_der_x.d1, self.der_slices.x[-1].d1)
        self.der_slices.x[-1].d2 = max(cur_der_x.d2, self.der_slices.x[-1].d2)
        self.der_slices.x[-1].der_ratio = max(cur_der_x.der_ratio,
                                              self.der_slices.x[-1].der_ratio)
        if cur_der_x.der_ratio >= 0:
            self.avg_ratio.x.append(cur_der_x.der_ratio)
            self.avg_der_answer.x[-1] = (self.avg_der_answer.x[-1] * (len(self.avg_ratio.x) - 1)
                                         + self.avg_ratio.x[-1]) / len(self.avg_ratio.x)
        self.der_slices.y[-1].d1 = min(cur_der_y.d1, self.der_slices.y[-1].d1)
        self.der_slices.y[-1].d2 = max(cur_der_y.d2, self.der_slices.y[-1].d2)
        self.der_slices.y[-1].der_ratio = max(cur_der_y.der_ratio,
                                              self.der_slices.y[-1].der_ratio)
        if cur_der_y.der_ratio >= 0:
            self.avg_ratio.y.append(cur_der_y.der_ratio)
            self.avg_der_answer.y[-1] = (self.avg_der_answer.y[-1] * (len(self.avg_ratio.y) - 1)
                                         + self.avg_ratio.y[-1]) / len(self.avg_ratio.y)


    def upgrade_der(self, n, N):
        self.der.write2file(str("{:10.4e}".format((n) / (N - 1))) + ' x '
                            + str("{:10.4e}".format(self.der_slices.x[n - 1].d1)) + ' '
                            + str("{:10.4e}".format(self.der_slices.x[n - 1].d2)) + ' '
                            + str("{:10.4e}".format(self.avg_der_answer.x[n - 1])) + ' '
                            + str("{:10.4e}".format(self.der_slices.x[n - 1].der_ratio)) + '\n')
        self.der.write2file(str("{:10.4e}".format((n) / (N - 1))) + ' y '
                            + str("{:10.4e}".format(self.der_slices.y[n - 1].d1)) + ' '
                            + str("{:10.4e}".format(self.der_slices.y[n - 1].d2)) + ' '
                            + str("{:10.4e}".format(self.avg_der_answer.y[n - 1])) + ' '
                            + str("{:10.4e}".format(self.der_slices.y[n - 1].der_ratio)) + '\n')


class derivative:
    def __init__(self, d1, d2):
        self.d1 = abs(d1)
        self.d2 = abs(d2)
        self.der_ratio = abs(d2 / d1) if abs(d1) != 0 else -1


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
