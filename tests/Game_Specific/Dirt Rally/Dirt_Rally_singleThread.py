from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import Dirt_Rally_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(Dirt_Rally_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        UDPData = data.get("UDPPacket")
        if UDPData:
            packetSpeed = UDPData.velocity
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")

            gear = UDPData.gear
            print(f"Gear: {gear}")
