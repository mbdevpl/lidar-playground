.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


================
LIDAR playground
================

Various experiments with LIDAR data.

This package was created as an experiment.


Requirements
============

Python 3.6 or later.

Python libraries as specified in `<requirements.txt>`_.

Building and running tests additionally requires packages listed in `<test_requirements.txt>`_.


How to install and run
======================

Testing
-------

This step is optional, but you might want to check if everything works before proceeding.

.. code:: bash

    pip3 install -r test_requirements.txt
    python3 -m unittest -v


To increase verbosity of the tests, you can do one of the following:

.. code:: bash

    LOGGING_LEVEL=info python3 -m unittest -v
    LOGGING_LEVEL=debug python3 -m unittest -v

To see test coverage:

.. code:: bash

    pip3 install coverage
    python3 -m coverage run --source . --branch -m unittest -v
    python3 -m coverage report --show-missing  # show coverage report in the terminal
    python3 -m coverage html  # generate HTML coverage report
    xdg-open htmlcov/index.html  # open the HTML report in the browser

Some tests are not ran by default because they test actual installation of package into the system.
To run those tests as well, do one of the following:

.. code:: bash

    TEST_PACKAGING=1 python3 -m unittest -v
    TEST_PACKAGING=1 python3 -m coverage run --source . --branch -m unittest -v


Installation
------------

You can use provided wheel or source distribution to install. To install from source, do:

.. code:: bash

    pip3 install .


Running
-------

To get help about available functionality:

.. code:: bash

    python3 -m lidar_playground --help
