Components
==========

.. _datasets:

Datasets
--------

National Renewable Energy Laboratory ("NREL") data source
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. autoclass:: windml.datasets.nrel.NREL
    :members:

.. _model:

Model
-----

When using windml, you need to know the two basic types of objects. 

 * Turbine
 * Windpark

See below for a detailed description of the concepts behind those.
Enjoy.

.. _turbine:

Turbine
++++++++

.. autoclass:: windml.model.turbine.Turbine
    :members:

.. _windpark:

Wind Park
++++++++

.. autoclass:: windml.model.windpark.Windpark
    :members:

.. _mapping:

Mapping
-------

.. _powermapping:

Power Mapping
+++++++++++++
.. autoclass:: windml.mapping.power_mapping.PowerMapping
    :members:

.. _powerdiffmapping:

Power Diff Mapping
++++++++++++++++++
.. autoclass:: windml.mapping.power_diff_mapping.PowerDiffMapping
    :members:


