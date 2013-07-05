"""
Example: Optimizing Variance of Topologic Weighting
-------------------------------------------------------------
"""

from windml.datasets.windmill import get_nrel_windmill
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data_aggregated import get_feature_and_label_data_aggregated
from windml.datasets.park_definitions import park_info
from windml.util.distance import distance
from windml.util.feature_assembly import FeatureAssembly
from windml.optimization.one_plus_one_ea import OnePlusOneEA

from numpy import zeros, exp, sqrt
from scipy.stats import norm
import math
import matplotlib.pyplot as plt

name = 'tehachapi'

def algorithm(args):

    target = args['target_id']
    radius = args['radius']
    mean = args['mean']
    std = args['std']
    k = args['k']
    feature_window = args['feature_window']
    horizon = args['horizon']

    my_windpark1 = get_nrel_windpark(target, radius, 2004, 2005)
    target = get_nrel_windmill(target, 2004, 2005)
    windmills = my_windpark1.get_windmills()

    # topologic weighting
    func = lambda x : norm.pdf(x, scale = std)
    distances = [(wm, distance(wm, target)) for wm in windmills]
    weights = map(lambda (wm, dist) : (wm, func(dist)), distances)
    normfac = sum(map(lambda (wm, weight) : weight, weights))
    weights = map(lambda (wm, weight) : (wm, (weight / normfac)), weights)

    # feature assembly
    fa = FeatureAssembly(windmills)
    weights = map(lambda t : t[1], weights)
    X = fa.X('corrected_score', 3, 3, weights)
    Y = fa.Y(target, 3, 3)

    ### KNN regression
    train_to=int(math.floor(len(X)*0.1))
    test_to = train_to+28800
    train_step=1

    """ # GPU todo
    try:
        from windml.ml.knn_regressor_gpu import KNNRegressorGPU
        knn = KNNRegressorGPU(k, 'uniform')
        from sklearn import neighbors
        knn = neighbors.KNeighborsRegressor(k, 'uniform')
    except ImportError:
    from sklearn import neighbors
    """
    from sklearn import neighbors

    knn = neighbors.KNeighborsRegressor(k, 'uniform')
    reg = knn.fit(X[0:train_to:train_step],Y[0:train_to:train_step])
    y_ = reg.predict(X[train_to:test_to])

    # calculate error
    naive = []
    times = []
    for i in range(0, test_to-train_to):
        times.append(i)
        naive.append(Y[i+train_to-horizon])

    sum_err_pred = 0.0
    sum_err_naiv = 0.0
    for i in range(0, test_to-train_to):
        sum_err_pred += (y_[i] - Y[i + train_to]) ** 2
        sum_err_naiv += (naive[i] - Y[i + train_to]) ** 2

    print "pred", sum_err_pred
    print "naive", sum_err_naiv

    return sum_err_pred

args = {
    'target_id': park_info['tehachapi'][0],\
    'radius': 15.0,\
    'mean': 0.0,\
    'k': 25,\
    'feature_window': 3,\
    'horizon': 3}

opt = OnePlusOneEA()
result = opt.minimize('std', 3.0, 10.0, [0.0, 15.0], 50, args, algorithm)

X = opt.logger.all()['offspring']
Y = opt.logger.all()['error']

plt.scatter(X,Y, color="g")
plt.show()

print "best std %f best error %f" % result
