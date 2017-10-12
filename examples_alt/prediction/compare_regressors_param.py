"""
Comparison of KNN and Random Forest Regression
----------------------------------------------

This example shows the mean squared error (forecast error) when using KNN with
different parameters K and random forest regression trees with a variable
number of estimators utilized in the ensemble regressor. In this example, the
turbine 'Tehachapi' is the target turbine. The forecast is based on the whole
wind park, which is defined by the id and a given radius of 3 kilometers. For
the mapping of pattern-label combinations, the :ref:`powermapping` is used.
The power mapping is based on the :ref:`generaltimeseriesmodel`. The feature
window consists of 6 time elements, while the forecast horizon consists of 3.
Because of performance issues, in this example only every fifth element is used
for training and testing.
"""

# Author: Justin P. Heinermann <justin.philipp.heinermann@uni-oldenburg.de>
# License: BSD 3 clause

import math
import matplotlib.pyplot as plt

from numpy import zeros, float32
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping

from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

def compute_mse(regressor, param):
    # get wind park and corresponding target. forecast is for the target
    # turbine
    park_id = NREL.park_id['tehachapi']
    windpark = NREL().get_windpark(park_id, 3, 2004)
    target = windpark.get_target()

    # use power mapping for pattern-label mapping. Feature window length
    # is 3 time steps and time horizon (forecast) is 3 time steps.
    feature_window = 6
    horizon = 3
    mapping = PowerMapping()
    X = mapping.get_features_park(windpark, feature_window, horizon)
    Y = mapping.get_labels_turbine(target, feature_window, horizon)

    # train roughly for the year 2004.
    train_to = int(math.floor(len(X) * 0.5))

    # test roughly for the year 2005.
    test_to = len(X)

    # train and test only every fifth pattern, for performance.
    train_step, test_step = 5, 5

    if(regressor == 'rf'):
        # random forest regressor
        reg = RandomForestRegressor(n_estimators=param, criterion='mse')
        reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
        y_hat = reg.predict(X[train_to:test_to:test_step])
    elif(regressor == 'knn'):
        # TODO the regressor does not need to be newly trained in
        # the case of KNN
        reg = KNeighborsRegressor(param, 'uniform')
        # fitting the pattern-label pairs
        reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
        y_hat = reg.predict(X[train_to:test_to:test_step])
    else:
        raise Exception("No regressor set.")

    # naive is also known as persistence model.
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

regressors = ['rf', 'knn']
params = [1, 2, 4, 8, 16, 32, 64, 128]

marker = {'rf': 'go--', 'knn': 'ro--', 'naive': 'bo--'}
labels = {'rf': 'Random Forest', 'knn': 'KNN', 'naive' : 'Naive'}

plt.title("MSE depending on Algorithm Parameter")
plt.xlabel("Algorithm Parameter (k for KNN, Number of Estimators for RF )")
plt.ylabel("MSE")
plt.xlim([1, 128])

mse_naive_hats = []
for regressor in regressors:
    mse = []
    mse_naive_hats = []
    for param in params:
        mse_y_hat, mse_naive_hat = compute_mse(regressor, param)
        mse.append(mse_y_hat)
        mse_naive_hats.append(mse_naive_hat)
    plt.plot(params, mse, marker[regressor], label=labels[regressor])

plt.plot(params, mse_naive_hats, marker['naive'], label=labels['naive'])

plt.legend(loc='upper right')
plt.show()
