from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import F1_2017_MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("UDPPacket")
            if telemetry:
                packetSpeed = telemetry.m_speed
                speedValue = round(packetSpeed * 2.237, 2)

                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("UDPPacket")
            if telemetry:
                currentLap = telemetry.m_lap

                print(f"Lap {currentLap}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(F1_2017_MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentLap)
activeThreads.StartTelemetry()
