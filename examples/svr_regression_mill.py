"""
SVR Regression for a Windmill with Neighbor-Windmills
-------------------------------------------------------------------------

.. _example_svr_regression:

Support Vector Regression for forecasting a time series for a certain windmill.
The forecasting of the windmill is based on its own time series and the time
series of neighbored windmills. The neighborhood is defined by a windpark,
which itself is defined by the spatial extent.

In this example the windmill 'tehachapi' is the target for forecasting.
Hence, the windpark center id 'tehachapi' is used. To define the neighborhood,
the spatial extent of 3 kilometers is chosen. For the mapping of pattern-label
combinations the :ref:`powermapping` is used. The power mapping is based on the
:ref:`generaltimeseriesmodel`. The feature window is 3 elements of every time
series, and the time (forecast) horizon is 3 elements of every time series as
well. Because of performance issues, in this example only the fifth element is
trained and tested.

The top left plot shows absolute pattern and label values of the actual
measurements and the forecast and the naive prediction model. The bottom left
plot illustrated the difference between the forecast and the true measurements.
On the right hand side two scatter plots show the measurements pairs of
forecast and true measurement with both forecasting models.
"""

import math
import matplotlib.pyplot as plt

from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn import __version__ as sklearn_version
from sklearn.svm import SVR

from numpy import zeros, float32
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from sklearn.neighbors import KNeighborsRegressor

# get windpark and corresponding target. forecast is for the target windmill
park_id = NREL.park_id['tehachapi']
windpark = NREL().get_windpark(park_id, 3, 2004, 2005)
target = windpark.get_target()

# use power mapping for pattern-label mapping. Feature window length is 3 time
# steps and time horizon (forecast) is 3 time steps.
feature_window = 3
horizon = 3
mapping = PowerMapping()
X = mapping.get_features_park(windpark, feature_window, horizon)
Y = mapping.get_labels_mill(target, feature_window, horizon)

# train roughly for the year 2004.
train_to = int(math.floor(len(X) * 0.5))

# test roughly for the year 2005.
test_to = len(X)

# train and test only every fifth pattern, for performance.
train_step, test_step = 5, 5

"""
# Due to performance issues we use fixed parameters
# for a real world scenerio we have to find optimal parameters
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
svr.fit(X[0:train_to:train_step], Y[0:train_to:train_step])

y_hat = svr.predict(X[train_to:test_to:test_step])

# naive is also known as persistance model.
naive_hat = zeros(len(y_hat), dtype = float32)
for i in range(0, len(y_hat)):
    # naive label is the label as horizon time steps before.
    # we have to consider to use only the fifth label here, too.
    naive_hat[i] = Y[train_to + (i * test_step) - horizon]

# computing the mean squared errors of SVR and naive prediction.
mse_y_hat, mse_naive_hat = 0, 0
for i in range(0, len(y_hat)):
    y = Y[train_to + (i * test_step)]
    mse_y_hat += (y_hat[i] - y) ** 2
    mse_naive_hat += (naive_hat[i] - y) ** 2

mse_y_hat /= float(len(y_hat))
mse_naive_hat /= float(len(y_hat))

print "MSE y_hat (SVR-Regressor): ", mse_y_hat
print "MSE naive_hat (Persistence): ", mse_naive_hat

figure = plt.figure(figsize=(15, 10))

plot_abs = plt.subplot(2, 2, 1)
plt.title("Absolute Labels and True Measurements")

# Array of true labels for plotting.
y = zeros(len(y_hat))
for i in range(0, len(y_hat)):
    y[i] = (Y[train_to + (i * test_step)])

time = range(0, len(y_hat))
plt.plot(time, y, "g-", label="Measurement")
plt.plot(time, y_hat, "r-", label="SVR Label")
plt.plot(time, naive_hat, "b-", label="Naive Label")
plt.xlim([9600, 9750])
plt.ylim([-30, 50])
plt.legend()

plot_scatter = plt.subplot(2, 2, 2)
plt.title("Naive Label and True Measurement")
col = abs(y - naive_hat)
plt.scatter(y, naive_hat, c=col, linewidth=0.0, cmap=plt.cm.jet)
plt.xlabel("Y")
plt.ylabel("Naive Label")
plt.xlim([0, 30])
plt.ylim([0, 30])

plot_abs = plt.subplot(2, 2, 3)
plt.title("Absolute Difference")
plt.plot(time, (y_hat - y), "r-", label="SVR Label")
plt.plot(time, (naive_hat - y), "b-", label="Naive Label")
plt.xlim([9600, 9750])
plt.ylim([-20, 30])
plt.legend()

plot_scatter = plt.subplot(2, 2, 4)
plt.title("SVR Label and True Measurement")
col = abs(y - y_hat)
plt.scatter(y, y_hat, c=col, linewidth=0.0, cmap=plt.cm.jet)
plt.xlabel("Y")
plt.ylabel("SVR Label")
plt.xlim([0, 30])
plt.ylim([0, 30])
# y_hat (SVR) might be greater than 30 and smaller than 0.

plt.show()


