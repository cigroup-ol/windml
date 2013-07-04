"""
Example: Histogram of Wind Speeds
-------------------------------------------------------------
"""

from windml.datasets.windmill import get_nrel_windmill
from windml.datasets.park_definitions import park_info
import matplotlib.pyplot as plt

from pylab import plt

name = 'cheyenne'
target = get_nrel_windmill(park_info[name][0], 2004, 2005)

feature_window = 3
horizon = 3

speeds = map(lambda x : x[2], target.measurements)

plt.hist(speeds, color="g")
plt.show()
