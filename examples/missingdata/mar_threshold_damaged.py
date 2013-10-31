"""
Damage the Timeseries MAR + Threshold
-------------------------------------------------------------------------

This example shows how to artificially damage a time series by uniform
distributed removal of data (MAR = 'Missing At Random') for data under a lower
bound and higher than the upper bound.The percentage of missing data is given
to the preprocessing operator.  """

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import destroy

from numpy import array
import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
measurements = turbine.get_measurements()[:1000]
damaged, indices = destroy(measurements, method='mar_with_threshold',\
                percentage=.80, lower_bound = 0, upper_bound = 20)

d = array([m[0] for m in measurements])
y1 = array([m[1] for m in measurements]) #score
y2 = array([m[2] for m in measurements]) #speed

d_hat = array([m[0] for m in damaged])
y1_hat = array([m[1] for m in damaged])
y2_hat = array([m[2] for m in damaged])

d_time = []
for i in range (len(d)):
    d_act = datetime.datetime.fromtimestamp(d[i])
    d_time.append(d_act)

d_time_hat = []
for i in range (len(d_hat)):
    d_act_hat = datetime.datetime.fromtimestamp(d_hat[i])
    d_time_hat.append(d_act_hat)

plt.subplots_adjust(bottom=0.25)
plt.xticks(rotation = 75)

ax=plt.gca()
xfmt = md.DateFormatter('%Y/%m/%d %H-h')
ax.xaxis.set_major_formatter(xfmt)

ax.grid(True)
plt.ylim(-2, 32)
plt.ylabel("Corrected Power (MW), Wind Speed (m/s)")

plt.plot(d_time, y1, label = 'Power Production', color="b", alpha=0.5)
plt.plot(d_time, y2, label = 'Wind Speed', color="g", alpha=0.5)

plt.plot(d_time_hat, y1_hat, label = 'Power Production (damaged)',
    color="b", linestyle=".", marker="o")
plt.plot(d_time_hat, y2_hat, label = 'Wind Speed (damaged)', color="g",
    marker="o", linestyle=".")

plt.legend(loc='lower right')
plt.title("Timeseries of the Selected Turbine")

plt.show()

