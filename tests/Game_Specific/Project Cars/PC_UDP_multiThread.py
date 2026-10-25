from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import PC_UDP_MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("sTelemetryData")
            if telemetry:
                speedPacket = telemetry.sSpeed
                speedValue = round(speedPacket * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            participantData = data.get("sTelemetryData")
            if participantData:
                currnetPlayer = participantData.sParticipantInfo[0]
                currentCar = currnetPlayer.sCurrentLap

                print(f"Lap: {currentCar}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(PC_UDP_MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentLap)
activeThreads.StartTelemetry()
