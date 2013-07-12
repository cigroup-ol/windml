.. _home:

Documentation of windML 
======================

.. topic:: Machine learning library for wind energy information systems. 

The windML framework provides an easy-to-use access to several wind data sources within the **Python** world, building upon `numpy <http://numpy.scipy.org/>`_ [1]_, `scipy <http://scipy.org>`_ [1]_, and `matplotlib <http://matplotlib.org>`_ [2]_. As a machine-learning module, it provides versatile tools several learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasts.

Brief Example
-------------

Here's a brief example of how to forecast using a KNN regressor. For a further list of examples with plots check out the example page, see :ref:`examples`. ::

    import math
    from windml.datasets.nrel import NREL
    from windml.mapping.power_mapping import PowerMapping
    from sklearn.neighbors import KNeighborsRegressor

    # get windpark and corresponding target. forecast is for the target windmill
    windpark = NREL().get_windpark(NREL.park_id['tehachapi'], 3, 2004, 2005)
    target = windpark.get_target()

    # use power mapping for pattern-label mapping. Feature window length is 3 time
    # steps and time horizon (forecast) is 3 time steps.
    feature_window, horizon = 3, 3
    mapping = PowerMapping()
    X = mapping.get_features_park(windpark, feature_window, horizon)
    Y = mapping.get_labels_mill(target, feature_window, horizon)

    # initialize KNN regressor from sklearn.
    k_neighbors = 10
    reg = KNeighborsRegressor(k_neighbors, 'uniform')

    # train roughly for the year 2004. test roughly for the year 2005.
    train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)

    # train and test only every fifth pattern, for performance.
    train_step, test_step = 5, 5

    # fitting the pattern-label pairs
    reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
    y_hat = reg.predict(X[train_to:test_to:test_step])

User Guide
----------

.. toctree::
    about
    installation
    gettingstarted
    examples/index
    datasets
    model
    mapping
    visualization
    genindex
    modindex
    search

Examples
--------

.. [1] Travis E. Oliphant (2007).  Python for Scientific Computing. Computing in Science & Engineering 9, IEEE Soc.
.. [2] Hunter, J.  D. (2007). Matplotlib: A 2D graphics environment. Computing In Science & Engineering 9, IEEE Soc., pp. 90-95


