from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.GT7_struct import MetaData


# the IP of the PS5
sourceIP = "192.168.1.1"

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.updateSendIP(sourceIP)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # only if heartbeat msg is 'C'
    if packetName == "PacketCData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")
