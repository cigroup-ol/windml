"""
=============================================================================
Different Feature Assembly Methods
=============================================================================
"""

from cProfile import run

from windml.datasets.windmill import get_nrel_windmill
from windml.datasets.windpark import get_nrel_windpark
from windml.datasets.park_definitions import park_info
from windml.util.feature_assembly import FeatureAssembly

target = park_info['tehachapi'][0]
radius = 3.0
windpark = get_nrel_windpark(target, radius, 2004, 2005)
target = get_nrel_windmill(target, 2004, 2005)
windmills = windpark.get_windmills()

# corrected score
fa = FeatureAssembly(windmills)

def corrected_score_features(fa):
    X = fa.X(method='corrected_score', feature_window=3, horizon=3)
    Y = fa.Y(target, feature_window=3, horizon=3)

def corrected_score_with_diffs_features(fa):
    X = fa.X(method='corrected_score_and_diffs', feature_window=3, horizon=3)
    Y = fa.Y(target, feature_window=3, horizon=3)

# corrected score with diffs
print "Initialize FeatureAssembly"
run("fa = FeatureAssembly(windmills)")

print "Assemble corrected score features and labels"
run("corrected_score_features(fa)")

print "Assemble corrected score with diff features and labels"
run("corrected_score_with_diffs_features(fa)")

