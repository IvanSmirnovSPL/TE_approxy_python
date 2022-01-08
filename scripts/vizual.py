from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm


def make_model(x, y, z, z_1, name):
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_trisurf(x, y, z_1, cmap=cm.jet,
                           alpha=0.5, linewidth=0.1)
    ax.scatter(x, y, z, c='k', s=10)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig('../rez/pictures/'+name+'.png')
    plt.close()
