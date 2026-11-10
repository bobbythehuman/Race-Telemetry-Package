from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import RaceRoom_MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(RaceRoom_MetaData)


for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        allData = data.get("Shared")
        if allData:
            packetSpeed = allData.CarSpeed
            speedValue = round(packetSpeed * 3.6, 2)
            print(f"{speedValue} KPH")

        allData = data.get("Shared")
        if allData:
            trackName = allData.TrackName
            layoutName = allData.LayoutName
            print(f"Track: {trackName} - Layout: {layoutName}")
