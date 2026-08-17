from __future__ import annotations
import threading
import logging

from types import SimpleNamespace
from typing import Any

LOGGER = logging.getLogger(__name__)


class CentralStorage:
    """
    Holds the latest network data.  Worker threads receive a read-only view
    via ReadOnlyStorage so they cannot accidentally edit the contents.
    """

    def __init__(self, metadata_cls: type) -> None:
        """
        Initializes the CentralStorage with the provided metadata class.
        The metadata class is expected to have a `packetInfo` attribute that
        defines the structure of the packets to be stored.
        """

        self._lock = threading.RLock()

        self.all_data: dict[str, list] = {}
        self.latest_data: dict[str, Any] = {}

        for _packet_id, packet_structs in metadata_cls.packetInfo.items():
            for packet_struct in packet_structs:
                packet_name = packet_struct.__name__
                if packet_name not in self.all_data:
                    self.all_data[packet_name] = []
                    self.latest_data[packet_name] = None

        LOGGER.debug("CentralStorage initialized with metadata: %r", metadata_cls.__name__)

    def _write(self, data: SimpleNamespace | None) -> None:
        """Called only by the network thread."""
        with self._lock:
            if data:
                packet_name = data.__name__

                self.all_data[packet_name].append(data)
                self.latest_data[packet_name] = data

    def snapshot(self) -> dict[str, Any]:
        """
        Return a consistent snapshot for worker threads.

        Keys are intentionally kept as "allData" / "latestData" (rather than
        renamed to match the snake_case internal attributes) to preserve the
        existing public contract that worker functions rely on.
        """
        with self._lock:
            return {
                "allData": self.all_data.copy(),
                "latestData": self.latest_data.copy(),
            }


class ReadOnlyStorage:
    """
    Thin wrapper passed to worker threads.
    Exposes only .snapshot() — no write methods visible.
    """

    def __init__(self, storage: CentralStorage) -> None:
        """Initializes the ReadOnlyStorage with a reference to the CentralStorage."""
        self._storage = storage
        LOGGER.debug("ReadOnlyStorage initialized.")

    def __iter__(self) -> "ReadOnlyStorage":
        LOGGER.debug("ReadOnlyStorage returned an iterable object of itself.")
        return self

    def __next__(self) -> dict[str, Any]:
        """Returns the latest data snapshot."""
        return self.snapshot().get("latestData", {"None": None})

    def snapshot(self) -> dict[str, Any]:
        """Returns a consistent snapshot of the latest data."""
        return self._storage.snapshot()
