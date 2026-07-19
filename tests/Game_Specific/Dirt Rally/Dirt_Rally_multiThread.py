from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.Dirt_4_struct import MetaData


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("UDPPacket")
            if telemetry:
                packetSpeed = telemetry.velocity
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


def displayGear(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("UDPPacket")
            if telemetry:
                gear = telemetry.gear

                print(f"Gear: {gear}")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displaySpeed)
activeThreads.addWorkerThread(displayGear)
activeThreads.StartTelemetry()
