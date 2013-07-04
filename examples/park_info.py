"""
=============================================================================
Information of a wind park
=============================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from windml.datasets.windpark import get_nrel_windpark
import windml.util.features
from windml.datasets.park_definitions import park_info
from windml.visualization.show_coord_topo import show_coord_topo

radius = 2
name = 'tehachapi'
my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004)
X = np.array(my_windpark.get_powermatrix())


feat, month_power, ramps_up, ramps_down, power_freq = windml.util.features.compute_highlevel_features(my_windpark.mills[0])

month_power = np.array(month_power)
ramps_up = np.array(ramps_up)
ramps_down = np.array(ramps_down)
power_freq = np.array(power_freq)


for windmill in my_windpark.mills[1:]:

    feat, month_power_m, ramps_up_m, ramps_down_m, power_freq_m = windml.util.features.compute_highlevel_features(windmill)

    month_power+=np.array(month_power_m)
    ramps_up+=np.array(ramps_up_m)
    ramps_down+=np.array(ramps_down_m)
    power_freq+=np.array(power_freq_m)
    

month = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
figure = plt.figure(figsize=(15, 10))

# plot 1
plot1 = plt.subplot(2, 2, 1)
plt.title("park topology")
show_coord_topo(my_windpark)

# plot 2
plot2 = plt.subplot(2, 2, 2)
plt.title("monthly power")
plot2.bar(range(1,13), month_power, color='red')
plot2.set_ylabel('power', color='black')
plot2.set_xlabel('month', color='black')
plot2.set_xticks([i+0.5 for i in range(1,13)])
plot2.set_xticklabels(month)

ramps_up = list(ramps_up)
ramps_down = list(ramps_down)

# plot 3
length = 2*len(windml.util.features.rampheights)+1
plot3 = plt.subplot(2, 2, 3)
plt.title("ramp statistics")
plot3.bar(range(1,length), ramps_up+ramps_down, color='yellow')
plot3.set_ylabel('# of ramps', color='black')
plot3.set_xticks([i+0.5 for i in range(1,length)])
plot3.set_xticklabels(['up '+str(i) for i in windml.util.features.rampheights]+['dwn '+str(i) for i in windml.util.features.rampheights])

# plot 4
plot4 = plt.subplot(2, 2, 4)
help = [i*windml.util.features.interval_width for i in range(1,30/windml.util.features.interval_width+1)]
labels = [str(i-windml.util.features.interval_width)+"-"+str(i) for i in help]
plot4.pie(power_freq, labels = labels, shadow=True)

plt.title("power level")
plt.show()