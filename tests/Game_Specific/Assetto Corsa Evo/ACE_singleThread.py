from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import ACE_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(ACE_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        staticData = data.get("SPageFileStaticEvoData")
        if staticData:
            session = staticData.session_name
            track = staticData.track_configuration
            print(f"Session: {session}\t\t Track: {track}")

        physicsData = data.get("SPageFilePhysicsData")
        if physicsData:
            packetSpeed = physicsData.speedKmh
            speedValue = round(packetSpeed / 1.60934, 1)
            print(f"{speedValue} MPH")

        graphicsData = data.get("SPageFileGraphicEvoData")
        if graphicsData:
            RPM = graphicsData.rpm_percent
            print(f"RPM: {RPM}%")
