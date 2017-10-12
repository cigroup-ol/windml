"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np


def plot_multiple_timeseries(windpark, show=True):
    """Plot multiple power series of some turbines.

    Parameters
    ----------

    windpark : Windpark
               A given windpark to plot power series.
    """

    X = np.array(windpark.get_powermatrix())
    number_turbines = len(X[0])
    number_measurements = len(X)

    length = 100
    X = X[:length]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

    def cc(arg):
        return colorConverter.to_rgba(arg, alpha=0.6)
    xs = range(1, number_measurements)
    verts = []
    zs = range(0, number_turbines)

    for z in zs:
        ys = X[:, z]
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))

    poly = PolyCollection(verts,
                          facecolors=[cc('r'), cc('g'), cc('b'),
                                      cc('y'), cc('r'), cc('g'), cc('b')])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlabel('Time')
    ax.set_xlim3d(0, length)
    ax.set_ylabel('Turbine')
    ax.set_ylim3d(-1, number_turbines)
    ax.set_zlabel('Power')
    ax.set_zlim3d(0, 30.)

    plt.title("Time Series Comparison")

    if show:
        plt.show()
