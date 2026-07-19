from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.PC2_struct import MetaData


telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetID == 0:
        speedPacket = packet.sSpeed
        speedValue = round(speedPacket * 3.6, 2)

        print(f"{speedValue} KPH")

    if packetID == 8:
        if packetName == "ParticipantVehicleNamesData":
            currnetPlayer = packet.sVehicleInfo[0]
            currentCar = currnetPlayer.sName

            print(f"Car: {currentCar}")
