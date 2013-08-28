import unittest

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

class TestPreprocessing(unittest.TestCase):
    def test_linear_interpolation(self):
        turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])
        timeseries = turbine.get_measurements()[24515:150000]
        t_hat = LinearInterpolation().interpolate(timeseries, timestep=300)
        misses = MissingDataFinder().find(t_hat, 300)
        assert(len(misses) < 1)

    def test_forward_copy_interpolation(self):
        turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])
        timeseries = turbine.get_measurements()[24515:150000]
        t_hat = ForwardCopy().interpolate(timeseries, timestep=300)
        misses = MissingDataFinder().find(t_hat, 300)
        assert(len(misses) < 1)

    def test_backward_copy_interpolation(self):
        turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])
        timeseries = turbine.get_measurements()[24515:150000]
        t_hat = BackwardCopy().interpolate(timeseries, timestep=300)
        misses = MissingDataFinder().find(t_hat, 300)
        assert(len(misses) < 1)

    def test_topological_interpolation(self):
        park_id = NREL.park_id['tehachapi']
        windpark = NREL().get_windpark(park_id, 10, 2004)
        target = windpark.get_target()
        timestep = 600
        measurements = target.get_measurements()[300:500]
        damaged = NMARDestroyer().destroy(measurements, percentage=.80,\
                min_length=10, max_length=100)

        tloc = (target.longitude, target.latitude)
        neighbors = windpark.get_turbines()[:-1]

        nseries = [t.get_measurements()[300:500] for t in neighbors]
        nlocs = [(t.longitude, t.latitude) for t in neighbors]

        tinterpolated = TopologicInterpolation().interpolate(\
                                    damaged, method="topologic",\
                                    timestep=timestep, location=tloc,\
                                    neighbor_series = nseries,\
                                    neighbor_locations = nlocs)
        misses = MissingDataFinder().find(tinterpolated, timestep)
        assert(len(misses) < 1)

    def test_mar_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged = MARDestroyer().destroy(timeseries, percentage=.50)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

    def test_marthres_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged = MARThresDestroyer().destroy(timeseries, percentage=.50,\
                lower_bound = 0, upper_bound = 20)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

    def test_nmar_destroyer(self):
        turbine = NREL().get_turbine(NREL.park_id['tehachapi'], 2004)
        timeseries = turbine.get_measurements()[:1000]
        damaged = NMARDestroyer().destroy(timeseries, percentage=.50,\
                min_length=10, max_length=50)
        misses = MissingDataFinder().find(damaged, 600)
        assert(len(misses) > 0)

if __name__ == '__main__':
    unittest.main()

