from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import ACC_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(ACC_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        staticData = data.get("SPageFileStaticData")
        if staticData:
            carModel = staticData.carModel
            print(f"Car Model: {carModel}")

        physicsData = data.get("SPageFilePhysicsData")
        if physicsData:
            packetSpeed = physicsData.speedKmh
            speedValue = round(packetSpeed / 1.60934, 1)
            print(f"{speedValue} MPH")

        graphicsData = data.get("SPageFileGraphicData")
        if graphicsData:
            distance = graphicsData.distanceTraveled
            print(f"Distance: {distance}")
