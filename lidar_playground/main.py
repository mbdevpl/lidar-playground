"""Commandline utility for lidar-playground package."""

import argparse
import pathlib
import sys

from ._version import VERSION
from .data_io import read_flight_data, read_lidar_data
from .data_plot import prepare_plot_data, visualize_flight


def prepare_parser():
    """Prepare command-line arguments parser."""

    parser = argparse.ArgumentParser(
        prog='lidar_playground',
        description='LIDAR playground: various experiments with LIDAR data.',
        epilog='Copyright 2019 Mateusz Bysiek https://mbdevpl.github.io/ Apache License 2.0',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version',
                        version='lidar-playground {}, Python {}'.format(VERSION, sys.version))

    subparsers = parser.add_subparsers(
        dest='command', metavar='command', help=f'''command to execute; one of: "plot",
        "...", "...";
        use "command --help" to see detailed help for a given command''')

    subparser = subparsers.add_parser('plot', help='visualize flight data')
    subparser.description = 'Combine GPS and LIDAR data to show where drone was and what it saw.'
    subparser.add_argument(
        '--lidar-data', metavar='PATH', type=pathlib.Path, default=None,
        help='path to CSV file with LIDAR data')
    subparser.add_argument(
        '--gps-data', metavar='PATH', type=pathlib.Path, default=None,
        help='path to CSV file with GPS data')
    subparser.add_argument(
        '--delay', metavar='SECONDS', type=float, default=0.1,
        help='delay in seconds between showing of subsequent frames')

    return parser


def main(args=None):
    """Parse commandline arguments and execute lidar-playground accordingly."""

    parser = prepare_parser()
    parsed_args = parser.parse_args(args)

    if parsed_args.command is None:
        parser.error('no command provided')

    if parsed_args.command == 'plot':
        if parsed_args.lidar_data is None or parsed_args.gps_data is None:
            parser.error('at least one of LIDAR or GPS data paths not provided')
        print('Loading input data...')
        flight_data = read_flight_data(parsed_args.gps_data)
        lidar_data = read_lidar_data(parsed_args.lidar_data)
        print('Post-processing...')
        all_, as_series = prepare_plot_data(flight_data, lidar_data)
        print('Visualizing...')
        visualize_flight(as_series, delay=parsed_args.delay)
