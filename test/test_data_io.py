
import pathlib
import unittest

from lidar_playground.data_io import read_flight_data, read_lidar_data

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def test_read_flight_data(self):
        path = pathlib.Path('FlightPath.csv')
        flight_data = read_flight_data(_HERE.joinpath('examples', path))
        self.assertEqual(len(flight_data), 34)

    def test_read_lidar_data(self):
        path = pathlib.Path('LIDARPoints.csv')
        lidar_data = read_lidar_data(_HERE.joinpath('examples', path))
        self.assertEqual(len(lidar_data), 34)

    def test_consistency(self):
        flight_data_path = pathlib.Path('FlightPath.csv')
        flight_data = read_flight_data(_HERE.joinpath('examples', flight_data_path))
        lidar_data_path = pathlib.Path('LIDARPoints.csv')
        lidar_data = read_lidar_data(_HERE.joinpath('examples', lidar_data_path))
        self.assertEqual(len(flight_data), len(lidar_data))
        self.assertEqual(set(flight_data.index), lidar_data.keys())
