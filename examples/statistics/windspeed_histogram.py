"""
Histogram of Wind Speeds
-------------------------------------------------------------

Histograms of wind speeds of a turbine near Cheyenne in the year 2004.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import matplotlib.pyplot as plt
from pylab import plt
from windml.datasets.nrel import NREL
from windml.visualization.colorset import colorset

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['cheyenne'], 2004)
speeds = map(lambda x : x[2], turbine.measurements)

plt.title("Histogram of Wind Speeds")
plt.xlabel("Wind Speed [m/s] in time t")
plt.ylabel("Relative Frequency")
plt.hist(speeds, color=colorset[0], bins=10, normed = 1)
plt.show()
