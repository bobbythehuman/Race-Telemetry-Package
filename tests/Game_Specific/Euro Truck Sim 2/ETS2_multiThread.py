from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import ETS2_MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
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

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("scsTelemetryMapData")
            if telemetry:
                engineRPM = telemetry.engineRpm

                print(f"Engine RPM: {engineRPM}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(ETS2_MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayRPM)
activeThreads.StartTelemetry()
