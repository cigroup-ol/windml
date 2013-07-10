"""
Flip-Book of Wind Speed Around Tehachapi
-------------------------------------------------------------------------
"""

from windml.datasets.nrel import NREL
from windml.visualization.show_flip_book import show_flip_book

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 30, 2004)
show_flip_book(windpark, 4, 3460, 2)

