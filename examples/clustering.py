"""
=============================================================================
Clustering of wind mills
=============================================================================
"""

import numpy as np
from windml.datasets.windpark import get_nrel_windpark
import windml.util.power_features
from windml.datasets.park_definitions import park_info
from sklearn.cluster import KMeans
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D

radius = 15
name = 'tehachapi'
my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004)
X = np.array(my_windpark.get_powermatrix())


clf = KMeans(k=3)
turbine = []

for windmill in my_windpark.mills:

    month_power = windml.util.power_features.compute_highlevel_features(windmill)
    turbine.append(month_power)


clf.fit(turbine)
labels = clf.labels_
turbine = np.array(turbine)


j=1
ax = plt.figure(figsize=(14, 9))
for i in range(0,6):

    ax = plt.subplot(3, 2, j)
    ax.scatter(turbine[:, 2*i], turbine[:, 2*i+1], c=labels.astype(np.float))
    ax.set_xlabel(str(2*i+1))
    ax.set_ylabel(str(2*i+2))
    j+=1

plt.show()
