"""
Time-Series of Wind Speed and Power
--------------------------------------------------

This example plots a time-series of a single
wind mill in the wind park 'tehachapi'.
"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Justin P. Heinermann <justin.philipp.heinermann@uni-oldenburg.de>
# License: BSD 3 clause

from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries

ds = NREL()
mill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)

plot_timeseries(mill)
