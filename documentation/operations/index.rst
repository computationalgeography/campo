Reference documentation
=======================

Reference documentation of the currently implemeted operations.

Initialisation
--------------

.. currentmodule:: campo

.. .dataset


.. autosummary::
   :toctree: generated

   Campo
   Campo.add_phenomenon
   Campo.create_dataset
   Campo.write
   Campo.set_time

   Phenomenon
   Phenomenon.add_property_set
   Phenomenon.set_epsg



Operations on field or agent properties
---------------------------------------


.. currentmodule:: campo

Operations
~~~~~~~~~~

.. autosummary::
   :toctree: generated

   abs
   exp
   uniform
   where


Operators
~~~~~~~~~

.. autosummary::
   :toctree: generated

   add
   divide
   equal
   greater_equal
   greater
   less_equal
   less
   mul
   not_equal
   power
   sub

Operations on field properties
------------------------------

.. autosummary::
   :toctree: generated

   slope
   spread



Exporting to other formats
--------------------------

.. autosummary::
   :toctree: generated

   to_csv
   to_gpkg
   to_tiff
