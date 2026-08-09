"""
Telemetry manager: receives packets over UDP or shared memory, decodes them
using ctypes packet definitions, and hands them off to worker threads via a
read-only snapshot of the latest data.
"""

import ctypes
import logging
import re

from datetime import datetime
from types import SimpleNamespace
from typing import Generator, Any, Callable

# from .digestion import dynamic_ingest
from .config import TelemetryConfig
from .router import PacketRouter
from .threads import ThreadSupervisor
from .transport import UDPTransport, SharedMemoryTransport
from .storage import CentralStorage, ReadOnlyStorage

# ---------------------------------------------------------------------------
# Other Setups
# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)


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

        LOGGER.debug("TelemetryManager initialized.")

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
            LOGGER.error("Invalid type for shared memory setting. Expected bool.")
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

    def _network_listener(self) -> None:
        """
        Listens for incoming network packets and writes them to the active storage.
        This function runs in a separate thread and should not be called directly.
        """
        if self.activeStorage is None:
            raise ValueError("Storage instance is not initialized.")

        for packet, packetID, headerPacket in self._telemetry_generator():
            # LOGGER.debug("Received packet ID %r", packetID)
            self.activeStorage._write(packet)

    def _telemetry_generator(self) -> Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        This function is used internally by GetTelemetry() and should not be called directly.
        """
        if not self.shared_memory_transport or not self.udp_transport:
            LOGGER.error("Telemetry transports are not initialized. Call updateMeta() before GetTelemetry().")
            return

        if self.shared_memory:
            yield from self.shared_memory_transport.get_shared_packets()
        else:
            yield from self.udp_transport.get_udp_packets()

    def GetTelemetry(self) -> ReadOnlyStorage | Generator[tuple[SimpleNamespace | None, int, SimpleNamespace | None], None, None]:
        """
        Call this to get a generator that yields (packet, packetID, headerPacket) tuples for each received packet.
        """

        if self.readOnlyStorage is None:
            LOGGER.error("Read-only storage is not initialized. Call updateMeta() before StartTelemetry().")
            raise RuntimeError("Read-only storage is not initialized. Call updateMeta() before StartTelemetry().")

        if self.supervisor.multi_threaded:
            LOGGER.info("Using multi-threaded telemetry with generator.")
            self.supervisor._start_threads(network_target=self._network_listener)
            return self.readOnlyStorage

        else:
            LOGGER.info("Using single-threaded telemetry with generator.")
            return self._telemetry_generator()

    def StartTelemetry(self) -> None:
        """
        Call this to start the network and worker threads.
        Will run until a stop signal is received (either Ctrl+C or manual stop).
        """
        if self.readOnlyStorage is None:
            LOGGER.error("Read-only storage is not initialized. Call updateMeta() before StartTelemetry().")
            raise RuntimeError("Read-only storage is not initialized. Call updateMeta() before StartTelemetry().")

        LOGGER.info("Start at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

        self.supervisor._start_threads(network_target=self._network_listener)
        LOGGER.info("Running — press Ctrl+C to stop.")

        self.supervisor._wait_for_stop_signal()
        LOGGER.info("End at %r", datetime.now().strftime("%a-%d-%b, %H-%M-%S-%f"))

    def StopTelemetry(self) -> None:
        """
        Call this to stop the network and worker threads.
        Can be called from a worker thread or the main thread.
        """
        self.supervisor._trigger_stop()
        self.supervisor._stop_threads()
        LOGGER.info("Stop signal sent to all threads.")

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
