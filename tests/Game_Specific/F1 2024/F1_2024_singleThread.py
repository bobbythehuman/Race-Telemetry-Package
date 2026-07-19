from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 6:
        currnetPlayer = packet.m_carTelemetryData[0]
        speedValue = currnetPlayer.m_speed

        print(f"{speedValue} KPH")
