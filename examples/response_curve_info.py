"""
Response Curve of a Turbine
--------------------------------------------------

This example illustrates the relationship between the wind speed and the generated
power. The response curve is fitted via a K-nearest neighbor regression. Finally,
the probabilty of cut-out events is shown.


"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# License: BSD 3 clause

from matplotlib import dates
import matplotlib.pylab as plt
import datetime, time
import numpy as np

from numpy import array, matrix
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn import __version__ as sklearn_version
from sklearn.svm import SVR

from sklearn.neighbors import KNeighborsRegressor
from windml.datasets.nrel import NREL
from windml.visualization.plot_response_curve import plot_response_curve


ds = NREL()
turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004, 2006)
timeseries = turbine.get_measurements()
max_speed = 40
skip = 1


# plot true values as blue points
speed = [m[2] for m in timeseries[::skip]]
score = [m[1] for m in timeseries[::skip]]


# Second Plot: KNN-Interpolation
# Built patterns und labels
X_train = speed[0:len(speed):1]
Y_train = score[0:len(score):1]
X_train_array = array([[element] for element in X_train])

# initialize KNN regressor from sklearn.
k_neighbors = 20
knn = KNeighborsRegressor(k_neighbors, 'uniform')
# fitting the pattern-label pairs
T = np.linspace(0, max_speed, 500)[:, np.newaxis]
Y_hat = knn.fit(X_train_array, Y_train).predict(T)


# Last Plot
start_speed = 15
threshold = 25
elements = max_speed-start_speed

num_over_thres = np.zeros((elements), dtype=np.int)
num_below_thres = np.zeros((elements), dtype=np.int)

for i in range(len(X_train)):
    elem = 0
    for j in range(start_speed, max_speed):
        act_value = np.float32(j)
        if (X_train[i] >= (act_value) and X_train[i] < (act_value+1)):
            if (Y_train[i] < threshold):
                num_below_thres[elem] += 1
            else:
                num_over_thres[elem] += 1
        elem += 1


fraction = np.zeros(max_speed, dtype=np.float32)
for i in range(start_speed, len(fraction)):
    if (np.float32(num_below_thres[i-start_speed]+num_over_thres[i-start_speed]) > 0):
        fraction[i] = np.float32(num_below_thres[i-start_speed])/(num_below_thres\
            [i-start_speed]+num_over_thres[i-start_speed])
    else:
        fraction[i] = -1
print fraction



figure = plt.figure(figsize=(15, 10))
plot_abs = plt.subplot(2, 2, 1)
plt.title("Measurements")
plt.scatter(speed, score, color="b")
plt.xlim([-1, max_speed])
plt.xlabel("Windspeed [m/s]")
plt.ylim([-2, 32])
plt.ylabel("Correct Score [MW]")

plot_scatter = plt.subplot(2, 2, 2)
plt.title("KNN Interpolation of the Response Curve")
plt.plot(T, Y_hat, color='b')
plt.scatter(speed, score, color="#CCCCCC")
plt.xlim([-1, max_speed])
plt.xlabel("Windspeed [m/s]")
plt.ylim([-2, 32])
plt.ylabel("Correct Score [MW]")

plot_abs = plt.subplot(2, 2, 3)
plt.title("Distribution of Wind Speeds")
plt.hist( X_train, bins=np.float(max_speed), histtype='stepfilled', \
    normed=True, color='b')
plt.xlim([-1, max_speed])
plt.ylim(-0.01, 0.13)
plt.xlabel("Windspeed [m/s]")
plt.ylabel("Relative Frequency")

plot_scatter = plt.subplot(2, 2, 4)
plt.title("Frequency of Cut-Outs")
steps = range(40)
plt.plot(steps, fraction, "o", color='b')
plt.xlim([-1,max_speed])
plt.xlabel("Windspeed [m/s]")
plt.ylim([-0.1, 1.1])
plt.ylabel("Probabilty of Cut-Out Events (Thres = 15)")

plt.show()


