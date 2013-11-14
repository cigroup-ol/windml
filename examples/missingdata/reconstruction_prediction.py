"""
Prediction with Imputated Time Series
-------------------------------------------------------------------------

The time series of the target turbine near Reno is destroyed missing at random
(MAR) given a certain percentage of damage. The damaged time series is
imputated using different imputation methods: last observation carried forward
(LOCF), linear interpolation, multiple linear regression and kNN regression.
The imputated time series is used for short-term wind prediction employing the
spatio-temporal time series model with multiple linear regression. The plot
shows the prediction MSE depending on the rate of missing data for different
imputation methods.
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
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn import linear_model

from windml.mapping.power_mapping import PowerMapping
from sklearn.neighbors import KNeighborsRegressor

import matplotlib.pyplot as plt
import matplotlib.dates as md
from pylab import *
from matplotlib.ticker import FuncFormatter

from numpy import array
from itertools import product, chain

parks = {
    'carway': 30498,
}

timestep = 600
methods = ['mreg_knn', 'mreg_lin', 'linear', 'forwardcopy']
rates = [0.1, 0.3, 0.5, 0.7, 0.9]
destroy_method = 'mar'
labels = {'linear': 'Linear Interpolation', 'forwardcopy':'LOCF',\
          'mreg_knn' : 'KNN Regression','mreg_lin' : 'Linear Regression'}

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

    return iargs, nseries

def static_mreg_lin(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]

    iargs = {'method':'mreg',
             'timestep': timestep,
             'neighbor_series': nseries,
             'reg' : 'linear_model'}
    return iargs, nseries

def static_linear(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]

    return {'method':'linear','timestep': timestep}, nseries

def static_forwardcopy(windpark):
    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    neighbors = windpark.get_turbines()[:-1]
    nseries = [repair_nrel(t.get_measurements()[:10000]) for t in neighbors]

    return {'method':'forwardcopy','timestep': timestep}, nseries

argfuncs = {'linear': static_linear,
            'forwardcopy' : static_forwardcopy,
            'mreg_knn' : static_mreg_knn,
            'mreg_lin' : static_mreg_lin}

# predict with imputated series
def experiment(method, windpark, windpark_test, damaged, rate):
    args, nseries = argfuncs[method](windpark)
    reconstructed = interpolate(damaged,  **args)

    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])
    turbines = windpark.get_turbines()

    for t in range(len(turbines)):
        turbines[t].add_measurements(\
            repair_nrel(turbines[t].get_measurements()[:10000]))

    # this is the target turbine, use the reconstructed here.
    turbines[-1].add_measurements(reconstructed)

    feature_window, horizon = 3,3

    mapping = PowerMapping()
    # with damaged
    X = mapping.get_features_park(windpark, feature_window, horizon)
    Y = mapping.get_labels_turbine(target, feature_window, horizon)

    train_to = int(math.floor(len(X)))
    train_step, test_step = 1, 1

    reg = linear_model.LinearRegression()
    reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])

    # USE THE 2005 YEAR FOR TESTING, WITHOUT DAMAGE
    # predict on second year without damage

    turbines = windpark_test.get_turbines()
    for t in turbines:
        t.add_measurements(repair_nrel(t.get_measurements()[:10000]))
    target_test = windpark_test.get_target()

    XT = mapping.get_features_park(windpark_test, feature_window, horizon)
    test_to = int(math.floor(len(XT)))

    YT = mapping.get_labels_turbine(target_test, feature_window, horizon)[:test_to]
    y_hat = reg.predict(XT[:test_to])

    mse_y_hat = 0
    for i in range(0, len(y_hat)):
        y = YT[i]
        mse_y_hat += (y_hat[i] - y) ** 2

    mse_y_hat /= float(len(y_hat))

    return mse_y_hat

# generating destroyed measurements which are constant over all
# methods

data = []

for park in parks.keys():
    windpark = NREL().get_windpark_nearest(parks[park], 5, 2004)
    windpark_test = NREL().get_windpark_nearest(parks[park], 5, 2005)

    target = windpark.get_target()
    measurements = repair_nrel(target.get_measurements()[:10000])

    for i in xrange(2):

        damaged_series = {}
        de = lambda (rate) : (rate, (destroy(measurements, method=destroy_method, percentage=rate)[0]))

        dseries = map(de, rates)
        for rate, series in dseries:
            damaged_series[rate] = series

        # with reconstruction

        def run(pars):
            method, rate = pars
            mse = experiment(method, windpark, windpark_test, damaged_series[rate], rate)
            return method, rate, mse

        results = map(run, list(chain(product(methods, rates))))

        encoding = lambda method, rate, mse, park :\
            {"method": method,\
            "rate": rate,\
            "mse": mse,\
            "park" : park }

        results = [encoding(method, rate, mse, park) for (method, rate, mse) in results]

        for result in results:
            data.append(result)

mse = {}
for result in data:
    keys = mse.keys()
    key = (result['method'], result['rate'], result['park'])
    if(key not in keys):
        mse[key] = []
    mse[key].append(result['mse'])

# calculate mean and var, std
mean = {}
var = {}
std = {}

for key in mse.keys():
    if(key not in mean.keys()):
        mean[key] = []
    mean[key] = array(mse[key]).mean()

for key in mse.keys():
    if(key not in var.keys()):
        var[key] = []
    var[key] = array(mse[key]).var()

for key in mse.keys():
    if(key not in std.keys()):
        std[key] = []
    std[key] = array(mse[key]).std()

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

park = "carway"

for method in methods:
    rmses = []
    yerrs = []
    for rate in rates:
        yerrs.append(std[method, rate, park])
        rmses.append(mean[method, rate, park])

    plt.errorbar(rates, rmses, yerr=yerrs,\
                 label=labels[method], linestyle="--", marker="o")

def to_percent(y, position):
    s = str(100 * y)
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

formatter = FuncFormatter(to_percent)

plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel("Rate of Missing Data in Percent")
plt.ylabel("Prediction MSE of Power [MW]")
plt.xlim([0.1, 0.9])
plt.ylim([12.5, 16])
plt.legend(loc="upper left")
plt.show()

