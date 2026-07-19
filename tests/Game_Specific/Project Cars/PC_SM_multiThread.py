from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.PC_SM_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("mTelemetryData")
            if telemetry:
                speedPacket = telemetry.mSpeed
                speedValue = round(speedPacket * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayCurrentLap(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            participantData = data.get("mTelemetryData")
            if participantData:
                currnetPlayer = participantData.mParticipantInfo[0]
                currentCar = currnetPlayer.mCurrentLap

                print(f"Lap: {currentCar}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayCurrentLap)
activeThreads.StartTelemetry()
