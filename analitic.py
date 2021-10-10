def get_solve(tau, N, func, DOTS, l):
    data = []
    for n in range(N):
        t = n * tau
        tmp = []
        for p in DOTS:
            tmp.append(func(p, t, l))
        data.append(tmp)
    return data

