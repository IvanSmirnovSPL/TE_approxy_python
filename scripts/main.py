import make_solutions
from utils import preliminary_preparation
from utils.analyse_show_results import Showing_results

figures = ['fig_1', 'fig_2', 'fig_3', 'fig_4', 'wave', 'cone', 'cube']

for figure in figures[1:2]:

    # generate paths and result directories
    PATHS = preliminary_preparation.PATHS(figure)
    scale = preliminary_preparation.scale  # scales of calculating grids
    grids_num = preliminary_preparation.grids_num  # number of calculating grids
    results = Showing_results(scale, PATHS)

    # main calculation
    for i in range(0, 2):
        results.new_grid(i)
        tmp = make_solutions.make_data(i, PATHS)
        results.add_grid(tmp)

    results.show_main_graphics()
