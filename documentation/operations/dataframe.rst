Reading from a LUE dataset
==========================

Simulations performed with Campo can generate different types of output data such as static or dynamic data for field- or point-agents.
The contents from a dataset generated with Campo can be accesed by a dictionary-based dataframe data structure.
The dataframe returns agent data in different ways, each specific for the spatio-temporal type of the agents.

In general, access to a LUE dataset by using the dataframe approach can be done as follows:


.. code-block:: python

   import lue.data_model as ldm
   import campo

   # Open LUE dataset of specific name
   dataset = ldm.open_dataset("catchment.lue")

   # Obtain elevation and landuse properties from the catchment phenomenon
   dataframe = campo.dataframe.select(dataset.catchment, property_names=['elevation', 'landuse'])


``dataframe`` returned by ``select()`` holds a nested dictionary with the following general structure:


.. code-block:: python

   { phenomenon :
     { property_set :
       { property_name1 : property_values,
         ...
         property_nameN : property_values
       }
     }
   }



The return value of ``property_values`` will be of different type based on the characteristics of an agent.
Basically, ``property_values`` is of type xarray and organised according to the different agent types.

.. ddetermine the return type of property_values:

Dataframe return types
----------------------

Static data
~~~~~~~~~~~

Agents have the same shape
^^^^^^^^^^^^^^^^^^^^^^^^^^

This situation applies to point agents, and field agents all having the same spatial extent (e.g. all field-agents are of size 1ha).
``select()`` returns a structure as follows:


.. code-block:: bash

   property_values is an xarray dataarray:

   values: 1d or 2d array depending on type agent
   xcoord: point coord or list with coords along x axis
   ycoord: point coord or list with coords along y axis
   objj_id: list of object IDs


Agents having different shapes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This situation applies field agents each having a different spatial extent (e.g. field-agents representing different catchments).
``select()`` returns a structure as follows:

.. code-block:: bash

   property_values is an xarray dataset with for each object a dataarray (key : object_id):

   values: 2d array depending on type agent
   xcoord: list with coords along x axis
   ycoord: list with coords along y axis


Dynamic data
~~~~~~~~~~~~


Agents have the same shape
^^^^^^^^^^^^^^^^^^^^^^^^^^

This situation applies to point agents, and field agents all having the same spatial extent (e.g. all field-agents are of size 1ha).
``select()`` returns a structure as follows:

.. code-block:: bash

   property_values is an xarray dataarray:

   values: array with shape (obj_ids, timesteps, 1)
   xcoord: list of x coord, e.g. [x1,x2,x3,x4,x5]
   ycoord: list of y coord, e.g. [y1,y2,y3,y4,y5]
   objj_id: list of object IDs, e.g. [1,2,3,4,5]
   time: list with timesteps, e.g. ['2000-01-01', '2000-01-02', '2000-01-03']

Agents having different shapes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


This situation applies field agents each having a different spatial extent (e.g. field-agents representing different catchments).
``select()`` returns a structure as follows:


.. code-block:: bash

   property_values is an xarray dataarray:

   values: array with shape (obj_ids, timesteps, rows, cols)
   xcoord: list of coords along x axis, [xmin,...,xmax]
   ycoord: list of coords along y axis, [ymax,...,ymin]
   objj_id: list of object IDs, e.g. [1,2,3,4,5]
   time: list with timesteps, e.g. ['2000-01-01', '2000-01-02', '2000-01-03']


Accessing data
--------------

Property values can be accessed using the dictionary notation:


.. code-block:: python

   property_values = dataframe['catchment']['area']['elevation']



Selections can then be done using the xarray notation, e.g. by object id as:

.. code-block:: python

   res = property_values.loc[3,:]

or by a timestep as:

.. code-block:: python

   res = property_values.loc[:,'2000-01-02' ,:]


In case you want to have plain access to the array values you can obtain them as NumPy array with

.. code-block:: python

   res = property_values.values








Reference
---------

.. currentmodule:: campo

.. autosummary::
   :toctree: generated

   dataframe.select
   to_csv
   to_gpkg
   to_tiff
   to_geotiff
