.. _techniques:

Techniques
==========

This page presents the techniques applied to the wind data sets. The focus is
on forecasting of wind speed, wind power and ramps. The forecasting is based on
machine learning methodologies on discrete time series. In the following the
:ref:`windenergyprediction` is discussed as a regression task. In the next
section the detection of ramps via classification is explained, see
:ref:`detectionoframps`. Finally, ML-derived visualization of time series is
illustrated, see :ref:`visualizationoftimeseries`.  

.. _windenergyprediction:

Wind Energy Prediction
----------------------

Motivation
++++++++++
For the integration of wind power into the grid, a precise forecast of energy
has an important part to play. Only with these informations a truly sustainable
supply with low support of conventional energy rersources can be achieved.

.. _generaltimeseriesmodel:

General Times Series Model
++++++++++++++++++++++++++

Our model makes predictions exclusively based on past wind power measurements.
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
:math:`\mu \in \mathbb{N^+}`.


.. figure:: _static/genmapping.png
   :alt: General Times Series Model
   :align: center

Furthermore, we test, if taking into account
differences of measurements :math:`\Delta p(t)=p(t)-p(t-1), \ldots,` :math:`\Delta
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

.. _detectionoframps:

Classsification of Wind Energy Ramp Events
------------------------------------------

Motivation and Overview
++++++++++++++++++++++
A critical issue in maintaining grid stability are sudden and large changes (up
and down) of wind power, which are called ramp events. In this section, we
introduce the wind power ramp event prediction module. After the definition of
ramp events, we define the ramp event prediction problem as classification
problem and introduce the ramp separation and the ramp detection application
case.


Ramp Event Definition
+++++++++++++++++++++

In literature, ramps are not clearly defined {kamath,focken} and may vary in
location and sizes of wind farms and turbines. We define a ramp events as
follows. Let :math:`\mathbf{x}(t)` be the wind time series of a wind park, and
let :math:`y(t)` be the time series of the target turbine, for which we
determine the forecast. A ramp event is defined as a wind energy change from
time step :math:`t` to time step :math:`t+\lambda` by :math:`\theta \in (0,
y_{\max}]`, i.e., for an ramp-up event, it holds :math:`y(t+\lambda) -
y(t)>\theta`, for a ramp-down event it holds :math:`y(t+\lambda) -
y(t)<-\theta`.

.. _visualizationoftimeseries:

Visualizing of Times Series: Dimensionality Reduction Moduls
------------------------------------------------------------

Motivation and Overview
+++++++++++++++++++++++

In this section one can find the explanation how to visualize high-dimensional
wind time series. Monitoring of high-dimensional time-series data is a
dimensionality reduction (DR) task. DR methods map high-dimensional patterns
:math:`\mathbf{X} = [\mathbf{x}_i \in \mathbb{R}^d]_{i=1}^N` to low-dimensional
representations :math:`[\hat{\mathbf{x}}_i \in \mathbb{R}^q]_{i=1}^N` in a
latent space :math:`\mathbb{R}^q` with :math:`q<d`. The mapping should maintain
important properties of the original high-dimensional data, e.g., topological
characteristics like distance and neighborhoods. Such properties could be
gradual changes in wind time series such as changing weather conditions or
seasonal changes. Visualization of alert states belongs to the main
applications of monitoring energy time series.

In [1]_, we employed self-organizing maps (SOMs) for sequence visualization of
high-dimensional wind time series. Similar to vector quantization, we employed
the SOM to place codebook vectors in the time series data space. Each neuron
was assigned to a color accruing to the position in the lattice structure of
the SOM. The capabilities to visualize gradual changes of SOM-based monitoring
is strongly restricted to the topology of the map, e.g., the number of neurons
and the structure of the network. 

The monitoring module of WindML allows embedding into continuous latent spaces
with scikit-learn DR methods like isometric mapping (ISOMAP) [2]_ and locally
linear embedding (LLE) [3]_. We demonstrate the applications in the following.
First, we show the results of embedding the high-dimensional patterns into
2-dimensional latent spaces. Then, we use the mapping into 3-dimensional latent
spaces to monitor high-dimensional wind power time-series on the time axis.

Latent Embeddings
+++++++++++++++++

The high-dimensional patterns :math:`\mathbf{X}` are mapped to a 2-dimensional
continuous latent space :math:`\mathbb{R}^2`. To illustrate, how the results of
this first step look like, we visualize the learning results for
two-dimensional latent spaces. The figure shows the learning results of ISOMAP
with (a) neighborhood size :math:`k = 10` and (b) neighborhood size :math:`k =
30`. The data set employs :math:`d = 66` wind turbines (grid points) in a
radius of :math:`r = 10` km around a turbine in Tehachapi, California. 

.. figure:: _static/latent_embeddings.png
   :alt: Comparision of Wind Time Series Embeddings of ISOMAP for different parameters
   :align: center

   Comparision of Wind Time Series Embeddings 

Both manifold learning results show that ISOMAP is able to adapt to gradually
changing wind situations. The embeddings employ colors according to the average
wind power in the corresponding sequence. For an code and plot example, see
:ref:`example_wind_embeddings`. 

Monitoring
++++++++++

The monitoring module also offers the possibility to visualize the DR result
along the time axis. For this sake, the latent positions of the trained
manifold are used for colorization of a horizontal bar over time of a test
time-series. In the test time-series, pattern :math:`\mathbf{x}_t` of time step
:math:`t` is assigned to the color that depends on the latent position
:math:`\hat{\mathbf{x}}^*` of its closest embedded pattern :math:`\mathbf{x}^*
= \arg \min_{\mathbf{x}' \in \mathbf{X}} \|  \mathbf{x}_t - \mathbf{x}'\|^2` in
the training manifold. For training, :math:`N_1 = 2000` patterns are used. We
visualize a test set of :math:`N_2 = 800` patterns at successive time steps in
the following figures. 

.. figure:: _static/dr.png
   :alt: dimensionality reduction (DR)
   :align: center

   Different Dimensionality Reduction Methods on a Time Series

The figure shows the monitoring results of ISOMAP with (a)-(d) :math:`k = 10,
30, 50, 100` and LLE with (e) :math:`k = 10` and (f) :math:`k = 30`. Areas
colorized with a similar color and few color changes can be found in each case,
while areas with frequent changes occur at the same locations in all plots.
Both methods turn out to be robust w.r.t. the chosen neighborhood size
:math:`k`. The learning result of LLE with small neighborhood size :math:`k =
10` is worse with unstable areas of fluctuating colors in stable not changing
wind situations. ISOMAP generates stable results with all neighborhood sizes.
For an code and plot example, see :ref:`example_sequence`. 

.. [1] Kramer, O, Gieseke, F., and Satzger, B. (2013). Wind energy prediction and monitoring with neural computation. Neurocomputing, 109:84-9.
.. [2] Tenenbaum, J.B., Silva, V.D., and Langford, J.C. (2000). A gloabal geometric framework for nonlinear dimensionality reduction. Science, 290:2319-2323.
.. [3] Roweis, T.S. and Saul, L.K. (2000). Nonlinear dimensionality reduction by locally linear embedding. Science, 290:2323-2326.
