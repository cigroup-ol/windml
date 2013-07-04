"""
Example: Flip-Book of wind speed around Tehachapi
-------------------------------------------------------------------------

"""
from windml.datasets.windpark import get_nrel_windpark
from windml.visualization.show_flip_book import show_flip_book
from windml.datasets.park_definitions import park_info

#------------------------------------------------------------

# Define a smaller radius (do not use the default value)

radius = 30
name = 'tehachapi'

my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004)
show_flip_book(my_windpark, 4, 3460, 6)
