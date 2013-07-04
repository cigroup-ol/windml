"""
Example Plot Time Series
--------------------------------------------------

This example plots a time series of one single given
wind mill in tehachapi park

"""

from windml.datasets.park_definitions import park_info
from windml.datasets.windmill import get_nrel_windmill
from windml.visualization.plot_timeseries import plot_timeseries
from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time


millname = 'tehachapi'
target_idx = park_info[millname][0]
my_windmill = get_nrel_windmill(target_idx, 2004)
plot_timeseries(my_windmill)