import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.ACE_struct import MetaData
from support.server import telemetryManager


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

    # for the SPageFileGraphicData packet
    if packetName == "SPageFileGraphicData":
        distance = packet.distanceTraveled
        print(f"Distance: {distance}")

    # for the SPageFileStaticData packet
    if packetName == "SPageFileStaticData":
        car = packet.carModel
        print(f"Car: {car}")

