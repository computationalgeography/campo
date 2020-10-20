Installation
============

You can install Campo on Windows, macOS or Linux.
Supported Python versions are 3.6 up to 3.9.

Installing Python
-----------------

We suggest to install |miniconda|, a Python package and environment management system.
An alternative is provided by |anaconda|.
The user guide and short reference on conda can be found |minicondadoc|.




Install using Conda
-------------------

We provide an environment file that you can use to install Campo.
|campoenv| the file or copy the following content to a file named ``environment.yaml``:

.. literalinclude:: ../environment.yaml

then install it with

.. code-block:: bash

   conda install -f environment.yaml



After a successful installation you can activate your environment with

.. code-block:: bash

   conda activate campo

You can test your installation by printing the Campo version number

.. code-block:: bash

   python -c "import campo; print(campo.__version__)"



.. |miniconda| raw:: html

   <a href="https://docs.conda.io/en/latest/miniconda.html" target="_blank">Miniconda</a>


.. |minicondadoc| raw:: html

   <a href="https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html" target="_blank">here</a>



.. |anaconda| raw:: html

   <a href="https://www.anaconda.com/" target="_blank">Anaconda</a>


.. |campoenv| raw:: html

   <a href="https://github.com/computationalgeography/campo/blob/master/environment/conda/environment.yaml" target="_blank">Download</a>
