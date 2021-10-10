
from sklearn.neighbors import KDTree
import point

class TREE:

    def __init__(self, points, dots, leaf_size = 2):
        self.points = points
        #dots = points in Point format
        self.dots = dots
        self.tree = KDTree(points, leaf_size, metric = 'euclidean')

    # determine the k - nearest
    def search(self, point, k):
        dist, ind = self.tree.query([[point.x, point.y]], k)
        ind = ind[0]
        rez_points = [self.dots[ind[i]] for i in range(len(ind))]
        return rez_points, dist



