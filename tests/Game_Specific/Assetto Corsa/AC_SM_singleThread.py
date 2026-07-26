from RaceTelemetry import TelemetryManager
from RaceTelemetry.data_structures.AC_SM_struct import MetaData

telemetry = TelemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.isSharedMemory(True)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # for the SPageFileStaticData packet
    if packetName == "SPageFileStaticData":
        track = packet.track
        carModel = packet.carModel

        print(f"Track: {track}\t\t Car Model: {carModel}")
        
    # for the SPageFilePhysicsData packet
    if packetName == "SPageFilePhysicsData":
        packetSpeed = packet.speedKmh
        speedValue = round(packetSpeed/1.60934, 1)

        print(f"{speedValue} MPH")
        
    # for the SPageFileGraphicData packet
    if packetName == "SPageFileGraphicData":
        status = packet.status
        time = packet.currentTime

        print(f"status: {status}\t\t Time: {time}")
