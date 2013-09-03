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

from numpy import zeros, int32, float32, nan, array

class MRegInterpolation(object):
    def interpolate(self, timeseries, **args):
        cs = 'corrected_score'
        sp = 'speed'
        date = 'date'

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

        X, Y = [], []
        for t in xrange(len(neighbor_series[0])):
            if(ovtimeseries[t][cs] != -1):
                Y.append([ovtimeseries[t][cs], ovtimeseries[t][sp]])
                pattern = []
                for nseries in neighbor_series:
                    pattern.append(nseries[t][cs])
                for nseries in neighbor_series:
                    pattern.append(nseries[t][sp])
                X.append(pattern)

        Xa, Ya = array(X), array(Y)
        reg.fit(Xa,Ya)

        for t in xrange(len(ovtimeseries)):
            if(ovtimeseries[t][cs] == -1):
                pattern = []
                for nseries in neighbor_series:
                    pattern.append(nseries[t][cs])
                for nseries in neighbor_series:
                    pattern.append(nseries[t][sp])
                y_hat = reg.predict(array(pattern))
                ovtimeseries[t][cs] = y_hat[0][0]
                ovtimeseries[t][sp] = y_hat[0][1]

        return ovtimeseries
