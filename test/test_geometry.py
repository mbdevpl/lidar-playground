
import math
import pathlib
import unittest

import numpy as np

from lidar_playground.data_io import read_lidar_data
from lidar_playground.geometry import normalize_radians, cartesian, polar

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def test_normalize_radians(self):
        for radians in np.linspace(-2 * np.pi, 2 * np.pi, 1000):
            radians = normalize_radians(radians)
            self.assertGreater(radians, -np.pi)
            self.assertLessEqual(radians, np.pi)

    def test_cartesian_polar_conversion(self):
        path = pathlib.Path('LIDARPoints.csv')
        lidar_data = read_lidar_data(_HERE.joinpath('examples', path))
        for id_, lidar_record in lidar_data.items():
            for angle, distance in lidar_record.items():
                self.assertTrue(np.isclose(angle, math.degrees(math.radians(angle))))
                angle = math.radians(angle)
                x, y = cartesian(distance, angle)
                _distance, _angle = polar(x, y)
                self.assertTrue(np.isclose(distance, _distance), msg=(id_, distance, _distance))
                self.assertTrue(
                    np.isclose(normalize_radians(angle), normalize_radians(angle)) or distance == 0,
                    msg=(id_, angle, _angle))
