from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.PC_SM_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 0:
        speedPacket = packet.mSpeed
        speedValue = round(speedPacket * 3.6, 2)

        print(f"{speedValue} KPH")
