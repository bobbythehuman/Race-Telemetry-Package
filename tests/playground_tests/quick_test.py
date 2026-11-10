from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import PC2_MetaData, FH6_MetaData, F1_2024_MetaData
from RaceTelemetry.DataStructures import BNG_MetaData, AC_SM_MetaData, AC_UDP_MetaData, RaceRoom_MetaData

import logging

root_logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s:\t%(message)s"))
root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)

###

telemetry = TelemetryManager()
telemetry.updateMeta(BNG_MetaData)
# telemetry.updateSendIP("127.0.0.1")
# telemetry.useSharedMemory(True)


def displaySpeed(worker_id: int, ro_storage, stop_event):
    print(f"[THRD] [INFO]\tWorker {worker_id} started.")
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("TelemetryData")
            if telemetry:
                packetSpeed = telemetry.speed
                speedValue = round(packetSpeed * 2.237, 2)
                print(f"{speedValue} MPH")

    print(f"[THRD] [INFO]\tWorker {worker_id} stopping.")


"""multi-threaded version with GetTelemetry() generator"""


def multi_thread_gen(telemetry):
    telemetry.isMultiThreaded(True)
    telemetryStream = telemetry.GetTelemetry()

    for snapshot in telemetryStream:

        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("TelemetryData")
            if telemetry:
                speed = telemetry.speed
                speedValue = round(speed * 2.237, 2)  # convert m/s to MPH
                print(f"Speed: {speedValue} MPH")


"""single-threaded version with GetTelemetry() generator"""


def single_thread_gen(telemetry):
    telemetry.isMultiThreaded(False)
    telemetryStream = telemetry.GetTelemetry()

    for snapshot in telemetryStream:

        # data = snapshot.get("latestData")
        # if data:
        #     telemetry = data.get("TelemetryData")
        #     if telemetry:
        #         packetSpeed = telemetry.speed
        #         speedValue = round(packetSpeed * 2.237, 2)
        #         print(f"{speedValue} MPH")

        data = snapshot.get("latestCommonData")
        # print(data)
        if data.speed is not None:
            packetSpeed = data.speed
            speedValue = packetSpeed
            # speedValue = round(packetSpeed * 2.237, 2) # convert m/s to MPH
            # speedValue = round(packetSpeed * 3.6, 2) # convert m/s to kph
            # speedValue = round(packetSpeed / 1.609, 2) # convert km/h to MPH
            print(f"{speedValue} MPH")


"""multi-threaded version with StartTelemetry()"""


def multi_thread_start(telemetry):
    telemetry.addWorkerThread(displaySpeed)
    telemetry.StartTelemetry()


###

single_thread_gen(telemetry)
# multi_thread_gen(telemetry)
# multi_thread_start(telemetry)
