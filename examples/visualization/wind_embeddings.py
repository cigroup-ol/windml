"""
Manifold Learning with PCA, LDA, ISOMAP and LLE.
--------------------------------------------------

For various post-provessing purposes, the reduction of the dimensionality of
high-dimensional wind power time series may be desirable. The embedding example
employs dimensionality reduction methods like ISOMAP to embed time series of a
single turbine into 2-dimensional latent spaces.
"""

# Author: Oliver Kramer <oliver.kramer@uni-oldenburg.de>
# Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# License: BSD 3 clause

import sklearn
import numpy as np
import pylab as plt
from matplotlib import offsetbox
from sklearn import manifold, datasets, decomposition, lda

from windml.visualization.plot_timeseries import plot_timeseries
from windml.visualization.colorset import cmap
from windml.datasets.nrel import NREL

K = 30
ds = NREL()
windpark = ds.get_windpark(NREL.park_id['tehachapi'], 20, 2004)

X = np.array(windpark.get_powermatrix())
y = np.array(X[:,-1])

X=X[:1000]
y=y[:1000]

# scale and plot method of embeddings - from SKLEARN

def plot_embedding(X, title=None, j=1):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    ax = plt.subplot(2, 2, j)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(int(y[i])),
                color = cmap(y[i] / 30.),
                fontdict={'weight': 'bold', 'size': 9})

    if title is not None:
        plt.title(title)

j = 1
figure = plt.figure(figsize=(15, 10))
title = "Projection of Wind Time Series"

# computation of PCA projection
print "Computation of PCA Projection"

X_pca = decomposition.RandomizedPCA(n_components=2).fit_transform(X)

plot_embedding(X_pca,
               "PCA "+title,j=1)

# computation of LDA projection
print "Computation of LDA Projection"
X2 = X.copy()
X2.flat[::X.shape[1] + 1] += 0.01  # make X invertible

X_lda = lda.LDA(n_components=2).fit_transform(X2, y)

plot_embedding(X_lda,
               "LDA "+title,j=2)

# computation of ISOMAP projection
print "Computation of ISOMAP Projection"
if(sklearn.__version__ == "0.9"):
    X_iso = manifold.Isomap(K, out_dim=2).fit_transform(X)
else:
    X_iso = manifold.Isomap(K, n_components=2).fit_transform(X)

plot_embedding(X_iso,
               "ISOMAP "+title,j=3)

# computation of LLE projection
print "Computation of LLE Projection"
if(sklearn.__version__ == "0.9"):
    clf = manifold.LocallyLinearEmbedding(K, out_dim=2, method='standard')
else:
    clf = manifold.LocallyLinearEmbedding(K, n_components=2, method='standard')

X_lle = clf.fit_transform(X)
plot_embedding(X_lle,
               "LLE "+title,j=4)

plt.show()
