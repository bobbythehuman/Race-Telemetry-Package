from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.ACE_struct import MetaData

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.isSharedMemory(True)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    # for the SPageFilePhysicsData packet
    if packetName == "SPageFilePhysicsData":
        speed = packet.speedKmh
        speedValue = round(speed/1.60934, 1)
        print(f"{speedValue} MPH")

    # for the SPageFileGraphicEvoData packet
    if packetName == "SPageFileGraphicEvoData":
        RPM = packet.rpm_percent
        print(f"RPM: {RPM}%")
        
    # for the SPageFileStaticEvoData packet
    if packetName == "SPageFileStaticEvoData":
        session = packet.session_name
        track = packet.track_configuration
        print(f"Session: {session}\t\t Track: {track}")
