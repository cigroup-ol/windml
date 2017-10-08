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
from numpy import zeros, int32, float32, nan
from builtins import range

class TopologicInterpolation(object):
    def interpolate(self, timeseries, **args):
        cs = 'corrected_score'
        sp = 'speed'
        date = 'date'

        timestep = args['timestep']
        location = args['location']
        neighbor_series = args['neighbor_series']
        neighbor_locations = args['neighbor_locations']

        # override missing on neighbors
        lnseries = len(neighbor_series)
        ov_neighbor_series = []
        ovm = OverrideMissing()
        for i in range(lnseries):
            ov_series = ovm.override(neighbor_series[i], timestep, -1)
            ov_neighbor_series.append(ov_series)

        # find missing data on target
        finder = MissingDataFinder()
        new_amount = timeseries.shape[0]
        misses = finder.find(timeseries, timestep)

        # calucating distances
        distances = []
        for i in range(0, len(neighbor_series)):
            d = haversine(location, neighbor_locations[i])
            if d == 0:
                raise Exception("distance is 0.")
            distances.append(d)

        # index start indices
        starts = {}
        for start, end, amount in misses:
            new_amount += int(amount)
            starts[start] = [int(end), int(amount)]

        # allocate new numpy array
        new_mat = zeros((new_amount,),\
                dtype=[('date', int32),\
                       ('corrected_score', float32),\
                       ('speed', float32)])

        keys = starts.keys()
        current_index = 0

        for i in range(len(timeseries)):
            if i in keys:
            # missing data starting
                # add start measurement
                new_mat[current_index] = timeseries[i]
                current_index += 1

                end, n = starts[i]
                n = int(n)    
                w_hat_k = {}
                for j in range(1, n + 1):
                    candidates = []
                    sum_of_w_hat = 0
                    sum_of_distances = 0

                    # search for candidates with no missing data
                    for k in range(len(ov_neighbor_series)):
                        nseries = ov_neighbor_series[k]
                        if(nseries[i + j][cs] != -1):
                            candidates.append(k)
                            sum_of_distances += distances[k]

                    # if no candidates available copy old data
                    if (len(candidates) == 0):
                        y = timeseries[i][cs]
                        new_timestep = timeseries[i][d] + j * timestep
                        new_mat[current_index] = (new_timestep, y, nan)
                        current_index += 1
                    else:
                        # calculate weight and sum, for later use in
                        # anti-proportional
                        for k in candidates:
                            w_hat_k[k] = 1.0 / (distances[k] / sum_of_distances)
                            sum_of_w_hat += w_hat_k[k]

                        # calculation of label
                        y = 0
                        ws = 0
                        for k in candidates:
                            # w_k is anti-proportional
                            w_k = w_hat_k[k] / sum_of_w_hat
                            y_k = w_k * ov_neighbor_series[k][i + j][cs]
                            ws_k = w_k * ov_neighbor_series[k][i + j][sp]
                            y += y_k
                            ws += ws_k

                        new_timestep = timeseries[i][date] + j * timestep
                        new_mat[current_index] = (new_timestep, y, ws)
                        current_index += 1
            else: # if not missing
                new_mat[current_index] = timeseries[i]
                current_index += 1

        return new_mat
