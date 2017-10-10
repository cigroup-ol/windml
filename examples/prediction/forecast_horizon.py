"""
Forecast Error Depending on Horizon
-------------------------------------------------------------------------

This example shows the dependence of the mean squared error (forecast error) on
a growing forecast horizon. The models KNN and SVR are compared. In this
example, the turbine 'Tehachapi' is the target turbine. The forecast is based
on the whole wind park, which is defined by the latter id and a given radius of
3 kilometres. For the mapping of pattern-label combinations the
:ref:`powermapping` is used.  The power mapping is based on the
:ref:`generaltimeseriesmodel`. The feature window and the forecast horizon both
consist of 3 elements of every time series.  Because of performance issues, in
this example only every fifth element is used for training and testing.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from __future__ import print_function
import numpy as np
import math
import matplotlib.pyplot as plt
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error


def compute_mse(regressor, horizon):
    # get wind park and corresponding target.
    windpark = NREL().get_windpark(NREL.park_id['tehachapi'], 3, 2004, 2005)
    target = windpark.get_target()

    # use power mapping for pattern-label mapping.
    feature_window = 3
    mapping = PowerMapping()
    X = mapping.get_features_park(windpark, feature_window, horizon)
    y = mapping.get_labels_turbine(target, feature_window, horizon)

    # train roughly for the year 2004, test for 2005.
    train_to = int(math.floor(len(X) * 0.5))
    test_to = len(X)
    train_step, test_step = 25, 25
    X_train = X[:train_to:train_step]
    y_train = y[:train_to:train_step]
    X_test = X[train_to:test_to:test_step]
    y_test = y[train_to:test_to:test_step]

    if regressor == 'svr':
        reg = SVR(kernel='rbf', epsilon=0.1, C=100.0,
                  gamma=0.0001).fit(X_train, y_train)
        mse = mean_squared_error(reg.predict(X_test), y_test)
    elif(regressor == 'knn'):
        reg = KNeighborsRegressor(10, 'uniform').fit(X_train, y_train)
        mse = mean_squared_error(reg.predict(X_test), y_test)
    return mse


regressors = ['svr', 'knn']
horizons = range(2, 18, 2)
errors = {}

for regressor in regressors:
    errors[regressor] = []
    for horizon in horizons:
        errors[regressor].append(compute_mse(regressor, horizon))
print("SVR MSE:", errors['svr'])
print("KNN MSE:", errors['knn'])

with plt.style.context("fivethirtyeight"):
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    N = len(horizons)
    ind = np.arange(N)                # the x locations for the groups
    width = 0.4                       # the width of the bars
    ax.set_xticks(ind + width)
    ax.set_xticklabels([str(i) for i in horizons])

    # the bars
    rects1 = ax.bar(ind, errors['svr'], width, color='#6795cf')
    rects2 = ax.bar(ind + width, errors['knn'], width, color='#918f90')

    plt.title("MSE depending on Forecast Horizon")
    plt.xlabel("Forecast Horizon")
    plt.ylabel("MSE")
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
