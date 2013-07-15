.. _home:

.. raw:: html

    <style type="text/css">
    a.image-reference {
        border-bottom: None;
    }

    a.image-reference:hover {
        border-bottom: None;
    }

    .figure {
        float: left;
        margin: 10px;
        margin-bottom: 1px;
        width: auto;
        height: 140px;
        width: 200px;
    }

    .figure img {
        display: inline;
        }

    </style>

Documentation of windML 
======================

.. topic:: Machine learning library for wind energy information systems. 

The windML framework provides an easy-to-use access to several wind data sources within the **Python** world, building upon `numpy <http://numpy.scipy.org/>`_ [1]_, `scipy <http://scipy.org>`_ [1]_, and `matplotlib <http://matplotlib.org>`_ [2]_. As a machine-learning module, it provides versatile tools several learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasks. For further information including the motivation for windML, see :ref:`about`.

Getting Started
---------------

For an overview of the architecture and the functionalities of windML please visit the :ref:`gettingstarted` page. The :ref:`examples` gallery illustrates the coverage of the main functionalities.  

.. figure:: ./_images/show_flip_book_1_thumb.png
    :target: ./examples/show_flip_book.html

.. figure:: ./_images/svr_regression_mill_1_thumb.png
    :target: ./examples/svr_regression_mill.html

.. figure:: ./_images/wind_embeddings_1_thumb.png
    :target: ./examples/wind_embeddings.html

Brief Example
-------------

Here's a brief example of how to forecast using a KNN regressor. For a further list of examples with plots check out the example page, see :ref:`examples`. ::

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


