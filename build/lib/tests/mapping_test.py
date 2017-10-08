import unittest

from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from windml.mapping.power_diff_mapping import PowerDiffMapping

class TestMapping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ds = NREL()
        cls.turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004, 2005)
        cls.windpark = ds.get_windpark(NREL.park_id['tehachapi'], 3, 2004, 2005)
        cls.pmapping = PowerMapping()
        cls.pdmapping = PowerDiffMapping()

    def test_power_get_features_turbine(self):
        X = self.pmapping.get_features_turbine(self.turbine, 3, 3)
        assert(X[0][2] == X[1][1])
        assert(X[0][1] == X[1][0])

    def test_power_get_labels_turbine(self):
        Y = self.pmapping.get_labels_turbine(self.turbine, 3, 3)
        assert(len(Y) == 105259)

    def test_power_get_features_park(self):
        X = self.pmapping.get_features_park(self.windpark, 3, 3)
        assert(X.shape == (105259, 21))

    def test_power_get_labels_park(self):
        Y = self.pmapping.get_labels_park(self.windpark, 3, 3)
        assert(len(Y) == 105259)

    def test_power_diff_mapping_get_features_turbine(self):
        X = self.pdmapping.get_features_turbine(self.turbine, 3, 3)
        assert(X.shape == (105259, 5))

    def test_power_diff_mapping_get_labels_turbine(self):
        Y = self.pdmapping.get_labels_turbine(self.turbine, 3, 3)
        assert(len(Y) == 105259)

    def test_power_diff_mapping_get_features_park(self):
        X = self.pdmapping.get_features_park(self.windpark, 3, 3)
        assert(X.shape == (105259, 35))

    def test_power_get_labels_park(self):
        Y = self.pdmapping.get_labels_park(self.windpark, 3, 3)
        assert(len(Y) == 105259)

if __name__ == '__main__':
    unittest.main()
