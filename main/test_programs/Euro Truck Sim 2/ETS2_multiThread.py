import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.ETS2_struct import MetaData
from support.server import telemetryManager


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("scsTelemetryMapData")
            if telemetry:
                packetSpeed = telemetry.speed
                speedValue = round(packetSpeed * 2.237, 1)

                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayRPM(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("scsTelemetryMapData")
            if telemetry:
                engineRPM = telemetry.engineRpm

                print(f"Engine RPM: {engineRPM}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.isSharedMemory(True)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayRPM)
activeThreads.StartTelemetry()
