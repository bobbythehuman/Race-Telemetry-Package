from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import AC_SM_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(AC_SM_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        staticData = data.get("SPageFileStaticData")
        if staticData:
            track = staticData.track
            carModel = staticData.carModel
            print(f"Track: {track}\t\t Car Model: {carModel}")

        physicsData = data.get("SPageFilePhysicsData")
        if physicsData:
            packetSpeed = physicsData.speedKmh
            speedValue = round(packetSpeed / 1.60934, 1)
            print(f"{speedValue} MPH")

        graphicsData = data.get("SPageFileGraphicData")
        if graphicsData:
            status = graphicsData.status
            time = graphicsData.currentTime
            print(f"status: {status}\t\t Time: {time}")
