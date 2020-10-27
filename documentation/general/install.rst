Installation
============

You can install Campo on Windows, macOS or Linux.
Supported Python versions are 3.6 up to 3.9.

Installing Python
-----------------

We suggest to install |miniconda|, a Python package and environment management system.
An alternative distribution is |anaconda| provided by Continuum Analytics.
The user guide and short reference on the conda pacakge manager can be found |minicondadoc|.




Installing Campo using Conda
----------------------------

We provide an environment file that you can use to install Campo.
|campoenv| the file or copy the following content to a file named ``campo.yaml``:

.. literalinclude:: ../campo.yaml

then install it with

.. code-block:: bash

   conda env create -f campo.yaml



After a successful installation you can activate your ``campo`` environment with

.. code-block:: bash

   conda activate campo

You can test your installation by printing the Campo version number

.. code-block:: bash

   python -c "import campo; print(campo.__version__)"



Upgrading Campo using pip
-------------------------

Most likely it is sufficient to upgrade the Campo module instead of recreating the conda environment.
Within your ``campo`` environment you can upgrade Campo to a newer version using pip:

.. include:: ../pip.rst




.. |miniconda| raw:: html

   <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>


.. |minicondadoc| raw:: html

   <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html" target="_blank">here</a>



.. |anaconda| raw:: html

   <a href="https://www.anaconda.com/" target="_blank">Anaconda</a>


.. |campoenv| raw:: html

   <a href="https://github.com/computationalgeography/campo/blob/master/environment/conda/campo.yaml" target="_blank">Download</a>
