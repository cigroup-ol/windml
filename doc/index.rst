.. _home:

.. raw:: html

    <style type="text/css">

    h1.div#windml {
        font-size: 350%;
    }

    a.image-reference {
        border-bottom: None;
    }

    a.image-reference:hover {
        border-bottom: None;
    }

    .figures {
        float: left;
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

windML 
===========================

.. .. topic:: Machine learning library for wind energy information systems. 

The `windML framework <https://github.com/cigroup-ol/windml>`_ provides an easy-to-use access to wind data sources within the **Python** world, building upon `numpy <http://numpy.scipy.org/>`_ [1]_, `scipy <http://scipy.org>`_ [1]_, `sklearn <http://scikit-learn.org>`_ [3]_, and `matplotlib <http://matplotlib.org>`_ [2]_. 
As a machine learning module, it provides versatile tools for various learning tasks like time-series prediction, classification, clustering, dimensionality reduction, and related tasks. For further information including the motivation for windML, see section :ref:`about`.

Getting Started
---------------

For an installation guide, an overview of the architecture, and the functionalities of windML, please visit the :ref:`gettingstarted` page. For a formal description of the applied techniques, see section :ref:`techniques`. The :ref:`examples` gallery illustrates the main functionalities.  

.. container:: figures

    .. figure:: ./_images/show_flip_book_1_thumb.png
        :target: ./examples/visualization/show_flip_book.html
    
    .. figure:: ./_images/svr_regression_turbine_1_thumb.png
        :target: ./examples/prediction/svr_regression_turbine.html
    
    .. figure:: ./_images/wind_embeddings_1_thumb.png
        :target: ./examples/visualization/wind_embeddings.html

.. raw:: html

    <div style="clear: both"></div>


Brief Example
-------------

In the following, we give a brief example
of wind time-series forecasting based on *K nearest neighbors* (KNN) regression.
For a further list of examples with plots, we refer to the :ref:`examples` page.
 ::

  from windml.datasets.nrel import NREL
  from windml.mapping.power_mapping import PowerMapping
  from sklearn.neighbors import KNeighborsRegressor
  import math
  
  windpark = NREL().get_windpark(NREL.park_id['tehachapi'], 3, 2004, 2005)
  target = windpark.get_target()
  
  feature_window, horizon = 3, 3
  mapping = PowerMapping()
  X = mapping.get_features_park(windpark, feature_window, horizon)
  Y = mapping.get_labels_turbine(target, feature_window, horizon)
  reg = KNeighborsRegressor(10, 'uniform')
  
  train_to, test_to = int(math.floor(len(X) * 0.5)), len(X)
  train_step, test_step = 5, 5
  reg = reg.fit(X[0:train_to:train_step], Y[0:train_to:train_step])
  y_hat = reg.predict(X[train_to:test_to:test_step])

Contributors
------------

The windML framework has initially been developed by the `Computational Intelligence Group <http://www.ci.uni-oldenburg.de/>`_ of the University in Oldenburg. The contributors are Nils André Treiber, Jendrik Poloczek, Oliver Kramer, Justin Philipp Heinermann, Fabian Gieseke. For questions and feedback contact us via `email <oliver.kramer@uni-oldenburg.de>`_.  

License
-------

The windML framework is released under the open source BSD 3-clause license. The LICENSE file is available `here <https://github.com/cigroup-ol/windml/blob/master/LICENSE>`_.

.. [1] Travis E. Oliphant (2007).  *Python for Scientific Computing.* Computing in Science & Engineering 9, IEEE Soc., pp. 10-20.
.. [2] Hunter, J.  D. (2007). *Matplotlib: A 2D Graphics Environment.* Computing in Science & Engineering 9, IEEE Soc., pp. 90-95.
.. [3] Pedregosa et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research (JMLR) 12, pp. 2825-2830.
