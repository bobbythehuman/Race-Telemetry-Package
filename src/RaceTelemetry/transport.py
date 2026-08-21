from __future__ import annotations
import logging
import mmap
import socket

from types import SimpleNamespace
from typing import Generator, TYPE_CHECKING

from .router import PacketRouter

if TYPE_CHECKING:
    from RaceTelemetry.main import TelemetryConfig, ThreadSupervisor

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# UDP transport — socket lifecycle only.
# ---------------------------------------------------------------------------


class UDPTransport:
    """
    Class to handle UDP transport for telemetry data.
    This class manages the lifecycle of a UDP socket and provides a generator to yield packets.
    """

    HEARTBEAT_INTERVAL: int = 5

    # def __init__(self, config: TelemetryConfig, router: PacketRouter, stop_event: threading.Event) -> None:
    def __init__(self, config: TelemetryConfig, router: PacketRouter, supervisor: ThreadSupervisor) -> None:
        self.config = config
        self.router = router

        # can work, but skips the _trigger_stop and _is_still_active functions, which may be important for some use cases
        # self.stop_event = stop_event
        self.supervisor = supervisor

        self.heartBeatDestination = None

        self._packet_counter: int = 0
        self._full_buffer_size: int = 0
        LOGGER.debug("UDPTransport initialized with config: %r", config.__class__.__name__)

    def call_handshake(self, sock: socket.socket, mode: str) -> None:
        """
        Call the handshake function if it is defined in the configuration.
        mode should be either "start" or "stop" to indicate the handshake phase.
        """

        handShakeDestination = (self.config.destination_ip, self.config.handshake_port)
        if not self.config.handshake_func:
            return

        if mode == "start":
            LOGGER.info("Calling handshake function for start.")
            self.config.handshake_func[0](sock, handShakeDestination)
        elif mode == "stop":
            LOGGER.info("Calling handshake function for stop.")
            self.config.handshake_func[1](sock, handShakeDestination)

    def get_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        """

        UDP_IP = self.config.local_ip
        UDP_PORT = self.config.main_port

        self.FULLBUFFERSIZE = self.router.get_max_packet_size()

        if (self.config.handshake_func or self.config.heartbeat_func) and not self.config.destination_ip:
            LOGGER.error("Destination IP must be set for handshakes or heartbeats.")
            raise ValueError("Destination IP must be set for handshakes or heartbeats.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # listen to occupied ports
        sock.settimeout(1.0)  # allows checking stop_event periodically

        try:
            sock.bind((UDP_IP, UDP_PORT))
        except OSError as e:
            LOGGER.error("Only one usage of each socket address, %s", e)
            self.supervisor._trigger_stop()
        else:
            LOGGER.info("Server started on %r:%r", UDP_IP, UDP_PORT)

            self.heartBeatDestination = self.config.heartbeat_destination
            self.call_handshake(sock, "start")

            LOGGER.info("Stop event provided, running until stop_event is set.")
            while self.supervisor._is_still_active():
                yield self._process_loop(sock)

            self.call_handshake(sock, "stop")

        finally:
            sock.close()
            LOGGER.info("Socket closed.")

    def _process_loop(self, sock: socket.socket) -> tuple[SimpleNamespace | None, int, SimpleNamespace | None]:
        """
        Helper function to process the main loop of receiving data, handling heartbeats, and retrieving packets.
        Returns a tuple of (packet, packetID, headerPacket) for the received data.
        """
        if self.config.heartbeat_func and not callable(self.config.heartbeat_func):
            LOGGER.error("Heart Beat Function is not a function.")
            raise ValueError("Heart Beat Function is not a function.")

        if self.config.decryption_func and not callable(self.config.decryption_func):
            LOGGER.error("Decryption Function is not a function.")
            raise ValueError("Decryption Function is not a function.")

        packet = None
        packetID = 0
        headerPacket = None

        if self.config.heartbeat_func:
            self._packet_counter += 1
            if self._packet_counter % self.HEARTBEAT_INTERVAL == 0:
                self.config.heartbeat_func(sock, self.heartBeatDestination)
                self._packet_counter = 0

        try:
            data, _ = sock.recvfrom(self.FULLBUFFERSIZE)  # TODO could verify ip matches destination IP
        except TimeoutError:
            if self.config.heartbeat_func:
                self.config.heartbeat_func(sock, self.heartBeatDestination)
                self._packet_counter = 0

        except KeyboardInterrupt:
            LOGGER.debug("Keyboard Interrupt from process_loop")
            LOGGER.info("Keyboard Interrupt received, shutting down server.")
            self.supervisor._trigger_stop()

        except OSError as exc:
            LOGGER.error("Socket error: %r", exc)
            self.supervisor._trigger_stop()

        else:
            if self.config.decryption_func:
                data = self.config.decryption_func(data)

            packet, packetID, headerPacket = self.router.retrieve_packet(data)
        return packet, packetID, headerPacket


# ---------------------------------------------------------------------------
# Shared-memory transport — mmap lifecycle only.
# ---------------------------------------------------------------------------


class SharedMemoryTransport:
    """
    Class to handle shared memory transport for telemetry data.
    This class manages the lifecycle of shared memory mappings and provides a generator to yield packets.
    """

    # def __init__(self, config: TelemetryConfig, router: PacketRouter, stop_event: threading.Event) -> None:
    def __init__(self, config: TelemetryConfig, router: PacketRouter, supervisor: ThreadSupervisor) -> None:
        self.config = config
        self.router = router

        # can work, but skips the _trigger_stop and _is_still_active functions, which may be important for some use cases
        # self.stop_event = stop_event
        self.supervisor = supervisor

        LOGGER.debug("SharedMemoryTransport initialized with config: %r", config.__class__.__name__)

    def connect_map(self, name: str, struct: type | None = None) -> dict[mmap.mmap, int]:
        if struct:
            SMSize = self.router.get_packet_size(struct)
        else:
            SMSize = self.router.get_max_packet_size()
        SMMap = mmap.mmap(-1, SMSize, tagname=name, access=mmap.ACCESS_READ)
        return {SMMap: SMSize}

    def setup_maps(self, allSharedMemoryNames: str | dict[str, str]) -> dict[mmap.mmap, int]:
        """
        Set up shared memory mappings based on the provided names and return a dictionary of mmap objects and their sizes.
        """

        if not self.config.packet_info:
            LOGGER.error("Packet Info is empty.")
            raise ValueError("Packet Info is empty.")

        sharedMemoryInfo = {}

        if isinstance(allSharedMemoryNames, str):
            SMInfo = self.connect_map(allSharedMemoryNames)
            sharedMemoryInfo.update(SMInfo)

            LOGGER.info("Server started on %r with size %r bytes" % (allSharedMemoryNames, SMInfo.values()))

        elif isinstance(allSharedMemoryNames, dict):
            SMNames = []
            for packetID, packetInfo in self.config.packet_info.items():
                for packetStruct in packetInfo:
                    SMName = allSharedMemoryNames.get(packetStruct.__name__)
                    if SMName:
                        SMNames.append(SMName)
                        SMInfo = self.connect_map(SMName, packetStruct)
                        sharedMemoryInfo.update(SMInfo)

            LOGGER.info("Server started for %r with sizes %r bytes", SMNames, [size for size in sharedMemoryInfo.values()])
        else:
            LOGGER.error("Shared memory name must be a string or a dict mapping packet names to shared memory names. Currently it is %r", allSharedMemoryNames.__class__.__name__)
            raise ValueError("Shared memory name must be a string or a dict mapping packet names to shared memory names.")

        return sharedMemoryInfo

    def get_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet from shared memory.
        """

        allSharedMemoryNames = self.config.all_shared_memory_names

        if not allSharedMemoryNames:
            LOGGER.critical("Shared memory name is not set.")
            raise ValueError("Shared memory name is not set.")

        sharedMemoryInfo = self.setup_maps(allSharedMemoryNames)

        while self.supervisor._is_still_active():
            try:
                SMRawData = []
                for SMMap, SMSize in sharedMemoryInfo.items():
                    SMMap.seek(0)
                    raw = SMMap.read(SMSize)
                    SMRawData.append(raw)

            except KeyboardInterrupt:
                LOGGER.debug("Keyboard Interrupt from get_shared_packets")
                LOGGER.info("KeyboardInterrupt received, shutting down server.")
                self.supervisor._trigger_stop()

            except OSError as exc:
                LOGGER.error("Shared memory error: %r", exc)
                self.supervisor._trigger_stop()

            else:
                for SMData in SMRawData:
                    if not any(SMData):
                        continue
                    packet, packetID, headerPacket = self.router.retrieve_packet(SMData)

                    yield packet, packetID, headerPacket

        for SMMap in sharedMemoryInfo.keys():
            SMMap.close()
        LOGGER.info("Server shutting down.")
