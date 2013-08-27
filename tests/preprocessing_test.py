import unittest

from windml.datasets.aemo import AEMO
from windml.datasets.nrel import NREL
from windml.preprocessing.missing_data_finder import MissingDataFinder
from windml.preprocessing.linear_interpolation import LinearInterpolation
from windml.preprocessing.mar_destroyer import MARDestroyer
from windml.preprocessing.nmar_destroyer import NMARDestroyer
from windml.preprocessing.marthres_destroyer import MARThresDestroyer

class TestAEMO(unittest.TestCase):
    def test_linear_interpolation(self):
        turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])
        timeseries = turbine.get_measurements()[24515:150000]
        t_hat = LinearInterpolation().interpolate(timeseries, timestep=300)
        misses = MissingDataFinder().find(t_hat, 300)
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

