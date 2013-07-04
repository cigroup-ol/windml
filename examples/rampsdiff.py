"""
Example Histogram of Deviations in Feature Window
--------------------------------------------------
"""

from windml.util.feature_assembly import FeatureAssembly
from windml.datasets.windmill import get_nrel_windmill
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.get_feature_and_label_data_aggregated import get_feature_and_label_data_aggregated
from windml.datasets.park_definitions import park_info

from pylab import plt

name = 'tehachapi'
target = get_nrel_windmill(park_info[name][0], 2004, 2005)

feature_window = 3
horizon = 3

timesteps = len(target.measurements) - (feature_window + horizon - 1)

fa = FeatureAssembly([target])
diffs = fa.all_diffs([1.0], 0, timesteps, feature_window)
diffs = map(lambda x : x[0], diffs)

X = []
for diff in diffs:
    for val in diff:
        X.append(val)

plt.hist(X, bins=200)
plt.show()
