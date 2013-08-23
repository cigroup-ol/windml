"""
Wind Changes of a Turbine
--------------------------------------------------

Wind ramp events play an important role for a stable integration of wind energy
into a smart grid. These plots show the frequencies of wind changes w.r.t.
different forecast horizons as deviations from the main diagonal.
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# License: BSD 3 clause

import matplotlib.pyplot as plt
import numpy as np

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
X=np.array([m[1] for m in turbine.get_measurements()])

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
