from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.BNG_struct import MetaData

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # for the TelemetryData packet
    if packetName == "TelemetryData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")

    # for the MotionSim packet
    if packetName == "MotionSim":
        format = packet.format

        print(f"Format: {format}")
