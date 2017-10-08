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

import numpy as np
from numpy import searchsorted

class Turbine(object):
    """The class Turbine represents a single turbine. It contains
    the properties of the turbine, including the index of the turbine,
    its coordinates, the average power density and capacity, the mean wind speed
    and the elevation of the hub."""

    def __init__(self, idx, latitude, longitude, power_density, power_capacity,\
        speed, elevation):
        """Initializes turbine with a given target id, lat, long, power
        density and power capacity.

        Parameters
        ----------
        target_idx : int
                     A user-defined id.
        latitude : float
                   Latitude.
        longitude : float
                    Longitude
        power_density : float
                        Power Density.
        power_capacity : float
                         Power Capacity.
        speed : float
                Mean wind speed of the turbine per year.
        elevation : float
                    Height of the turbine hub.
        """

        self.idx = idx
        self.latitude = latitude
        self.longitude = longitude
        self.power_density=power_density
        self.power_capacity=power_capacity
        self.speed=speed
        self.elevation=elevation
        self.measurements = None

    def add_measurements(self, measurements):
        """Set measurements of the turbine.

        Parameters
        ----------
        measurements : np.array
        """

        self.measurements = measurements

    def get_measurements_between(self, start, end):
        """Get measurements between certain timestamp

        Parameters
        ----------
        start : start timestmap
        end : end timestmap

        Returns
        -------
        np.array
            Numpy array of measurements.
        """
        start_index = searchsorted(self.measurements['date'], start)
        end_index = searchsorted(self.measurements['date'], end)
        return self.measurements[start_index : end_index]

    def get_measurements(self):
        """Get measurements of the turbine.

        Returns
        -------
        np.array
            Numpy array of measurements.
        """
        return self.measurements
