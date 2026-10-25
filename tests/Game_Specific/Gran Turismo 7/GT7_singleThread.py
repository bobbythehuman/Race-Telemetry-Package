from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import GT7_MetaData

# the IP of the PS5
sourceIP = "192.168.1.1"

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(GT7_MetaData)
telemetry.updateSendIP(sourceIP)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        packetData = data.get("PacketCData")
        if packetData:
            packetSpeed = packetData.speed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")
