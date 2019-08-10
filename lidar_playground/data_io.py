import csv
import logging
import pathlib
import typing as t

# import numpy as np
import pandas as pd

_LOG = logging.getLogger(__name__)


def read_flight_data(path: pathlib.Path) -> pd.DataFrame:
    """Read drone flight data.

    FlightPath

    FlightPath data is provided (and should be written in if you generate it) as a CSV file.
    The first line has the scan ID and number of data line (always 1). The next line is the X,Y
    location of the drone in meters
    """
    index = []
    data = []
    with path.open() as flight_file:
        flight_csv = csv.reader(flight_file)
        record = None
        for raw_record in flight_csv:
            _LOG.debug('%s', raw_record)
            if record is None:
                id_, data_len = raw_record
                id_ = int(id_)
                data_len = int(data_len)
                assert id_ not in index, raw_record
                assert data_len == 1, raw_record
                record = []
                index.append(id_)
                continue
            x, y = raw_record
            x = float(x)
            y = float(y)
            record.append(x)
            record.append(y)
            data.append(record)
            record = None
    return pd.DataFrame(data=data, index=index, columns=('x', 'y'))


def read_lidar_data(path: pathlib.Path) -> t.Dict[int, t.Dict[float, float]]:
    """Read drone LIDAR data.

    LIDARDPoints

    LIDARPoints data is provided (and should also be the output format, if you generate LIDAR data)
    as a CSV file. The first line has the scan ID and number of data lines (number of recorded
    points for that sweep). Each following line has the angle of the data point (in degrees)
    and the distance (in millimeters) until the next scan ID header line. 34 sweeps are included.
    """
    lidar_data = {}
    with path.open() as lidar_file:
        lidar_csv = csv.reader(lidar_file)
        record = None
        remaining = None
        for raw_record in lidar_csv:
            _LOG.debug('%s', raw_record)
            if record is None:
                id_, data_len = raw_record
                id_ = int(id_)
                data_len = int(data_len)
                assert id_ not in lidar_data, raw_record
                assert data_len > 0, raw_record
                record = {}
                remaining = data_len
                lidar_data[id_] = record
                continue
            angle, distance = raw_record
            angle = float(angle)
            distance = float(distance) / 1000
            record[angle] = distance
            remaining -= 1
            if remaining == 0:
                record = None
    return lidar_data