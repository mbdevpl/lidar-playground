
import pathlib
import tempfile
import unittest

from lidar_playground.data_io import \
    read_flight_data, write_flight_data, read_lidar_data, write_lidar_data, \
    read_walls_data, write_walls_data

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

    def test_write_lidar_data(self):
        path = pathlib.Path('LIDARPoints.csv')
        lidar_data = read_lidar_data(_HERE.joinpath('examples', path))
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            write_lidar_data(lidar_data, tmp_path)
            roundtrip_data = read_lidar_data(tmp_path)
        self.assertListEqual(list(lidar_data.keys()), list(roundtrip_data.keys()))
        for val1, val2 in zip(list(lidar_data.values()), list(roundtrip_data.values())):
            self.assertEqual(len(val1), len(val2))
            for (k1, v1), (k2, v2) in zip(val1.items(), val2.items()):
                self.assertEqual(k1, k2)
                self.assertEqual(v1, v2)

    def test_read_write_wall_data(self):
        path = pathlib.Path('walls1.csv')
        walls_data = read_walls_data(_HERE.joinpath('examples', path))
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            write_walls_data(walls_data, tmp_path)
            roundtrip_data = read_walls_data(tmp_path)
        self.assertListEqual(walls_data, roundtrip_data)

    def test_consistency(self):
        flight_data_path = pathlib.Path('FlightPath.csv')
        flight_data = read_flight_data(_HERE.joinpath('examples', flight_data_path))
        lidar_data_path = pathlib.Path('LIDARPoints.csv')
        lidar_data = read_lidar_data(_HERE.joinpath('examples', lidar_data_path))
        self.assertEqual(len(flight_data), len(lidar_data))
        self.assertEqual(set(flight_data.index), lidar_data.keys())
