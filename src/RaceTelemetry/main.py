import ctypes
import socket
import mmap
import threading
import re
import logging

from types import SimpleNamespace
from typing import Generator, Any, Callable
from datetime import datetime
from copy import deepcopy

from .digestion import dynamic_ingest

# ---------------------------------------------------------------------------
# Other Setups
# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Central Storage
# ---------------------------------------------------------------------------


class CentralStorage:
    """
    Holds the latest network data.  Worker threads receive a read-only view
    via ReadOnlyStorage so they cannot accidentally edit the contents.
    """

    def __init__(self, MetaData: type) -> None:
        self._lock = threading.RLock()

        self.allData = {}
        self.latestData = {}

        packetNames = MetaData.packetInfo.items()
        for packetID, packetInfo in packetNames:
            for packetStruct in packetInfo:
                packetName = packetStruct.__name__
                if packetName not in self.allData:
                    self.allData[packetName] = []
                    self.latestData[packetName] = None

    def _write(self, data: SimpleNamespace | None) -> None:
        """Called only by the network thread."""
        with self._lock:
            if data:
                packetName = data.__name__

                self.allData[packetName].append(data)
                self.latestData[packetName] = data

    def snapshot(self) -> dict[str, Any]:
        """Return a consistent, snapshot for worker threads."""
        with self._lock:
            return {
                "allData": self.allData.copy(),
                # "allData": deepcopy(self.allData),
                "latestData": self.latestData.copy(),
                # "latestData": deepcopy(self.latestData),
            }


class ReadOnlyStorage:
    """
    Thin wrapper passed to worker threads.
    Exposes only .snapshot() — no write methods visible.
    """

    def __init__(self, storage: CentralStorage) -> None:
        self._storage = storage

    def snapshot(self) -> dict[str, Any]:
        return self._storage.snapshot()


# ---------------------------------------------------------------------------
# Manages Threads
# ---------------------------------------------------------------------------


class TelemetryManager:
    def __init__(self):
        self.ACTIVE_METADATA: type | None = None
        self.IP: str = "0.0.0.0"
        self.destinationIP: str | None = None

        # from meta data
        self.mainPort: int | None = None
        self.heartBeatPort: int | None = None
        self.heartBeatFunc: Callable[..., Any] | None = None
        self.handShakePort: int | None = None
        self.handShakeFunc: tuple[Callable[..., Any], Callable[..., Any]] | None = None
        self.decryptionFunc: Callable[..., Any] | None = None
        self.headerPacket: type | None = None
        self.packetIDAttr: str | None = None
        self.allSharedMemoryNames: str | None | dict[str, str] = None
        self.packetInfo: dict[int, tuple[type, ...]] | None = None

        self.activeStorage = None
        self.readOnlyStorage = None
        self.stop_event = threading.Event()
        self.manuallyStopped: bool = False

        self.networkThread = None
        self.workerThreads: dict[int, threading.Thread] = {}

        self.workersAreWorking: bool = False
        self.threadCount: int = 0
        self.multiThreaded: bool = True

        self.sharedMemory: bool = False
        self.sharedMemoryName = None
        self.sharedMemorySize = None

        # extra constants and single purpose
        self.HEARTBEAT_INTERVAL: int = 5
        self.PACKET_COUNTER: int = 0
        self.FULLBUFFERSIZE: int = 0

        self.enumMode: int = 0

    # User controlled functions

    def updateMeta(self, MetaData: type) -> None:
        """
        Call this to update the metadata and reset storage.
        Must be called at least once before starting threads.
        """
        if self.workersAreWorking:
            LOGGER.warning("[MAIN] Tried to update meta after telemetry has started.")
            return

        if self.ACTIVE_METADATA != MetaData:
            self.ACTIVE_METADATA = MetaData
            self.activeStorage = CentralStorage(self.ACTIVE_METADATA)
            self.readOnlyStorage = ReadOnlyStorage(self.activeStorage)
        self.__unpack_meta_data()

    def updateLocalIP(self, ip: str) -> bool:
        """
        Call this to update the local IP address the server listens on.
        Default is "0.0.0.0"
        """

        if not self.__is_valid_ip(ip):
            return False

        self.IP = ip
        return True

    def updateSendIP(self, ip: str) -> bool:
        """
        Call this to update the destination IP address for handshakes and heartbeats.
        Default is None, which will cause an error if handshakes or heartbeats are enabled.
        """

        if not self.__is_valid_ip(ip):
            return False

        self.destinationIP = ip
        return True

    def addWorkerThread(self, mainFunc: Callable[..., Any]) -> bool:
        """
        Call this to add a worker thread to access the data.
        The function must accept three keyword arguments: worker_id (int), ro_storage (ReadOnlyStorage), and stop_event (threading.Event).
        """
        if not callable(mainFunc):
            LOGGER.warning("[MAIN] [Warning]\tWorker function must be callable.")
            return False

        if isinstance(mainFunc, type):
            LOGGER.warning("[MAIN] [Warning]\tWorker Function must not be a class.")
            return False

        self.threadCount += 1
        workerThread = threading.Thread(
            target=mainFunc,
            kwargs={"worker_id": self.threadCount, "ro_storage": self.readOnlyStorage, "stop_event": self.stop_event},
            daemon=True,
        )
        self.workerThreads.update({self.threadCount: workerThread})
        return True

    def manualStop(self, target: bool) -> bool:
        """Manually stop the program"""
        if not self.__valid_type(target, bool, "Manual Stop"):
            return False

        self.manuallyStopped = target
        return True

    def isMultiThreaded(self, target: bool = True) -> bool:
        """Currently does nothing"""
        if not self.__valid_type(target, bool, "Multi Thread"):
            return False

        self.multiThreaded = target
        return True

    def isSharedMemory(self, target: bool = False) -> bool:
        """
        Call this to set whether to use shared memory or UDP for telemetry.
        Default is False (UDP).
        """
        if not self.__valid_type(target, bool, "Shared Memory"):
            return False

        self.sharedMemory = target
        return True

    def setEnumMode(self, target: int = 0) -> bool:
        """
        Call this to set the enum mode for handling enum values.
        Default is 0 (no special handling).
        Modes:
        0: No special handling (default)
        1: Convert fields with to the raw value
        2: Convert fields to their enum type
        """
        if not self.__valid_type(target, int, "Enum Mode"):
            return False
        if target not in [0, 1, 2]:
            LOGGER.warning(f"[MAIN] [Warning]\tEnum mode must be 0, 1, or 2.")
            return False

        self.enumMode = target
        return True

    # Misc innit functions

    def __meta_data_check(self, name: str, value: Any = None) -> Any:
        """
        Helper function to check if metadata has the attribute, and return it if it does.
        Otherwise return the provided default value.
        """

        if hasattr(self.ACTIVE_METADATA, name):
            return getattr(self.ACTIVE_METADATA, name)
            # _heartBeatPort = self.ACTIVE_METADATA.value
        else:
            return value
            # _heartBeatPort = None

    def __unpack_meta_data(self) -> None:
        """
        Helper function to unpack metadata attributes into class attributes for easy access
        """
        self.mainPort = self.__meta_data_check("port")

        self.heartBeatPort = self.__meta_data_check("heartBeatPort")
        self.heartBeatFunc = self.__meta_data_check("heartBeatFunc")

        self.handShakePort = self.__meta_data_check("handShakePort")
        self.handShakeFunc = self.__meta_data_check("handShakeFunc")

        self.decryptionFunc = self.__meta_data_check("decryptionFunc")

        self.headerPacket = self.__meta_data_check("headerInfo")
        self.packetIDAttr = self.__meta_data_check("packetIDAttribute")

        self.allSharedMemoryNames = self.__meta_data_check("allSharedMemoryNames")

        self.packetInfo = self.__meta_data_check("packetInfo", {})

    def __get_packet_size(self, packet: type) -> int:
        """Helper function to get the size of a packet using ctypes.sizeof, which is needed for shared memory reading and UDP packet construction."""
        size = ctypes.sizeof(packet)
        return size

    def __get_max_packet_size(self) -> int:
        """Helper function to get the maximum packet size from the packet info in the metadata, which is needed for setting the full buffer size if not provided in the metadata."""
        if not self.packetInfo:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        allSizes = []
        for packetID, packetInfo in self.packetInfo.items():
            for packetStruct in packetInfo:
                packetSize = self.__get_packet_size(packetStruct)
                allSizes.append(packetSize)
        return max(allSizes) if allSizes else 0

    def __is_valid_ip(self, ip: str) -> bool:
        if not self.__valid_type(ip, str, "IP"):
            return False

        if re.match(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", ip):
            return True

        LOGGER.warning("[NTWK] [Warning]\tInvalid IP address: %r", ip)
        return False

    def __valid_type(self, object_: object, type_, name: str) -> bool:
        if isinstance(object_, type_):
            return True
        else:
            LOGGER.warning("[MAIN] [Warning]\t%r must be a %r.", name, type_)
            return False

    # Misc thread function

    def __wait(self, time: float) -> None:
        """
        Helper function to wait while still checking for stop_event
        """
        self.stop_event.wait(time)

    def __trigger_stop(self, mode: bool = True) -> None:
        """
        Helper function to toggle the stop event
        """
        if self.stop_event and mode:
            self.stop_event.set()
        else:
            self.stop_event.clear()

    def __is_still_active(self) -> bool:
        """
        Helper function to check if the program should still be running
        """
        return not self.stop_event.is_set() and not self.manuallyStopped

    # Start and Stop functions

    def __start_threads(self) -> None:
        """
        Helper function to start the network thread and worker threads
        Does not start if metadata is not set or if IP is not set (for network thread)
        """
        if not self.ACTIVE_METADATA:
            return
        if not self.IP:
            return

        self.networkThread = threading.Thread(
            target=self.__network_listener,
            kwargs={},
            daemon=True,
        )

        self.networkThread.start()

        for workerName, workerThread in self.workerThreads.items():
            workerThread.start()

        self.workersAreWorking = True

    def __wait_for_stop_signal(self) -> None:
        """
        Helper function to wait for a stop signal (either Ctrl+C or manual stop) while keeping the main thread alive
        """
        endProgram = ""
        try:
            while self.__is_still_active():
                self.__wait(0.5)

                if self.manuallyStopped:
                    # only stop threads here if they dont get stopped any where else
                    endProgram = input(f"[Q] to quit the program: ")
                    if endProgram.lower() == "q":
                        self.__trigger_stop()

        except KeyboardInterrupt:
            LOGGER.debug("Keyboard Interrupt from wait_for_stop_signal")
            LOGGER.info("[MAIN] [INFO]\tKeyboardInterrupt received.")
        finally:
            LOGGER.info("[MAIN] [INFO]\tStopping all threads")
            self.__stop_threads()

    def __stop_threads(self) -> None:
        """
        Helper function to stop all threads gracefully by triggering the stop event and joining threads with a timeout
        """
        if not self.workersAreWorking:
            return
        if not self.networkThread:
            return

        self.__trigger_stop()
        self.networkThread.join(timeout=0.5)

        for workerName, workerThread in self.workerThreads.items():
            workerThread.join(timeout=0.5)
            if workerThread.is_alive():
                LOGGER.warning("[MAIN] [WARNING]\tWarning: %r did not stop in time.", workerName)

        self.workersAreWorking = False
        LOGGER.info("[MAIN] [INFO]\tAll threads stopped. Exiting.")

    def StartTelemetry(self) -> None:
        """
        Call this to start the network and worker threads.
        Will run until a stop signal is received (either Ctrl+C or manual stop).
        """
        if self.readOnlyStorage is None:
            LOGGER.error("[MAIN] [Error]\tRead-only storage is not initialized. Call updateMeta() before StartTelemetry().")
            raise RuntimeError("[MAIN] [Error]\tRead-only storage is not initialized. Call updateMeta() before StartTelemetry().")

        LOGGER.info("[MAIN] [INFO]\tStart at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))
        self.__start_threads()
        LOGGER.info("[MAIN] [INFO]\tRunning — press Ctrl+C to stop.")
        # comment lines below to make a manual stop outside class
        self.__wait_for_stop_signal()
        LOGGER.info("[MAIN] [INFO]\tEnd at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # Misc packet function

    def __construct_packet(self, data: bytes, possiblePacketStruct: tuple) -> SimpleNamespace | None:
        """
        Helper function to construct a packet from the data using the possible packet structures provided in the metadata.
        Returns the constructed packet, or None if no matching packet structure is found.
        """
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetStruct in possiblePacketStruct:
            packetBufferSize = self.__get_packet_size(packetStruct)
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    LOGGER.debug("Packet failed to unpack with %r", packetStruct.__name__)
                    continue
                else:
                    packet = dynamic_ingest(rawPacket, self.enumMode)
                    break
        if len(possiblePacketStruct) == len(packetSizes):
            LOGGER.warning("[Warning]\tNo matching packet size [%r] for received data length %r", packetSizes, dataLength)
            packet = None

        # do enum check here
        # do enum convert

        return packet

    def __retrieve_packet(self, data: bytes) -> tuple[SimpleNamespace | None, int, Any]:
        """
        Helper function to retrieve the packet, packet ID, and header packet (if applicable) from the raw data.
        Returns a tuple of (packet, packetID, headerPacket).
        packet and headerPacket may be None if no matching packet structure is found or if no header is defined in the metadata.
        """

        if not self.packetInfo:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        if self.headerPacket:
            if not self.packetIDAttr:
                LOGGER.error("[NTWK] [Error]\tPacket ID Attribute is empty.")
                raise ValueError("[NTWK] [Error]\tPacket ID Attribute is empty.")

            headerBufferSize = self.__get_packet_size(self.headerPacket)
            rawHeaderPacket = self.headerPacket.from_buffer_copy(data[0:headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            if hasattr(headerPacket, self.packetIDAttr):
                packetID = int(getattr(headerPacket, self.packetIDAttr))
            else:
                LOGGER.warning("[NTWR] [Warning]\tHeader packet %r doesnt contain the ID attribute %r", headerPacket, self.packetIDAttr)
                packetID = 0
        else:
            headerPacket = None
            packetID = 0

        possiblePacketStruct = self.packetInfo.get(packetID)
        if possiblePacketStruct:
            packet = self.__construct_packet(data, possiblePacketStruct)
        else:
            LOGGER.warning("ID not found")
            packet = None

        return packet, packetID, headerPacket

    # Main UDP packet function

    def __process_loop(self, sock: socket.socket) -> tuple[SimpleNamespace | None, int, SimpleNamespace | None]:
        """
        Helper function to process the main loop of receiving data, handling heartbeats, and retrieving packets.
        Returns a tuple of (packet, packetID, headerPacket) for the received data.
        """
        if self.heartBeatFunc and not callable(self.heartBeatFunc):
            LOGGER.error("[NTWK] [Error]\tHeart Beat Function is not a function.")
            raise ValueError("[NTWK] [Error]\tHeart Beat Function is not a function.")

        if self.decryptionFunc and not callable(self.decryptionFunc):
            LOGGER.error("[NTWK] [Error]\tDecryption Function is not a function.")
            raise ValueError("[NTWK] [Error]\tDecryption Function is not a function.")

        packet = None
        packetID = 0
        headerPacket = None
        heartBeatDestination = (self.destinationIP, self.heartBeatPort)

        if self.heartBeatFunc:
            self.PACKET_COUNTER += 1
            if self.PACKET_COUNTER % self.HEARTBEAT_INTERVAL == 0:
                self.heartBeatFunc(sock, heartBeatDestination)
                self.PACKET_COUNTER = 0

        try:
            data, _ = sock.recvfrom(self.FULLBUFFERSIZE)  # TODO could verify ip matches destination IP
        except TimeoutError:
            if self.heartBeatFunc:
                self.heartBeatFunc(sock, heartBeatDestination)
                self.PACKET_COUNTER = 0

        except KeyboardInterrupt:
            LOGGER.debug("Keyboard Interrupt from process_loop")
            LOGGER.info("[NTWK] [Info]\tKeyboard Interrupt received, shutting down server.")
            self.__trigger_stop()

        except OSError as exc:
            LOGGER.error("[NTWK] [Error]\tSocket error: %r", exc)
            self.__trigger_stop()

        else:
            if self.decryptionFunc:
                data = self.decryptionFunc(data)

            packet, packetID, headerPacket = self.__retrieve_packet(data)
        return packet, packetID, headerPacket

    def get_udp_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        """

        UDP_IP = self.IP
        UDP_PORT = self.mainPort
        self.PACKET_COUNTER = 0
        self.FULLBUFFERSIZE = self.__get_max_packet_size()

        handShakeDestination = (self.destinationIP, self.handShakePort)

        if (self.handShakeFunc or self.heartBeatFunc) and not self.destinationIP:
            LOGGER.error("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")
            raise ValueError("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")

        # if self.handShakeFunc and len(self.handShakeFunc) != 2:
        #     LOGGER.error("[NTWK] [Error]\tHand Shake function needs 2 function.")
        #     raise ValueError("[NTWK] [Error]\tHand Shake function needs 2 function.")

        # if not callable(self.handShakeFunc[0]) or not callable(self.handShakeFunc[1]):
        #     LOGGER.error("[NTWK] [Error]\tHand Shake function must be a function.")
        #     raise ValueError("[NTWK] [Error]\tHand Shake function must be a function.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # listen to occupied ports
        sock.settimeout(1.0)  # allows checking stop_event periodically

        try:
            sock.bind((UDP_IP, UDP_PORT))
        except OSError:
            LOGGER.error("[NTWK] [ERROR]\tOnly one usage of each socket address")
            self.__trigger_stop()
        else:
            LOGGER.info("[NTWK] [Info]\tServer started on %r:%r", UDP_IP, UDP_PORT)

            if self.handShakeFunc:
                self.handShakeFunc[0](sock, handShakeDestination)  # TODO fix this function not callable

            LOGGER.info("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
            while self.__is_still_active():
                yield self.__process_loop(sock)

            if self.handShakeFunc:
                self.handShakeFunc[1](sock, handShakeDestination)
        finally:
            sock.close()
            LOGGER.info("[NTWK] [Info]\tServer shutting down.")

    # Main shared memory packet function

    def get_shared_packets(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        allSharedMemoryNames = self.allSharedMemoryNames

        if not allSharedMemoryNames:
            LOGGER.critical("[NTWK] [Error]\tShared memory name is not set.")
            raise ValueError("[NTWK] [Error]\tShared memory name is not set.")

        if not self.packetInfo:
            LOGGER.error("[NTWK] [Error]\tPacket Info is empty.")
            raise ValueError("[NTWK] [Error]\tPacket Info is empty.")

        sharedMemoryInfo = {}

        if isinstance(allSharedMemoryNames, str):
            # SMSize = self.__get_max_packet_size()
            SMSize = self.FULLBUFFERSIZE
            SMMap = mmap.mmap(-1, SMSize, tagname=allSharedMemoryNames, access=mmap.ACCESS_READ)
            sharedMemoryInfo.update({SMMap: SMSize})
            LOGGER.info("[NTWK] [Info]\tServer started on %s with size %d bytes" % (allSharedMemoryNames, SMSize))

        elif isinstance(allSharedMemoryNames, dict):
            SMNames = []
            for packetID, packetInfo in self.packetInfo.items():
                for packetStruct in packetInfo:
                    SMName = allSharedMemoryNames.get(packetStruct.__name__)
                    SMSize = self.__get_packet_size(packetStruct)
                    if SMName:
                        SMNames.append(SMName)
                        SMMap = mmap.mmap(-1, SMSize, tagname=SMName, access=mmap.ACCESS_READ)
                        sharedMemoryInfo.update({SMMap: SMSize})

            LOGGER.info("[NTWK] [Info]\tServer started for %r with sizes %r bytes", SMNames, [size for size in sharedMemoryInfo.values()])
        else:
            raise ValueError("[NTWK] [Error]\tShared memory name must be a string or a dict mapping packet names to shared memory names.")

        while self.__is_still_active():
            try:
                SMRawData = []
                for SMMap, SMSize in sharedMemoryInfo.items():
                    SMMap.seek(0)
                    raw = SMMap.read(SMSize)
                    SMRawData.append(raw)

            except TimeoutError:
                pass
            except KeyboardInterrupt:
                LOGGER.debug("Keyboard Interrupt from get_shared_packets")
                LOGGER.info("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                self.__trigger_stop()
                # continue
            except OSError as exc:
                LOGGER.error("[NTWK] [Error]\tShared memory error: %r", exc)
                self.__trigger_stop()
                # continue
            else:
                for SMData in SMRawData:
                    if not any(SMData):
                        continue
                    packet, packetID, headerPacket = self.__retrieve_packet(SMData)

                    yield packet, packetID, headerPacket

        for SMMap in sharedMemoryInfo.keys():
            SMMap.close()
        LOGGER.info("[NTWK] [Info]\tServer shutting down.")

    # Main thread functions

    def GetTelemetry(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        if self.sharedMemory:
            LOGGER.info("[NTWK] [Info]\tUsing shared memory telemetry.")
            yield from self.get_shared_packets()
        else:
            LOGGER.info("[NTWK] [Info]\tUsing UDP telemetry.")
            yield from self.get_udp_packets()

    def __network_listener(self) -> None:
        """
        Listens for incoming network packets and writes them to the active storage.
        This function runs in a separate thread and should not be called directly.
        """
        if self.activeStorage is None:
            raise ValueError("[NTWK] [Error]\tStorage instance is not initialized.")

        for packet, packetID, headerPacket in self.GetTelemetry():
            # LOGGER.debug("[NTWK] [Info]\tReceived packet ID %r", packetID)
            self.activeStorage._write(packet)
