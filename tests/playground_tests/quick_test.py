from RaceTelemetry import TelemetryManager

# from RaceTelemetry.data_structures.BNG_struct import MetaData
from RaceTelemetry.DataStructures import BNG_MetaData

from time import sleep
import logging

root_logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s:\t%(message)s"))
root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)

###

telemetry = TelemetryManager()
telemetry.updateMeta(BNG_MetaData)


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("TelemetryData")
            if telemetry:
                packetSpeed = telemetry.speed
                speedValue = round(packetSpeed * 3.6, 2)

                print(f"{speedValue} KPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


"""multi-threaded version with GetTelemetry() generator"""
# telemetry.isMultiThreaded(True)
# telemetryStream = telemetry.GetTelemetry()
# for data in telemetryStream:
#     # print(data)
#     if not isinstance(data, dict):
#         continue

#     a = data.get("TelemetryData")
#     if a:
#         speed = a.speed
#         speedValue = round(speed * 2.237, 2)  # convert m/s to MPH
#         print(f"Speed: {speedValue} MPH")

#         if a.gear == "":
#             print("Gear: Reverse")
#             telemetry.StopTelemetry()
#             break


"""single-threaded version with GetTelemetry() generator"""
# telemetry.isMultiThreaded(False)
# telemetryStream = telemetry.GetTelemetry()

# for packet, packetID, headerPacket in telemetryStream:
#     if not packet:
#         continue

#     packetName = packet.__name__

#     # for the TelemetryData packet
#     if packetName == "TelemetryData":
#         packetSpeed = packet.speed
#         speedValue = round(packetSpeed * 2.237, 2)

#         print(f"{speedValue} MPH")


"""multi-threaded version with StartTelemetry()"""
telemetry.addWorkerThread(displaySpeed)
telemetry.StartTelemetry()
