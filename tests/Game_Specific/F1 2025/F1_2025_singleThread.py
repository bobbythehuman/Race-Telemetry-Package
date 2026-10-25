from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import F1_2025_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(F1_2025_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        telemetryData = data.get("PacketCarTelemetryData")
        if telemetryData:
            currnetPlayer = telemetryData.m_carTelemetryData[0]
            speedValue = currnetPlayer.m_speed
            print(f"{speedValue} KPH")
