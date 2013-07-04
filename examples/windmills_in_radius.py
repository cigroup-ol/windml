"""
Example: Plotting the Amount of Windmills with Given Radius
-------------------------------------------------------------
"""

from windml.datasets.windmill import get_nrel_windmill
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.park_definitions import park_info
from windml.util.distance import distance
from pickle import dump

import math
import matplotlib.pyplot as plt

parks = ['vantage', 'palmsprings', 'tehachapi', 'cheyenne']
radius_interval = [0.0, 8.0]
stepsize = 0.5

def amount_of_windmills(radius, park):
    target = park_info[park][0]
    my_windpark1 = get_nrel_windpark(target, radius, 2004, 2005)
    target = get_nrel_windmill(target, 2004, 2005)
    windmills = my_windpark1.get_windmills()
    return len(windmills)

results = {}
for park in parks:
    diff = radius_interval[1] - radius_interval[0]
    if(diff % stepsize > 0):
        raise Exception("Steps dont fit into interval")
    steps = int(diff / stepsize)

    values, results_park = [], {}
    for step in xrange(steps):
        value = radius_interval[0] + step * stepsize
        values.append(value)

    for value in values:
        k = amount_of_windmills(value, park)
        results_park[value] = k

    results[park] = results_park

# plot

colors = {'vantage':'k', 'palmsprings':'r', 'tehachapi':'b', 'cheyenne':'g'}

for park in parks:
    items = results[park].items()
    X, Y = [], []
    for x,y in items:
        X.append(x)
        Y.append(y)

    plt.xlim([0, 8])
    plt.ylim([0, 80])

    plt.xlabel('Radius')
    plt.ylabel('Amount of Windmills')
    plt.scatter(X,Y, color=colors[park])

plt.show()
