"""
Wind Changes of a Wind Mill in Tehachapi
--------------------------------------------------

This example plots the measurement pairs of a measurement and a measurement in
a certain time horizon. With these measurement pairs different wind change
situations can be visualized.
"""

import matplotlib.pyplot as plt
import numpy as np

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries

ds = NREL()
windmill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)
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
        # depending on the distance to the diagonal,
        # choose the color of the event
        colors.append(abs(X[i]-X[i+steps]))
        ax = plt.subplot(2, 2, j)
    plt.title("Ramps, Horizon = "+str(steps))
    ax.scatter(x1, x2, s=15, c=colors, linewidth=0.0, cmap=plt.cm.jet)
    j+=1

plt.show()
