"""
    Computation of power features for a wind turbine
    --------------------------------------------------
    
    ...
    """

import numpy as np

rampheights = [10,15,20,25] # list of height of ramps
interval_width = 5

def compute_highlevel_features(turbine, power_features = True, ramp_features = True, stability_features = True):

    X = np.array([m[1] for m in turbine.get_measurements()])
    feat = []
    month_power = []
    
    
    """
    power features    
    """
    


# sum of power each month (list of length 12)
    l = len(X)/12
    indices= [(i*l,(i+1)*l) for i in range(12)]
    x = [sum(X[i:j]) for i,j in indices]
    feat=feat+x
    month_power = x


    return month_power

