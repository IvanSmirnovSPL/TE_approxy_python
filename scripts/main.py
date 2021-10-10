import test
import scipy as sp
import numpy as np
import time
import matplotlib.pyplot as plt

f = open('../rez/main_rez.txt', 'w')

scale = [0.2, 0.1, 0.05, 0.025, 0.0125]

r = []
h = []
hh = []
h_d = []
for i in range(5):
    print(i)
    f.write(str(i) + ' scale: ' + str(scale[i]) + ' ')
    start_time = time.time()
    tmp = test.make_data(i)
    f.write('dots: ' + str(tmp[1]) + ' step: '
            + str("{:10.4e}".format(1 / np.sqrt(tmp[1]))) + ' ')
    r.append(np.log(tmp[0]))
    h_d.append(np.log(1 / tmp[1]))
    hh.append(np.log(scale[i]))
    h.append(np.log(1 / np.sqrt(tmp[1])))
    f.write('time: ' + "%.4f"%(time.time() - start_time) + '\n')



fp, residuals, rank, sv, rcond = sp.polyfit(h, r, 1, full=True)
func_1 = sp.poly1d(fp)
f.write('\n' + 'function_(1/sqrt(dots)): ' + str(func_1) + '\n')
fp, residuals, rank, sv, rcond = sp.polyfit(hh, r, 1, full=True)
func_2 = sp.poly1d(fp)
f.write('\n' + 'function_(scale): ' + str(func_2) + '\n')
fp, residuals, rank, sv, rcond = sp.polyfit(h_d, r, 1, full=True)
func_3 = sp.poly1d(fp)
f.write('\n' + 'function_(1 / dots): ' + str(func_3) + '\n')
f.close()
plt.scatter(h, r, c='r', label=r'$\frac{1}{\sqrt{dots}}$')
plt.scatter(hh, r, c='g',label=r'$\frac{1}{scale}$')
plt.scatter(h_d, r, c='b',label=r'$\frac{1}{dots}$')
plt.plot(h, list(map(lambda t: t * func_1[1] + func_1[0], h)),'--', c='r',
         label=func_1)
plt.plot(hh, list(map(lambda t: t * func_2[1] + func_2[0], hh)),'--', c='g',
         label=func_2)
plt.plot(h_d, list(map(lambda t: t * func_3[1] + func_3[0], h_d)),'--', c='b',
         label=func_3)
plt.legend()
plt.grid(True)
plt.savefig('../rez/main_rez.png')