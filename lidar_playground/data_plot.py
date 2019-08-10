import logging
import math
import typing as t

import numpy as np

_LOG = logging.getLogger(__name__)


# def normalize_degrees(degrees: float) -> float:
#     if degrees > 180:
#         _LOG.debug('normalizing degrees %f', degrees)
#         return degrees - 360
#     if degrees <= -180:
#         _LOG.debug('normalizing degrees %f', degrees)
#         return degrees + 360
#     return degrees


def normalize_radians(radians: float) -> float:
    if radians > np.pi:
        _LOG.debug('normalizing radians %f', radians)
        return radians - 2 * np.pi
    if radians <= -np.pi:
        _LOG.debug('normalizing radians %f', radians)
        return radians + 2 * np.pi
    return radians


def pair(complex_: complex) -> t.Tuple[float, float]:
    return np.real(complex_), np.imag(complex_)


def cartesian(distance: float, radians: float) -> t.Tuple[float, float]:
    return pair(distance * np.exp(1j * radians))


def polar(x: float, y: float) -> t.Tuple[float, float]:
    return np.hypot(x, y), np.arctan2(y, x)


def prepare_plot_data(flight_data, lidar_data):
    all_ = {'x': [], 'y': []}
    as_series = []
    for id_ in lidar_data:
        flight_record = flight_data.loc[id_]
        lidar_record = lidar_data[id_]
        series = {
            'drone': {'x': flight_record.x, 'y': -flight_record.y},
            'scan': {'x': [], 'y': []}}
        _LOG.debug('drone at (%f, %f)', flight_record.x, flight_record.y)
        for angle, distance in lidar_record.items():
            assert np.isclose(angle, math.degrees(math.radians(angle)))
            angle = math.radians(angle)
            x, y = cartesian(distance, angle)
            _distance, _angle = polar(x, y)
            assert np.isclose(distance, _distance), (id_, distance, _distance)
            assert (np.isclose(normalize_radians(angle), normalize_radians(angle))
                    or distance == 0), (id_, angle, _angle)
            x += flight_record.x
            y -= flight_record.y  # y coordinate is inverted in the flight vs lidar data
            all_['x'].append(x)
            all_['y'].append(y)
            series['scan']['x'].append(x)
            series['scan']['y'].append(y)
        as_series.append(series)
    return all_, as_series
