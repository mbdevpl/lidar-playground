import collections
import pathlib
import typing as t

import pandas as pd
from svglib.svglib import svg2rlg
from reportlab.graphics.shapes import Group, Rect, Path
from reportlab.lib.colors import Color

Point = collections.namedtuple('Point', 'x, y')

Line = collections.namedtuple('Line', 'x1, y1, x2, y2')


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
                Line(x1=elem.x, y1=elem.y, x2=elem.x + elem.width, y2=elem.y),
                Line(x1=elem.x, y1=elem.y, x2=elem.x, y2=elem.y + elem.height),
                Line(x1=elem.x, y1=elem.y + elem.height,
                     x2=elem.x + elem.width, y2=elem.y + elem.height),
                Line(x1=elem.x + elem.width, y1=elem.y,
                     x2=elem.x + elem.width, y2=elem.y + elem.height),
            ]
        elif isinstance(elem, Path):
            elem_lines = [
                Line(x1=x1, y1=y1, x2=x2, y2=y2)
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

    flight_points = [Point(line.x1, line.y1) for line in flight]
    flight_points.append(Point(flight[-1].x2, flight[-1].y2))

    return walls, flight_points


def simulate_flight(walls: t.List[Line], sweep_locations: t.List[Point]):
    flight_data = pd.DataFrame(
        data=[[point.x, point.y] for point in sweep_locations],
        columns=['x', 'y'], index=list(range(len(sweep_locations))))

    lidar_data = None

    return flight_data, lidar_data
