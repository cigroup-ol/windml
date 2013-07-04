"""
    Computation of features for a wind turbine
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
    
# sum of power a year

    x =  np.sum(X)
    feat=feat+[x]

# sum of power each month (list of length 12)
    l = len(X)/12
    indices= [(i*l,(i+1)*l) for i in range(12)]
    x = [sum(X[i:j]) for i,j in indices]
    feat=feat+x
    month_power = x

# mean of power each month (list of length 12)
    x = [np.mean(np.array(X[i:j])) for i,j in indices]
    feat=feat+x

# variance of power each month (list of lenght 12)
    x = [np.var(np.array(X[i:j])) for i,j in indices]
    feat=feat+x

# sum of power at daytime (6h-18h)
    l = len(X)/(365*2)
    dayindices= [(i*l,(i+1)*l) for i in range(365*2)] # day indices
    indices = [dayindices[2*i] for i in range(len(dayindices)/2)] # daytime indices
    x = sum([np.sum(np.array(X[i:j])) for i,j in indices])
    feat=feat+[x]

# sum of power at night (18h-6h)
    indices = [dayindices[2*i+1] for i in range(len(dayindices)/2)] # nighttime indices
    x = sum([np.sum(np.array(X[i:j])) for i,j in indices])
    feat=feat+[x]


    """
    ramp features
    """
    
# measured features
    ramps_up = []
    ramps_down = []


# ramp computations
    for step in [1]:
        for thresh in rampheights:
            ramps_up.append(0)
            ramps_down.append(0)
            for i in xrange(len(X)-step):
                diff = X[i]-X[i+step]
                if diff > thresh:
                    ramps_up[-1]+=1
                if diff < -thresh:
                    ramps_down[-1]+=1

    feat=feat+ramps_up+ramps_down



    """
    stability features
    """

# parameters
    epsilon = 1.0 # insensitiv value to tolerate deviations from plateau
    mid = 15.0 # definition of mid of power generation
    plateau_height = 30.0

# measured features
    d_min = 0
    c_min = 0
    d_max = 0
    c_max = 0
    transitions = 0

    for i in xrange(len(X)):

# minimum plateau computation
        if X[i]<=epsilon:
            c_min+=1
        else:
            c_min=0
        d_min = max(d_min,c_min)


# maximum plateau computation
        if X[i]>=plateau_height-epsilon:
            c_max+=1
        else:
            c_max=0
        d_max = max(d_max,c_max)


# mid transitions computation
    for i in xrange(len(X)-1):
        if (X[i]>mid and X[i+1]<mid) or (X[i]<mid and X[i+1]>mid):
            transitions+=1


# frequencies of power values w.r.t. interval

    power_freq = np.zeros(30./interval_width)

    for i in xrange(len(X)):
        if X[i]==30.0:
            power_freq[-1]+=1
        else:
            power_freq[int(X[i]/interval_width)]+=1

    feat+=[epsilon]+[d_min]+[d_max]+[transitions]

    return feat, month_power, ramps_up, ramps_down, power_freq

