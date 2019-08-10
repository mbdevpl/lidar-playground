.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python


================
LIDAR playground
================

.. image:: https://travis-ci.com/mbdevpl/lidar-playground.svg?token=yEUe1Xs3qujpSZnGZsCt&branch=master
    :target: https://travis-ci.com/mbdevpl/lidar-playground
    :alt: build status from Travis CI

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

Below is the description of current features.


Visuzalization
~~~~~~~~~~~~~~

The aim of this functionality is to satisfy the following criteria:

Create a program to provide an appropriate visualization of the drone’s path and the LIDAR data.
Ideally, the display should be able to show 1 sweep (1 scan ID) of data in isolation as well as
all the sweeps combined together. This can be on separate displays or on the same display
(with individual sweeps shown by highlighting for example)

Input: LIDARDPoints.csv and FlightPath.csv (provided or created from another Task)

Output: On-screen display

To display a visualization of drone's flight:

.. code:: bash

    python3 -m lidar_playground plot --lidar-data PATH --gps-data PATH [--frame NUMBER] [--delay SECONDS]
    # example:
    python3 -m lidar_playground plot --lidar-data test/examples/LIDARPoints.csv --gps-data test/examples/FlightPath.csv

Where LIDAR data should be a CSV file. The first line has the scan ID and number of data lines
(number of recorded points for that sweep). Each following line has the angle of the data point
(in degrees) and the distance (in millimeters) until the next scan ID header line.

And GPS data should also a CSV file. The first line has the scan ID and number of data line
(always 1). The next line is the X,Y location of the drone in meters.

In an example files ``test/examples/LIDARPoints.csv`` and ``test/examples/FlightPath.csv`` 34 sweeps are included.

Optional arguments:

*   ``--frame NUMBER``: when used, only one frame of the visualization is diplayed, i.e. no animation happens.

*   ``--delay SECONDS``: when used, delay between frames (in case when there is animation) can be changed.


Data creation
~~~~~~~~~~~~~

To create synthetic data simulating a drone's flight:

.. code:: bash

    python3 -m lidar_playground create --svg PATH --lidar-data PATH --gps-data PATH
    # example:
    python3 -m lidar_playground create --svg test/examples/layout1.svg --lidar-data test/examples/my_lidar.csv --gps-data test/examples/my_flight.csv

Where SVG file provided can be created in visual tool such as Inkscape, according to the following rules:

1. Each shape in black colour will be treated as obstacle and it's outline will be interpreted
   as walls which reflect LIDAR signal.

2. Each shape in any other colour will be treate as part of drone's flight path.

It is recommended to create many shapes in black colour, but only one shape in other colour.

The following restrictions/remarks apply:

1. Only each shape's outline is taken into account (whether it is filled or not doesn't matter).

2. Only certain shape types are allowed (currently: rectangles and paths).

3. In any line to be treated as part of drone's flight plan, only end points of the line will
   be used as places where sweep takes place.

LIDAR and GPS data files will be created according to specification given above in the visualization section.
