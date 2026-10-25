from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import FM8_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(FM8_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        sledData = data.get("SledData")
        if sledData:
            engineRPM = sledData.CurrentEngineRpm
            print(f"{engineRPM} RPM")

        dashData = data.get("DashData")
        if dashData:
            packetSpeed = dashData.Speed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")
