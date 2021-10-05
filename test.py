import make_points
import tree
import point
import calculate
import matplotlib.pyplot as plt
import sys
import numpy as np
import time
import matplotlib.animation as animation
from progress.bar import IncrementalBar


if len(sys.argv) > 1:
    name = sys.argv[1]
else:
    name = 'square.msh'

#function of initial conditions
def func(p):
    r = np.sqrt((p.x)**2 + (p.y)**2)
    return (np.cos(abs(p.x) * np.pi * 0.5))**2

#make dictionary name from coordinate
def coord_to_name(coord):
    name = str(coord.x) + ' ' + str(coord.y)
    return name


#make z coordinate from tree
def make_z(TREE, d):
    z = []
    for point in TREE.dots:
        z.append(d[coord_to_name(point)])
    return z
    
#structure of points 
a = make_points.POINTS(name)
#POINTS is needed only for building tree
#DOTS is list of points in point.Point format
DOTS = a.dots
POINTS = a.points
print('POINTS: ', len(DOTS))
TREE_OF_POINTS = tree.TREE(POINTS, DOTS)

#make dictionary of points and determine their relation to bounds
d = {}
for p in DOTS:
    d[coord_to_name(p)] = func(p)

#calculate
l_x = 8
l_y = -3
l = [l_x , l_y]
x = [p.x for p in DOTS]
y = [p.y for p in DOTS]
z = make_z(TREE_OF_POINTS, d)

N = 51#time nodes
tau = 1 / (N - 1)
doc = open('doc.txt', 'w')

bar = IncrementalBar('ChargingBar', max = N)

for n in range(N):
    #if n % 10 == 0: 
    if True:
        #plt.axis([-1.2 , 1.2,  -0.2, 1.2])
        plt.scatter(x, z, label = 'function in '
                                  + str('%.4f'%(n/(N - 1))) + ' seconds')
        plt.xlabel('x')
        plt.ylabel('function')
        plt.grid(True)
        #plt.legend()
        plt.pause(0.7)
        #plt.savefig('x_cont_both_dim_2_'+str(n//10)+'.png')
        #plt.close()
    d = calculate.make_new_d(l, tau, TREE_OF_POINTS, d, coord_to_name, doc)
    z = make_z(TREE_OF_POINTS, d)
    bar.next()

plt.show()
doc.close()
bar.finish()





