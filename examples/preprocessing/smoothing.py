"""
Smoothing of a Time Series
--------------------------------------------------

This example shows how to smooth a time series with the
smoothen preprocessing operator.
"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import smoothen

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
measurements = turbine.get_measurements()

smoothed_measurements = smoothen(measurements, interval_length=11)
turbine.add_measurements(smoothed_measurements)

plot_timeseries(turbine, 0, 288)



