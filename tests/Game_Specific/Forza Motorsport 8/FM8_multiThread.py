from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.FM8_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            sledData = data.get("SledData")
            if sledData:
                engineRPM = sledData.CurrentEngineRpm

                print(f"{engineRPM} RPM")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayFormat(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            dashData = data.get("DashData")
            if dashData:
                packetSpeed = dashData.Speed
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayFormat)
activeThreads.StartTelemetry()
