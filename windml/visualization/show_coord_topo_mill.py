"""
Example of visualiszing the topographie around a mill
--------------------------------------------------

... get_ids, visualization, todo

"""
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

def show_coord_topo_mill(windmill):
    radius = 20
    coord = [0.0, 0.0]
    coord[0] = np.float64(windmill.latitude)
    coord[1] = np.float64(windmill.longitude)
    print coord[1]
    # Topographic Map with farms
    #see: http://matplotlib.org/basemap/users/examples.html
    # Basemap
    graddiff = (radius/111.0) + 0.5  # degree in km

    m = Basemap(projection='stere', lon_0=coord[1], lat_0=coord[0],\
        llcrnrlon = coord[1]-graddiff, llcrnrlat = coord[0]-graddiff ,\
        urcrnrlon = coord[1]+graddiff, urcrnrlat = coord[0]+graddiff ,\
        rsphere=6371200., resolution = 'l', area_thresh=1000)


    # Target
    x_mill,y_mill = m(coord[1],coord[0])


    # labels = [left,right,top,bottom]
    parallels = np.arange(int(coord[0]-3), int(coord[0]+3), 1.)
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(int(coord[1]-3), int(coord[1]+3), 1.)
    m.drawmeridians(meridians,labels=[True,False,False,True])

    # plot farms in the radius
    m.plot(x_mill, y_mill, 'bo')

    #m.bluemarble()
    m.etopo()
    m.drawcoastlines()
    #plt.title("Topography around a Mill")
    #plt.show()

