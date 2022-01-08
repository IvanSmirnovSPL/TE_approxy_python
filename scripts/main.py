import test
import scipy as sp
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import shutil

# make directory for saving results
shutil.rmtree('../rez', ignore_errors=True)
os.mkdir('../rez')
os.mkdir('../rez/pictures')
f = open('../rez/main_rez.txt', 'w')

# parameters of grid
scale = [0.2, 0.1, 0.05, 0.025, 0.0125]


class residual:
    def __init__(self):
        self.e1 = []
        self.e2 = []
        self.e3 = []


def switch_residual_norm(residual_norm, real_residual):
    if residual_norm == 0:
        residual = real_residual.e1
        res_name = 'main_rez_e1.png'
    elif residual_norm == 1:
        residual = real_residual.e2
        res_name = 'main_rez_e2.png'
    elif residual_norm == 2:
        residual = real_residual.e3
        res_name = 'main_rez_e3.png'
    return residual, res_name


def get_func(h_dots, h_dots_scale, residual, file, num):
    fp, residuals, rank, sv, rcond = np.polyfit(h_dots, residual, 1, full=True)
    func_1 = sp.poly1d(fp)
    file.write('=====================e' + str(num + 1) + '=======================')
    file.write('\n' + 'function_(1 / sqrt(dots)): ' + str(func_1) + '\n')
    fp, residuals, rank, sv, rcond = np.polyfit(h_dots_scale, residual, 1, full=True)
    func_2 = sp.poly1d(fp)
    file.write('\n' + 'function_(scale): ' + str(func_2) + '\n')
    return func_1, func_2


r = residual()
h_dots = []
h_dots_scale = []

# main calculation
for i in range(3):
    print(i)
    f.write(str(i) + ' scale: ' + str(scale[i]) + ' ')
    start_time = time.time()
    tmp = test.make_data(i)
    f.write('dots: ' + str(tmp[-1]) + ' step: '
            + str("{:10.4e}".format(1 / np.sqrt(tmp[1]))) + ' ')
    r.e1.append(np.log(tmp[0]))
    r.e2.append(np.log(tmp[1]))
    r.e3.append(np.log(tmp[2]))
    h_dots_scale.append(np.log(scale[i]))
    h_dots.append(np.log(1 / np.sqrt(tmp[-1])))
    f.write('time: ' + "%.4f" % (time.time() - start_time) + '\n')

# show results
for i in range(3):
    residual, name = switch_residual_norm(i, r)
    plt.clf()
    func_1, func_2 = get_func(h_dots, h_dots_scale, residual, f, i)

    plt.scatter(h_dots, residual, c='b', label=r'$\frac{1}{\sqrt{dots}}$')
    plt.scatter(h_dots_scale, residual, c='g', label=r'$\frac{1}{scale}$')
    plt.plot(h_dots, list(map(lambda t: t * func_1[1] + func_1[0], h_dots)), '--', c='b',
             label=func_1)
    plt.plot(h_dots_scale, list(map(lambda t: t * func_2[1] + func_2[0], h_dots_scale)), '--', c='g',
             label=func_2)
    plt.legend()
    plt.xlabel(r'$\ln h_{dots}$')
    plt.ylabel(r'$\ln r$')
    plt.grid(True)
    plt.savefig('../rez/' + name, dpi=1000)

f.close()
