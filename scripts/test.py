import initial
import rezult
import calculate


def make_data(num):
    name = '../exp/mesh_' + str(num) + '.msh'
    ic = initial.IC([8, -3], name)
    analitic_solve = ic.a_data
    d = ic.i_data
    z = ic.make_z(d)
    # calculate
    rez = rezult.REZULT(num)
    for n in range(1, ic.N):
        rez.draw(ic.x, z, analitic_solve[n - 1], n - 1, ic.N)
        rez.upgrade_error(n, ic.N, z, analitic_solve[n - 1])
        d = calculate.make_new_d(ic.l, ic.tau, ic.TREE_OF_POINTS,
                             d, ic.coord_to_name, rez.doc)
        z = ic.make_z(d)

    rez.draw(ic.x, z, analitic_solve[-1], ic.N - 1, ic.N)
    rez.upgrade_error(ic.N, ic.N, z, analitic_solve[-1])
    rez.finish()
    return rez.err.e1[-1], len(ic.DOTS)
