Mapping
=======

The General Times Series Model

Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.
Our model makes predictions exclusively based on past wind power measurements. For this task, we formulate the prediction as regression problem. Let us first assume we want to predict the power production of a single turbine with its time series: The wind power measurement $\mathbf{x} = p(t)$ (pattern) is mapped to the power production at target time \mbox{$y = p(t+t_h)$} (label). For our regression model we assume to have $N$ of such pattern label pairs $(\mathbf{x}^i,y^i)$ that are basis of our training set $\mbox{$T=\{(\mathbf{x}^1,y^1),\ldots,(\mathbf{x}^n,y^n)\}$}$ and allow via a regression to predict the label for unknown patterns. 

One can assume, that this model generates better prediction, if more information of the times series will be used. For this reason, we extend the patterns by appending past measurements $p(t-1),\ldots, p(t-\mu)$ with $\mu \in \mathbb{N^+}$. Furthermore, we test, if taking into account differences of measurements $\Delta p(t)=p(t)-p(t-1), \ldots, \Delta p\big(t-(\mu-1)\big)-p(t-\mu)$ leads to better results. Therefore, we consider on the one hand only the absolute values of the measurements as features
and get patterns with dimension \mbox{$d_{st}=(\mu+1)$}. On the other hand we use both, i.e. the absolute values and their differences that results in patterns with a dimension of \mbox{$d_{st}=(2\mu+1)$}.:

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


