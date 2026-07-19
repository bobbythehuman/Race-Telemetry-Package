import sys
from pathlib import Path

# Add parent directory to path so imports work when running this file directly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from data_structures.ETS2_struct import MetaData
from support.server import telemetryManager

telemetry = telemetryManager()
telemetry.isMultiThreaded(False)
telemetry.updateMeta(MetaData)
telemetry.isSharedMemory(True)

for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    packetName = packet.__name__

    if packetName == "scsTelemetryMapData":
        packetSpeed = packet.speed
        speedValue = round(packetSpeed * 2.237, 1)


        print(f"{speedValue} MPH")
