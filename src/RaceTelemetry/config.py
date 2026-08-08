import re
import logging

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

        self.enum_mode: int = 0

        LOGGER.debug("[MAIN] [Info]\tTelemetryConfig initialized.")

    def update_meta(self, metadata_cls: type) -> bool:
        if self.active_metadata == metadata_cls:
            return True

        self.active_metadata = metadata_cls
        self._unpack_meta_data()
        LOGGER.debug("[MAIN] [Info]\tMetadata updated to %r.", metadata_cls.__name__ if metadata_cls else None)
        return True

    def update_local_ip(self, ip: str) -> bool:
        if not self._is_valid_ip(ip):
            return False

        self.local_ip = ip
        return True

    def update_send_ip(self, ip: str) -> bool:
        if not self._is_valid_ip(ip):
            return False

        self.destination_ip = ip
        return True

    def set_enum_mode(self, target: int = 0) -> bool:
        if not self._valid_type(target, int, "Enum Mode"):
            return False
        if target not in [0, 1, 2]:
            LOGGER.warning("[MAIN] [Warning]\tEnum mode must be 0, 1, or 2.")
            return False

        self.enum_mode = target
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

        self.handshake_port = self._meta_data_check("handShakePort")
        self.handshake_func = self._meta_data_check("handShakeFunc")

        self.decryption_func = self._meta_data_check("decryptionFunc")

        self.header_packet = self._meta_data_check("headerInfo")
        self.packet_id_attr = self._meta_data_check("packetIDAttribute")

        self.all_shared_memory_names = self._meta_data_check("allSharedMemoryNames")

        self.packet_info = self._meta_data_check("packetInfo", {})

        LOGGER.debug("[MAIN] [Info]\tMetadata unpacked: %r", self.active_metadata.__name__ if self.active_metadata else None)

    def _is_valid_ip(self, ip: str) -> bool:
        if not self._valid_type(ip, str, "IP"):
            return False

        if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", ip):
            return True

        LOGGER.warning("[NTWK] [Warning]\tInvalid IP address: %r", ip)
        return False

    def _valid_type(self, value: object, expected_type: type, name: str) -> bool:
        if isinstance(value, expected_type):
            return True
        else:
            LOGGER.warning("[MAIN] [Warning]\t%r must be a %r.", name, expected_type)
            return False
