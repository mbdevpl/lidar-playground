
import pathlib
import unittest

from lidar_playground.data_io import read_flight_data, read_lidar_data
from lidar_playground.data_plot import prepare_plot_data

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def setUp(self):
        path = pathlib.Path('FlightPath.csv')
        self.flight_data = read_flight_data(_HERE.joinpath('examples', path))
        path = pathlib.Path('LIDARPoints.csv')
        self.lidar_data = read_lidar_data(_HERE.joinpath('examples', path))

    def test_prepare_plot_data(self):
        prepare_plot_data(self.flight_data, self.lidar_data)
