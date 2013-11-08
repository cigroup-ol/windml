"""
KNN Regression for Interpolation
-------------------------------------------------------------------------

In this example, the target turbine in the windpark Tehachapi lacks of wind
power and wind speed data. The distribution of the missing data is Not Missing
At Random (NMAR). The missing data is interpolated by k-nearest neighbor
regression.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import matplotlib.pyplot as plt

from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from windml.preprocessing.preprocessing import destroy
from windml.preprocessing.preprocessing import interpolate
from windml.visualization.plot_timeseries import plot_timeseries

import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

from numpy import array, zeros, float32, int32

# get windpark and corresponding target. forecast is for the target turbine
park_id = NREL.park_id['tehachapi']
windpark = NREL().get_windpark(park_id, 3, 2004)
target = windpark.get_target()

measurements = target.get_measurements()[300:1000]
damaged, indices = destroy(measurements, method="nmar", percentage=.80,\
        min_length=10, max_length=100)

neighbors = windpark.get_turbines()[:-1]
nseries = [t.get_measurements()[300:1000] for t in neighbors]

tinterpolated = interpolate(damaged, method='mreg',\
                            timestep=600,\
                            neighbor_series = nseries,\
                            reg = 'knn',
                            regargs = {'n': 10, 'variant':'uniform'})

d = array([m[0] for m in tinterpolated])
y1 = array([m[1] for m in tinterpolated]) #score
y2 = array([m[2] for m in tinterpolated]) #speed

d_hat = array([m[0] for m in damaged])
y1_hat = array([m[1] for m in damaged])
y2_hat = array([m[2] for m in damaged])

d_true = array([m[0] for m in measurements])
y1_true = array([m[1] for m in measurements])
y2_true = array([m[2] for m in measurements])

d_time = []
for i in range (len(d)):
    d_act = datetime.datetime.fromtimestamp(d[i])
    d_time.append(d_act)

d_time_hat = []
for i in range (len(d_hat)):
    d_act_hat = datetime.datetime.fromtimestamp(d_hat[i])
    d_time_hat.append(d_act_hat)

d_time_true = []
for i in range (len(d_true)):
    d_act_true = datetime.datetime.fromtimestamp(d_true[i])
    d_time_true.append(d_act_true)

plt.subplots_adjust(bottom=0.25)
plt.xticks(rotation = 75)

ax=plt.gca()
xfmt = md.DateFormatter('%Y/%m/%d %H-h')
ax.xaxis.set_major_formatter(xfmt)

ax.grid(True)
plt.ylim(-2, 32)
plt.ylabel("Corrected Power (MW), Wind Speed (m/s)")

plt.plot(d_time, y1, label = 'Power Production (interpolated)', color="b")
plt.plot(d_time, y2, label = 'Wind Speed (interpolated)', color="g")

plt.plot(d_time_true, y1_true, label = 'Power Production', color="b", linestyle="--")
plt.plot(d_time_true, y2_true, label = 'Wind Speed', color="g", linestyle="--")


plt.plot(d_time_hat, y1_hat, label = 'Power Production (damaged)',
    color="b", linestyle=".", marker="o")
plt.plot(d_time_hat, y2_hat, label = 'Wind Speed (damaged)', color="g",
    marker="o", linestyle=".")

plt.legend(loc='lower right')
plt.title("Timeseries of the Selected Turbine")

plt.show()

