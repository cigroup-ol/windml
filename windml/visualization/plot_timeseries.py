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
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dr
import time
from pylab import *

def plot_timeseries(windmill, show = True):
    """Plot windspeed and power production of a windmill

    Parameters
    ----------
    windmill : Windmill
               The given windmill to the timeseries.
    """

    plt.clf()

    timeseries=windmill.get_measurements()
    d=np.array([m[0] for m in timeseries])
    y1=np.array([m[1] for m in timeseries]) #score
    y2=np.array([m[2] for m in timeseries]) #speed

    d_time = []
    for i in range (len(d)):
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
    plt.plot(d_time[0:288], y1[0:288], label = 'Power Production')
    plt.plot(d_time[0:288], y2[0:288], label = 'Wind Speed')
    plt.legend(loc='lower right')
    plt.title("Timeseries of the Selected Mill")

    if(show):
        plt.show()

