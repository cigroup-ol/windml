.. _gettingstarted:

Getting Started
===============

The windML framework provides an easy-to-use access to several wind data sources within the Python world, building upon numpy [1]_, scipy [1]_, and matplotlib [2]_. As a machine-learning module, it provides versatile tools several learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasks. On this page a big picture of the architecture is discussed and the core features and components are presented. 

Architecture
------------
Below a schematic image of architecture is illustrated. The following description of the architecture is done from top to bottom. On the top you can see available data sources of wind data time series on the internet. DataSource classes are implemented in windML which download the data from data mirrors, parse the data into an windML-specific format and cache the data locally. The windML-specific format is defined by the Windpark and Windmill classes. The Windmills and Windparks are selected by ID and a certain radius.

.. figure:: _static/schema.png
   :alt: architecture
   :align: center

   windML schematic architecture

Given windpark and windmill objects you can visualize the data via different visualization components such a dimension reduction, park / mill information, information on the time series, topology etc., see :ref:`examples`. The main motivation of windML is forecasting time series with machine learning. In this field of research, regression and classifcation of time series is possible. For both methodologies a mapping of a time series to labels is essential. Different mapping approaches have been tested in the past, see :ref:`mapping` for explanation of the various mapping methods. In the current release only regression techniques have been applied to forecasting. The implemented methods are Support Vector Regression, KNN Regression and Linear Regression. 

.. [1] Travis E. Oliphant (2007).  Python for Scientific Computing. Computing in Science & Engineering 9, IEEE Soc.
.. [2] Hunter, J.  D. (2007). Matplotlib: A 2D graphics environment. Computing In Science & Engineering 9, IEEE Soc., pp. 90-95


