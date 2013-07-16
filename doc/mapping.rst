Mapping
=======

The General Times Series Model


One can assume, that this model generates better prediction, if more information of the times series will be used. For this reason, we extend the patterns by appending past measurements :math:`p(t-1),\ldots, p(t-\mu)` with :math:`\mu \in \mathbb{N^+}`. Furthermore, we test, if taking into account differences of measurements :math:`\Delta p(t)=p(t)-p(t-1), \ldots, \Delta p\big(t-(\mu-1)\big)-p(t-\mu)` leads to better results. Therefore, we consider on the one hand only the absolute values of the measurements as features
and get patterns with dimension :math:`d_{st}=(\mu+1)`. On the other hand we use both, i.e. the absolute values and their differences that results in patterns with a dimension of :math:`d_{st}=(2\mu+1)`.

The methods of this class handle the construction of features and labels from the raw data (see datasets). 
One can choose between features consisting only of absolute measurements or features also including the corresponding changes. See the following documentation 


Power Mapping
-------------
.. autoclass:: windml.mapping.power_mapping.PowerMapping
    :members:

Power Diff Mapping
------------------
.. autoclass:: windml.mapping.power_diff_mapping.PowerDiffMapping
    :members:


