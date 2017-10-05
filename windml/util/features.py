"""
Copyright (c) 2013,
Fabian Gieseke, Justin P. Heinermann, Oliver Kramer, Jendrik Poloczek,
Nils A. Treiber
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    Neither the name of the Computational Intelligence Group of the University
    of Oldenburg nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import numpy as np
from past.builtins import range


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

    for i in range(len(X)):

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
    for i in range(len(X)-1):
        if (X[i]>mid and X[i+1]<mid) or (X[i]<mid and X[i+1]>mid):
            transitions+=1


# frequencies of power values w.r.t. interval

    power_freq = np.zeros(30./interval_width)

    for i in range(len(X)):
        if X[i]==30.0:
            power_freq[-1]+=1
        else:
            power_freq[int(X[i]/interval_width)]+=1

    feat+=[epsilon]+[d_min]+[d_max]+[transitions]

    return feat, month_power, ramps_up, ramps_down, power_freq

