from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.F1_2017_struct import MetaData


telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "UDPPacket":
        packetSpeed = packet.m_speed
        speedValue = round(packetSpeed * 2.237, 2)

        print(f"{speedValue} MPH")
