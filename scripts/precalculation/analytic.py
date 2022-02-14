from scripts.utils import point
from scripts.utils.point import FILE
import numpy as np
from pathlib import Path


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


def get_solve(tau, N, func, DOTS, lamb, PATHS, num):
    w = FILE(Path(PATHS.files_path, 'analytic' + str(num) +'.txt'))
    data = []
    for n in range(N):
        if n > 0:
            w.write2file('Slice №' + str(n) + ' _x_ ' '\n')
        carta = point.CARTA()
        t = n * tau
        t_prev = t - tau if n > 1 else 0
        tmp = []
        for p in DOTS:
            x = p.x - lamb[0] * t
            x_ = check(x)
            y = p.y - lamb[1] * t_prev
            y_ = check(y)
            tmp.append(func(point.Point(x_, y_)))
            if n > 0:
                w.write2file('[' + str("%.4f" % p.x) + ', '
                         + str("%.4f" % p.y) + '] -> ' +
                         str(func(point.Point(x_, y_))) + '\n')
        carta.x_cart = tmp
        tmp = []
        if n > 0:
            w.write2file('Slice №' + str(n) + ' _y_ ' '\n')
        for p in DOTS:
            x = p.x - lamb[0] * t
            x_ = check(x)
            y = p.y - lamb[1] * t
            y_ = check(y)
            tmp.append(func(point.Point(x_, y_)))
            if n > 0:
                w.write2file('[' + str("%.4f" % p.x) + ', '
                         + str("%.4f" % p.y) + '] -> '
                         + str(func(point.Point(x_, y_))) + '\n')
        carta.y_cart = tmp
        data.append(carta)


    return data
