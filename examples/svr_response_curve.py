"""
Learn a Response Curve of a Windmill with SVR
--------------------------------------------------
This example learns the response curve of a windmill near Tehachapi.
"""

from matplotlib import dates
import matplotlib.pylab as plt
import datetime, time

from numpy import array, matrix
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn import __version__ as sklearn_version
from sklearn.svm import SVR

from windml.datasets.nrel import NREL
from windml.visualization.plot_response_curve import plot_response_curve

ds = NREL()
windmill = ds.get_windmill(NREL.park_id['tehachapi'], 2004)
timeseries = windmill.get_measurements()
skip = 10

# plot true values
X = [m[2] for m in timeseries[::skip]]
Y = [m[1] for m in timeseries[::skip]]
plt.scatter(X, Y, color="#CCCCCC")

amount = len(timeseries)
speed = matrix([[m[2]] for m in timeseries[::skip]])
score = array([m[1] for m in timeseries[::skip]])

"""
# Due to performance issues we use fixed parameters
# for a real world scenerio we have to find optimal parameters
# for the SVR regressor.

cv_method = KFold(amount, 10)
gamma_range = [0.0001, 0.000001]
C_range = [2 ** i for i in range(1, 4, 1)]

tuned_parameters = [{
    'kernel': ['rbf'],
    'C': C_range,
    'gamma': gamma_range}]

# search for the best parameters with crossvalidation.
grid = GridSearchCV(SVR(kernel='rbf', epsilon = 0.1),\
    param_grid = tuned_parameters, cv=cv_method, verbose = 0)

grid.fit(speed, score)

# train a SVR regressor with best found parameters.
svr = SVR(kernel='rbf', epsilon=0.1, C = grid.best_estimator.C,\
    gamma = grid.best_estimator.gamma)
"""

# train a SVR regressor with best found parameters.
svr = SVR(kernel='rbf', epsilon=0.1, C = 100.0,\
    gamma = 0.001)

# fitting the pattern-label pairs
svr.fit(speed, score)

speeds = sorted([m[2] for m in timeseries[::skip]])
speeds_X = array([[speed] for speed in speeds])
score_hat = svr.predict(speeds_X)

plt.title("SVR Regression of a Response Curve")
plt.plot(speeds, score_hat)
plt.xlim([0,25])
plt.xlabel("Windspeed [m/s]")
plt.ylim([-5, 35])
plt.ylabel("Correct Score [MW]")
plt.show()
