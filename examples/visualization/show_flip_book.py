"""
Flip-Book of Wind Speed
-------------------------------------------------------------------------

This example illustrates the wind speed of the turbines in the park
'tehachapi'. The figures visualize the wind situation at four different times
(with a difference of 20 min). The turbines are colorized with regard to the
wind strengths (from strong in red to low in blue).
"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# License: BSD 3 clause

from windml.datasets.nrel import NREL
from windml.visualization.show_flip_book import show_flip_book

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 30, 2004)
show_flip_book(windpark, 4, 3460, 2)

