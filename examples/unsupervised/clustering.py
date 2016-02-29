"""
Clustering of Turbines
-------------------------------------------------------------------------

Clustering of 150 turbines near Tehachapi for 12 months with k-means
clustering. 
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

clf = KMeans(n_clusters=3)
info = []

for turbine in windpark.turbines:
    month_power = windml.util.power_features.compute_highlevel_features(turbine)
    info.append(month_power)

clf.fit(info)
labels = clf.labels_
info = np.array(info)

with plt.style.context("fivethirtyeight"):
    ax = plt.figure(figsize=(8, 5))
    ax = plt.subplot(1, 1, 1)
    ax.scatter(info[:, 0], info[:, 1], c=labels.astype(np.float))
    ax.set_xlabel(str("Jan"))
    ax.set_ylabel(str("Feb"))
    plt.tight_layout()
    plt.show()
