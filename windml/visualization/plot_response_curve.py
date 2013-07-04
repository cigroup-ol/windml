"""
Plot the response curve of the given windmill
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dr
import time
from pylab import *

def plot_response_curve(windmill):
    #farm=get_windfarm(idx, 2004)
    timeseries=windmill.get_measurements()
    score=np.array([m[1] for m in timeseries]) #score
    speed=np.array([m[2] for m in timeseries]) #speed
    
    plt.xlim(-2, 36)
    plt.ylim(-2, 32)
    plt.xlabel("Wind Speed(m/s)")
    plt.ylabel("Corrected Power (MW)")
    plt.plot(speed, score, 'bo')
    plt.title("Response Curve Of The Selected Farm")
    plt.show()


