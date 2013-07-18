Techniques
==========


Wind Energy Prediction
----------------------
For the integration of wind power into the grid, a precise forecast of energy has an important part to play. Only with these informations a truly sustainable supply with low support of conventional energy rersources can be achieved.


General Times Series Model
++++++++++++++++++++++++++
Our model mades predictions exclusively based on past wind power measurements.
For this task, we formulate the prediction as regression problem. Let us first
assume we want to predict the power production of a single turbine with its
time series: The wind power measurement :math:`\mathbf{x} = p(t)` (pattern) is
mapped to the power production at target time :math:`y = p(t+t_h)` (label).
For our regression model we assume to have :math:`N` of such pattern label
pairs :math:`(\mathbf{x}^i,y^i)` that are basis of our training set
:math:`T=\{(\mathbf{x}^1,y^1),\ldots,(\mathbf{x}^n,y^n)\}` and allow
via a regression to predict the label for unknown patterns.


One can assume, that this model generates better prediction, if more information of the times series will be used. For this reason, we extend the patterns by appending past measurements :math:`p(t-1),\ldots, p(t-\mu)` with
:math:`\mu \in \mathbb{N^+}`. Furthermore, we test, if taking into account differences of measurements :math:`\Delta p(t)=p(t)-p(t-1), \ldots, \Delta p\big(t-(\mu-1)\big)-p(t-\mu)`
leads to better results. Therefore, we consider on the one hand only the absolute values of the measurements as features
and get patterns with dimension :math:`d_{st}=(\mu+1)`, see :ref:`powermapping`. On the other hand we use both, i.e. the absolute values and their differences that results in patterns with a dimension of :math:`d_{st}=(2\mu+1)`, see :ref:`powerdiffmapping`.

Visualizing of Times Series: Dimensionality Reduction Moduls
------------------------------------------------------------

Classsification of Wind Energy Ramp Events
------------------------------------------

