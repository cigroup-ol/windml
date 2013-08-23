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

def show_coord_topo_turbine(turbine, show = True):
    """Plot the topology of a turbine

    Topographic Map with farms
    see: http://matplotlib.org/basemap/users/examples.html
    Basemap

    Parameters
    ----------
    turbine : Turbine
               The given turbine to show the topology.
    """

    radius = 20
    coord = [0.0, 0.0]
    coord[0] = np.float64(turbine.latitude)
    coord[1] = np.float64(turbine.longitude)

    graddiff = (radius/111.0) + 0.5  # degree in km

    m = Basemap(projection='stere', lon_0=coord[1], lat_0=coord[0],\
        llcrnrlon = coord[1]-graddiff, llcrnrlat = coord[0]-graddiff ,\
        urcrnrlon = coord[1]+graddiff, urcrnrlat = coord[0]+graddiff ,\
        rsphere=6371200., resolution = 'l', area_thresh=1000)

    # Target
    x_turbine,y_turbine = m(coord[1],coord[0])

    # labels = [left,right,top,bottom]
    parallels = np.arange(int(coord[0]-3), int(coord[0]+3), 1.)
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(int(coord[1]-3), int(coord[1]+3), 1.)
    m.drawmeridians(meridians,labels=[True,False,False,True])

    # plot farms in the radius
    m.plot(x_turbine, y_turbine, 'bo')
    m.shadedrelief()

    plt.title("Topography around a Turbine")

    if(show):
        plt.show()

