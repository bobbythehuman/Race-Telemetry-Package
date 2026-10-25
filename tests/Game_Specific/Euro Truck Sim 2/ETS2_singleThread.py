from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import ETS2_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(ETS2_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        telemetryData = data.get("scsTelemetryMapData")
        if telemetryData:
            packetSpeed = telemetryData.speed
            speedValue = round(packetSpeed * 2.237, 2)
            print(f"{speedValue} MPH")
