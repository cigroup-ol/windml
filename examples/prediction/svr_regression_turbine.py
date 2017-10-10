"""
.. _example_svr_regression:

SVR Wind Power Forecasting
-------------------------------------------------------------------------
Support Vector Regression for prediction of a time series of wind power for a
target turbine in Tehachapi. The prediction model is based on the wind power
time series of the target turbine and the time series of its neighbors defined by
a radius of 3 kilometers.For the mapping of pattern-label combinations the
:ref:`powermapping` is used. The power mapping is based on the
:ref:`generaltimeseriesmodel`. The feature window and the forecast horizon both
consist of 3 elements of every time series. Because of performance issues, in
this example only every fifth element is used for training and testing.  The
plot compares the SVR prediction and the naive model to the actual
wind power measurements.  
"""
# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Oliver Kramer <okramer@icsi.berkeley.com>
# Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# Justin P. Heinermann <justin.heinermann@uni-oldenburg.de>
# Stefan Oehmcke <stefan.oehmcke@uni-oldenburg.de>
# License: BSD 3 clause

from __future__ import print_function
import math
import matplotlib.pyplot as plt
from numpy import zeros, float32
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

# get windpark and corresponding target. forecast is for the target turbine
park_id = NREL.park_id['tehachapi']
windpark = NREL().get_windpark(park_id, 3, 2004, 2005)
target = windpark.get_target()

# use power mapping for pattern-label mapping.
feature_window, horizon = 3,3
mapping = PowerMapping()
X = mapping.get_features_park(windpark, feature_window, horizon)
y = mapping.get_labels_turbine(target, feature_window, horizon)

# train roughly for the year 2004, test roughly for the year 2005.
train_to,test_to = int(math.floor(len(X) * 0.5)), len(X)
# train and test only every fifth pattern, for performance.
train_step, test_step = 5, 5
X_train=X[:train_to:train_step]
y_train=y[:train_to:train_step]
X_test=X[train_to:test_to:test_step]
y_test=y[train_to:test_to:test_step]

"""
# Due to performance issues we use fixed parameters.
# For a real world scenerio we have to find optimal parameters
# for the SVR regressor.

cv_method = KFold(len(X[0:train_to:train_step]), 10)
gamma_range = [0.0001, 0.000001]
C_range = [2 ** i for i in range(1, 4, 1)]

tuned_parameters = [{
    'kernel': ['rbf'],
    'C': C_range,
    'gamma': gamma_range}]

# search for the best parameters with crossvalidation.
grid = GridSearchCV(SVR(kernel='rbf', epsilon = 0.1),\
    param_grid = tuned_parameters, cv=cv_method, verbose = 0)

grid.fit(X[0:train_to:train_step], Y[0:train_to:train_step])

# train a SVR regressor with best found parameters.
svr = SVR(kernel='rbf', epsilon=0.1, C = grid.best_estimator.C,\
    gamma = grid.best_estimator.gamma)
"""

# train a SVR regressor with best found parameters.
svr = SVR(kernel='rbf', epsilon=0.1, C = 100.0,\
    gamma = 0.0001)

# fitting the pattern-label pairs
svr.fit(X_train,y_train)

y_hat = svr.predict(X_test)

# naive is also known as persistence model.
naive_hat = zeros(len(y_hat), dtype = float32)
for i in range(0, len(y_hat)):
    # naive label is the label as horizon time steps before.
    # we have to consider to use only the fifth label here, too.
    naive_hat[i] = y[train_to + (i * test_step) - horizon]

# computing the mean squared errors of KNN and naive prediction.
mse_y_hat=mean_squared_error(y_test, y_hat)
mse_naive_hat=mean_squared_error(y_test, naive_hat)
print("MSE y_hat (KNN-Regressor): ", mse_y_hat)
print("MSE naive_hat (Persistence): ", mse_naive_hat)

with plt.style.context("fivethirtyeight"):
    figure = plt.figure(figsize=(8, 5))
    time = range(0, len(y_hat))
    plt.plot(time, y_test, label="Measurement")
    plt.plot(time, naive_hat, label="Naive Label")
    plt.plot(time, y_hat, label="SVR Label")
    plt.xlim([6600, 7000])
    plt.ylim([-5, 50])
    plt.xlabel("Time Steps")
    plt.ylabel("Wind Power [MW]")
    plt.legend()
    plt.tight_layout()
    plt.show()
