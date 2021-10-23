import test
import scipy as sp
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import shutil

shutil.rmtree('../rez', ignore_errors=True)
os.mkdir('../rez')
os.mkdir('../rez/pictures')






f = open('../rez/main_rez.txt', 'w')
scale = [0.2, 0.1, 0.05, 0.025, 0.0125]

r = []
h = []
hh = []
for i in range(2):
    print(i)
    f.write(str(i) + ' scale: ' + str(scale[i]) + ' ')
    start_time = time.time()
    tmp = test.make_data(i)
    f.write('dots: ' + str(tmp[1]) + ' step: '
            + str("{:10.4e}".format(1 / np.sqrt(tmp[1]))) + ' ')
    r.append(np.log(tmp[0]))
    hh.append(np.log(scale[i]))
    h.append(np.log(1 / np.sqrt(tmp[1])))
    f.write('time: ' + "%.4f"%(time.time() - start_time) + '\n')




fp, residuals, rank, sv, rcond = np.polyfit(h, r, 1, full=True)
func_1 = sp.poly1d(fp)

fp, residuals, rank, sv, rcond = np.polyfit(hh, r, 1, full=True)
func_2 = sp.poly1d(fp)

f.write('\n' + 'function_(scale): ' + str(func_2) + '\n')

f.write('\n' + 'function_(1 / dots): ' + str(func_1) + '\n')
f.close()
plt.scatter(h, r, c='b', label=r'$\frac{1}{\sqrt{dots}}$')
plt.scatter(hh, r, c='g', label=r'$\frac{1}{scale}$')
plt.plot(h, list(map(lambda t: t * func_1[1] + func_1[0], h)), '--', c='b',
         label=func_1)
plt.plot(hh, list(map(lambda t: t * func_2[1] + func_2[0], hh)), '--', c='g',
         label=func_2)
plt.legend()
plt.xlabel(r'$\ln h$')
plt.ylabel(r'$\ln r$')
plt.grid(True)
plt.savefig('../rez/main_rez.png', dpi=1000)