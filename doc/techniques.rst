.. _techniques:

Techniques
==========

Wind Energy Prediction
----------------------
For the integration of wind power into the grid, a precise forecast of energy
has an important part to play. Only with these informations a truly sustainable
supply with low support of conventional energy rersources can be achieved.

.. _generaltimeseriesmodel:

General Times Series Model
++++++++++++++++++++++++++

Our model mades predictions exclusively based on past wind power measurements.
For this task, we formulate the prediction as regression problem. Let us first
assume we want to predict the power production of a single turbine with its
time series: The wind power measurement :math:`\mathbf{x} = p(t)` (pattern) is
mapped to the power production at target time :math:`y = p(t+t_h)` (label).
For our regression model we assume to have :math:`N` of such pattern label
pairs :math:`(\mathbf{x}^i,y^i)` that are basis of our training set
:math:`T=\{(\mathbf{x}^1,y^1),\ldots,(\mathbf{x}^n,y^n)\}` and allow via a
regression to predict the label for unknown patterns.

One can assume, that this model generates better prediction, if more
information of the times series will be used. For this reason, we extend the
patterns by appending past measurements :math:`p(t-1),\ldots, p(t-\mu)` with
:math:`\mu \in \mathbb{N^+}`. Furthermore, we test, if taking into account
differences of measurements :math:`\Delta p(t)=p(t)-p(t-1), \ldots, \Delta
p\big(t-(\mu-1)\big)-p(t-\mu)` leads to better results. Therefore, we consider
on the one hand only the absolute values of the measurements as features and
get patterns with dimension :math:`d_{st}=(\mu+1)`, see :ref:`powermapping`. On
the other hand we use both, i.e. the absolute values and their differences that
results in patterns with a dimension of :math:`d_{st}=(2\mu+1)`, see
:ref:`powerdiffmapping`.

Different Regressors
++++++++++++++++++++

Different regressors can be used for forecasting. Currently, the `Linear
Regression <http://en.wikipedia.org/wiki/Linear_regression>`_, the `Support
Vector Regression
<http://en.wikipedia.org/wiki/Support_vector_machine#Regression>`_ (SVR) and the
`K-nearest Neighbor Regression
<http://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm#For_regression>`_
(KNN Regression) are presented in examples. In Example
:ref:`example_linear_regression` a linear regressor is used. The SVR is used in
example :ref:`example_svr_regression`. In Example :ref:`example_knn_regression`
a KNN regressor is employed. 


Classsification of Wind Energy Ramp Events
------------------------------------------


Ramp Event Definition
+++++++++++++++++++++





Visualizing of Times Series: Dimensionality Reduction Moduls
------------------------------------------------------------

In this section one can find the explanation how to visualize high-dimensional wind time series. Monitoring of high-dimensional time-series data is a dimensionality reduction (DR) task. DR methods map high-dimensional patterns :math:`\mathbf{X} = [\mathbf{x}_i \in \mathbb{R}^d]_{i=1}^N` to low-dimensional representations :math:`[\hat{\mathbf{x}}_i \in \mathbb{R}^q]_{i=1}^N` in a latent space :math:`\mathbb{R}^q` with :math:`q<d`. The mapping should maintain important properties of the original high-dimensional data, e.g., topological characteristics like distance and neighborhoods. Such properties could be gradual changes in wind time series such as changing weather conditions or seasonal changes. Visualization of alert states belongs to the main applications of monitoring energy time series.

In [1]_, we employed self-organizing maps (SOMs) for sequence visualization of high-dimensional wind time series. Similar to vector quantization, we employed the SOM to place codebook vectors in the time series data space. Each neuron was assigned to a color accruing to the position in the lattice structure of the SOM. The capabilities to visualize gradual changes of SOM-based monitoring is strongly restricted to the topology of the map, e.g., the number of neurons and the structure of the network. 

The monitoring module of WindML allows embeddings in continuous latent spaces. It allows the application of the scikit-learn DR methods like PCA, isometric mapping (ISOMAP) [2]_, and locally linear embedding (LLE) [3]_. 



Latent Embeddings
+++++++++++++++++

Monitoring
++++++++++

.. [1] Kramer, O, Gieseke, F., and Satzger, B. (2013). Wind energy prediction and monitoring with neural computation. Neurocomputing, 109:84-9.
.. [2] Tenenbaum, J.B., Silva, V.D., and Langford, J.C. (2000). A gloabal geometric framework for nonlinear dimensionality reduction. Science, 290:2319-2323.
.. [3] Roweis, T.S. and Saul, L.K. (2000). Nonlinear dimensionality reduction by locally linear embedding. Science, 290:2323-2326.
