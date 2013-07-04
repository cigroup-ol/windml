"""
=============================================================================
Plot multiple time series
=============================================================================
"""
import numpy as np
from windml.datasets.park_definitions import park_info
from windml.datasets.windpark import get_nrel_windpark
from windml.visualization.plot_multiple_timeseries import plot_timeseries


radius = 3
name = 'tehachapi'
my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004)
plot_timeseries(my_windpark)