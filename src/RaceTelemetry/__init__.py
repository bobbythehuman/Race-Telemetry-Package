# src/RaceTelemetry/__init__.py
import logging

from .main import TelemetryManager
from . import data_structures

DataStructures = data_structures

__version__ = "v6.11.12"
__all__ = ["TelemetryManager", "DataStructures", "data_structures"]

logging.getLogger(__name__).addHandler(logging.NullHandler())
