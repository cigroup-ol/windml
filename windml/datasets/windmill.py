import numpy as np
from windml.datasets.nrel import fetch_nrel_data
from windml.datasets.nrel_meta import fetch_nrel_meta_data
from windml.datasets.nrel_meta import fetch_nrel_meta_data_all

class Windmill(object):
    """
    Class Windmill
    --------------------------------------------------

    The class Windfarm represents a single windfarm. It contains
    the properties of the windmill.

    """
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



def get_nrel_windmill(target_idx, year_from, year_to=0):
    """
    This method fetches and returns a single windfarm.
    """
    #if only one year is desired
    if year_to==0:
        year_to=year_from

    # determine the coordinates of the target
    target=fetch_nrel_meta_data(target_idx)

    #add target farm as last element
    newmill = Windmill(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
    for y in range(year_from, year_to+1):
       measurement = fetch_nrel_data(target[0], y, ['date','corrected_score', 'speed'])
       if y==year_from:
           measurements = measurement
       else:
           measurements = np.concatenate((measurements, measurement))
    newmill.add_measurements(measurements)
    return newmill


