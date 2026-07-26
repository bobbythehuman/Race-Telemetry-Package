from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.FH6_struct import MetaData


telemetry = TelemetryManager()
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
