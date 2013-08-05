"""
Histogram of Wind Speeds of a Wind Mill
-------------------------------------------------------------

Histograms of wind speeds of a wind mill near Cheyenne in the year 2004.
"""

import matplotlib.pyplot as plt
from pylab import plt
from windml.datasets.nrel import NREL

ds = NREL()
mill = ds.get_windmill(NREL.park_id['cheyenne'], 2004)
speeds = map(lambda x : x[2], mill.measurements)

plt.hist(speeds, color="#c4d8eb", bins = 100, normed = 1)
plt.ylim([0, 15000])
plt.show()
