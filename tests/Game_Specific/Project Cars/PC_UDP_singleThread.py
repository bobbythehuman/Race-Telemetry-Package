from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import PC_UDP_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(PC_UDP_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        telemetryData = data.get("sTelemetryData")
        if telemetryData:
            packetSpeed = telemetryData.sSpeed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")
