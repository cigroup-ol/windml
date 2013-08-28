"""
Reconstruction Mean Squared Error Depend on MAR Rate
-------------------------------------------------------------------------
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import destroy
from windml.preprocessing.preprocessing import interpolate

import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

from numpy import array
from itertools import product

start, end = 0, 500
timestep = 600
imethods = ['linear', 'topologic', 'forwardcopy', 'backwardcopy']
rates = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
destroy_method = 'mar'

def static():
    park_id = NREL.park_id['tehachapi']
    windpark = NREL().get_windpark(park_id, 3, 2004)
    return windpark

def static_topologic(windpark):
    target = windpark.get_target()
    measurements = target.get_measurements()[start:end]
    tloc = (target.longitude, target.latitude)
    neighbors = windpark.get_turbines()[:-1]
    nseries = [t.get_measurements()[start:end] for t in neighbors]
    nlocs = [(t.longitude, t.latitude) for t in neighbors]

    iargs = {'timestep': timestep,
             'location': tloc,
             'neighbor_series': nseries,
             'neighbor_locations': nlocs}
    return iargs

def static_linear(windpark):
    return {'timestep': timestep}

def static_forwardcopy(windpark):
    return {'timestep': timestep}

def static_backwardcopy(windpark):
    return {'timestep' : timestep}

argfuncs = {'linear': static_linear,
            'topologic': static_topologic,
            'forwardcopy' : static_forwardcopy,
            'backwardcopy' : static_backwardcopy}

def rmse_score(measurements, reconstructed):
    cs = 'corrected_score'
    total_error = 0
    print len(measurements), len(reconstructed)
    for i in xrange(len(reconstructed)):
        total_error += ((measurements[i][cs] - reconstructed[i][cs]) ** 2)
    return total_error

def experiment(method, windpark, damaged, rate):
    args = argfuncs[method](windpark)
    reconstructed = interpolate(damaged, method=method, **args)

    error = rmse_score(measurements, reconstructed)
    print "method %s, mar-rate %f error %i" % (method, rate, error)
    return method, rate, error

# generating destroyed measurements which are constant over all
# methods

windpark = static()
target = windpark.get_target()
measurements = target.get_measurements()[start:end]

damaged_series = {rate : destroy(measurements, method=destroy_method,\
                  percentage=rate) for rate in rates}

results = {(method, rate) : 0 for method, rate in product(imethods, rates)}

for method in imethods:
    for rate in rates:
        results[(method, rate)] =\
            experiment(method, windpark, damaged_series[rate], rate)

# plotting code
labels = {'linear' : 'Linear',
          'topologic' : 'Topological',
          'forwardcopy' : 'Forward Copy',
          'backwardcopy' : 'Backward Copy'}

for method in imethods:
    rmse = [results[method, rate][-1] for rate in rates]
    plt.plot(rates, rmse, label=labels[method])

plt.xlabel("MAR Rate")
plt.ylabel("Reconstruction MSE")
plt.title("Reconstruction MSE Depend on MAR Destroy Rate")
plt.legend(loc='upper left')
plt.show()
