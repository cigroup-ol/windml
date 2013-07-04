"""
Example Plot Response Curve Of Windmill 
--------------------------------------------------

This example plots the response curve of a windmill near Tehachapi.

"""

from windml.datasets.park_definitions import park_info
from windml.datasets.windmill import get_nrel_windmill
from windml.visualization.plot_response_curve import plot_response_curve
from matplotlib import dates
import matplotlib.pylab as plt
import numpy as np
import datetime, time


millname = 'tehachapi'
target_idx = park_info[millname][0]
my_windmill = get_nrel_windmill(target_idx, 2004)
plot_response_curve(my_windmill)
