"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from windml.util.distance import haversine
from windml.preprocessing.missing_data_finder import MissingDataFinder
from windml.preprocessing.override_missing import OverrideMissing

from sklearn.neighbors import KNeighborsRegressor
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import KFold
from sklearn.svm import SVR
from sklearn import linear_model

from numpy import zeros, int32, float32, nan, array

class MRegInterpolation(object):
    def interpolate(self, timeseries, **args):
        cs = 'corrected_score'
        sp = 'speed'
        date = 'date'
        fields = ['corrected_score', 'speed']

        timestep = args['timestep']
        neighbor_series = args['neighbor_series']
        reg = args['reg']

        # override missing on neighbors
        lnseries = len(neighbor_series)
        # if neighbor missing raise exception
        for nseries in neighbor_series:
            misses = MissingDataFinder().find(nseries, timestep)
            if(len(misses) > 0):
                print misses
                raise Exception("missing data in neighbors")

        ovtimeseries = OverrideMissing().override(timeseries, timestep, -1)

        for field in fields:
            X, Y = [], []

            for t in xrange(len(neighbor_series[0])):
                if(ovtimeseries[t][field] != -1):
                    Y.append(ovtimeseries[t][field])
                    pattern = []
                    for nseries in neighbor_series:
                        pattern.append(nseries[t][field])
                    X.append(pattern)

            Xa, Ya = array(X), array(Y)

            if(reg == 'knn'):
                regargs = args['regargs']
                neighbors = regargs['n']
                variant = regargs['variant']
                regressor = KNeighborsRegressor(neighbors, variant)
            elif(reg == 'linear_model'):
                regressor = linear_model.LinearRegression()
            elif(reg == 'svr'):
                regargs = args['regargs']

                if(regargs['cv_method'] == 'kfold'):
                    fold = regargs['cv_args']['k_folds']
                    pattern_count = Xa.shape[0]
                    cv_method = KFold(pattern_count, fold)
                else:
                    raise Exception("not implemented")

                # search for the best parameters with crossvalidation.
                kernel, epsilon, tuned_parameters =\
                    regargs['kernel'], regargs['epsilon'], regargs['tuned_parameters']
                grid = GridSearchCV(SVR(kernel = kernel, epsilon = epsilon),\
                    param_grid = tuned_parameters, cv=cv_method, verbose = 0)

                grid.fit(Xa, Ya)

                # train a SVR regressor with best found parameters.
                regressor = SVR(kernel=kernel, epsilon=0.1, C = grid.best_params_['C'],\
                    gamma = grid.best_params_['gamma'])

                # if regressor hook function specified, call hook
                if('reghook' in args.keys()):
                    args['reghook'](regressor)
            else:
                raise Exception("No regressor selected.")

            regressor.fit(Xa,Ya)

            for t in xrange(len(ovtimeseries)):
                if(ovtimeseries[t][field] == -1):
                    pattern = []
                    for nseries in neighbor_series:
                        pattern.append(nseries[t][field])
                    y_hat = regressor.predict(array(pattern))
                    if(len(y_hat.shape) > 0):
                        ovtimeseries[t][field] = y_hat[0]
                    else:
                        ovtimeseries[t][field] = y_hat

        return ovtimeseries
