import initial
import rezult
import calculate
import vizual
import point


def make_data(num):
    name = '../exp/mesh_' + str(num) + '.msh'
    ic = initial.IC([-1, 5], name)
    analytic_solve = ic.a_data
    SoT = point.slice_of_time()
    # SoT.update(0, ic.i_data)
    # SoT.update(1, ic.i_data)
    d = ic.i_data
    z = ic.make_z(d)
    # z = point.z_cart(SoT, ic)
    vizual.make_model(ic.x, ic.y, z, analytic_solve[0].y_cart, 'start' + str(num))
    # calculate
    rez = rezult.REZULT(num)
    for n in range(1, ic.N):
        rez.draw(ic.x, ic.y, z, analytic_solve[n - 1].y_cart, n - 1, ic.N)

        # rez.upgrade_error(n, ic.N, z.x, analytic_solve[n - 1].x_cart, 0)
        rez.upgrade_error(n, ic.N, z, analytic_solve[n - 1].y_cart, 1)

        d = calculate.make_new_d(ic.l, ic.tau, ic.TREE_OF_POINTS,
                                 d, ic.coord_to_name, rez.doc)
        z = ic.make_z(d)
        # z = point.z_cart(SoT, ic)
    vizual.make_model(ic.x, ic.y, z, analytic_solve[-1].y_cart, 'finish' + str(num))
    rez.draw(ic.x, ic.y, z, analytic_solve[-1].y_cart, ic.N - 1, ic.N)

    # rez.upgrade_error(ic.N, ic.N, z.x, analytic_solve[-1].x_cart, 0)
    rez.upgrade_error(ic.N, ic.N, z, analytic_solve[-1].y_cart, 1)

    rez.finish()
    return rez.err.e1[-1], rez.err.e2[-1], rez.err.e3[-1], len(ic.DOTS)
