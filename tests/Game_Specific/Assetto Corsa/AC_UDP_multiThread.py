from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.AC_UDP_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("RTCarData")

            if telemetry:
                packetSpeed = telemetry.speed_Mph
                speedValue = round(packetSpeed, 2)
                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            lapData = data.get("RTLapData")
            if lapData:
                lap = lapData.lap
                print(f"Lap: {lap}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


sourceIP = "127.0.0.1"

activeThreads = TelemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.updateSendIP(sourceIP)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayLap)
activeThreads.StartTelemetry()
