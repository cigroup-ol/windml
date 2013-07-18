"""
.. _example_linear_regression:

Linear Regression for a Windmill with Neighbor-Windmills
-------------------------------------------------------------------------

Linear Regression for forecasting a time series for a certain windmill. The
forecasting of the windmill is based on its own time series and the time series
of neighbored windmills. The neighborhood is defined by a windpark, which
itself is defined by the spatial extent.

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

from numpy import zeros, float32
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping

from sklearn.grid_search import GridSearchCV
from sklearn import linear_model

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

# fitting the pattern-label pairs
reg = linear_model.LinearRegression()
reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
y_hat = reg.predict(X[train_to:test_to:test_step])

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

print "MSE y_hat (Linear-Regressor): ", mse_y_hat
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
plt.plot(time, y_hat, "r-", label="Linear Label")
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
plt.plot(time, (y_hat - y), "r-", label="Linear Label")
plt.plot(time, (naive_hat - y), "b-", label="Naive Label")
plt.xlim([9600, 9750])
plt.ylim([-20, 30])
plt.legend()

plot_scatter = plt.subplot(2, 2, 4)
plt.title("Linear Label and True Measurement")
col = abs(y - y_hat)
plt.scatter(y, y_hat, c=col, linewidth=0.0, cmap=plt.cm.jet)
plt.xlabel("Y")
plt.ylabel("Linear Label")
plt.xlim([0, 30])
plt.ylim([0, 30])

plt.show()


