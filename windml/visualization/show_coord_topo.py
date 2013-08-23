"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

def show_coord_topo(windpark, title, show = True):
    """Plot the topology of a given windpark

    Topographic Map with farms
    see: http://matplotlib.org/basemap/users/examples.html
    Basemap

    Parameters
    ----------

    windpark : Windpark
               A given windpark to show the topology.
    """

    turbines = windpark.get_turbines()
    target = windpark.get_target()
    radius = windpark.get_radius()

    #pack latitude and longitude in lists
    rel_input_lat = []
    rel_input_lon = []
    for row in turbines:
        rel_input_lat.append(np.float64(row.latitude))
        rel_input_lon.append(np.float64(row.longitude))

    targetcoord = [0.0, 0.0]
    targetcoord[0] = np.float64(target.latitude)
    targetcoord[1] = np.float64(target.longitude)

    graddiff = (radius/111.0) + 0.3 # degree in km

    m = Basemap(fix_aspect=False, projection='stere', lon_0=targetcoord[1], lat_0=targetcoord[0],\
        llcrnrlon = targetcoord[1]-graddiff, llcrnrlat = targetcoord[0]-graddiff ,\
        urcrnrlon = targetcoord[1]+graddiff, urcrnrlat = targetcoord[0]+graddiff ,\
        rsphere=6371200., resolution = 'l', area_thresh=1000)
    # Target
    x_target,y_target = m(targetcoord[1],targetcoord[0])
    # Input Farms
    rel_inputs_lon, rel_inputs_lat = m(rel_input_lon, rel_input_lat)

    # labels = [left,right,top,bottom]
    parallels = np.arange(int(targetcoord[0]-3), int(targetcoord[0]+3), 1.)
    #m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(int(targetcoord[1]-3), int(targetcoord[1]+3), 1.)
    #m.drawmeridians(meridians,labels=[True,False,False,True])

    # plot farms in the radius
    m.scatter(rel_inputs_lon, rel_inputs_lat,20, marker='o', color="#000000")
    m.scatter(x_target, y_target, 20, marker='o', color="r")
    m.shadedrelief()
    plt.title(title)

    if(show):
        plt.show()

