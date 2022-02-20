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
                      'smth': np.array([abs(p.d2x / p.d1x) if p.d1x != 0 else -1.0 for p in points])})
