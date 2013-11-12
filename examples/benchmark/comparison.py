from windml.benchmark.benchmark import Benchmark
from windml.prediction.std_linreg import StdLinreg
from windml.prediction.smoothed_linreg import SmoothedLinreg

bench = Benchmark()
bench.run(SmoothedLinreg(smooth=3), 'QuickNDirty')
bench.run(StdLinreg(), 'QuickNDirty')
bench.visualize_mse_on_parks()

