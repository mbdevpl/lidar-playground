import logging
import math
import pathlib
import typing as t

import numpy as np
import pandas as pd
from shapely.geometry import Point, LineString
from svglib.svglib import svg2rlg
from reportlab.graphics.shapes import Group, Rect, Path
from reportlab.lib.colors import Color

from .geometry import cartesian, polar, closest_intersection

_LOG = logging.getLogger(__name__)


def extract_group_shapes_recursive(group):
    extracted = []
    for elem in group.contents:
        if isinstance(elem, Group):
            extracted += extract_group_shapes_recursive(elem)
        elif isinstance(elem, (Rect, Path)):
            extracted.append(elem)
        else:
            raise NotImplementedError(f'Handling of {type(elem)} is not implemented yet!')
    return extracted


def extract_vectors(path: pathlib.Path):
    drawing = svg2rlg(str(path))
    elems = extract_group_shapes_recursive(drawing)

    walls = []
    flight = []
    for elem in elems:
        if isinstance(elem, Rect):
            elem_lines = [
                LineString([(elem.x, elem.y), (elem.x + elem.width, elem.y)]),
                LineString([(elem.x, elem.y), (elem.x, elem.y + elem.height)]),
                LineString([(elem.x, elem.y + elem.height),
                            (elem.x + elem.width, elem.y + elem.height)]),
                LineString([(elem.x + elem.width, elem.y),
                            (elem.x + elem.width, elem.y + elem.height)]),
            ]
        elif isinstance(elem, Path):
            elem_lines = [
                LineString([(x1, y1), (x2, y2)])
                for x1, y1, x2, y2 in zip(
                    elem.points[:-2:2], elem.points[1:-2:2],
                    elem.points[2::2], elem.points[3::2])]
        else:
            raise NotImplementedError(f'Handling of {type(elem)} is not implemented yet!')
        if elem.strokeColor == Color(0, 0, 0, 1):
            walls += elem_lines
        else:
            flight += elem_lines

    assert flight

    flight_points = [Point(line.coords[0]) for line in flight]
    flight_points.append(Point(flight[-1].coords[1]))

    return walls, flight_points


def simulate_flight(walls: t.List[LineString], sweep_locations: t.List[Point]):
    flight_data = pd.DataFrame(
        data=[[point.x, -point.y] for point in sweep_locations],
        columns=['x', 'y'], index=list(range(len(sweep_locations))))

    _LOG.debug('GPS points: %i', len(flight_data))

    angles = np.linspace(-np.pi, np.pi, 500)
    cartesians = [cartesian(1000, radians) for radians in angles]

    lidar_data: t.Dict[int, t.Dict[float, float]] = {}

    for i, point in enumerate(sweep_locations):
        lidar_data[i] = {}
        for x, y in cartesians:
            ray = LineString([(point.x, point.y), (point.x + x, point.y + y)])
            intersection = closest_intersection(ray, walls)
            if intersection is None:
                continue
            distance, radians = polar(intersection.x - point.x, intersection.y - point.y)
            lidar_data[i][math.degrees(radians)] = distance
        assert len(lidar_data[i]) <= 500

    _LOG.debug('LIDAR points: %i', len(lidar_data))
    assert len(flight_data) == len(lidar_data)

    return flight_data, lidar_data
