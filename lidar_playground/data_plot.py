import logging
import math
import time
import typing as t

from matplotlib import lines
from matplotlib import pyplot as plt
import numpy as np

from .geometry import normalize_radians, cartesian, polar

_LOG = logging.getLogger(__name__)


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


def visualize_flight(
        plot_data_series, begin_frame: int = 0, end_frame: int = None, delay: float = 0.5):
    """Visualize specified flight data frames by plotting each frame with given delay."""
    if end_frame is None:
        end_frame = len(plot_data_series)

    fig, ax = plt.subplots(1, 1)
    fig.figsize = (8, 8)
    fig.show()

    legend_data = [
        lines.Line2D([0], [0], color='red', lw=3, label='current sweep'),
        lines.Line2D([0], [0], marker='o', color='w', label='drone now',
                     markerfacecolor='black', markersize=6),
        lines.Line2D([0], [0], color='blue', lw=3, label='past sweeps'),
        lines.Line2D([0], [0], marker='o', color='w', label='past drone loc.',
                     markerfacecolor='silver', markersize=6)]

    for i, series in enumerate(plot_data_series[begin_frame:end_frame]):
        if i > 0:
            previous = plot_data_series[begin_frame + i - 1]
            ax.scatter(
                previous['scan']['x'], previous['scan']['y'],
                s=3, color='blue')
            ax.plot(
                [previous['drone']['x']], [previous['drone']['y']],
                marker='o', markersize=4, color='gray')
        ax.scatter(
            series['scan']['x'], series['scan']['y'],
            s=3, color='red')
        ax.plot(
            [series['drone']['x']], [series['drone']['y']],
            marker='o', markersize=4, color='black')

        fig.legend(handles=legend_data, ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.0))
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(delay)
    plt.ion()
    plt.pause(delay + 1)
    input('Press ENTER to end.')
