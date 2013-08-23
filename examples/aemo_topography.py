"""
Location of AEMO Turbines
-------------------------------------------------------------------------

The black dots illustrate the locations of the turbines. The red dot
illustrates the target windmill.
"""

# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from windml.datasets.aemo import AEMO
from windml.visualization.show_coord_topo import show_coord_topo

# see http://windfarmperformance.info/ for more information of the park
windpark = AEMO().get_windpark(AEMO.park_id['cathrock'], 3200)

print "Working on windpark around target mill", str(windpark.get_target_idx())
print "Plotting windpark ..."

title = "Turbines of AEMO Data Set"
show_coord_topo(windpark, title)
