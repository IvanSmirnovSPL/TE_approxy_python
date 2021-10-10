import iter_
import numpy as np
import point
#from mpi4py import MPI



#calculate new slice of time
def make_new_d(l, tau, TREE_OF_POINTS, prev_d, coord_to_name, doc):

    #comm = MPI.COMM_WORLD
    #rank = comm.Get_rank()
    #size = comm.Get_size()

    d = {}
    doc.write('----------------level----------------------' + '\n')
    for j in range(2):
        perem = 'x' if j == 0 else 'y'
        doc.write(perem + '\n')

        #comm.Barrier()

        for p in TREE_OF_POINTS.dots:
            inter_coord = determine_coord(p, l[j], tau, j, doc)
            coef, frame, bounds = interpolate_polinom(prev_d, TREE_OF_POINTS,
                                          inter_coord, coord_to_name, doc)
            new_value = generate_new_value(inter_coord, coef, frame,
                                           doc, bounds)
            d[coord_to_name(p)] = new_value

        #comm.Barrier()

        prev_d = d.copy()
    doc.write('-------------------------------------------' + '\n')
    return d


#frame of reference structure
class FoR:
    def __init__(self, x_0, y_0, x_del, y_del):
        self.trans = point.Point(x_0, y_0)
        self.comp = point.Point(x_del, y_del)

#make argument in [-T /2, T/ 2] bounds
def check(q):
    T = 2
    q = q - (abs(q) // T) * T
    if abs(q) <= 1:
        rez = q
    else:
        if q > 0:
            rez = q - T
        else:
            rez = q + T
    return rez


def determine_coord(p, l, tau, j, doc):
    delta = l * (tau)
    if j == 0:
        q = p.x - delta
        tmp = check(q)
        inter_coord = point.Point(tmp, p.y)
    else:
        q = p.y - delta
        tmp = check(q)
        inter_coord = point.Point(p.x, tmp)

    doc.write('========================================================='
              + '==================================' + '\n')
    doc.write('point: ['+ str('%.4f'%(p.x)) +','+ str('%.4f'%(p.y))
              + '] inter_coord: [' + str( '%.4f'%(inter_coord.x)) + ', '
              + str('%.4f'%(inter_coord.y))  + ']' + '\n')

    return inter_coord

#make local frame
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

#translation coordinates in local frame
def normalization(points):
    frame = make_frame(points)
    ksi = []
    eta = []
    for i in range(len(points)):
        ksi.append((points[i].x - frame.trans.x) / frame.comp.x)
        eta.append((points[i].y - frame.trans.y) / frame.comp.y)
    return ksi, eta, frame

#matrix for system of interpolate coef
def make_matrix(prev_d, coord_to_name, points, ksi, eta):
    A = []
    f = []
    for i in range(len(points)):
        x = ksi[i]
        y = eta[i]
        if len(points) == 6:
            tmp = [x**2, x * y, y**2, x, y, 1]
        elif len(points) == 3:
            tmp = [x, y, 1]
        else:
            print('ERROR IN LENGTH OF POINTS')
        A.append(tmp)
        f.append(prev_d[coord_to_name(points[i])])
    A = np.array(A)
    f = np.array(f)
    return A, f


def interpolate_polinom(prev_d, TREE_OF_POINTS, inter_coord, coord_to_name, doc):
    points, dist = TREE_OF_POINTS.search(inter_coord, 10)
    variants = iter_.generate_variants(points, 6)
    for u in variants:
        u = list(u)
        ksi, eta, frame = normalization(u)
        A, f = make_matrix(prev_d, coord_to_name, u, ksi, eta)
        if abs(np.linalg.det(A)) > 0.01:
            data = u
            break


    doc.write('points: ')
    for q in data:
         doc.write('[' + str('%.4f'%(q.x)) +  ', ' +str( '%4.f'%(q.y)) + '] ')
    doc.write('\n')
    doc.write('value: ')
    for i in range(len(f)):
        doc.write(str('%.4f'%(f[i])) + ' ')
    doc.write('\n')


    #coef = np.linalg.solve(A, f)
    coef = np.linalg.lstsq(A,f, rcond = - 1)[0]
    return coef, frame, [min(f), max(f)]
    
def generate_new_value(inter_coord, coef, frame, doc, bounds):
    x = (inter_coord.x - frame.trans.x) / frame.comp.x
    y = (inter_coord.y - frame.trans.y) / frame.comp.y
    if len(coef) == 6:
        rez = coef[0] * x**2 + coef[1] * x * y + coef[2] * y**2\
              + coef[3] * x + coef[4] * y + coef[5]
    elif len(coef) == 3:
        rez = coef[0] * x + coef[1] * y + coef[2]
    else:
        print("ERROR IN LENGTH OF COEF")
    if rez > bounds[1] or rez < bounds[0]:
        rez = bounds[1] if rez > bounds[0] else bounds[0]
    doc.write('new_value: ' + str( "%.4f"%(rez)))


    doc.write('=================================================='
             + '=========================================')

    return rez
