from precalculation import initial
import calculate
from results_during_calculation import vizual, rezult
from utils.point import slice_of_time, CARTA
from pathlib import Path
from utils.point import FILE
from results_during_calculation.make_vtk import export_data
from tqdm import tqdm


def calculate_z(SoT, ic):
    z = CARTA()
    z.x_cart = ic.make_z(SoT.x_cart)
    z.y_cart = ic.make_z(SoT.y_cart)
    return z


def calculate_z0(ic):
    z = CARTA()
    z.x_cart = ic.a_data[0].x_cart
    z.y_cart = ic.a_data[0].y_cart
    return z


def make_data(num, PATHS):
    doc = FILE(Path(PATHS.grid_file_path[num], 'doc' + str(num) + '.txt'))
    # der = FILE(Path(PATHS.files_path, 'derivative' + str(num) + '.txt'))
    name = PATHS.meshes_path[num]
    ic = initial.IC(name, PATHS, num)
    analytic_solution = ic.a_data
    SoT = slice_of_time()
    SoT.x_cart = ic.i_data
    SoT.y_cart = ic.i_data
    z = calculate_z0(ic)

    vizual.make_model(ic.x, ic.y, z.y_cart, analytic_solution[0].y_cart,
                      Path(PATHS.grid_pic_path[num], 'start' + str(num) + '.png'))

    # calculate
    rez = rezult.REZULT(num, PATHS)
    for n in tqdm(range(1, ic.N)):
        rez.draw(ic.x, ic.y, z.y_cart, analytic_solution[n - 1].y_cart, n - 1, ic.N)

        SoT, points_information = calculate.make_new_d(ic.lamb, ic.tau, ic.TREE_OF_POINTS,
                                   SoT.y_cart, ic.coord_to_name, ic.dots_for_calc, doc, n, rez)
        z = calculate_z(SoT, ic)
        rez.upgrade_error(n, ic.N,
                          Path(PATHS.grid_file_path[num], 'analytic' + str(num) + '.txt'),
                          Path(PATHS.grid_file_path[num], 'doc' + str(num) + '.txt'))
        rez.upgrade_der(n, ic.N)
        export_data(points_information.y, z, Path(PATHS.grid_vtk_path[num], f'state_{n}'))

    vizual.make_model(ic.x, ic.y, z.y_cart, analytic_solution[-1].y_cart,
                      Path(PATHS.grid_pic_path[num], 'finish' + str(num) + '.png'))

    rez.draw(ic.x, ic.y, z.y_cart, analytic_solution[-1].y_cart, ic.N - 1, ic.N)

    rez.upgrade_error(ic.N - 1, ic.N,
                      Path(PATHS.grid_file_path[num], 'analytic' + str(num) + '.txt'),
                      Path(PATHS.grid_file_path[num], 'doc' + str(num) + '.txt'))



    return rez.err.e1.x[-1], rez.err.e2.x[-1], rez.err.e3.x[-1], rez.err.e1.y[-1], rez.err.e2.y[-1], rez.err.e3.y[
        -1], len(ic.DOTS)
