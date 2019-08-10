"""General-purpose 2D geometry functions."""

import logging
import typing as t

import numpy as np
from shapely.geometry import LineString, Point

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
