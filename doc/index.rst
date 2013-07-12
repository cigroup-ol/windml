.. _home:

Documentation of windML 
======================

.. topic:: Machine learning library for wind energy information systems. 

The windML framework provides an easy-to-use access to several wind data sources within the **Python** world, building upon `numpy <http://numpy.scipy.org/>`_ [1]_, `scipy <http://scipy.org>`_ [1]_, and `matplotlib <http://matplotlib.org>`_ [2]_. As a machine-learning module, it provides versatile tools several learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasts.

Brief Example
-------------

Here's a brief example of how to plot a time series. For a further list of examples check out the example page, see :ref:`examples/index`. ::

    from windml.datasets.nrel import NREL
    from windml.visualization.plot_timeseries import plot_timeseries

    mill = NREL().get_windmill(NREL.park_id['tehachapi'], 2004)
    plot_timeseries(mill)

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


