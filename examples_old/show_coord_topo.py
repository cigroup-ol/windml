"""
Example for Visualization of the Topography of a Wind Mill near Tehachapi
-------------------------------------------------------------------------

"""
from windml.datasets.windpark import get_nrel_windpark
from windml.visualization.show_coord_topo import show_coord_topo
from windml.datasets.park_definitions import park_info

#------------------------------------------------------------
# Define a smaller radius (do not use the default value)

radius = 5000
name = 'tehachapi'

my_windpark = get_nrel_windpark(park_info[name][0], radius)
print "Working on windpark around target mill", str(my_windpark.get_target_idx())
print "Plotting windpark ..."
show_coord_topo(my_windpark)
