"""
Reconstruction MSE of Imputation
-------------------------------------------------------------------------

The time series of the target turbine near Reno is destroyed missing at random
(MAR) given a certain percentage of damage. Different imputation methods are
compared w.r.t. their reconstruction MSE and to the original time series. For
the imputation the last observation carried forward (LOCF), linear
interpolation, multiple linear regression and kNN regression are used.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.datasets.nrel import NREL
from windml.visualization.plot_timeseries import plot_timeseries
from windml.preprocessing.preprocessing import destroy
from windml.preprocessing.preprocessing import interpolate
from windml.preprocessing.preprocessing import repair_nrel
from sklearn.neighbors import KNeighborsRegressor
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold, cross_val_score

import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *

from numpy import array
from itertools import product, chain
from builtins import range

parks = {
    'reno' : 11637,
}

timestep = 600
methods = ['mreg_knn', 'mreg_lin', 'linear', 'forwardcopy']
rates = [0.1, 0.3, 0.5, 0.7, 0.9]
destroy_method = 'mar'
labels = {'linear': 'Linear Interpolation', 'forwardcopy':'LOCF',\
          'backwardcopy': 'Backward Copy', 'mreg_knn' :'KNN Regression',
          'mreg_lin' : 'Linear Regression'}

def static_topologic(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    tloc = (target.longitude, target.latitude)
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]
    nlocs = [(t.longitude, t.latitude) for t in neighbors]

    iargs = {'method' : 'topologic',
             'timestep': timestep,
             'location': tloc,
             'neighbor_series': nseries,
             'neighbor_locations': nlocs}
    return iargs

def static_mreg_knn(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]

    iargs = {'method':'mreg',
             'timestep': timestep,
             'neighbor_series': nseries,
             'reg' : 'knn',
             'regargs' : {'kfold': 5, 'n' : [5,10,20,50,100], 'variant' : 'uniform'}}

    return iargs

def static_mreg_svr(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]
    reg = linear_model.LinearRegression()

    gamma_range = [0.0001, 0.000001]
    C_range = [2 ** i for i in range(1, 4, 1)]
    regargs = {
        "epsilon" : 0.1,
        "cv_method" : KFold,
        "cv_args" : {"n_folds" : 10},
        "kernel" : 'rbf',
        "tuned_parameters" : [{
            'kernel': [kernel],
            'C': C_range,
            'gamma': gamma_range}]}

    iargs = {'method':'mreg',
             'timestep': timestep,
             'neighbor_series': nseries,
             'reg' : reg,
             'regargs' : regargs}

    return iargs

def static_mreg_lin(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]

    iargs = {'method':'mreg',
             'timestep': timestep,
             'neighbor_series': nseries,
             'reg' : 'linear_model'}
    return iargs

def static_linear(windpark):
    return {'method':'linear','timestep': timestep}

def static_forwardcopy(windpark):
    return {'method':'forwardcopy','timestep': timestep}

argfuncs = {'linear': static_linear,
            'topologic': static_topologic,
            'forwardcopy' : static_forwardcopy,
            'mreg_knn' : static_mreg_knn,
            'mreg_lin' : static_mreg_lin}

def scores(measurements, reconstructed):
    cs = 'corrected_score'
    total_error = 0
    diffs = []
    for i in xrange(len(reconstructed)):
        total_error += ((measurements[i][cs] - reconstructed[i][cs]) ** 2)
        diffs.append(measurements[i][cs] - reconstructed[i][cs])
    diffs = array(diffs)
    return (1.0 / len(measurements)) * total_error, diffs.var(), diffs.std()

def experiment(method, windpark, damaged, rate):
    args = argfuncs[method](windpark)
    reconstructed = interpolate(damaged,  **args)

    error, var, std = scores(measurements, reconstructed)
    return error, var, std

# generating destroyed measurements which are constant over all
# methods

data = []

park = 'reno'
windpark = NREL().get_windpark_nearest(parks[park], 5, 2004)
target = windpark.get_target()
measurements = repair_nrel(target.get_measurements()[:10000])

for i in range(2):
    damaged_series = {}
    de = lambda rate : (rate, (destroy(measurements, method=destroy_method, percentage=rate)[0]))

    dseries = map(de, rates)
    for rate, series in dseries:
        damaged_series[rate] = series

    def run(pars):
        method, rate = pars
        error, var, std = experiment(method, windpark, damaged_series[rate], rate)
        return method, rate, error, var, std

    results = map(run, list(chain(product(methods, rates))))
    encoding = lambda method, rate, error, park, var, std :\
        {"method": method,\
        "rate": rate,\
        "rmse": error,\
        "park" : park,\
        "var" : var,\
        "std" : std}

    results = [encoding(method, rate, error, park, var, std)
                    for (method, rate, error, var, std) in results]

    for result in results:
        data.append(result)

rmse = {}
for result in data:
    keys = rmse.keys()
    key = (result['method'], result['rate'], result['park'])
    if(key not in keys):
        rmse[key] = []
    rmse[key].append(result['rmse'])

# calculate mean and var, std
mean = {}
var = {}
std = {}

for key in rmse.keys():
    if(key not in mean.keys()):
        mean[key] = []
    mean[key] = array(rmse[key]).mean()

for key in rmse.keys():
    if(key not in var.keys()):
        var[key] = []
    var[key] = array(rmse[key]).var()

for key in rmse.keys():
    if(key not in std.keys()):
        std[key] = []
    std[key] = array(rmse[key]).std()

## mean of all means of parks, std for this
amean = {}
astd = {}
for method in methods:
    for rate in rates:
        means = []
        for park in parks.keys():
            means.append(mean[method, rate, park])
        amean[method, rate] = array(means).mean()
        astd[method, rate] = array(means).std()

park = "reno"

for method in methods:
    rmses = []
    yerrs = []
    for rate in rates:
        yerrs.append(std[method, rate, park])
        rmses.append(mean[method, rate, park])
    plt.errorbar(rates, rmses, yerr=yerrs, label=labels[method],\
                    linestyle="--", marker="o")
#plt.legend(loc="upper left")

def to_percent(y, position):
    s = str(100 * y)
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

formatter = FuncFormatter(to_percent)

plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel("Rate of Missing Data")
plt.ylabel("Reconstruction MSE")
plt.xlim([0.1, 0.9])
plt.ylim([0, 10])
plt.legend(loc="upper left")

plt.show()

