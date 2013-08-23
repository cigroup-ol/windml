import unittest

from windml.datasets.aemo import AEMO
from windml.preprocessing.missing_data_finder import MissingDataFinder
from windml.preprocessing.linear_interpolation import LinearInterpolation

class TestAEMO(unittest.TestCase):
    def test_linear_interpolation(self):
        turbine = AEMO().get_turbine(AEMO.park_id['cathrock'])
        timeseries = turbine.get_measurements()[24515:150000]
        t_hat = LinearInterpolation().interpolate(timeseries, timestep=300)
        misses = MissingDataFinder().find(t_hat, 300)
        assert(len(misses) < 1)
if __name__ == '__main__':
    unittest.main()

