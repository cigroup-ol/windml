# windml


The importance of wind in smart grids with a large number of renewable energy resources is increasing. 
With the growing infrastructure of wind turbines and the availability of time-series data with high spatial and temporal resolution, the application of data mining techniques comes into play. 

The windML framework provides an easy-to-use access to wind data sources within the Python world, building upon [numpy](http://www.numpy.org/), [scipy](http://www.scipy.org/), [sklearn](http://scikit-learn.org/stable/), and [matplotlib](http://matplotlib.org/). As a machine learning module, it provides versatile tools for various learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasks.

## Getting Started

For an installation guide, an overview of the architecture, and the functionalities of windML, please visit the [Getting Started](http://www.windml.org/gettingstarted.html#gettingstarted) page. For a formal description of the applied techniques, see [Techniques](http://www.windml.org/techniques.html#techniques). The [Examples](http://www.windml.org/examples/index.html#examples) gallery illustrates the main functionalities.

## Brief Example

<pre>
from windml.datasets.nrel import NREL
from windml.mapping.power_mapping import PowerMapping
from sklearn.neighbors import KNeighborsRegressor
import math

windpark = NREL().get_windpark(NREL.park_id['tehachapi'], 3, 2004, 2005)
target = windpark.get_target()

feature_window, horizon = 3, 3
mapping = PowerMapping()
X = mapping.get_features_park(windpark, feature_window, horizon)
Y = mapping.get_labels_mill(target, feature_window, horizon)
reg = KNeighborsRegressor(10, 'uniform')

train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)
train_step, test_step = 5, 5
reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
y_hat = reg.predict(X[train_to:test_to:test_step])
</pre>

## License

The windML framework is licensed under the three clause BSD License. 

## Install

Using pip: `pip install git+https://github.com/aschmu/windml.git@setup-py3`.

The `basemap` is tricky to install unless you are using conda (`conda install basemap`). Otherwise you should install from source e.g. : `pip install https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz`.

pkgconfig, freetype and libpng are necessary to build the package from source (matplotlib install depends on it). 
The requirements.txt file is purely cosmetic as scikit-learn requires scipy (and numpy) to be preinstalled and more importantly there is no guarantee that scipy will be installed prior to scikit-learn.

* MacOS: 
```
brew install pkg-config
brew install freetype
brew install libpng
```

