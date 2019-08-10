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


def closest_intersection(line: LineString, lines: t.Sequence[LineString]) -> t.Optional[Point]:
    intersections = []
    for line_ in lines:
        intersection = line.intersection(line_)
        if not isinstance(intersection, Point):
            continue
        intersections.append(intersection)

    if not intersections:
        return None

    xfun = min if line.coords[0][0] < line.coords[1][0] else max
    yfun = min if line.coords[0][1] < line.coords[1][1] else max

    return Point(xfun(_.x for _ in intersections), yfun(_.y for _ in intersections))
