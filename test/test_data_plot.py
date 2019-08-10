
import math
import pathlib
import unittest

import numpy as np

from lidar_playground.data_io import read_flight_data, read_lidar_data
from lidar_playground.data_plot import normalize_radians, cartesian, polar, prepare_plot_data

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def setUp(self):
        path = pathlib.Path('FlightPath.csv')
        self.flight_data = read_flight_data(_HERE.joinpath('examples', path))
        path = pathlib.Path('LIDARPoints.csv')
        self.lidar_data = read_lidar_data(_HERE.joinpath('examples', path))

    def test_normalize_radians(self):
        for radians in np.linspace(-2 * np.pi, 2 * np.pi, 1000):
            radians = normalize_radians(radians)
            self.assertGreater(radians, -np.pi)
            self.assertLessEqual(radians, np.pi)

    def test_cartesian_polar_conversion(self):
        for id_, lidar_record in self.lidar_data.items():
            for angle, distance in lidar_record.items():
                self.assertTrue(np.isclose(angle, math.degrees(math.radians(angle))))
                angle = math.radians(angle)
                x, y = cartesian(distance, angle)
                _distance, _angle = polar(x, y)
                self.assertTrue(np.isclose(distance, _distance), msg=(id_, distance, _distance))
                self.assertTrue(
                    np.isclose(normalize_radians(angle), normalize_radians(angle)) or distance == 0,
                    msg=(id_, angle, _angle))

    def test_prepare_plot_data(self):
        prepare_plot_data(self.flight_data, self.lidar_data)
