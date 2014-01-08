"""
Propagating Wind Changes
--------------------------------------------------
"""

# Author: Jendrik Poloczek <jendrik.poloczek@uni-oldenburg.de>
# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# License: BSD 3 clause

import matplotlib.pyplot as plt
import numpy as np
from windml.datasets.nrel import NREL

ds = NREL()

park_id = NREL.park_id['tehachapi']
windpark = NREL().get_windpark(park_id, 3, 2004)
turbines = windpark.get_turbines()
t1, t2 = turbines[0], turbines[1]

i=7
window_size = 200
steps = 3

X1 = t1.get_measurements()['speed']
X2 = t2.get_measurements()['speed']
X1 = X1[i*window_size:i*window_size+window_size]
X2 = X2[i*window_size:i*window_size+window_size]

x1= []
x2 = []
colors = []
for i in xrange(len(X1)-steps):
    x1.append(X1[i])
    x2.append(X2[i+steps])
    # depending on the distance to the diagonal,
    # choose the color of the event
    colors.append(abs(X1[i]-X2[i+steps]))
    ax = plt.subplot(1, 1, 1)
plt.title("Propagating Ramps, Horizon = "+str(steps))
ax.scatter(x1, x2, s=15, c=colors, linewidth=0.0, cmap=plt.cm.jet)
plt.xlabel("Wind Speed in time t (Turbine 1)")
plt.ylabel("Wind Speed in time t + 3 (Turbine 2)")
plt.show()
