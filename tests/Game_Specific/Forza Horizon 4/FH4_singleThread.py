from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import FH4_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(FH4_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        dashData = data.get("DashData")
        if dashData:
            packetSpeed = dashData.Speed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")
