"""
Topography of a Wind Windpark Near Tehachapi
-------------------------------------------------------------------------

This example shows the topography of a wind park near Tehachapi. The red dots
illustrate the locations of wind mills.
"""

from windml.datasets.nrel import NREL
from windml.visualization.show_coord_topo import show_coord_topo

radius = 30
name = 'tehachapi'

windpark = NREL().get_windpark(NREL.park_id['tehachapi'], 30, 2004)

print "Working on windpark around target mill", str(windpark.get_target_idx())
print "Plotting windpark ..."

show_coord_topo(windpark)
