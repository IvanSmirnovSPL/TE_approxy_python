import test
import scipy as sp
import numpy as np
import time

f = open('../rez/main_rez.txt', 'w')

scale = [0.2, 0.1, 0.05, 0.025, 0.0125]

r = []
h = []
for i in range(2):
    print(i)
    f.write(str(i) + ' scale: ' + str(scale[i]) + ' ')
    start_time = time.time()
    tmp = test.make_data(i)
    f.write('dots: ' + str(tmp[1]) + ' step: '
            + str("{:10.4e}".format(1 / np.sqrt(tmp[1]))) + ' ')
    r.append(np.log(tmp[0]))
    h.append(np.log(1 / np.sqrt(tmp[1])))
    f.write('time: ' + str("{:10.4e}".format(time.time() - start_time)) + '\n')



fp, residuals, rank, sv, rcond = sp.polyfit(h, r, 1, full=True)
func = sp.poly1d(fp)
f.write('\n' + 'function: ' + str(func) + '\n')
f.close()
