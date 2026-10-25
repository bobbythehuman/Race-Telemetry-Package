from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import PC2_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(PC2_MetaData)
# use the shared memory option
telemetry.useSharedMemory(False)


for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        carData = data.get("RTCarData")
        if carData:
            packetSpeed = carData.sSpeed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")

        participantData = data.get("ParticipantVehicleNamesData")
        if participantData:
            currnetPlayer = participantData.sVehicleInfo[0]
            currentCar = currnetPlayer.sName

            print(f"Car: {currentCar}")
