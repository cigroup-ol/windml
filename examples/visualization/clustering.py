"""
Clustering of Turbines
-------------------------------------------------------------------------

Clustering of monthly wind power for 12 months for a wind park near Tehachapi
with k-means clustering. It is remarkable that elements of the same cluster lie
together in all monthly comparison plots.
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import numpy as np
from sklearn.cluster import KMeans
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D

from windml.datasets.nrel import NREL
import windml.util.power_features

ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 15, 2004)
X = np.array(windpark.get_powermatrix())

clf = KMeans(k=3)
info = []

for turbine in windpark.turbines:

    month_power = windml.util.power_features.compute_highlevel_features(turbine)
    info.append(month_power)

clf.fit(info)
labels = clf.labels_
info = np.array(info)

j=1
ax = plt.figure(figsize=(14, 9))
for i in range(0,6):

    ax = plt.subplot(3, 2, j)
    ax.scatter(info[:, 2*i], info[:, 2*i+1], c=labels.astype(np.float))
    ax.set_xlabel(str(2*i+1))
    ax.set_ylabel(str(2*i+2))
    j+=1

plt.show()
