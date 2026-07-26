from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.ETS2_struct import MetaData


telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.isSharedMemory(True)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "scsTelemetryMapData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 2.237, 1)


        print(f"{speedValue} MPH")
