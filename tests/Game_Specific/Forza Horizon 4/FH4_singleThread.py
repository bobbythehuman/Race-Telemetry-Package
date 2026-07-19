from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.FH4_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "DashData":
        packetSpeed = packet.Speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
