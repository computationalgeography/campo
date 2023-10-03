Installation
============

You can install Campo on Windows, macOS or Linux.
Supported Python versions are 3.6 or higher.

Installing Python
-----------------

We suggest to install the |mambaforge| distribution.
Alternative distributions are |miniconda|, or |anaconda| provided by Continuum Analytics.
The user guide and short reference on the conda pacakge manager can be found |minicondadoc|.


Installing Campo using Conda
----------------------------

You can install Campo in an existing environment with

.. code-block:: console

   conda install -c conda-forge campo


..
.. After a successful installation you can activate your ``campo`` environment with
..
.. .. code-block:: bash
..
.. ..    conda activate campo

You can test your installation afterwards by printing the Campo version number

.. code-block:: console

   python -c "import campo; print(campo.__version__)"




.. |mambaforge| raw:: html

   <a href="https://mamba.readthedocs.io/en/latest/mamba-installation.html" target="_blank">Mambaforge</a>


.. |miniconda| raw:: html

   <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>


.. |minicondadoc| raw:: html

   <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html" target="_blank">here</a>



.. |anaconda| raw:: html

   <a href="https://www.anaconda.com/" target="_blank">Anaconda</a>
