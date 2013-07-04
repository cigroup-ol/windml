"""
To do ....
--------------------------------------------------

This .....

"""
import numpy as np


def get_data_matrix_old(windpark):
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


#todo could be a method of the Class Windpark
#todo Step-Width for feature window
def get_feature_and_label_data(windpark, feature_window, horizon):
    mills = windpark.get_windmills()
    timesteps = len(mills[-1].measurements)-(feature_window+horizon-1) # todo docu

    number_of_mills = len(mills)
    cols = number_of_mills * feature_window
    rows = timesteps

    data = np.zeros( (rows,cols) ,dtype=np.float32)
    labels = np.zeros(timesteps,dtype=np.float32)

    mill_idx=0

    for mill in mills:
        for t in range(1,timesteps):
             data[t][mill_idx*feature_window:(mill_idx+1)*feature_window]=mill.measurements['corrected_score'][t:t+feature_window]
        mill_idx+=1

    for t in range(1,timesteps):
        labels[t]=(mills[-1].measurements[t+feature_window+horizon-1][1]) 

    return data, labels
