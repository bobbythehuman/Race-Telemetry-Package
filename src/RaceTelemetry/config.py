from __future__ import annotations
import re
import logging
import ctypes

from typing import Any, Callable

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config — metadata + settings, validation only
# ---------------------------------------------------------------------------


class TelemetryConfig:
    """
    Holds the metadata and settings for the telemetry system.
    Provides validation and unpacking of metadata attributes for easy access.
    """

    def __init__(self):
        self.active_metadata: type | None = None
        self.local_ip: str = "0.0.0.0"
        self.destination_ip: str | None = None

        # from meta data
        self.main_port: int | None = None
        self.heartbeat_port: int | None = None
        self.heartbeat_func: Callable[..., Any] | None = None
        self.handshake_port: int | None = None
        self.handshake_func: tuple[Callable[..., Any], Callable[..., Any]] | None = None
        self.decryption_func: Callable[..., Any] | None = None
        self.header_packet: type | None = None
        self.packet_id_attr: str | None = None
        self.all_shared_memory_names: str | None | dict[str, str] = None
        self.packet_info: dict[int, tuple[type, ...]] | None = None

        self.receiver_mode: str = "udp"
        self.decoder_mode: str = "static"

        self.enum_mode: int = 0

        self.heartbeat_destination: tuple[str, int] | None = None

        LOGGER.debug("TelemetryConfig initialized.")

    def update_meta(self, metadata_cls: type) -> bool:
        if self.active_metadata == metadata_cls:
            return True

        self.active_metadata = metadata_cls
        self._unpack_meta_data()
        LOGGER.debug("Metadata updated to %r.", metadata_cls.__name__ if metadata_cls else None)
        return True

    def update_local_ip(self, ip: str) -> bool:
        if not self._is_valid_ip(ip):
            return False

        self.local_ip = ip
        LOGGER.debug("Local IP has been set to %s", self.local_ip)
        return True

    def update_send_ip(self, ip: str) -> bool:
        if not self._is_valid_ip(ip):
            return False

        self.destination_ip = ip
        self._update_heartbeat_destination()
        LOGGER.debug("Destination IP has been set to %s", self.destination_ip)
        return True

    def set_enum_mode(self, target: int = 0) -> bool:
        if not self._valid_type(target, int, "Enum Mode"):
            return False
        if target not in [0, 1, 2]:
            LOGGER.warning("Enum mode must be 0, 1, or 2.")
            return False

        self.enum_mode = target
        LOGGER.debug("Enum Mode has been set to %s", self.enum_mode)
        return True

    def _meta_data_check(self, name: str, default_value: Any = None) -> Any:
        """
        Helper function to check if metadata has the attribute, and return it if it does.
        Otherwise return the provided default value.
        """

        if hasattr(self.active_metadata, name):
            return getattr(self.active_metadata, name)
        else:
            return default_value

    def _unpack_meta_data(self) -> None:
        """
        Helper function to unpack metadata attributes into class attributes for easy access
        """
        self.main_port = self._meta_data_check("port")

        self.heartbeat_port = self._meta_data_check("heartBeatPort")
        self.heartbeat_func = self._meta_data_check("heartBeatFunc")
        self._update_heartbeat_destination()

        self.handshake_port = self._meta_data_check("handShakePort")
        self.handshake_func = self._meta_data_check("handShakeFunc")

        self.decryption_func = self._meta_data_check("decryptionFunc")

        self.header_packet = self._meta_data_check("headerInfo")
        self.packet_id_attr = self._meta_data_check("packetIDAttribute")

        self.all_shared_memory_names = self._meta_data_check("allSharedMemoryNames")

        self.packet_info = self._meta_data_check("packetInfo", {})

        self.receiver_mode = self._meta_data_check("receiverMode", "udp")
        self.decoder_mode = self._meta_data_check("decoderMode", "static")

        LOGGER.debug("Metadata unpacked: %r", self.active_metadata.__name__ if self.active_metadata else None)

    def _is_valid_ip(self, ip: str) -> bool:
        if not self._valid_type(ip, str, "IP"):
            return False

        if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", ip):
            return True

        LOGGER.warning("Invalid IP address: %r", ip)
        return False

    def _valid_type(self, value: object, expected_type: type, name: str) -> bool:
        if isinstance(value, expected_type):
            return True
        else:
            LOGGER.warning("%r must be a %r.", name, expected_type)
            return False

    def _update_heartbeat_destination(self) -> None:
        if self.destination_ip and self.heartbeat_port:
            self.heartbeat_destination = (self.destination_ip, self.heartbeat_port)
        else:
            self.heartbeat_destination = None

    def get_packet_size(self, packet: type) -> int:
        """Helper function to get the size of a packet using ctypes.sizeof, which is needed for shared memory reading and UDP packet construction."""
        size = ctypes.sizeof(packet)
        return size

    def get_max_packet_size(self) -> int:
        """Helper function to get the maximum packet size from the packet info in the metadata, which is needed for setting the full buffer size if not provided in the metadata."""
        if not self.packet_info:
            LOGGER.error("Packet Info is empty.")
            raise ValueError("Packet Info is empty.")

        allSizes = []
        for packetID, packetInfo in self.packet_info.items():
            for packetStruct in packetInfo:
                packetSize = self.get_packet_size(packetStruct)
                allSizes.append(packetSize)

        LOGGER.debug("Maximum packet size calculated: %r", max(allSizes) if allSizes else 0)
        return max(allSizes) if allSizes else 0
