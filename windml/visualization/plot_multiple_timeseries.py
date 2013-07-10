from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

def plot_multiple_timeseries(windpark, show = True):
    """Plot multiple power series of some mills.

    Parameters
    ----------

    windpark : Windpark
               A given windpark to plot power series.
    """

    plt.clf()

    X = np.array(windpark.get_powermatrix())
    number_turbines = len(X[0])
    number_measurements = len(X)

    length = 100
    X = X[:length]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

    xs = range(1,number_measurements)
    verts = []
    zs = range(0,number_turbines)

    for z in zs:
        ys = X[:,z]
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))

    poly = PolyCollection(verts, facecolors = [cc('r'), cc('g'), cc('b'), cc('y'),cc('r'), cc('g'), cc('b')])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlabel('Time')
    ax.set_xlim3d(0, length)
    ax.set_ylabel('Windmill')
    ax.set_ylim3d(-1, number_turbines)
    ax.set_zlabel('Power')
    ax.set_zlim3d(0,30.)

    plt.title("Time Series Comparison")

    if(show):
        plt.show()

