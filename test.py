import analitic
import make_points
import error
import tree
import calculate
import matplotlib.pyplot as plt
import sys
import numpy as np
from progress.bar import IncrementalBar

if len(sys.argv) > 1:
    name = sys.argv[1]
    num = 0
elif len(sys.argv) >2:
    name = sys.argv[1]
    num = int(sys.argv[2])
else:
    name = 'square.msh'
    num = 0



# function of initial conditions
def func(p, t = 0, l = [0, 0]):
    # r = np.sqrt((p.x) ** 2 + (p.y) ** 2)
    return (np.cos(abs(p.x - t * l[0]) * np.pi * 0.5)) ** 2


# make dictionary name from coordinate
def coord_to_name(coord):
    name = str(coord.x) + ' ' + str(coord.y)
    return name


# make z coordinate from tree
def make_z(TREE, d):
    z = []
    for point in TREE.dots:
        z.append(d[coord_to_name(point)])
    return z


# structure of points
a = make_points.POINTS(name)
# POINTS is needed only for building tree
# DOTS is list of points in point.Point format
DOTS = a.dots
POINTS = a.points
print('POINTS: ', len(DOTS))
TREE_OF_POINTS = tree.TREE(POINTS, DOTS)

# make dictionary of points and determine their relation to bounds
d = {}
for p in DOTS:
    d[coord_to_name(p)] = func(p)

# calculate
l_x = 8
l_y = -3
l = [l_x, l_y]
x = [p.x for p in DOTS]
y = [p.y for p in DOTS]
z = make_z(TREE_OF_POINTS, d)

N = 51  # time nodes
tau = 1 / (N - 1)

analitic_solve = analitic.get_solve(tau, N, func, DOTS, l)

doc = open('./rez/doc.txt', 'w')
err_f = open('./rez/err_' + str(num) + '.txt', 'w')
err_f.write('time e1 e2 e3' + '\n')
bar = IncrementalBar('ChargingBar', max=N)
err = error.ERROR()
for n in range(1, N):
    # if n % 10 == 0:
    if True:
        # plt.axis([-1.2 , 1.2,  -0.2, 1.2])
        plt.scatter(x, z, label='function in '
                                + str('%.4f' % ((n - 1) / (N - 1))) + ' seconds')
        plt.scatter(x, analitic_solve[n - 1], label='analitic in '
                                + str('%.4f' % ((n - 1) / (N - 1))) + ' seconds')
        err.calc_error(z, analitic_solve[n - 1])
        err_f.write(str("{:10.4e}".format((n - 1) / (N - 1))) + ' '
                    + str("{:10.4e}".format(err.e1[-1])) + ' '
                    + str("{:10.4e}".format(err.e2[-1])) + ' '
                    + str("{:10.4e}".format(err.e3[-1])) + '\n')
        plt.xlabel('x')
        plt.ylabel('function')
        plt.grid(True)
        plt.legend()
        #plt.pause(1)
        plt.savefig('./rez/'+'x_'+str(n//10)+'.png')
        plt.close()
    d = calculate.make_new_d(l, tau, TREE_OF_POINTS, d, coord_to_name, doc)
    z = make_z(TREE_OF_POINTS, d)
    bar.next()
    err.calc_error(z, analitic_solve[-1])
err_f.write(str("{:10.4e}".format((N - 1 ) / (N - 1))) + ' '
            + str("{:10.4e}".format(err.e1[-1])) + ' '
            + str("{:10.4e}".format(err.e2[-1])) + ' '
            + str("{:10.4e}".format(err.e3[-1])) + '\n')
err.make_max()
err_f.write('\n' + 'max_errors: '
            + str("{:10.4e}".format(err.e1_max)) + ' '
            + str("{:10.4e}".format(err.e2_max)) + ' '
            + str("{:10.4e}".format(err.e3_max)) + '\n')

#plt.show()
doc.close()
err_f.close()
bar.finish()
