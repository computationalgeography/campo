Installation
============

You can install Campo on Windows, macOS or Linux.

Installing Python
-----------------

We suggest to install |miniconda|, a Python package and environment management system.
The user guide and short reference on conda can be found |minicondadoc|.

Supported Python versions are 3.6, 3.7 or 3.8.



Installing Campo
----------------

We provide an environment file that you can use to install Campo.
Copy the following content to a file named ``environment.yaml``

.. Download the file at
.. environment.yaml
.. or c

.. literalinclude:: ../environment.yaml

then install it with

.. code-block:: bash

   conda install -f environment.yaml



After a successful installation you can activate your environment with

.. code-block:: bash

   conda activate campo






.. |miniconda| raw:: html

   <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>


.. |minicondadoc| raw:: html

   <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html" target="_blank">here</a>


.. Install LUE
.. -----------
..
.. .. code-block:: bash
..
..    conda install -c conda-forge -c http://pcraster.geo.uu.nl/pcraster/pcraster/ lue
..
..
.. Install framework
.. -----------------
..
.. .. code-block:: bash
..
..    git clone git@github.com:pcraster/fame.git
..
..
.. Install PCRaster
.. ----------------
..
.. .. code-block:: bash
..
..    conda install -c conda-forge pcraster
