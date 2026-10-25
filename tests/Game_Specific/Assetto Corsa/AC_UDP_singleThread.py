from RaceTelemetry import TelemetryManager
from RaceTelemetry.DataStructures import AC_UDP_MetaData

sourceIP = "127.0.0.1"

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(AC_UDP_MetaData)
telemetry.updateSendIP(sourceIP)

for snapshot in telemetry.GetTelemetry():
    data = snapshot.get("latestData")
    if data:

        carData = data.get("RTCarData")
        if carData:
            packetSpeed = carData.speed_Mph
            speedValue = round(packetSpeed, 2)
            print(f"{speedValue} MPH")

        lapData = data.get("RTLapData")
        if lapData:
            lap = lapData.lap
            print(f"Lap: {lap}")
