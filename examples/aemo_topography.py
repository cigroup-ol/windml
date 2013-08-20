"""
Topography of a Wind Windpark
-------------------------------------------------------------------------

This example shows the topography of a wind park near Tehachapi. The red dots
illustrate the locations of wind mills.
"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.datasets.aemo import AEMO
from windml.visualization.show_coord_topo import show_coord_topo

windpark = AEMO().get_windpark(5, 3200)

print "Working on windpark around target mill", str(windpark.get_target_idx())
print "Plotting windpark ..."

title = "Turbines of AEMO Data Set"
show_coord_topo(windpark, title)
