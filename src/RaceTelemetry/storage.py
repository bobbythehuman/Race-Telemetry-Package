from __future__ import annotations
import threading
import logging

from types import SimpleNamespace
from typing import Any
import re

LOGGER = logging.getLogger(__name__)


def prepare(text: str) -> list[list[Any]]:
    """'a[b.c].d' -> [['a', [['b'], ['c']]], ['d']]. Raises ValueError if invalid."""
    tokens = re.findall(r"\w+|[.\[\]*]", text)
    if "".join(tokens) != "".join(text.split()):
        LOGGER.error("Invalid character in %r", text)
        raise ValueError(f"Invalid character in {text!r}")
    pos = 0

    def path():
        nonlocal pos
        segments = []
        while True:
            segment = [tokens[pos]]
            pos += 1
            while pos < len(tokens) and tokens[pos] == "[":
                pos += 1
                if tokens[pos].isdigit():
                    segment.append(int(tokens[pos])); pos += 1
                elif tokens[pos] == "*":
                    segment.append("*"); pos += 1
                else:
                    segment.append(path()) # nested path as the index
                if tokens[pos] != "]":
                    LOGGER.error("Expected ']' in %r", text)
                    raise ValueError(f"Expected ']' in {text!r}")
                pos += 1
            segments.append(segment)
            if pos < len(tokens) and tokens[pos] == ".":
                pos += 1
            else:
                return segments

    try:
        result = path()
    except IndexError:
        LOGGER.error("Incomplete path %r", text)
        raise ValueError(f"Incomplete path {text!r}") from None
    if pos != len(tokens):
        LOGGER.error("Unexpected token %r in %r", tokens[pos], text)
        raise ValueError(f"Unexpected {tokens[pos]!r} in {text!r}")
    return result


def fetch(root, path, obj=None):
    """Walk a prepared path. Dynamic indices are resolved from root."""
    obj = root if obj is None else obj
    for n, (name, *indices) in enumerate(path):
        if name is not None: # None = continue after a '*'
            if not hasattr(obj, name):
                return None
            obj = getattr(obj, name)
        for k, i in enumerate(indices):
            if i == "*":
                rest = [[None, *indices[k + 1:]], *path[n + 1:]]
                return [fetch(root, rest, item) for item in obj]
            if not isinstance(i, int):
                i = fetch(root, i)
                if i < 0:
                    LOGGER.error("Negative index %r in %r", i, path)
                    raise IndexError(f"Negative index {i}")
            obj = obj[i]
    return obj


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
        self.common_attributes = ["speed", "engineRPM", "gear", "throttle", "brake", "clutch", "steering"]

        self._lock = threading.RLock()

        self.all_data: dict[str, list] = {}
        self.latest_data: dict[str, Any] = {}

        self.mapped_data = getattr(metadata_cls, "commonFieldMap", {})
        self.prepared = {key: prepare(path) for key, path in self.mapped_data.items()}

        self.all_common_data: SimpleNamespace = self._create_data_object(self.common_attributes, default_value=list)
        self.latest_common_data: SimpleNamespace = self._create_data_object(self.common_attributes)

        for _packet_id, packet_structs in metadata_cls.packetInfo.items():
            for packet_struct in packet_structs:
                packet_name = packet_struct.__name__
                if packet_name not in self.all_data:
                    self.all_data[packet_name] = []
                    self.latest_data[packet_name] = None

        LOGGER.debug("CentralStorage initialized with metadata: %r", metadata_cls.__name__)

    def _create_data_object(self, attributes: list[str], default_value: Any = None) -> SimpleNamespace:
        data = SimpleNamespace()
        for attr in attributes:
            value = default_value() if callable(default_value) else default_value
            setattr(data, attr, value)
        return data

    def _copy_data_object(self, data: SimpleNamespace, copy_lists: bool = False) -> SimpleNamespace:
        copied = SimpleNamespace()
        for attribute, value in vars(data).items():
            setattr(copied, attribute, value.copy() if copy_lists else value)
        return copied

    def _write(self, data: SimpleNamespace | None) -> None:
        """Called only by the network thread."""
        with self._lock:
            if data:
                # Retrieve packet name
                packet_name = data.__name__

                # Store packet data
                self.all_data[packet_name].append(data)
                self.latest_data[packet_name] = data

                # Store common data if present
                for common_key, mapped_key in self.prepared.items():
                    if common_key not in self.common_attributes:
                        continue
                    rootValue = sum(mapped_key, [])[0]  # Get the root attribute name
                    if hasattr(data, rootValue):
                        # value = getattr(data, mapped_key)
                        value = fetch(data, mapped_key)
                        getattr(self.all_common_data, common_key).append(value)
                        setattr(self.latest_common_data, common_key, value)

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
                "allCommonData": self._copy_data_object(self.all_common_data, copy_lists=True),
                "latestCommonData": self._copy_data_object(self.latest_common_data),
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
        return self.snapshot()

    def snapshot(self) -> dict[str, Any]:
        """Returns a consistent snapshot of the latest set of data including all packets and the latest packet."""
        return self._storage.snapshot()
