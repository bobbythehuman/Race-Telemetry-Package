from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.AC_UDP_struct import MetaData


sourceIP = "127.0.0.1"

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.updateSendIP(sourceIP)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # for the TelemetryData packet
    if packetName == "RTCarData":
        packetSpeed = packet.speed_Mph
        speedValue = round(packetSpeed, 2)

        print(f"{speedValue} MPH")

    # for the MotionSim packet
    if packetName == "RTLapData":
        lap = packet.lap

        print(f"Lap: {lap}")
