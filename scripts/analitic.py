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
    w = open('../rez/analytic.txt', 'w')
    data = []
    for n in range(N):
        SoT_a = point.slice_of_time()
        carta = point.CARTA()
        t = n * tau
        tmp = []
        q = 0
        for p in DOTS:
            x = p.x - l[0] * t
            x_ = check(x)
            y = p.y - l[1] * (t - tau)
            y_ = check(y)
            #if q < 26:
            #    print(n, 'x', p.x, x_, p.y, y_, func(point.Point(x_, y_)))
            #    q += 1
            tmp.append(func(point.Point(x_, y_)))
        carta.x_cart = tmp
        tmp = []
        q = 0
        for p in DOTS:
            x = p.x - l[0] * t
            x_ = check(x)
            y = p.y - l[1] * t
            y_ = check(y)
            #if q < 26:
            #    print(n, 'y', p.x, x_, p.y, y_, func(point.Point(x_, y_)))
            #    q += 1
            tmp.append(func(point.Point(x_, y_)))
        carta.y_cart = tmp
        data.append(carta)
        #for g in range(1, n + 1):
        #    res = [abs(data[g].x_cart[q] - data[g - 1].y_cart[q]) for q in range(len(data[0].x_cart))]
        #    if max(res) > 1e-14:
        #        print(max(res))
        #    for q in range(len(res)):
        #        if res[q] > 0:
        #            print(res[q], q)

    w.close()
    return data
