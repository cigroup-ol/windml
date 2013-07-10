"""
Plot Response Curve of Windmill
--------------------------------------------------
This example plots the response curve of a windmill near Tehachapi.
"""

from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time

from windml.datasets.nrel import NREL
from windml.visualization.plot_response_curve import plot_response_curve

ds = NREL()
mill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)
plot_response_curve(mill)
