import unittest

from windml.datasets.nrel import NREL
from windml.visualization.show_flip_book import show_flip_book
from windml.visualization.show_coord_topo import show_coord_topo
from windml.visualization.show_coord_topo_turbine import show_coord_topo_turbine
from windml.visualization.show_coord_topo_zoom import show_coord_topo_zoom
from windml.visualization.plot_timeseries import plot_timeseries
from windml.visualization.plot_multiple_timeseries import plot_multiple_timeseries
from windml.visualization.plot_response_curve import plot_response_curve

class TestVisualization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ds = NREL()
        cls.turbine = ds.get_turbine(NREL.park_id['tehachapi'], 2004)
        cls.windpark = ds.get_windpark(NREL.park_id['tehachapi'], 3, 2004)

    def test_show_flip_book(self):
        show_flip_book(self.windpark, 4, 0, 4, show = False)

    def test_coord_topo(self):
        show_coord_topo(self.windpark, 'wind park topology', show = False)

    def test_coord_topo_turbine(self):
        show_coord_topo_turbine(self.turbine,  show = False)

    def test_coord_topo_zoom(self):
        show_coord_topo_zoom(self.windpark, show = False)

    def test_plot_timeseries(self):
        plot_timeseries(self.turbine, show = False)

    def test_plot_response_curve(self):
        plot_response_curve(self.turbine, show = False)

    def test_plot_timeseries(self):
        plot_multiple_timeseries(self.windpark, show = False)

if __name__ == '__main__':
    unittest.main()
