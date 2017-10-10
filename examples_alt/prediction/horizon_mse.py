"""
Forecast Error Depending on Horizon
-------------------------------------------------------------------------

This example shows the dependence of the mean squared error (forecast error) on
a growing forecast horizon. The models KNN, linear regression, and the naive
(persistance) model are compared. In this example, the turbine 'Tehachapi' is
the target turbine. The forecast is based on the whole wind park, which is defined
by the latter id and a given radius of 3 kilometres. For the mapping of
pattern-label combinations the :ref:`powermapping` is used.  The power mapping
is based on the :ref:`generaltimeseriesmodel`. The feature window and the
forecast horizon both consist of 3 elements of every time series.  Because of
performance issues, in this example only every fifth element is used for
training and testing.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import math
import matplotlib.pyplot as plt

from numpy import zeros, float32
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping

from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn.neighbors import KNeighborsRegressor

def compute_mse(regressor, horizon):
    # get wind park and corresponding target. forecast is for the target
    # turbine
    park_id = NREL.park_id['tehachapi']
    windpark = NREL().get_windpark(park_id, 3, 2004, 2005)
    target = windpark.get_target()

    # use power mapping for pattern-label mapping. Feature window length
    # is 3 time steps and time horizon (forecast) is 3 time steps.
    feature_window = 3
    mapping = PowerMapping()
    X = mapping.get_features_park(windpark, feature_window, horizon)
    Y = mapping.get_labels_turbine(target, feature_window, horizon)

    # train roughly for the year 2004.
    train_to = int(math.floor(len(X) * 0.5))

    # test roughly for the year 2005.
    test_to = len(X)

    # train and test only every fifth pattern, for performance.
    train_step, test_step = 5, 5

    if regressor == 'linear':
        # fitting the pattern-label pairs
        reg = linear_model.LinearRegression()
        reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
        y_hat = reg.predict(X[train_to:test_to:test_step])
    elif regressor == 'knn':
        k_neighbors = 10
        reg = KNeighborsRegressor(k_neighbors, 'uniform')
        # fitting the pattern-label pairs
        reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
        y_hat = reg.predict(X[train_to:test_to:test_step])
    else:
        raise Exception("No regressor set.")

    # naive is also known as persistance model.
    naive_hat = zeros(len(y_hat), dtype = float32)
    for i in range(0, len(y_hat)):
        # naive label is the label as horizon time steps before.
        # we have to consider to use only the fifth label here, too.
        naive_hat[i] = Y[train_to + (i * test_step) - horizon]

    # computing the mean squared errors of Linear and naive prediction.
    mse_y_hat, mse_naive_hat = 0, 0
    for i in range(0, len(y_hat)):
        y = Y[train_to + (i * test_step)]
        mse_y_hat += (y_hat[i] - y) ** 2
        mse_naive_hat += (naive_hat[i] - y) ** 2

    mse_y_hat /= float(len(y_hat))
    mse_naive_hat /= float(len(y_hat))

    return mse_y_hat, mse_naive_hat

regressors = ['linear', 'knn']
horizons = range(2, 18, 2)

marker = {'linear': 'go--', 'knn': 'ro--', 'naive': 'bo--'}
labels = {'linear': 'Linear', 'knn': 'KNN', 'naive' : 'Naive'}

plt.title("MSE depending on Forecast Horizon")
plt.xlabel("Forecast Horizon")
plt.ylabel("MSE")

mse_naive_hats = []
for regressor in regressors:
    mse = []
    mse_naive_hats = []
    for horizon in horizons:
        mse_y_hat, mse_naive_hat = compute_mse(regressor, horizon)
        mse.append(mse_y_hat)
        mse_naive_hats.append(mse_naive_hat)
    plt.plot(horizons, mse, marker[regressor], label=labels[regressor])

plt.plot(horizons, mse_naive_hats, marker['naive'], label=labels['naive'])

plt.legend(loc='lower right')
plt.show()

