# src/my_package/__init__.py
from .main import TelemetryManager
import logging

__all__ = ["TelemetryManager"]
logging.getLogger(__name__).addHandler(logging.NullHandler())
