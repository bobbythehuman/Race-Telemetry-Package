import threading
import logging

from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from RaceTelemetry.storage import ReadOnlyStorage

LOGGER = logging.getLogger(__name__)


class ThreadSupervisor:
    """
    Supervises the network thread and worker threads.
    Provides methods to start, stop, and monitor the threads.
    """

    def __init__(self):
        self.stop_event = threading.Event()
        self.manually_stopped: bool = False

        self.network_thread: threading.Thread | None = None
        self.worker_threads: dict[int, threading.Thread] = {}

        self.workers_are_working: bool = False
        self.thread_count: int = 0
        self.multi_threaded: bool = True  # unused for now

        LOGGER.debug("ThreadSupervisor initialized.")

    def add_worker_thread(self, mainFunc: Callable[..., Any], ro_storage: ReadOnlyStorage | None) -> bool:
        """
        Call this to add a worker thread to access the data.
        The function must accept three keyword arguments:
        worker_id (int), ro_storage (ReadOnlyStorage), and stop_event (threading.Event).
        """

        if not callable(mainFunc):
            LOGGER.warning("Worker function must be callable.")
            return False

        if isinstance(mainFunc, type):
            LOGGER.warning("Worker Function must not be a class.")
            return False

        if not ro_storage:
            LOGGER.warning("Read-only storage is not initialized. Call updateMeta() before adding worker threads.")
            return False

        self.thread_count += 1
        workerThread = threading.Thread(
            target=mainFunc,
            kwargs={"worker_id": self.thread_count, "ro_storage": ro_storage, "stop_event": self.stop_event},
            daemon=True,
        )
        self.worker_threads.update({self.thread_count: workerThread})
        return True

    def manual_stop(self, target: bool) -> bool:
        """Manually stop the program"""

        if not isinstance(target, bool):
            LOGGER.error("Invalid type for manual stop. Expected bool.")
            return False

        self.manually_stopped = target
        return True

    def is_multi_threaded(self, target: bool = True) -> bool:
        """Currently does nothing"""

        if not isinstance(target, bool):
            LOGGER.error("Invalid type for multi-threading. Expected bool.")
            return False

        self.multi_threaded = target
        LOGGER.debug("Multi-threading set to %r.", target)
        return True

    def _start_threads(self, network_target: Callable[[], None]) -> None:
        """
        Helper function to start the network thread and worker threads
        Does not start if metadata is not set or if IP is not set (for network thread)
        """

        self.network_thread = threading.Thread(
            target=network_target,
            kwargs={},
            daemon=True,
        )

        self.network_thread.start()
        LOGGER.debug("Network thread started.")

        for workerName, workerThread in self.worker_threads.items():
            workerThread.start()

        self.workers_are_working = True
        LOGGER.debug("Worker threads started: %r", list(self.worker_threads.keys()))

    def _wait_for_stop_signal(self) -> None:
        """
        Helper function to wait for a stop signal (either Ctrl+C or manual stop) while keeping the main thread alive
        """

        endProgram = ""
        try:
            while self._is_still_active():
                self._wait(0.5)

                if self.manually_stopped:
                    # only stop threads here if they dont get stopped any where else
                    endProgram = input("[Q] to quit the program: ")
                    if endProgram.lower() == "q":
                        self._trigger_stop()

        except KeyboardInterrupt:
            LOGGER.debug("Keyboard Interrupt from wait_for_stop_signal")
            LOGGER.info("KeyboardInterrupt received.")
        finally:
            LOGGER.info("Stopping all threads")
            self._stop_threads()

    def _stop_threads(self) -> None:
        """
        Helper function to stop all threads gracefully by triggering the stop event and joining threads with a timeout
        """
        if not self.workers_are_working:
            return
        if not self.network_thread:
            return

        self._trigger_stop()
        current_thread = threading.current_thread()
        if self.network_thread is not current_thread:
            self.network_thread.join(timeout=0.5)

        for workerName, workerThread in self.worker_threads.items():
            if workerThread is current_thread:
                continue
            workerThread.join(timeout=0.5)
            if workerThread.is_alive():
                LOGGER.warning("Warning: %r did not stop in time.", workerName)

        self.workers_are_working = False
        LOGGER.info("All threads stopped. Exiting.")

    def _wait(self, time: float) -> None:
        """
        Helper function to wait while still checking for stop_event
        """
        self.stop_event.wait(time)

    def _trigger_stop(self, mode: bool = True) -> None:
        """
        Helper function to toggle the stop event
        """
        if self.stop_event and mode:
            self.stop_event.set()
        else:
            self.stop_event.clear()

    def _is_still_active(self) -> bool:
        """
        Helper function to check if the program should still be running
        """
        return not self.stop_event.is_set()
