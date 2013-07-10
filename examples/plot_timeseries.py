"""
Plot Time Series of Wind Speed and Power
--------------------------------------------------

This example plots a time series of one single given
wind mill in tehachapi park
"""

from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries

ds = NREL()
mill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)
plot_timeseries(mill)
