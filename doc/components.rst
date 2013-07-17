Components
==========

.. _datasets:

Datasets
========

National Renewable Energy Laboratory ("NREL") data source
---------------------------------------------------------

.. autoclass:: windml.datasets.nrel.NREL
    :members:

.. _model:

Model
=====

When using windml, you need to know the two basic types of objects. 

 * Windmill
 * Windpark

See below for a detailed description of the concepts behind those.
Enjoy.

.. _windmill:

Windmill
--------

.. autoclass:: windml.model.windmill.Windmill
    :members:

.. _windpark:

Windpark
--------

.. autoclass:: windml.model.windpark.Windpark
    :members:

.. _mapping:

Mapping
=======

.. _generaltimeseriesmodel:

The General Times Series Model
------------------------------

Our model mades predictions exclusively based on past wind power measurements.
For this task, we formulate the prediction as regression problem. Let us first
assume we want to predict the power production of a single turbine with its
time series: The wind power measurement :math:`\mathbf{x} = p(t)` (pattern) is
mapped to the power production at target time `y = p(t+t_h)` (label).
For our regression model we assume to have :math:`N` of such pattern label
pairs :math:`(\mathbf{x}^i,y^i)` that are basis of our training set
:math:`T=\{(\mathbf{x}^1,y^1),\ldots,(\mathbf{x}^n,y^n)\}` and allow
via a regression to predict the label for unknown patterns. 


One can assume, that this model generates better prediction, if more
information of the times series will be used. For this reason, we extend the
patterns by appending past measurements :math:`p(t-1),\ldots, p(t-\mu)` with
:math:`\mu \in \mathbb{N^+}`. Furthermore, we test, if taking into account
differences of measurements :math:`\Delta p(t)=p(t)-p(t-1), \ldots, \Delta p\big(t-(\mu-1)\big)-p(t-\mu)` 
leads to better results. Therefore, we consider 
on the one hand only the absolute values of the measurements as features
and get patterns with dimension :math:`d_{st}=(\mu+1)`, see class *PowerMapping*. On the other hand we use both, i.e. the absolute values and their differences that results in patterns with a dimension of :math:`d_{st}=(2\mu+1)`, see class *PowerDiffMapping*.

.. _powermapping:

Power Mapping
-------------
.. autoclass:: windml.mapping.power_mapping.PowerMapping
    :members:

Power Diff Mapping
------------------
.. autoclass:: windml.mapping.power_diff_mapping.PowerDiffMapping
    :members:


