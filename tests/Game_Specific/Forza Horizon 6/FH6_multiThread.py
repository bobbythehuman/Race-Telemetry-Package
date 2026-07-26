from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.FH6_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("DashData")
            if telemetry:
                packetSpeed = telemetry.Speed
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayGear(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("DashData")
            if telemetry:
                gearValue = telemetry.Gear

                print(f"Gear: {gearValue}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayGear)
activeThreads.StartTelemetry()
