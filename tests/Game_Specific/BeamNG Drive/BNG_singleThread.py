from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import BNG_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(BNG_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        telemetryData = data.get("TelemetryData")
        if telemetryData:
            packetSpeed = telemetryData.speed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")

        motionData = data.get("MotionSim")
        if motionData:
            format = motionData.format
            print(f"Format: {format}")
