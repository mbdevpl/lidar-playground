"""Default logging mechanism for lidar-playground package."""

import logging
import os

logging.basicConfig(
    level=getattr(logging, os.environ.get('LOGGING_LEVEL', 'warning').upper(), logging.WARNING))
