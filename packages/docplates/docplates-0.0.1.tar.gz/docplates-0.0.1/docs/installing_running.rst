.. _Installing & Running:

Installing & Running
====================

There are many ways to install or run Docplates.



Install Using Pip
-----------------

Docplates can be simply installed by running:

.. code-block:: shell

    pip install docplates


Or if you prefer the development branch, one could use:

.. code-block:: shell

    pip install git+https://gitlab.oscdev.io/software/docplates/docplates.git


Alternatively if you prefer installing from a checked out git repository:

.. code-block:: shell

    pip install .


Lastly, you could also build it and install the wheel...

.. code-block:: shell

    tox -e build
    pip install dist/docplates-*.whl



Run Using Tox
-------------

You can also simply run Docplates from a checked out Git repository using the following:

.. code-block:: shell

    tox -e run -- ...

This will install a virtual environment in ``.tox`` which will be used to satisfy the Python dependencies.
