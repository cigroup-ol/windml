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

import unittest

from windml.preprocessing.nrel_repair import NRELRepair
from windml.datasets.aemo import AEMO
from windml.datasets.nrel import NREL
from windml.preprocessing.missing_data_finder import MissingDataFinder
from windml.preprocessing.linear_interpolation import LinearInterpolation
from windml.preprocessing.mar_destroyer import MARDestroyer
from windml.preprocessing.nmar_destroyer import NMARDestroyer
from windml.preprocessing.marthres_destroyer import MARThresDestroyer
from windml.preprocessing.topologic_interpolation import TopologicInterpolation
from windml.preprocessing.forward_copy import ForwardCopy
from windml.preprocessing.backward_copy import BackwardCopy
from windml.preprocessing.mreg_interpolation import MRegInterpolation
from sklearn.neighbors import KNeighborsRegressor

#@todo every interpolation method test with nmar, mar_thres, mar.
class TestPreprocessing(unittest.TestCase):
    def test_nrel_repair(self):
        ds = NREL()
        target = ds.get_turbine(NREL.park_id['tehachapi'], 2005)
        measurements = target.get_measurements()[:43504]
        measurements = NRELRepair().repair(measurements)
        assert(NRELRepair().validate(measurements))

    def test_mreg_interpolation_multi(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 3, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:350]
        damaged, indices = MARDestroyer().destroy(measurements, percentage=.50)
        before_misses = MissingDataFinder().find(damaged, timestep)
        neighbors = windpark.get_turbines()[:-1]
        count_neighbors = len(neighbors)
        reg = 'knn' # KNeighborsRegressor(10, 'uniform')
        regargs = {'n' : 10, 'variant' : 'uniform'}

        processed = 0
        missed = {k : count_neighbors for k in indices}
        exclude = []
        damaged_nseries = []

        for neighbor in neighbors:
            nseries = neighbor.get_measurements()[300:350]
            damaged, indices = MARDestroyer().destroy(nseries, percentage=.50, exclude=exclude)

            for index in indices:
                if(index not in missed.keys()):
                    missed[index] = count_neighbors
                missed[index] -= 1
                if(missed[index] == 1):
                    exclude.append(index) # exclude in next iterations
            damaged_nseries.append(damaged)

        t_hat = MRegInterpolation().interpolate(damaged, timestep=timestep,\
            neighbor_series=damaged_nseries, reg=reg, regargs=regargs)

        after_misses = MissingDataFinder().find(t_hat, timestep)
        assert(len(after_misses) < 1)

    def test_mreg_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 3, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged, indices = MARDestroyer().destroy(measurements, percentage=.50)
        before_misses = MissingDataFinder().find(damaged, timestep)
        neighbors = windpark.get_turbines()[:-1]

        reg = 'knn' # KNeighborsRegressor(10, 'uniform')
        regargs = {'n' : 10, 'variant' : 'uniform'}

        nseries = [t.get_measurements()[300:500] for t in neighbors]
        t_hat = MRegInterpolation().interpolate(damaged, timestep=timestep,\
            neighbor_series=nseries, reg=reg, regargs=regargs)
        after_misses = MissingDataFinder().find(t_hat, timestep)
        assert(len(after_misses) < 1)

    def test_linear_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 10, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged, indices = MARDestroyer().destroy(measurements, percentage=.50)
        before_misses = MissingDataFinder().find(damaged, timestep)
        t_hat = LinearInterpolation().interpolate(damaged, timestep=timestep)
        after_misses = MissingDataFinder().find(t_hat, timestep)

        assert(measurements.shape[0] == t_hat.shape[0])
        assert(len(after_misses) < 1)

    def test_forward_copy_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 10, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged, indices = MARDestroyer().destroy(measurements, percentage=.50)
        before_misses = MissingDataFinder().find(damaged, timestep)
        t_hat = ForwardCopy().interpolate(measurements, timestep=timestep)
        after_misses = MissingDataFinder().find(t_hat, timestep)

        assert(measurements.shape[0] == t_hat.shape[0])
        assert(len(after_misses) < 1)

    def test_backward_copy_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 10, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged, indices = MARDestroyer().destroy(measurements, percentage=.50)
        before_misses = MissingDataFinder().find(damaged, timestep)
        t_hat = BackwardCopy().interpolate(measurements, timestep=timestep)
        after_misses = MissingDataFinder().find(t_hat, timestep)

        assert(measurements.shape[0] == t_hat.shape[0])
        assert(len(after_misses) < 1)

    def test_topological_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 10, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged, indices = NMARDestroyer().destroy(measurements, percentage=.80,\
                min_length=10, max_length=100)

        tloc = (target.longitude, target.latitude)
        neighbors = windpark.get_turbines()[:-1]

        nseries = [t.get_measurements()[300:500] for t in neighbors]
        nlocs = [(t.longitude, t.latitude) for t in neighbors]

        t_hat = TopologicInterpolation().interpolate(\
                                    damaged, method="topologic",\
                                    timestep=timestep, location=tloc,\
                                    neighbor_series = nseries,\
                                    neighbor_locations = nlocs)
        misses = MissingDataFinder().find(t_hat, timestep)

        assert(measurements.shape[0] == t_hat.shape[0])
        assert(len(misses) < 1)

    def test_mar_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged, indices = MARDestroyer().destroy(timeseries, percentage=.50)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

    def test_marthres_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged, indices = MARThresDestroyer().destroy(timeseries, percentage=.50,\
                lower_bound = 0, upper_bound = 20)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

    def test_nmar_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged, indices = NMARDestroyer().destroy(timeseries, percentage=.50,\
                min_length=10, max_length=50)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

if __name__ == '__main__':
    unittest.main()

