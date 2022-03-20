from pyevtk.hl import pointsToVTK
import numpy as np


def export_data(points, z,  name):
    pointsToVTK(str(name),
                np.array([p.x for p in points]),
                np.array([p.y for p in points]),
                np.array(z.y_cart),
                data={'d1x': np.array([p.d1x for p in points]),
                      'd2x': np.array([p.d2x for p in points]),
                      'd1y': np.array([p.d1x for p in points]),
                      'd2y': np.array([p.d2x for p in points]),
                      'ratio_x': np.array([p.ratio_x for p in points]),
                      'ratio_y': np.array([p.ratio_y for p in points])})
