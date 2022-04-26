from precalculation import iter_
import numpy as np
from utils import point
from utils.point import Point
from utils.point import point_with_data


# calculate new slice of time
def make_new_d(l, tau, TREE_OF_POINTS, prev_d, coord_to_name, DOTS, doc, n, rez):
    rez.new_der_slice()
    SoT = point.slice_of_time()
    d = {}
    points_information = Point()
    points_information.x = []
    points_information.y = []
    for j in range(2):
        perem = '_x_' if j == 0 else '_y_'
        if True:
            doc.write2file('Slice №' + str(n) + ' _x_ ' '\n')
        for p in DOTS:
            inter_coord = determine_coord(p, l[j], tau, j)
            coef, frame, bounds = interpolate_polinom(prev_d, TREE_OF_POINTS,
                                                      inter_coord, coord_to_name, 2)
            x, y, coef, bounds, inf_point = check_der(inter_coord, coef, frame, bounds,
                                                      n, rez, p, coord_to_name,
                                                      prev_d, TREE_OF_POINTS, l)
            new_value = generate_new_value(x, y, coef, bounds)
            if j == 0:
                points_information.x.append(inf_point)
            else:
                points_information.y.append(inf_point)
            d[coord_to_name(p)] = new_value
            if True:
                doc.write2file('[' + str("%.4f" % p.x) + ', '
                               + str("%.4f" % p.y) + '] -> ' +
                               str(new_value) + '\n')
        if j == 0:
            SoT.x_cart = d
        else:
            SoT.y_cart = d
        prev_d = d.copy()
    return SoT, points_information


# frame of reference structure
class FoR:
    def __init__(self, x_0, y_0, x_del, y_del):
        self.trans = point.Point(x_0, y_0)
        self.comp = point.Point(x_del, y_del)


# make argument in [-T /2, T/ 2] bounds
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


def determine_coord(p, l, tau, j):
    delta = l * (tau)
    if j == 0:
        q = p.x - delta
        tmp = check(q)
        inter_coord = point.Point(tmp, p.y)
    else:
        q = p.y - delta
        tmp = check(q)
        inter_coord = point.Point(p.x, tmp)

    return inter_coord


# make local frame


def make_frame(points):
    x_ = [points[i].x for i in range(len(points))]
    y_ = [points[i].y for i in range(len(points))]
    x_lim = [min(x_), max(x_)]
    y_lim = [min(y_), max(y_)]
    x_del = x_lim[1] - x_lim[0] if x_lim[1] - x_lim[0] != 0 else 0.0001
    y_del = y_lim[1] - y_lim[0] if y_lim[1] - y_lim[0] != 0 else 0.0001
    x_0 = x_[0]
    y_0 = y_[0]
    frame = FoR(x_0, y_0, x_del, y_del)
    return frame


# translation coordinates in local frame


def normalization(points):
    frame = make_frame(points)
    ksi = []
    eta = []
    for i in range(len(points)):
        ksi.append((points[i].x - frame.trans.x) / frame.comp.x)
        eta.append((points[i].y - frame.trans.y) / frame.comp.y)
    return ksi, eta, frame


# matrix for system of interpolate coef
def make_matrix(prev_d, coord_to_name, points, ksi, eta):
    A = []
    f = []
    for i in range(len(points)):
        x = ksi[i]
        y = eta[i]
        if len(points) == 6:
            tmp = [x ** 2, x * y, y ** 2, x, y, 1]
        elif len(points) == 10:
            tmp = [x ** 3, y ** 3, x ** 2 * y, y ** 2 * x, x ** 2, y ** 2, x * y, x, y, 1]
        elif len(points) == 3:
            tmp = [x, y, 1]
        else:
            print('ERROR IN LENGTH OF POINTS')
        A.append(tmp)
        f.append(prev_d[coord_to_name(points[i])])
    A = np.array(A)
    f = np.array(f)
    return A, f


def interpolate_polinom(prev_d, TREE_OF_POINTS, inter_coord, coord_to_name, order):
    points, dist = TREE_OF_POINTS.search(inter_coord, 5 * order)
    variants = iter_.generate_variants(points, 3 * order)
    for u in variants:
        ksi, eta, frame = normalization(list(u))
        A, f = make_matrix(prev_d, coord_to_name, u, ksi, eta)
        if abs(np.linalg.det(A)) > 0.01:
            data = u
            break

    # coef = np.linalg.solve(A, f)
    coef = np.linalg.lstsq(A, f, rcond=- 1)[0]
    return coef, frame, [min(f), max(f)]


def generate_new_value(x, y, coef, bounds):
    if len(coef) == 6:
        rez = coef[0] * x ** 2 + coef[1] * x * y + coef[2] * y ** 2 \
              + coef[3] * x + coef[4] * y + coef[5]
    elif len(coef) == 10:
        rez = coef[0] * x ** 3 + coef[1] * y ** 3 + coef[2] * x ** 2 * y \
              + coef[3] * y ** 2 * x + coef[4] * x ** 2 + coef[5] * y ** 2 \
              + coef[6] * x * y + coef[7] * x * coef[8] * y + coef[9]
    elif len(coef) == 3:
        rez = coef[0] * x + coef[1] * y + coef[2]
    else:
        print("ERROR IN LENGTH OF COEF")
    if rez > bounds[1] or rez < bounds[0]:
        rez = bounds[1] if rez > bounds[0] else bounds[0]

    return rez


def check_rough(inf, n, q):
    if n < 7:
        second_der = abs(inf.d2x) > 1e-4 or abs(inf.d2y) > 1e-4
        ratio = (0.5 + n / 6 < abs(inf.ratio_x) < 15 - 5 / 6) or (
                (0.5 + n / 6) / q < abs(inf.ratio_y) < (15 - 5 / 6) / q)
        return second_der or ratio
    return False


def check_der(inter_coord, coef, frame, bounds, n, result,
              p, coord_to_name, prev_d, TREE_OF_POINTS, l):
    x = (inter_coord.x - frame.trans.x) / frame.comp.x
    y = (inter_coord.y - frame.trans.y) / frame.comp.y
    result.update_slice(coef[3], 2 * coef[0], coef[4], 2 * coef[2])

    inf_point = point_with_data(p.x, p.y,
                                2 * coef[0] * x + coef[1] * y + coef[3],
                                2 * coef[2] * y + coef[1] * x + coef[4],
                                2 * coef[0], 2 * coef[2])
    inf_point.ratio_x = abs(inf_point.d2x / inf_point.d1x) if inf_point.d1x != 0 else -1.
    inf_point.ratio_y = abs(inf_point.d2y / inf_point.d1y) if inf_point.d1y != 0 else -1.

    #if check_rough(inf_point, n, abs(l[1] / l[0]) if l[0] != 0 else 1):
    if False:
        coef, frame, bounds = interpolate_polinom(prev_d, TREE_OF_POINTS,
                                                  inter_coord, coord_to_name, 1)
        x = (inter_coord.x - frame.trans.x) / frame.comp.x
        y = (inter_coord.y - frame.trans.y) / frame.comp.y

    return x, y, coef, bounds, inf_point
