"""
Manifold Learning with ISOMAP
--------------------------------------------------

For various post-provessing purposes, the reduction of the dimensionality of
high-dimensional wind power time series may be desirable. The embedding example
employs dimensionality reduction methods like ISOMAP to embed time series of a
single turbine into 2-dimensional latent spaces.
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

from __future__ import print_function
import sklearn
import numpy as np
import pylab as plt
from matplotlib import offsetbox
from sklearn import manifold

from windml.visualization.plot_timeseries import plot_timeseries
from windml.datasets.nrel import NREL

K = 30
ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 20, 2004)

X = np.array(windpark.get_powermatrix())
y = np.array(X[:, -1])

X = X[:1000]
y = y[:1000]

# scale and plot method of embeddings - from SKLEARN

# computation of ISOMAP projection
print("Computation of ISOMAP Projection")
X_iso = manifold.Isomap(K, n_components=2).fit_transform(X)
x_min, x_max = np.min(X, 0), np.max(X, 0)
X = (X - x_min) / (x_max - x_min)

with plt.style.context("fivethirtyeight"):
    figure = plt.figure(figsize=(8, 5))
    title = "Projection of Wind Time Series"
    ax = plt.subplot(1, 1, 1)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(int(y[i])),
                 color=plt.cm.jet(y[i] / 30.),
                 fontdict={'weight': 'bold', 'size': 9})
plt.show()
