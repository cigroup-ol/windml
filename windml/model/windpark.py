import math
import numpy as np
import datetime, time

class Windpark(object):
    """The class Windpark represents a park, which consists of
    one or more windmills."""

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

    def get_powermatrix(self):
        num_m = len(self.mills[0].measurements)
        num_mills = len(self.mills)

        p_matrix = [[0 for col in range(num_mills)] for row in range(num_m)]
        for f in range(num_mills):
            for time in range(num_m):
                p_matrix[time][f] = self.mills[f].measurements[time][1]

        p_matrix = np.array(p_matrix)
        return p_matrix

    def get_data_matrix(self):
        data_array = []
        mills = self.get_windmills()
        timesteps = len(mills[-1].measurements)

        for t in range(timesteps):
            liste = []
            for row in mills:
                liste.append(row.measurements[t][1])
            data_array.append(liste)

        data_array = np.array(data_array)
        return data_array


