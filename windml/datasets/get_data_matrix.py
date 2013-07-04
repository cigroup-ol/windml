"""
To do ....
--------------------------------------------------

This .....

"""
import numpy as np


def get_data_matrix(windpark):
    data_array = []
    mills = windpark.get_windmills()
    timesteps = len(mills[-1].measurements)

    for t in range(timesteps):
        liste = []
        for row in mills:
            liste.append(row.measurements[t][1])
        data_array.append(liste)

    data_array = np.array(data_array)
    return data_array


