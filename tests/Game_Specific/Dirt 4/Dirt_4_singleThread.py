from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.Dirt_4_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "Mode3":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 3.6, 2)

        print(f"{speedValue} KPH")

    if packetName == "Mode1":
        gear = packet.gear

        print(f"Gear: {gear}")
