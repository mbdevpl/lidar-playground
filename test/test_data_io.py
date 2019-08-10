
import pathlib
import tempfile
import unittest

from lidar_playground.data_io import read_flight_data, write_flight_data, read_lidar_data

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def test_read_flight_data(self):
        path = pathlib.Path('FlightPath.csv')
        flight_data = read_flight_data(_HERE.joinpath('examples', path))
        self.assertEqual(len(flight_data), 34)

    def test_write_flight_data(self):
        path = pathlib.Path('FlightPath.csv')
        flight_data = read_flight_data(_HERE.joinpath('examples', path))
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            write_flight_data(flight_data, tmp_path)
            roundtrip_data = read_flight_data(tmp_path)
        self.assertTrue(flight_data.equals(roundtrip_data))

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
