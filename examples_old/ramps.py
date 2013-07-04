"""
=============================================================================
Wind changes of turbine in tehachapi
=============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np

from windml.datasets.windmill import get_nrel_windmill
from windml.visualization.plot_timeseries import plot_timeseries

park_indices = {'tehachapi': 4155}

windmill = get_nrel_windmill(park_indices['tehachapi'], 2004)
X=np.array([m[1] for m in windmill.get_measurements()])


# variables necessare for computation of wind changes and their colors

x1= []
x2 = []
colors = []

figure = plt.figure(figsize=(15, 10))
j = 1


# for four time horizons, save wind at time t and t+1 and add this to plot

for steps in [0,1,2,4]:
    x1= []
    x2 = []
    colors = []
    for i in xrange(len(X)-steps):
        x1.append(X[i])
        x2.append(X[i+steps])
        colors.append(abs(X[i]-X[i+steps])) # depending on the distance to the diagonal, choose the color of the event
    ax = plt.subplot(2, 2, j)
    plt.title("ramps, horizon = "+str(steps))
    ax.scatter(x1, x2, s=15, c=colors, linewidth=0.0, cmap=plt.cm.jet)
    j+=1


plt.show()
