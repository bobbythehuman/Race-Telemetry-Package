from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import Dirt_4_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(Dirt_4_MetaData)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        mode1Data = data.get("Mode3")
        if mode1Data:
            packetSpeed = mode1Data.speed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")

        mode2Data = data.get("Mode1")
        if mode2Data:
            gear = mode2Data.gear
            print(f"Gear: {gear}")
