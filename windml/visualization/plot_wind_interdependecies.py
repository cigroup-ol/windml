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
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import time

def plot_joined(turbine_a, turbine_b):

    speeds_a = turbine_a.get_measurements()['speed']
    speeds_b = turbine_b.get_measurements()['speed']

    bins = (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25)
    X_a, Y_a = np.histogram(speeds_a, bins = bins, density = True)
    X_b, Y_b = np.histogram(speeds_b, bins = bins, density = True)

    akv = {k: v for k, v in zip(Y_a, X_a)}
    bkv = {k: v for k, v in zip(Y_b, X_b)}

    def join(x,y):
        return akv[x] * bkv[y]

    def generate(X,Y):
        Z = np.zeros(X.shape)
        for i in range(X.shape[0]):
            Z[i] = map(join, X[i], Y[i])
        return Z

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = range(0, 25, 2)
    ys = range(0, 25, 2)
    X, Y = np.meshgrid(xs, ys)
    Z = generate(X, Y)

    plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, linewidth=0,\
                    cmap=cm.coolwarm)

    ax.set_xlabel("Turbine 1")
    ax.set_ylabel("Turbine 2")
    ax.set_zlabel("Joined Windspeed Probability")
    ax.set_title("Joined Windspeed Probability")

    plt.show()

