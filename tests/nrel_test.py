import unittest

from windml.datasets.nrel import NREL

class TestNREL(unittest.TestCase):
    def test_get_windmill(self):
        ds = NREL()
        target = ds.get_windmill(NREL.park_id['tehachapi'], 2004, 2005)
        t = target.get_measurements()[0]
        assert(len(t) == 3)

    def test_get_windpark(self):
        ds = NREL()
        windpark = ds.get_windpark(NREL.park_id['tehachapi'], 10, 2004, 2005)
        assert(len(windpark.mills) == 66)

if __name__ == '__main__':
    unittest.main()
