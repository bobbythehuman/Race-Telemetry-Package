import ctypes
import socket
import mmap

import threading
from dataclasses import dataclass
from typing import Generator, Tuple, Type, Any, Optional
from datetime import datetime

from support.digestion import dynamic_ingest


# ---------------------------------------------------------------------------
# Central Storage
# ---------------------------------------------------------------------------


@dataclass
class CentralStorage:
    """
    Holds the latest network data.  Worker threads receive a read-only view
    via ReadOnlyStorage so they cannot accidentally mutate the contents.
    """

    def __init__(self, MetaData) -> None:
        self._lock = threading.RLock()

        self.allData = {}
        self.lastestData = {}

        packetNames = MetaData.packetInfo.items()
        for packetID, packetInfo in packetNames:
            for packetStruct in packetInfo:
                packetName = packetStruct.__name__
                if packetName not in self.allData:
                    self.allData[packetName] = []
                    self.lastestData[packetName] = None

    def _write(self, packetID: int, data) -> None:
        """Called only by the network thread."""
        with self._lock:
            if data:
                packetName = data.__name__

                self.allData[packetName].append(data)
                self.lastestData[packetName] = data

    def snapshot(self) -> dict[str, Any]:
        """Return a consistent, immutable snapshot for worker threads."""
        with self._lock:
            return {
                "allData": self.allData.copy(),
                "lastestData": self.lastestData.copy(),
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


class telemetryManager:
    def __init__(self):
        self.ACTIVE_METADATA = None
        self.IP = "0.0.0.0"
        self.destinationIP = None

        self.activeStorage = None
        self.readOnlyStorage = None
        self.stop_event = threading.Event()
        self.manuallyStopped = False

        self.networkThread = None
        self.workerThreads: dict[int, threading.Thread] = {}

        self.workersAreWorking = False
        self.threadCount = 0
        self.multiThreaded = True
        
        self.sharedMemory = False
        self.sharedMemoryName = None
        self.sharedMemorySize = None
        
        self.enumMode = 0
        
    # User controlled functions

    def updateMeta(self, MetaData):
        '''
        Call this to update the metadata and reset storage.
        Must be called at least once before starting threads.
        '''
        if self.ACTIVE_METADATA != MetaData:
            self.ACTIVE_METADATA = MetaData
            self.activeStorage = CentralStorage(self.ACTIVE_METADATA)
            self.readOnlyStorage = ReadOnlyStorage(self.activeStorage)
        self.__unpackMetaData()

    def updateLocalIP(self, ip: str):
        '''
        Call this to update the local IP address the server listens on.
        Default is "0.0.0.0"
        '''
        self.IP = ip

    def updateSendIP(self, ip: str):
        '''
        Call this to update the destination IP address for handshakes and heartbeats.
        Default is None, which will cause an error if handshakes or heartbeats are enabled.
        '''
        self.destinationIP = ip

    def addWorkerThread(self, mainFunc):
        '''
        Call this to add a worker thread to access the data. 
        The function must accept three keyword arguments: worker_id (int), ro_storage (ReadOnlyStorage), and stop_event (threading.Event).
        '''
        self.threadCount += 1
        # readOnlyStorage may need updating when metadata gets updated
        workerThread = threading.Thread(
            target=mainFunc,
            kwargs={"worker_id": self.threadCount, "ro_storage": self.readOnlyStorage, "stop_event": self.stop_event},
            daemon=True,
        )
        self.workerThreads.update({self.threadCount: workerThread})

    def manualStop(self, target: bool):
        """Manually stop the program by entering q to stop"""
        self.manuallyStopped = target

    def isMultiThreaded(self, target: bool = True):
        '''Currently does nothing'''
        self.multiThreaded = target

    def isSharedMemory(self, target: bool = False):
        '''
        Call this to set whether to use shared memory or UDP for telemetry.
        Default is False (UDP).
        '''
        self.sharedMemory = target
    
    def setEnumMode(self, target: int = 0):
        '''
        Call this to set the enum mode for handling enum values.
        Default is 0 (no special handling).
        Modes:
        0: No special handling (default)
        1: Convert fields with to the raw value
        2: Convert fields to their enum type
        '''
        self.enumMode = target

    # Misc packet functions

    def __metaDataCheck(self, name: str, value: Any = None):
        '''
        Helper function to check if metadata has the attribute, and return it if it does.
        Otherwise return the provided default value.
        '''
        
        if hasattr(self.ACTIVE_METADATA, name):
            return getattr(self.ACTIVE_METADATA, name)
            # _heartBeatPort = self.ACTIVE_METADATA.value
        else:
            return value
            # _heartBeatPort = None

    def __unpackMetaData(self):
        '''
        Helper function to unpack metadata attributes into class attributes for easy access
        '''
        self.mainPort = self.__metaDataCheck("port")

        self.heartBeatPort = self.__metaDataCheck("heartBeatPort")
        self.heartBeatFunc = self.__metaDataCheck("heartBeatFunc")

        self.handShakePort = self.__metaDataCheck("handShakePort")
        self.handShakeFunc = self.__metaDataCheck("handShakeFunc")

        self.decryptionFunc = self.__metaDataCheck("decrytionFunc")

        self.headerPacket = self.__metaDataCheck("headerInfo")
        self.packetIDAttr = self.__metaDataCheck("packetIDAttribute")
        
        self.allSharedMemoryNames = self.__metaDataCheck("allSharedMemoryNames")

        self.packetInfo = self.__metaDataCheck("packetInfo", [])

    def __getPacketSize(self, packet):
        '''Helper function to get the size of a packet using ctypes.sizeof, which is needed for shared memory reading and UDP packet construction.'''
        size = ctypes.sizeof(packet)
        return size
    
    def __getMaxPacketSize(self):
        '''Helper function to get the maximum packet size from the packet info in the metadata, which is needed for setting the full buffer size if not provided in the metadata.'''
        maxSize = 0
        for packetID, packetInfo in self.packetInfo.items():
            for packetStruct in packetInfo:
                packetSize = self.__getPacketSize(packetStruct)
                if packetSize > maxSize:
                    maxSize = packetSize
        return maxSize
    
    # Misc thread function

    def __wait(self, time: float):
        '''
        Helper function to wait while still checking for stop_event
        '''
        self.stop_event.wait(time)

    def __triggerStop(self):
        '''
        Helper function to trigger the stop event and set manuallyStopped to True
        '''
        if self.stop_event:
            self.stop_event.set()
        self.manuallyStopped = True

    def __isStillActive(self) -> bool:
        '''
        Helper function to check if the program should still be running
        '''
        return self.stop_event.is_set() or self.manuallyStopped

    # Start and Stop functions

    def __startThreads(self) -> None:
        '''
        Helper function to start the network thread and worker threads
        Does not start if metadata is not set or if IP is not set (for network thread)
        '''
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

    def __waitForStopSignal(self):
        '''
        Helper function to wait for a stop signal (either Ctrl+C or manual stop) while keeping the main thread alive
        '''
        endProgram = ""
        try:
            while not self.__isStillActive():
                self.__wait(0.5)

                if self.manuallyStopped:
                    # only stop threads here if they dont get stopped any where else
                    endProgram = input(f"[Q] to quit the program: ")
                    if endProgram.lower() == "q":
                        self.__triggerStop()

        except KeyboardInterrupt:
            print("\n[MAIN] [INFO]\tKeyboardInterrupt received.")
        finally:
            print("[MAIN] [INFO]\tStopping all threads\n")
            self.__stopThreads()

    def __stopThreads(self):
        '''
        Helper function to stop all threads gracefully by triggering the stop event and joining threads with a timeout
        '''
        if not self.workersAreWorking:
            return
        if not self.networkThread:
            return

        self.__triggerStop()
        self.networkThread.join(timeout=0.5)

        for workerName, workerThread in self.workerThreads.items():
            workerThread.join(timeout=0.5)
            if workerThread.is_alive():
                print(f"[MAIN] [WARNING]\tWarning: {workerName} did not stop in time.")

        self.workersAreWorking = False
        print("\n[MAIN] [INFO]\tAll threads stopped. Exiting.")

    def StartTelemetry(self):
        '''
        Call this to start the network and worker threads.
        Will run until a stop signal is received (either Ctrl+C or manual stop).
        '''
        print("[MAIN] [INFO]\tStart at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))
        self.__startThreads()
        print("\n[MAIN] [INFO]\tRunning — press Ctrl+C to stop.")
        # comment lines below to make a manual stop outside class
        self.__waitForStopSignal()
        print("[MAIN] [INFO]\tEnd at ", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    # Misc packet function

    def __construct_packet(self, data: bytes, possiblePacketStruct: Tuple) -> type | None:
        '''
        Helper function to construct a packet from the data using the possible packet structures provided in the metadata.
        Returns the constructed packet, or None if no matching packet structure is found.
        '''
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetStruct in possiblePacketStruct:
            packetBufferSize = self.__getPacketSize(packetStruct)
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    continue
                else:
                    packet = dynamic_ingest(rawPacket, self.enumMode)
                    break
        if len(possiblePacketStruct) == len(packetSizes):
            print(f"[Warning]\tNo matching packet size [{packetSizes}] for received data length {dataLength}")
            packet = None
        
        # do enum check here
        # do enum convert
        
        return packet

    def __retrieve_packet(self, data: bytes) -> tuple[type | None, int, Any]:
        '''
        Helper function to retrieve the packet, packet ID, and header packet (if applicable) from the raw data.
        Returns a tuple of (packet, packetID, headerPacket).
        packet and headerPacket may be None if no matching packet structure is found or if no header is defined in the metadata.
        '''
        if self.headerPacket:
            headerBufferSize = self.__getPacketSize(self.headerPacket)
            rawHeaderPacket = self.headerPacket.from_buffer_copy(data[0 : headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            packetID = int(getattr(headerPacket, self.packetIDAttr))
        else:
            headerPacket = None
            packetID = 0

        possiblePacketStruct = self.packetInfo.get(packetID)
        if possiblePacketStruct:
            packet = self.__construct_packet(data, possiblePacketStruct)
        else:
            print("ID not found")
            packet = None

        return packet, packetID, headerPacket

    # Main UDP packet function

    def __process_loop(self, sock: socket.socket, PACKET_COUNTER) -> Tuple[Type[Any] | None, int, Type[Any] | None]:
        '''
        Helper function to process the main loop of receiving data, handling heartbeats, and retrieving packets.
        Returns a tuple of (packet, packetID, headerPacket) for the received data.
        '''
        HEARTBEAT_INTERVAL = 5
        packet = None
        packetID = 0
        headerPacket = None
        heartBeatDestination = (self.destinationIP, self.heartBeatPort)
        fullBufferSize = self.__getMaxPacketSize()

        if self.heartBeatFunc:
            if PACKET_COUNTER % HEARTBEAT_INTERVAL == 0:
                self.heartBeatFunc(sock, heartBeatDestination)
                PACKET_COUNTER += 1
            else:
                PACKET_COUNTER = 0

        try:
            data, _ = sock.recvfrom(fullBufferSize)
        except TimeoutError:
            if self.heartBeatFunc:
                self.heartBeatFunc(sock, heartBeatDestination)
                PACKET_COUNTER = 0
            # continue
        except KeyboardInterrupt:
            print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
            self.__triggerStop()
            # continue
        except OSError as exc:
            print(f"[NTWK] [Error]\tSocket error: {exc}")
            self.__triggerStop()
            # continue
        else:
            if self.decryptionFunc:
                data = self.decryptionFunc(data)

            packet, packetID, headerPacket = self.__retrieve_packet(data)
        return packet, packetID, headerPacket

    def get_udp_packets(self) -> Generator[Tuple[Type[Any] | None, int, Type[Any] | None], None, None]:
        '''
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        '''
        
        UDP_IP = self.IP
        UDP_PORT = self.mainPort
        # HEARTBEAT_INTERVAL = 5
        PACKET_COUNTER = 0

        handShakeDestination = (self.destinationIP, self.handShakePort)

        if (self.handShakeFunc or self.heartBeatFunc) and not self.destinationIP:
            raise ValueError("[NTWK] [Error]\tDestination IP must be set for handshakes or heartbeats.")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # listen to occupied ports
        sock.settimeout(1.0)  # allows checking stop_event periodically
        sock.bind((UDP_IP, UDP_PORT))

        print(f"[NTWK] [Info]\tServer started on {UDP_IP}:{UDP_PORT}")

        if self.handShakeFunc:
            self.handShakeFunc[0](sock, handShakeDestination)

        print("[NTWK] [Info]\tStop event provided, running until stop_event is set.")
        while not self.__isStillActive():
            yield self.__process_loop(sock, PACKET_COUNTER)

        if self.handShakeFunc:
            self.handShakeFunc[1](sock, handShakeDestination)
        sock.close()
        print("[NTWK] [Info]\tServer shutting down.")

    # Main shared memory packet function
    
    def get_shared_packets(self) -> Generator[Tuple[Type[Any] | None, int, Type[Any] | None], None, None]:
        allSharedMemoryNames = self.allSharedMemoryNames

        if not allSharedMemoryNames:
            raise ValueError("[NTWK] [Error]\tShared memory name is not set.")

        sharedMemoryInfo = {}

        if isinstance(allSharedMemoryNames, str):
            SMSize = self.__getMaxPacketSize()
            SMMap = mmap.mmap(-1, SMSize, tagname=allSharedMemoryNames, access=mmap.ACCESS_READ)
            sharedMemoryInfo.update({SMMap: SMSize})
            print(f"[NTWK] [Info]\tServer started on {allSharedMemoryNames} with size {SMSize} bytes")
        elif isinstance(allSharedMemoryNames, dict):
            SMNames = []
            for packetID, packetInfo in self.packetInfo.items():
                for packetStruct in packetInfo:
                    SMName = allSharedMemoryNames.get(packetStruct.__name__)
                    SMSize = self.__getPacketSize(packetStruct)
                    if SMName:
                        SMNames.append(SMName)
                        SMMap = mmap.mmap(-1, SMSize, tagname=SMName, access=mmap.ACCESS_READ)
                        sharedMemoryInfo.update({SMMap: SMSize})
            print(f"[NTWK] [Info]\tServer started for {SMNames} with sizes {[size for size in sharedMemoryInfo.values()]} bytes")
        else:
            raise ValueError("[NTWK] [Error]\tShared memory name must be a string or a dict mapping packet names to shared memory names.")
        
        while not self.__isStillActive():
            try:
                SMRawData = []
                for SMMap, SMSize in sharedMemoryInfo.items():
                    SMMap.seek(0)
                    raw = SMMap.read(SMSize)
                    SMRawData.append(raw)
            except TimeoutError:
                pass
            except KeyboardInterrupt:
                print("[NTWK] [Info]\tKeyboardInterrupt received, shutting down server.")
                self.__triggerStop()
                # continue
            except OSError as exc:
                print(f"[NTWK] [Error]\tShared memory error: {exc}")
                self.__triggerStop()
                # continue
            else:
                for SMData in SMRawData:
                    non_zeros = set(SMData).difference(b'\x00')
                    if not non_zeros:
                        continue
                    packet, packetID, headerPacket = self.__retrieve_packet(SMData)
                
                    yield packet, packetID, headerPacket
        
        for SMMap in sharedMemoryInfo.keys():
            SMMap.close()
        print("[NTWK] [Info]\tServer shutting down.")

    # Main thread functions

    def GetTelemetry(self) -> Generator[Tuple[Type[Any] | None, int, Type[Any] | None], None, None]:
        if self.sharedMemory:
            print("[NTWK] [Info]\tUsing shared memory telemetry.")
            yield from self.get_shared_packets()
        else:
            print("[NTWK] [Info]\tUsing UDP telemetry.")
            yield from self.get_udp_packets()

    def __network_listener(self) -> None:
        '''
        Listens for incoming network packets and writes them to the active storage.
        This function runs in a separate thread and should not be called directly.
        '''
        if self.activeStorage is None:
            raise ValueError("[NTWK] [Error]\tStorage instance is not initialized.")

        for packet, packetID, headerPacket in self.GetTelemetry():
            # print(f"[NTWK] [Info]\tReceived packet ID {packetID}")
            self.activeStorage._write(packetID, packet)
