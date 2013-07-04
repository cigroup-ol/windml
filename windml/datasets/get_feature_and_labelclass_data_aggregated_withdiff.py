"""
To do ....
--------------------------------------------------

This .....

"""
import numpy as np

def get_feature_and_labelclass_data_aggregated_withdiff(windpark, feature_window, horizon, diff_for_ramp):
    measurements = windpark.compute_aggregated_measurements()
    timesteps = len(measurements)-(feature_window+horizon-1)

    cols = (feature_window*2)-1
    rows = timesteps

    data = np.zeros( (rows,cols) ,dtype=np.float32)
    labels = np.zeros(timesteps,dtype=np.float32)


    activated_ramp = 0
    number_of_ramps = 0
    list_of_power = []
    for t in range(timesteps):
        for i in range(feature_window):
            data[t][i]=measurements[t+i]
            if i != 0:
                data[t][feature_window+i-1] = measurements[t+i]-measurements[t+i-1] #todo DOKU! erst alle leistungen dann alle differenzen in array

        list_of_power.append(measurements[t+feature_window-1])
        diff_act = (measurements[t+feature_window+horizon-1]) - (measurements[t+feature_window-1])
        if (diff_act >= diff_for_ramp):
            if (activated_ramp == 0):
                labels[t] = 1
                activated_ramp = 0
                number_of_ramps += 1
            else:
                labels[t] = 0
        else:
            labels[t] = 0
            activated_ramp = 0
    print "Number of ramps (in dataset):", number_of_ramps
    return data, labels, number_of_ramps, list_of_power





