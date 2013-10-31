"""
Multivariate Regression for Interpolation
-------------------------------------------------------------------------

In this example the target turbine in the windpark Tehachapi lacks of wind
power and wind speed data. Further the neighbors lack of wind power and wind
speed data. Here the assumption holds, that at least one turbine has got the
information of wind power and speed at a given time. The distribution of the
missing data is Not Missing At Random (NMAR). The missing data is interpolated
by a multivariate regression.  In this example the k-nearest neighbor
regression is used.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import matplotlib.pyplot as plt

from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from windml.preprocessing.preprocessing import destroy
from windml.preprocessing.preprocessing import interpolate
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.mar_destroyer import MARDestroyer
from windml.preprocessing.mreg_interpolation import MRegInterpolation

import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

from numpy import array, zeros, float32, int32

park_id = NREL.park_id['tehachapi']
windpark = NREL().get_windpark(park_id, 3, 2004)
target = windpark.get_target()
timestep = 600
measurements = target.get_measurements()[300:1000]

damaged_target, indices_target = destroy(measurements, method="nmar", min_length=10, max_length=100, percentage=.50)

neighbors = windpark.get_turbines()[:-1]
count_neighbors = len(neighbors)
reg = 'knn' # KNeighborsRegressor(10, 'uniform')
regargs = {'n' : 10, 'variant' : 'uniform'}

processed = 0
missed = {k : count_neighbors for k in indices_target}
exclude = []
damaged_nseries = []

for neighbor in neighbors:
    nseries = neighbor.get_measurements()[300:1000]
    damaged, indices = destroy(measurements, method="nmar", percentage=.50, min_length=10, max_length=100, exclude=exclude)

    for index in indices:
        if(index not in missed.keys()):
            missed[index] = count_neighbors
        missed[index] -= 1
        if(missed[index] == 1):
            exclude.append(index) # exclude in next iterations
    damaged_nseries.append(damaged)

tinterpolated = interpolate(damaged_target, method='mreg',\
                            timestep=600,\
                            neighbor_series = damaged_nseries,\
                            reg = 'knn',
                            regargs = {'n': 10, 'variant':'uniform'})


d = array([m[0] for m in tinterpolated])
y1 = array([m[1] for m in tinterpolated]) #score

d_hat = array([m[0] for m in damaged_target])
y1_hat = array([m[1] for m in damaged_target])

d_true = array([m[0] for m in measurements])
y1_true = array([m[1] for m in measurements])

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

plt.plot(d_time_true, y1_true, label = 'Power Production', color="b", linestyle="--")

plt.plot(d_time_hat, y1_hat, label = 'Power Production (damaged)',
    color="b", linestyle=".", marker="o")

plt.legend(loc='lower right')
plt.title("Timeseries of the Selected Turbine")

plt.show()

