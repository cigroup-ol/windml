# Instanz vom Typ windpark soll mittels get_windpark erstellt werden:

import math
import numpy as np
from windml.datasets.nrel import fetch_nrel_data
from windml.datasets.nrel_meta import fetch_nrel_meta_data
from windml.datasets.nrel_meta import fetch_nrel_meta_data_all
from windml.datasets.windmill import Windmill
from windml.datasets.park_definitions import park_info
import datetime, time



class Windpark(object):
    """
    Class Windpark
    --------------------------------------------------

    The class Windpark represents a park, which consists of
    one or more windmills.

    """
    def __init__(self, target_idx, radius):
        self.target_idx = target_idx
        self.radius = radius
        self.mills = []

    def get_target_idx(self):
        return self.target_idx

    def get_target(self):
        return self.mills[len(self.mills)-1]

    def add_windmill(self, mill):
        self.mills.append(mill)

    def get_windmills(self):
        return self.mills
    def get_radius(self):
        return self.radius

    def compute_aggregated_measurements(self):
        num_m = len(self.mills[0].measurements)
        #todo datetime as well
        result =  np.zeros((num_m), dtype=np.float32)
        for f in self.mills:
            m_idx = 0
            for m in f.measurements:
                result[m_idx]+=m[1]
                m_idx+=1
        return result

    def get_powermatrix(self):
        num_m = len(self.mills[0].measurements)
        num_mills = len(self.mills)

        p_matrix = [[0 for col in range(num_mills)] for row in range(num_m)]
        for f in range(num_mills):
            for time in range(num_m):
                p_matrix[time][f] = self.mills[f].measurements[time][1]

        p_matrix = np.array(p_matrix)
        return p_matrix


def get_nrel_windpark(target_idx, radius, year_from=0, year_to=0):
    """
    This method fetches and returns a windpark from NREL, which consists of the target farm with
    the given target_idx and the surrounding wind farm within a given radius
    around the target farm. When called, the wind measurements for a given
    range of years are downloaded for every farm in the park.
    """
    #if only one year is desired
    if year_to==0:
        year_to=year_from

    result = Windpark(target_idx, radius)

    # determine the coordinates of the target
    target=fetch_nrel_meta_data(target_idx)

    Earth_Radius = 6371
    lat_target = math.radians(np.float64(target[1]))
    lon_target = math.radians(np.float64(target[2]))

    rel_input_lat = []
    rel_input_lon = []

    #fetch all farms
    mills=fetch_nrel_meta_data_all()
    for row in mills:
        mill_index = np.int(row[0])
        if (mill_index != target_idx):
            lat_act = math.radians(np.float64(row[1])) # todo "latitude" instead of 1
            lon_act = math.radians(np.float64(row[2]))
            dLat = (lat_act-lat_target)
            dLon = (lon_act-lon_target)

            # Haversine formula:
            a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat_target) * math.cos(lat_act) * math.sin(dLon/2) * math.sin(dLon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance_act = Earth_Radius * c;
            if (distance_act < radius):
                newmill = Windmill(row[0], row[1] , row[2] , row[3] , row[4] , row[5], row[6])
                if year_from != 0:
                    for y in range(year_from, year_to+1):
                       measurement = fetch_nrel_data(row[0], y, ['date','corrected_score','speed'])
                       if y==year_from:
                           measurements = measurement
                       else:
                           measurements = np.concatenate((measurements, measurement))
                    newmill.add_measurements(measurements)
                result.add_windmill(newmill)

    #add target farm as last element
    newmill = Windmill(target[0], target[1] , target[2] , target[3] , target[4] , target[5], target[6])
    if year_from != 0:
        for y in range(year_from, year_to+1):
           measurement = fetch_nrel_data(target[0], y, ['date','corrected_score','speed'])
           if y==year_from:
               measurements = measurement
           else:
               measurements = np.concatenate((measurements, measurement))
        newmill.add_measurements(measurements)
    result.add_windmill(newmill)
    return result
