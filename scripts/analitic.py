import point
import numpy as np

def check(q):
    T = 2
    q = q - np.sign(q) * (abs(q) // T) * T
    if abs(q) <= 1:
        rez = q
    else:
        if q > 0:
            rez = q - T
        else:
            rez = q + T
    return rez


def get_solve(tau, N, func, DOTS, l):
    w = open('../rez/analitic.txt', 'w')
    data = []
    for n in range(N):
        t = n * tau
        tmp = []
        for p in DOTS:
            x = p.x - l[0] * t
            y = p.y - l[1] * t
            x_ = check(x)
            y_ = check(y)
            #w.write('n: ' + str(n) + ' x: ' + str("%.4f" % x)
            #        + ' x_: ' + str("%.4f" % x_) + ' y: '
            #        + str("%.4f" % y) + ' y_: ' + str("%.4f" % y_) + '\n')
            tmp.append(func(point.Point(x_, y_)) )
        data.append(tmp)
    w.close()
    return data

