"""
Multiple Time Series of Power
-------------------------------------------------------------------------

This example visualizes multiple time series of various turbines. It is
useful to illustrate differences and correlations of neighboring turbines.
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# License: BSD 3 clause

import numpy as np

from windml.datasets.nrel import NREL
from windml.visualization.plot_multiple_timeseries import plot_multiple_timeseries

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 3, 2004)
plot_multiple_timeseries(windpark)
