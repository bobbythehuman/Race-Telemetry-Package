from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import PC_SM_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(PC_SM_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        telemetryData = data.get("mTelemetryData")
        if telemetryData:
            packetSpeed = telemetryData.mSpeed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")
