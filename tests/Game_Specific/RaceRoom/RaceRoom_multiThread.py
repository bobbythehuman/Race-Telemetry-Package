from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import RaceRoom_MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            allData = data.get("Shared")
            if allData:
                speedPacket = allData.CarSpeed
                speedValue = round(speedPacket * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayTrack(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            allData = data.get("Shared")
            if allData:
                trackName = allData.TrackName
                layoutName = allData.LayoutName

                print(f"Track: {trackName} - Layout: {layoutName}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = TelemetryManager()
activeThreads.updateMeta(RaceRoom_MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayTrack)

activeThreads.StartTelemetry()
