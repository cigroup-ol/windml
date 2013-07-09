import numpy as np

class Windmill(object):
    """The class Windfarm represents a single windfarm. It contains
    the properties of the windmill."""

    def __init__(self, idx, latitude, longitude, power_density, power_capacity, speed, elevation):
        self.idx = idx
        self.latitude = latitude
        self.longitude = longitude
        self.power_density=power_density
        self.power_capacity=power_capacity
        self.speed=speed
        self.elevation=elevation
        self.measurements = None

    def add_measurements(self, measurements):
        self.measurements = measurements

    def get_measurements(self):
        return self.measurements




