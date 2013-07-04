"""
To do ....
--------------------------------------------------

This .....

"""
import numpy as np

def get_feature_and_label_data_aggregated(windpark, feature_window, horizon):
    measurements = windpark.compute_aggregated_measurements()
    timesteps = len(measurements)-(feature_window+horizon-1) 
    
    cols = feature_window
    rows = timesteps

    data = np.zeros( (rows,cols) ,dtype=np.float32) 
    labels = np.zeros(timesteps,dtype=np.float32) 

 
    for t in range(timesteps):
        for i in range(feature_window):
            data[t][i]=measurements[t+i]
        labels[t]=(measurements[t+feature_window+horizon-1])
             
    return data, labels

    
        


