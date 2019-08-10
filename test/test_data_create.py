
import pathlib
import unittest

from lidar_playground.data_create import extract_vectors

_HERE = pathlib.Path(__file__).parent


class Tests(unittest.TestCase):

    def test_extract_vectors(self):
        path = pathlib.Path('layout1.svg')
        walls, sweep_locations = extract_vectors(_HERE.joinpath('examples', path))
        self.assertGreater(len(walls), 10)
        self.assertEqual(len(sweep_locations), 6)
