from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2016_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "UDPPacket":
        packetSpeed = packet.m_speed
        # speedValue = currnetPlayer.m_speed

        print(f"{packetSpeed} MPH")
