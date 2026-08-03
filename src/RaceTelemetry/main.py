"""
Telemetry manager: receives packets over UDP or shared memory, decodes them
using ctypes packet definitions, and hands them off to worker threads via a
read-only snapshot of the latest data.

Public method names use snake_case. The original camelCase/PascalCase method
names (updateMeta, addWorkerThread, StartTelemetry, ...) are kept as
deprecated aliases at the bottom of TelemetryManager so existing callers are
not broken by this refactor.

Note: ReadOnlyStorage.snapshot() intentionally still returns a dict with the
string keys "allData" / "latestData" — worker functions written against the
original API read these keys directly, so they are NOT renamed here even
though the internal CentralStorage attributes have been cleaned up.
"""

import ctypes
import logging
import re

from datetime import datetime
from types import SimpleNamespace
from typing import Generator, Any, Callable

from .digestion import dynamic_ingest
from .threads import ThreadSupervisor
from .transport import UDPTransport, SharedMemoryTransport
from .storage import CentralStorage, ReadOnlyStorage

# ---------------------------------------------------------------------------
# Other Setups
# ---------------------------------------------------------------------------

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

    def update_meta(self, metadata_cls: type) -> bool:
        if self.active_metadata == metadata_cls:
            return True

        self.active_metadata = metadata_cls
        self._unpack_meta_data()
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


# ---------------------------------------------------------------------------
# Packet decoding — function of config + bytes
# ---------------------------------------------------------------------------


class PacketRouter:
    """
    Takes raw bytes and decodes them into packets using the metadata.
    """

    def __init__(self, config: TelemetryConfig):
        self.config = config

    def get_packet_size(self, packet: type) -> int:
        """Helper function to get the size of a packet using ctypes.sizeof, which is needed for shared memory reading and UDP packet construction."""
        size = ctypes.sizeof(packet)
        return size

    def get_max_packet_size(self) -> int:
        """Helper function to get the maximum packet size from the packet info in the metadata, which is needed for setting the full buffer size if not provided in the metadata."""
        if not self.config.packet_info:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        allSizes = []
        for packetID, packetInfo in self.config.packet_info.items():
            for packetStruct in packetInfo:
                packetSize = self.get_packet_size(packetStruct)
                allSizes.append(packetSize)

        return max(allSizes) if allSizes else 0

    def construct_packet(self, data: bytes, possiblePacketStruct: tuple) -> SimpleNamespace | None:
        """
        Helper function to construct a packet from the data using the possible packet structures provided in the metadata.
        Returns the constructed packet, or None if no matching packet structure is found.
        """
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetStruct in possiblePacketStruct:
            packetBufferSize = self.get_packet_size(packetStruct)
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    LOGGER.debug("Packet failed to unpack with %r", packetStruct.__name__)
                    continue
                else:
                    packet = dynamic_ingest(rawPacket, self.config.enum_mode)
                    break
        if len(possiblePacketStruct) == len(packetSizes):
            LOGGER.warning("[Warning]\tNo matching packet size [%r] for received data length %r", packetSizes, dataLength)
            packet = None
        return packet

    def retrieve_packet(self, data: bytes) -> tuple[SimpleNamespace | None, int, Any]:
        """
        Helper function to retrieve the packet, packet ID, and header packet (if applicable) from the raw data.
        Returns a tuple of (packet, packetID, headerPacket).
        packet and headerPacket may be None if no matching packet structure is found or if no header is defined in the metadata.
        """

        if not self.config.packet_info:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        if self.config.header_packet:
            if not self.config.packet_id_attr:
                LOGGER.error("[NTWK] [Error]\tPacket ID Attribute is empty.")
                raise ValueError("[NTWK] [Error]\tPacket ID Attribute is empty.")

            headerBufferSize = self.get_packet_size(self.config.header_packet)
            rawHeaderPacket = self.config.header_packet.from_buffer_copy(data[0:headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            if hasattr(headerPacket, self.config.packet_id_attr):
                packetID = int(getattr(headerPacket, self.config.packet_id_attr))
            else:
                LOGGER.warning("[NTWK] [Warning]\tHeader packet %r doesnt contain the ID attribute %r", headerPacket, self.config.packet_id_attr)
                packetID = 0
        else:
            headerPacket = None
            packetID = 0

        possiblePacketStruct = self.config.packet_info.get(packetID)
        if possiblePacketStruct:
            packet = self.construct_packet(data, possiblePacketStruct)
        else:
            LOGGER.warning("ID not found")
            packet = None

        return packet, packetID, headerPacket


# ---------------------------------------------------------------------------
# telemetry manager — orchestrates config, storage, router, transport, and threads.
# ---------------------------------------------------------------------------


class TelemetryManager:
    """
    Main class to manage telemetry data reception, decoding, and worker thread management.
    """

    def __init__(self):
        self.config = TelemetryConfig()
        self.supervisor = ThreadSupervisor()

        self.activeStorage: CentralStorage | None = None
        self.readOnlyStorage: ReadOnlyStorage | None = None

        self.router: PacketRouter | None = None
        self.udp_transport: UDPTransport | None = None
        self.shared_memory_transport: SharedMemoryTransport | None = None

        self.shared_memory: bool = False

    # -- configuration passthroughs -------------------------------------

    def updateMeta(self, MetaData: type) -> None:
        """
        Call this to update the metadata and reset storage.
        Must be called at least once before starting threads.
        """

        if self.supervisor.workers_are_working:
            LOGGER.warning("[MAIN] [Warning]\tTried to update meta after telemetry has started.")
            return

        metadata_changed = self.config.active_metadata != MetaData
        self.config.update_meta(MetaData)

        if not self.config.active_metadata:
            LOGGER.warning("[MAIN] [Warning]\tMetadata update failed or none provided. No active metadata set.")
            return

        if metadata_changed:
            self.activeStorage = CentralStorage(self.config.active_metadata)
            self.readOnlyStorage = ReadOnlyStorage(self.activeStorage)
            self.router = PacketRouter(self.config)
            self.udp_transport = UDPTransport(self.config, self.router, self.supervisor)
            self.shared_memory_transport = SharedMemoryTransport(self.config, self.router, self.supervisor)

    def updateLocalIP(self, ip: str) -> bool:
        """
        Call this to update the local IP address the server listens on.
        Default is"""
        return self.config.update_local_ip(ip)

    def updateSendIP(self, ip: str) -> bool:
        """
        Call this to update the destination IP address for handshakes and heartbeats.
        Default is None, which will cause an error if handshakes or heartbeats are enabled.
        """
        return self.config.update_send_ip(ip)

    def setEnumMode(self, target: int = 0) -> bool:
        """
        Call this to set the enum mode for handling enum values.
        Default is 0 (no special handling).
        Modes:
        0: No special handling (default)
        1: Convert fields with to the raw value
        2: Convert fields to their enum name
        """
        return self.config.set_enum_mode(target)

    def isSharedMemory(self, target: bool = False) -> bool:
        """
        Call this to set whether to use shared memory or UDP for telemetry.
        Default is False (UDP).
        """
        if not isinstance(target, bool):
            LOGGER.error("[MAIN] [Error]\tInvalid type for shared memory setting. Expected bool.")
            return False

        self.shared_memory = target
        return True

    # -- thread supervision passthroughs ---------------------------------

    def addWorkerThread(self, mainFunc: Callable[..., Any]) -> bool:
        """
        Call this to add a worker thread to access the data.
        The function must accept three keyword arguments:
        worker_id (int), ro_storage (ReadOnlyStorage), and stop_event (threading.Event).
        """
        return self.supervisor.add_worker_thread(mainFunc, self.readOnlyStorage)

    def manualStop(self, target: bool) -> bool:
        """Manually stop the program, via the terminal"""
        return self.supervisor.manual_stop(target)

    def isMultiThreaded(self, target: bool = True) -> bool:
        """Currently does nothing"""
        return self.supervisor.is_multi_threaded(target)

    # -- telemetry -------------------------------------------------------

    def GetTelemetry(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        """
        if not self.shared_memory_transport or not self.udp_transport:
            LOGGER.error("[NTWK] [Error]\tTelemetry transports are not initialized. Call updateMeta() before GetTelemetry().")
            return

        if self.shared_memory:
            LOGGER.info("[NTWK] [Info]\tUsing shared memory telemetry.")
            yield from self.shared_memory_transport.get_shared_packets()
        else:
            LOGGER.info("[NTWK] [Info]\tUsing UDP telemetry.")
            yield from self.udp_transport.get_udp_packets()

    def StartTelemetry(self) -> None:
        """
        Call this to start the network and worker threads.
        Will run until a stop signal is received (either Ctrl+C or manual stop).
        """
        if self.readOnlyStorage is None:
            LOGGER.error("[MAIN] [Error]\tRead-only storage is not initialized. Call updateMeta() before StartTelemetry().")
            raise RuntimeError("[MAIN] [Error]\tRead-only storage is not initialized. Call updateMeta() before StartTelemetry().")

        LOGGER.info("[MAIN] [INFO]\tStart at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

        self.supervisor._start_threads(network_target=self._network_listener)
        LOGGER.info("[MAIN] [INFO]\tRunning — press Ctrl+C to stop.")

        self.supervisor._wait_for_stop_signal()
        LOGGER.info("[MAIN] [INFO]\tEnd at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    def _network_listener(self) -> None:
        """
        Listens for incoming network packets and writes them to the active storage.
        This function runs in a separate thread and should not be called directly.
        """
        if self.activeStorage is None:
            raise ValueError("[NTWK] [Error]\tStorage instance is not initialized.")

        for packet, packetID, headerPacket in self.GetTelemetry():
            # LOGGER.debug("[NTWK] [Info]\tReceived packet ID %r", packetID)
            self.activeStorage._write(packet)

    # ------------------------------------------------------------------
    # Deprecated or changed aliases — kept so existing callers
    # using the original camelCase/PascalCase API keep working unchanged.
    # ------------------------------------------------------------------

    # updateMeta = update_meta
    # updateLocalIP = update_local_ip
    # updateSendIP = update_send_ip
    # addWorkerThread = add_worker_thread
    # manualStop = manual_stop
    # isMultiThreaded = is_multi_threaded
    # isSharedMemory = is_shared_memory
    # setEnumMode = set_enum_mode
    # StartTelemetry = start_telemetry
    # GetTelemetry = get_telemetry
