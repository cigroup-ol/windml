"""
MSE Comparison of Predictors
-------------------------------------------------------------------------

This example shows a comparison of different predictors: Standard
spatio-temporal predictor with linear regression, univariate predictor
with linear regression (only based on target turbine measurements) and
the naive / persistance model. The testbed is QuickNDirty,
which is only used for the example page presentation.
"""

# Author: Jendrik Poloczek <jendrik.poloczek@madewithtea.com>
# Author: Nils A. Treiber <nils.andre.treiber@uni-oldenburg.de>
# License: BSD 3 clause

from windml.benchmark.benchmark import Benchmark
from windml.prediction.std_linreg import StdLinreg
from windml.prediction.univariate_linreg import UnivariateLinreg
from windml.prediction.naive import Naive

bench = Benchmark()
bench.run(StdLinreg(), 'QuickNDirty')
bench.run(UnivariateLinreg(), 'QuickNDirty')
bench.run(Naive(), 'QuickNDirty')

bench.visualize_mse_on_parks()

