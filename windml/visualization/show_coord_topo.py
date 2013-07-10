import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

def show_coord_topo(windpark, show = True):
    """Plot the topology of a given windpark

    Topographic Map with farms
    see: http://matplotlib.org/basemap/users/examples.html
    Basemap

    Parameters
    ----------

    windpark : Windpark
               A given windpark to show the topology.
    """

    plt.clf()

    mills = windpark.get_windmills()
    target = windpark.get_target()
    radius = windpark.get_radius()

    #pack latitude and longitude in lists
    rel_input_lat = []
    rel_input_lon = []
    for row in mills:
        rel_input_lat.append(np.float64(row.latitude))
        rel_input_lon.append(np.float64(row.longitude))

    targetcoord = [0.0, 0.0]
    targetcoord[0] = np.float64(target.latitude)
    targetcoord[1] = np.float64(target.longitude)

    graddiff = (radius/111.0) + 0.5  # degree in km

    m = Basemap(projection='stere', lon_0=targetcoord[1], lat_0=targetcoord[0],\
        llcrnrlon = targetcoord[1]-graddiff, llcrnrlat = targetcoord[0]-graddiff ,\
        urcrnrlon = targetcoord[1]+graddiff, urcrnrlat = targetcoord[0]+graddiff ,\
        rsphere=6371200., resolution = 'l', area_thresh=1000)

    # Target
    x_target,y_target = m(targetcoord[1],targetcoord[0])
    # Input Farms
    rel_inputs_lon, rel_inputs_lat = m(rel_input_lon, rel_input_lat)

    # labels = [left,right,top,bottom]
    parallels = np.arange(int(targetcoord[0]-3), int(targetcoord[0]+3), 1.)
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(int(targetcoord[1]-3), int(targetcoord[1]+3), 1.)
    m.drawmeridians(meridians,labels=[True,False,False,True])

    # plot farms in the radius
    m.plot(x_target, y_target, 'bo')
    m.plot(rel_inputs_lon, rel_inputs_lat, 'r*')

    #m.bluemarble()
    m.etopo()
    m.drawcoastlines()
    plt.title("Selected Wind Farms")

    if(show):
        plt.show()

