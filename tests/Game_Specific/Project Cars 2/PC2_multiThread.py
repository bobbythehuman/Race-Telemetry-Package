from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.PC2_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("TelemetryData")
            if telemetry:
                speedPacket = telemetry.sSpeed
                speedValue = round(speedPacket * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentCar(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            participantData = data.get("ParticipantVehicleNamesData")
            if participantData:
                currnetPlayer = participantData.sVehicleInfo[0]
                currentCar = currnetPlayer.sName

                print(f"Car: {currentCar}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentCar)
activeThreads.StartTelemetry()
