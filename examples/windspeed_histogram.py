"""
Histogram of Wind Speeds
-------------------------------------------------------------
"""

import matplotlib.pyplot as plt
from pylab import plt
from windml.datasets.nrel import NREL

ds = NREL()
mill = ds.get_windmill(NREL.park_id['cheyenne'], 2004)
speeds = map(lambda x : x[2], mill.measurements)

plt.hist(speeds, color="g")
plt.show()
