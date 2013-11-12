"""
MSE Comparison of Predictors
-------------------------------------------------------------------------

This example shows a comparison of different predictors: Standard
spatio-temporal predictor and standard spatio-temporal predictor with
a smooth training set. The testbed is QuickNDirty, which is only used
for the example page presentation.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# License: BSD 3 clause

from windml.benchmark.benchmark import Benchmark
from windml.prediction.std_linreg import StdLinreg
from windml.prediction.smoothed_linreg import SmoothedLinreg

bench = Benchmark()
bench.run(SmoothedLinreg(smooth=3), 'QuickNDirty')
bench.run(StdLinreg(), 'QuickNDirty')
bench.visualize_mse_on_parks()

