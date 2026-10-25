from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import F1_2016_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(F1_2016_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        UDPData = data.get("UDPPacket")
        if UDPData:
            packetSpeed = UDPData.m_speed
            print(f"{packetSpeed} MPH")
