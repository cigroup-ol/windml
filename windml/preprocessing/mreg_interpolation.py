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
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.svm import SVR
from sklearn import linear_model

import numpy as np
from numpy import zeros, int32, float32, nan, array
from builtins import range


class MRegInterpolation(object):

    #@todo highly experimental
    def multi_interpolate(self, timeseries, args):
        timestep = args['timestep']
        neighbor_series = args['neighbor_series']
        reg = args['reg']
        regargs = args['regargs']

        # order by damaged elements, ascending.
        mdf = MissingDataFinder()

        order = []
        for i in range(len(neighbor_series)):
            misses = mdf.find(neighbor_series[i], timestep)
            missing = sum(map(lambda m : m[2], misses)) #OK py3 compat
            order.append((i, missing - i))

        sorted(order, key = lambda o : o[1])
        merge_order = list(map(lambda o : o[0], order))

        data = neighbor_series

        for i in range(len(data)):
           data[i] = OverrideMissing().override(data[i], timestep, -1)

        field = 'corrected_score'

        ## algorithm
        merged = []
        for m in merge_order:
            mseries = data[m]
            regressors = {}
            pattern_size = {}
            useful = {}
            repairable = {}
            misses = []
            available_in_c = {}
            cnt_patterns = {}

            for i in range(len(mseries)):
                if(mseries[i][field] == -1):
                    if(i not in useful.keys()):
                        useful[i] = []

            for c in merge_order:
                if(c == m or c in merged):
                    continue # dont want merge with itself or merged
                cseries = data[c]
                cnt_patterns[c] = 0
                available_in_c[c] = []

                for i in range(len(mseries)):
                    if(mseries[i][field] == -1 and cseries[i][field] != -1):
                        if(i not in useful.keys()):
                            useful[i] = []
                        useful[i].append(c)
                        continue # cannot be used as pattern but for predicting
                    if(mseries[i][field] == -1 or cseries[i][field] == -1):
                       continue # cannot be used as a pattern
                    available_in_c[c].append(i)
                    cnt_patterns[c] += 1

            # now check which one has most patterns from candidates of useful
            for missing, candidates in useful.items():
                if(len(candidates) > 0): # we have candidates
                    highest_ps = 0
                    highest_candidate = None
                    for candidate in candidates:
                        if(cnt_patterns[candidate] > highest_ps):
                            highest_ps = cnt_patterns[candidate]
                            highest_candidate = candidate

                    labels, patterns = [], []
                    # use highest_candidate with merge
                    ### FITTING
                    for i in available_in_c[highest_candidate]:
                        labels.append(mseries[i][field])
                        pattern = []
                        pattern.append(data[highest_candidate][i][field])
                        for am in merged:
                            pattern.append(data[am][i][field])
                        patterns.append(pattern)
                    if reg == 'knn':
                        regargs = args['regargs']
                        neighbors = regargs['n']
                        variant = regargs['variant']
                        regressor = KNeighborsRegressor(neighbors, variant)
                    patterns = np.array(patterns)
                    
                    reg = regressor.fit(patterns, labels)

                    ### PREDICTION
                    pattern = []
                    pattern.append(data[highest_candidate][missing][field])
                    for am in merged:
                        pattern.append(data[am][missing][field])
                        
                    data[m][missing][field] = reg.predict(np.array(pattern).reshape(1, -1))
                else:   # we have no candidates, and we use merged here
                    ### FITTING
                    labels, patterns = [],[]
                    for i in range(len(mseries)):
                        if mseries[i][field] == -1:
                            continue
                        labels.append(mseries[i][field])
                        pattern = []
                        for am in merged:
                            pattern.append(data[am][i][field])
                        patterns.append(pattern)
                    if reg == 'knn':
                        regargs = args['regargs']
                        neighbors = regargs['n']
                        variant = regargs['variant']
                        regressor = KNeighborsRegressor(neighbors, variant)
                    patterns = np.array(patterns)
                    
                    reg = regressor.fit(patterns, labels)
                    ### PREDICTION
                    pattern = []
                    for am in merged:
                        pattern.append(data[am][missing][field])
                        
                    data[m][missing][field] = reg.predict(np.array(pattern).reshape(1, -1))

            merged.append(m)

        # we used the interpolated information of all turbines to interpolate
        # the missing data of the target turbine.
        ovtimeseries = OverrideMissing().override(timeseries, timestep, -1)

        labels, patterns = [], []
        for i in range(len(timeseries)):
            if(timeseries[i][field] != -1):
                labels.append(ovtimeseries[i][field])
            pattern = []
            for series in data:
                pattern.append(series[i][field])
            patterns.append(pattern)
        if(reg == 'knn'):
            regargs = args['regargs']
            neighbors = regargs['n']
            variant = regargs['variant']
            regressor = KNeighborsRegressor(neighbors, variant)
        patterns = np.array(patterns)
        
        regressor.fit(patterns, labels)

        for i in range(len(ovtimeseries)):
            if(ovtimeseries[i][field] == -1):
                pattern = []
                for series in data:
                    pattern.append(series[i][field])
                
                ovtimeseries[i][field] = regressor.predict(np.array(pattern).reshape(1, -1))

        return ovtimeseries

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
                return self.multi_interpolate(timeseries, args)

        ovtimeseries = OverrideMissing().override(timeseries, timestep, -1)

        for field in fields:
            X, Y = [], []

            for t in range(len(neighbor_series[0])):
                if(ovtimeseries[t][field] != -1):
                    Y.append(ovtimeseries[t][field])
                    pattern = []
                    for nseries in neighbor_series:
                        pattern.append(nseries[t][field])
                    X.append(pattern)

            Xa, Ya = array(X), array(Y)            
            if(reg == 'knn'):
                regargs = args['regargs']
                variant = regargs['variant']

                if('kfold' in regargs.keys()):
                    kfold = regargs['kfold']
                    ncandidates = regargs['n']

                    regressors = {}
                    best_n = ncandidates[0]
                    regressor = KNeighborsRegressor(best_n, variant)
                    regressors[best_n] = regressor
                    best_score = cross_val_score(regressor, Xa, Ya, cv=kfold).mean()

                    for n in ncandidates[1:]: # try every n and use cross validation
                        regressor = KNeighborsRegressor(n, variant)
                        regressors[n] = regressor
                        score = cross_val_score(regressor, Xa, Ya, cv=kfold).mean()
                        if(score > best_score):
                            best_n = n
                            best_score = score
                    regressor = regressors[best_n]
                else:
                    neighbors = regargs['n']
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

            for t in range(len(ovtimeseries)):
                if(ovtimeseries[t][field] == -1):                    
                    pattern = []
                    for nseries in neighbor_series:
                        pattern.append(nseries[t][field])
                        
                    y_hat = regressor.predict(array(pattern).reshape(1, -1))
                    if(len(y_hat.shape) > 0):
                        ovtimeseries[t][field] = y_hat[0]
                    else:
                        ovtimeseries[t][field] = y_hat

        return ovtimeseries
