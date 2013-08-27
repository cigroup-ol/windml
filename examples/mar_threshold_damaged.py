"""
Damage the Timeseries MAR + Threshold
-------------------------------------------------------------------------

This example shows how to artificially damage a time series by uniform
distributed removal of data (MAR = 'Missing At Random') for data under a lower
bound and higher than the upper bound.The percentage of missing data is given
to the preprocessing operator.  """

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import destroy

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
measurements = turbine.get_measurements()[:1000]
damaged = destroy(measurements, method='mar_with_threshold', percentage=.80,\
                lower_bound = 0, upper_bound = 20)
turbine.measurements = damaged
plot_timeseries(turbine, 0, 1000)

