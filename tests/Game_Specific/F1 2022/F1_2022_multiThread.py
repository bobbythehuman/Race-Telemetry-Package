from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.F1_2022_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                currnetPlayer = telemetry.m_carTelemetryData[0]
                speedValue = currnetPlayer.m_speed

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            lapData = data.get("PacketLapData")
            if lapData:
                currnetPlayer = lapData.m_lapData[0]
                currentLap = currnetPlayer.m_currentLapNum

                print(f"Lap {currentLap}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentLap)
activeThreads.StartTelemetry()
