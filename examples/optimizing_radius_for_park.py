"""
Example: Optimizing Outer Radius for a Park (KNN Regression)
-------------------------------------------------------------

This example optimizizes the radius of the chosen trainingset
by a (1+1)-EA in a feasible interval of solutions. Each fitness
function evaluation is a training of a KNN-regressor with 18 months
and tested on 6 months.
"""

from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data_aggregated import get_feature_and_label_data_aggregated
from windml.datasets.park_definitions import park_info
from windml.optimization.one_plus_one_ea import OnePlusOneEA 

from sklearn import neighbors
import math
import matplotlib.pyplot as plt

name = 'tehachapi'
k_neighbors = 25
feature_window = 3
horizon = 3

my_windpark1 = get_nrel_windpark(park_info[name][0], 10, 2004, 2005)
X_remove,Y = get_feature_and_label_data_aggregated(my_windpark1,feature_window,horizon)

def algorithm(args):
    name = 'tehachapi'
    radius1 = args['radius']
    k_neighbors = 25
    feature_window = 3
    horizon = 3

    my_windpark1 = get_nrel_windpark(park_info[name][0], radius1, 2004, 2005)
    X,Y_remove = get_feature_and_label_data_aggregated(my_windpark1,feature_window,horizon)

    number = len(my_windpark1.mills)

    #knn regression
    knn = neighbors.KNeighborsRegressor(k_neighbors, 'uniform')
    train_to=int(math.floor(len(X)*0.1))
    test_to = train_to+28800
    train_step=1

    reg = knn.fit(X[0:train_to:train_step],Y[0:train_to:train_step])
    y_ = reg.predict(X[train_to:test_to])

    sum_err_pred = 0.0
    for i in range(0, test_to-train_to):
        sum_err_pred+=(y_[i]-Y[i+train_to])**2
    print "sum of square err of prediction", sum_err_pred

    return sum_err_pred
opt = OnePlusOneEA()
best_radius, best_error = opt.minimize('radius', 5.0, 5.0, [0, 50], 30, {}, algorithm)
print "best radius is %f and best sum of square err of prediction is %f" % (best_radius, best_error)
