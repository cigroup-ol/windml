"""
To do ...
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dr
import time
from pylab import *

def plot_timeseries(windfarm):
    #farm=get_windfarm(idx, 2004)
    timeseries=windfarm.get_measurements()
    d=np.array([m[0] for m in timeseries])
    y1=np.array([m[1] for m in timeseries]) #score
    y2=np.array([m[2] for m in timeseries]) #speed
    


    d_time = []
    for i in range (len(d)):    # January and February
        d_act = datetime.datetime.fromtimestamp(d[i])
        d_time.append(d_act)
    plt.subplots_adjust(bottom=0.25)
    plt.xticks(rotation = 75)

    ax=plt.gca()
    xfmt = md.DateFormatter('%Y/%m/%d %H-h')
    ax.xaxis.set_major_formatter(xfmt)


    ax.grid(True)
    plt.ylim(-2, 32)
    plt.ylabel("Corrected Power (MW), Wind Speed (m/s)")
    plt.plot(d_time[0:288], y1[0:288], label = 'power production')
    plt.plot(d_time[0:288], y2[0:288], label = 'wind speed')
    plt.legend(loc='lower right')
    plt.title("Timeseries of the selected Farm")
    plt.show()


