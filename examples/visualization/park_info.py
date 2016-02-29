"""
Power Levels of a Wind Turbine
-------------------------------------------------------------------------

This examples shows a statistical overview of the power levels of a wind turbine. 
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# License: BSD 3 clause

import matplotlib.pyplot as plt
import numpy as np
import windml.util.features

from windml.datasets.nrel import NREL
from windml.visualization.show_coord_topo import show_coord_topo

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 2, 2004)
X = np.array(windpark.get_powermatrix())

feat, month_power, ramps_up, ramps_down, power_freq =\
    windml.util.features.compute_highlevel_features(windpark.turbines[0])



help = [i*windml.util.features.interval_width for i in range(1,30/windml.util.features.interval_width+1)]
labels = [str(i-windml.util.features.interval_width)+"-"+str(i) for i in help]

with plt.style.context("fivethirtyeight"):
    figure = plt.figure(figsize=(8, 5))
    plt.pie(power_freq, labels = labels, shadow=True)


    plt.title("Power Level")
    plt.show()
