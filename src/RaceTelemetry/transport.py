import logging
import mmap
import socket

from types import SimpleNamespace
from typing import Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from RaceTelemetry.main import PacketRouter, TelemetryConfig, ThreadSupervisor

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

        self._packet_counter: int = 0
        self._full_buffer_size: int = 0

    def get_udp_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        """

        UDP_IP = self.config.local_ip
        UDP_PORT = self.config.main_port

        self.FULLBUFFERSIZE = self.router.get_max_packet_size()

        handShakeDestination = (self.config.destination_ip, self.config.handshake_port)

        if (self.config.handshake_func or self.config.heartbeat_func) and not self.config.destination_ip:
            LOGGER.error("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")
            raise ValueError("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")

        # if self.config.handshake_func and len(self.config.handshake_func) != 2:
        #     LOGGER.error("[NTWK] [Error]\tHand Shake function needs 2 function.")
        #     raise ValueError("[NTWK] [Error]\tHand Shake function needs 2 function.")

        # if not callable(self.config.handshake_func[0]) or not callable(self.config.handshake_func[1]):
        #     LOGGER.error("[NTWK] [Error]\tHand Shake function must be a function.")
        #     raise ValueError("[NTWK] [Error]\tHand Shake function must be a function.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # listen to occupied ports
        sock.settimeout(1.0)  # allows checking stop_event periodically

        try:
            sock.bind((UDP_IP, UDP_PORT))
        except OSError:
            LOGGER.error("[NTWK] [ERROR]\tOnly one usage of each socket address")
            self.supervisor._trigger_stop()
        else:
            LOGGER.info("[NTWK] [Info]\tServer started on %r:%r", UDP_IP, UDP_PORT)

            if self.config.handshake_func:
                self.config.handshake_func[0](sock, handShakeDestination)  # TODO fix this function not callable

            LOGGER.info("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
            while self.supervisor._is_still_active():
                yield self._process_loop(sock)

            if self.config.handshake_func:
                self.config.handshake_func[1](sock, handShakeDestination)
        finally:
            sock.close()
            LOGGER.info("[NTWK] [Info]\tServer shutting down.")

    def _process_loop(self, sock: socket.socket) -> tuple[SimpleNamespace | None, int, SimpleNamespace | None]:
        """
        Helper function to process the main loop of receiving data, handling heartbeats, and retrieving packets.
        Returns a tuple of (packet, packetID, headerPacket) for the received data.
        """
        if self.config.heartbeat_func and not callable(self.config.heartbeat_func):
            LOGGER.error("[NTWK] [Error]\tHeart Beat Function is not a function.")
            raise ValueError("[NTWK] [Error]\tHeart Beat Function is not a function.")

        if self.config.decryption_func and not callable(self.config.decryption_func):
            LOGGER.error("[NTWK] [Error]\tDecryption Function is not a function.")
            raise ValueError("[NTWK] [Error]\tDecryption Function is not a function.")

        packet = None
        packetID = 0
        headerPacket = None
        heartBeatDestination = (self.config.destination_ip, self.config.heartbeat_port)

        if self.config.heartbeat_func:
            self.PACKET_COUNTER += 1
            if self.PACKET_COUNTER % self.HEARTBEAT_INTERVAL == 0:
                self.config.heartbeat_func(sock, heartBeatDestination)
                self.PACKET_COUNTER = 0

        try:
            data, _ = sock.recvfrom(self.FULLBUFFERSIZE)  # TODO could verify ip matches destination IP
        except TimeoutError:
            if self.config.heartbeat_func:
                self.config.heartbeat_func(sock, heartBeatDestination)
                self.PACKET_COUNTER = 0

        except KeyboardInterrupt:
            LOGGER.debug("Keyboard Interrupt from process_loop")
            LOGGER.info("[NTWK] [Info]\tKeyboard Interrupt received, shutting down server.")
            self.supervisor._trigger_stop()

        except OSError as exc:
            LOGGER.error("[NTWK] [Error]\tSocket error: %r", exc)
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

    def get_shared_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        allSharedMemoryNames = self.config.all_shared_memory_names

        if not allSharedMemoryNames:
            LOGGER.critical("[NTWK] [Error]\tShared memory name is not set.")
            raise ValueError("[NTWK] [Error]\tShared memory name is not set.")

        if not self.config.packet_info:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        sharedMemoryInfo = {}

        if isinstance(allSharedMemoryNames, str):
            SMSize = self.router.get_max_packet_size()
            SMMap = mmap.mmap(-1, SMSize, tagname=allSharedMemoryNames, access=mmap.ACCESS_READ)

            sharedMemoryInfo.update({SMMap: SMSize})
            LOGGER.info("[NTWK] [Info]\tServer started on %r with size %r bytes" % (allSharedMemoryNames, SMSize))

        elif isinstance(allSharedMemoryNames, dict):
            SMNames = []
            for packetID, packetInfo in self.config.packet_info.items():
                for packetStruct in packetInfo:
                    SMName = allSharedMemoryNames.get(packetStruct.__name__)
                    SMSize = self.router.get_packet_size(packetStruct)
                    if SMName:
                        SMNames.append(SMName)
                        SMMap = mmap.mmap(-1, SMSize, tagname=SMName, access=mmap.ACCESS_READ)
                        sharedMemoryInfo.update({SMMap: SMSize})

            LOGGER.info("[NTWK] [Info]\tServer started for %r with sizes %r bytes", SMNames, [size for size in sharedMemoryInfo.values()])
        else:
            raise ValueError("[NTWK] [Error]\tShared memory name must be a string or a dict mapping packet names to shared memory names.")

        while self.supervisor._is_still_active():
            try:
                SMRawData = []
                for SMMap, SMSize in sharedMemoryInfo.items():
                    SMMap.seek(0)
                    raw = SMMap.read(SMSize)
                    SMRawData.append(raw)

            # except TimeoutError:
            #     pass
            except KeyboardInterrupt:
                LOGGER.debug("Keyboard Interrupt from get_shared_packets")
                LOGGER.info("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                self.supervisor._trigger_stop()
                # continue
            except OSError as exc:
                LOGGER.error("[NTWK] [Error]\tShared memory error: %r", exc)
                self.supervisor._trigger_stop()
                # continue
            else:
                for SMData in SMRawData:
                    if not any(SMData):
                        continue
                    packet, packetID, headerPacket = self.router.retrieve_packet(SMData)

                    yield packet, packetID, headerPacket

        for SMMap in sharedMemoryInfo.keys():
            SMMap.close()
        LOGGER.info("[NTWK] [Info]\tServer shutting down.")
