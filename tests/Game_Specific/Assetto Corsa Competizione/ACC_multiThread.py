from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import ACC_MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("SPageFilePhysicsData")
            if telemetry:
                speed = telemetry.speedKmh
                speedValue = round(speed / 1.60934, 1)
                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayTime(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            graphics = data.get("SPageFileGraphicData")
            if graphics:
                distance = graphics.distanceTraveled
                print(f"Distance: {distance}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(ACC_MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayTime)
activeThreads.StartTelemetry()
