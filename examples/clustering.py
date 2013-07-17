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

"""
Clustering of Windmills
-------------------------------------------------------------------------
"""

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
turbine = []

for windmill in windpark.mills:

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
