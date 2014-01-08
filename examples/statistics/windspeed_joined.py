"""
Joined Probability of Wind Speeds
-------------------------------------------------------------------------

This example plots show the joined probability of wind speeds.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import numpy as np

from windml.datasets.nrel import NREL
from windml.visualization.plot_wind_interdependecies import plot_joined

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 3, 2004)

turbines = windpark.get_turbines()
turbine_a = turbines[0]
turbine_b = turbines[1]

plot_joined(turbine_a, turbine_b)
