from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import FH6_MetaData


telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(FH6_MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "DashData":
        packetSpeed = packet.Speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
