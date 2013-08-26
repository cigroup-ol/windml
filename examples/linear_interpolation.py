"""
Linear Interpolation of Missing Data
-------------------------------------------------------------------------

The AEMO data set lacks of complete data. Some measurements are missing.  There
are different methodologies available to handle missing data. In this example
the linear interpolation is used to estimate missing power values. For the
visualization purpose, the missing values are set to -5.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# License: BSD 3 clause

from windml.datasets.aemo import AEMO
from windml.preprocessing.missing_data_finder import MissingDataFinder
from windml.preprocessing.preprocessing import interpolate, override_missing

import numpy as np
import pylab as plt

turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])

start_ts = 100000 + 1.295e9
end_ts = 250000 + 1.295e9

timeseries = turbine.get_measurements_between(start_ts, end_ts)

timeseries_over = override_missing(timeseries, timestep=300, override_val=-5)
timeseries_hat = interpolate(timeseries, method='linear', timestep=300)

plt.ylabel("Corrected Power (MW), Wind Speed (m/s)")
plt.plot(timeseries_over['date'], timeseries_over['corrected_score'],\
         label="Orginal", linestyle="--")

plt.xlim([timeseries_hat['date'][0], timeseries_hat['date'][-1]])
plt.plot(timeseries_hat['date'].tolist(), timeseries_hat['corrected_score'].tolist(),\
         label="Linear Interpolated", linestyle="-")

plt.legend()
plt.show()
