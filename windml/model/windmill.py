import numpy as np

class Windmill(object):
    """The class Windfarm represents a single windfarm. It contains
    the properties of the windmill. Check."""

    def __init__(self, idx, latitude, longitude, power_density, power_capacity,\
        speed, elevation):
        """Initializes windmill with a given target id, lat, long, power
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
                Mean wind speed of the mill per year.
        elevation : float
                    Height of the windmill hub.
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
        """Set measurements of the windmill.

        Parameters
        ----------
        measurements : np.array
        """

        self.measurements = measurements

    def get_measurements(self):
        """Get measurements of the windmill.

        Returns
        -------
        np.array
            Numpy array of measurements.
        """
        return self.measurements