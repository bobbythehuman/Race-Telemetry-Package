from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.BNG_struct import MetaData

from time import sleep
import logging

root_logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s\t%(name)s\t%(levelname)s:\t%(message)s"))
root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)

###

telemetry = TelemetryManager()
telemetry.updateMeta(MetaData)


"""multi-threaded version with GetTelemetry() generator"""
telemetry.isMultiThreaded(True)
telemetryStream = telemetry.GetTelemetry()
for data in telemetryStream:
    # print(data)
    if not isinstance(data, dict):
        continue

    a = data.get("TelemetryData")
    if a:
        speed = a.speed
        speedValue = round(speed * 2.237, 2)  # convert m/s to MPH
        print(f"Speed: {speedValue} MPH")


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
