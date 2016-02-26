.. _gettingstarted:

Getting Started
===============

The first part of this page provides an installation guide, see :ref:`installation`.
Second, an overview of the architecture is presented and the core
features and components are discussed, see :ref:`architecture`. At last,
it is exemplary illustrated how windML is used, see :ref:`runningexample`.  

.. _installation:

Installation
------------

.. highlight:: none

Before the installation of windML you have to make sure that all needed
:ref:`dependencies` are installed. In order to install windML, you have to
check out a working copy of our stable branch in our development repository. ::
    
    $ git clone https://github.com/cigroup-ol/windml.git 

After cloning the stable branch, the new folder *windml* is located in your
current working directory. Make sure your windML-folder is in your Python PATH
by executing. ::
    
    $ export PYTHONPATH=$PYTHONPATH:<windml-directory>

.. highlight:: python

.. _architecture:

Architecture
------------

Below, an illustration of the windML architecture is presented.  At the top,
one can see exemplary available data sources of wind data time-series open to
the public on the internet. The DataSource classes implemented in windML
download the data from data mirrors, parse the data into an windML-specific
data format and keep the data in a local cache. The windML-specific format is
defined by the *Windpark* and *Turbine* classes. See :ref:`windpark` and
:ref:`turbine` documentation for the windML-specific model. The wind parks and
turbines are selected by specifying ID and radius. See :ref:`datasets` page
for the documentation of the data sets and methods to fetch time-series.

.. figure:: _static/schema.png
   :alt: architecture
   :align: center

   windML schematic architecture

Given *Windpark* and *Turbine* objects, one can visualize the data via
different visualization components such as dimensionality reduction,
park and turbine information, information about the time-series, topology
etc., see :ref:`examples`. An important motivation of windML is forecasting
time-series with regression and classification. For both methodologies, a
mapping of a time-series to labels is required.
Different mapping
approaches have been tested in the past, see :ref:`mapping` for
explanation of the various mapping methods. In the current release,
the following regression techniques have been applied: support vector regression (SVR), KNN regression, and linear regression. 

.. _runningexample:

Running an Example
------------------

Running some examples of windML is probably the best way to start. In the :ref:`examples` gallery all scripts from the /examples folder of the windML installation are plotted. In order to run an example, one only has to execute the corresponding Python script. Please make sure to install windML correctly, see the :ref:`installation` page. 

