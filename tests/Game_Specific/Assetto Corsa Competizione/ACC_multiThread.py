from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.ACE_struct import MetaData

def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("SPageFilePhysicsData")
            if telemetry:
                speed = telemetry.speedKmh
                speedValue = round(speed/1.60934, 1)
                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayTime(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            graphics = data.get("SPageFileGraphicData")
            if graphics:
                distance = graphics.distanceTraveled
                print(f"Distance: {distance}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.isSharedMemory(True)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayTime)
activeThreads.StartTelemetry()
