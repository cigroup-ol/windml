"""
=============================================================================
Sequence visualization based on ISOMAP
=============================================================================
"""


import numpy as np
import pylab as plt
from sklearn import manifold, decomposition
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.park_definitions import park_info


# load data and define parameters / training and test sequences
K = 30
radius = 10
name = 'tehachapi'
my_windpark = get_nrel_windpark(park_info[name][0], radius, 2004)
X = np.array(my_windpark.get_powermatrix())
X_train = X[:2000]
X_test = X[2000:2000+200*4]


# computation of ISOMAP projection
print "computation of ISOMAP projection"
X_latent = manifold.Isomap(K, out_dim=2).fit_transform(X_train)


# computation of sequence of closest embedded patterns
sequence = []
for x in X_test:
    win = 0
    smallest = 10E100
    for b in xrange(len(X_train)):
        if np.dot(x-X_train[b],x-X_train[b])<smallest:
            smallest = np.dot(x-X_train[b],x-X_train[b])
            win = b
    sequence.append(X_latent[win])


# normalization of the sequence
sequence = np.array(sequence)
sequence[:,0] = (sequence[:,0]-sequence[:,0].min())/abs(sequence[:,0].max()-sequence[:,0].min())
sequence[:,1] = (sequence[:,1]-sequence[:,1].min())/abs(sequence[:,1].max()-sequence[:,1].min())
col = [[i,j,0.5] for [i,j] in sequence]

# plotting ...
fig = plt.figure(figsize=(20,4))
ax = plt.subplot(4, 1, 1)

for i in range(0,200):
    ax.bar(i, 1, 1, linewidth=0.0, color=col[i])

ax = plt.subplot(4, 1, 2)
for i in range(200,400):
    ax.bar(i, 1, 1, linewidth=0.0, color=col[i])

ax = plt.subplot(4, 1, 3)
for i in range(400,600):
    ax.bar(i, 1, 1, linewidth=0.0, color=col[i])

ax = plt.subplot(4, 1, 4)
for i in range(600,800):
    ax.bar(i, 1, 1, linewidth=0.0, color=col[i])

plt.show()
