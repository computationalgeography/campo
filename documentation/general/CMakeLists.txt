file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/install_test.rst "
.. code-block:: console

   $ conda activate campo
   (campo) $ python -c \"import campo; print(campo.__version__)\"
   ${campo_VERSION}
")
