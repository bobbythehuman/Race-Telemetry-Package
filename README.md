# Race-Telemetry-Package

A single telemetry package that can extract UDP and shared memory data from multiple racing games including: <br>
F1 2017 to F1 2025, BeamNG Drive, Project Cars 2, Forza Horizon, Forza Motorsport, Gran Turismo, and more.

## Features

- Single package for multiple racing game telemetry protocols
- Support for both single-threaded and multi-threaded operation modes
- Extensible packet structure system for adding new games
- Real-time UDP or shared memory data reception and decoding
- Thread-safe data storage for concurrent access

## Architecture

The multi-threaded system uses the following architecture:

- **Main Thread**: Creates and manages the telemetry system, starts worker threads, waits for stop signal
- **Network Listener Thread**: Continuously receives UDP or shared memory packets, decodes them according to the game protocol, and stores the latest data in `CentralStorage`
- **Worker Threads**: User-defined threads that access telemetry data via read-only snapshots, preventing accidental data mutation

Data is stored in `CentralStorage` with thread-safe locking mechanisms. Worker threads receive a `ReadOnlyStorage` interface that only allows taking immutable snapshots, ensuring thread safety without requiring manual locking.

## Options

### Single-Threaded Mode

The single-threaded mode provides a simple, blocking function that listens for UDP packets and returns decoded telemetry data. This is suitable for applications that don't require concurrent processing or real-time worker threads.

Located in [`server.py`](main/support/server.py), the `telemetryManager.GetTelemetry()` function:

- Blocks until a packet is received
- No threading overhead, simpler for basic usage

### Multi-Threaded Mode

The multi-threaded mode runs a full telemetry server with separate threads for network listening and data processing. This allows for real-time data processing while continuously receiving new packets.

Located in [`server.py`](main/support/server.py), the `telemetryManager.StartTelemetry()` class:

- Starts a network listener thread that continuously receives UDP data
- Provides a thread-safe central storage system (`CentralStorage`) for data
- Allows multiple worker threads to process data concurrently via read-only access

## Setup

### Prerequisites

- Python 3.8+
- On the same local network as the gaming device (or loopback for same device)
- For UDP telemetry: Game configured to send telemetry data to the correct IP and port
- For shared memory telemetry: Game configured to write telemetry data to shared memory (if supported)

### Single-Threaded Setup

For basic telemetry extraction without threading: <br>
See [`test_programs`](main/test_programs) for more single thread examples.

```python
from data_structures.f1_2024_struct import MetaData
from support.server import telemetryManager

# Initialize the class
telemetry = telemetryManager()

# Configure metadata and network settings
telemetry.updateMeta(MetaData)

# Use shared memory instead of UDP (if supported by the game)
telemetry.isSharedMemory(True)

# Start receiving telemetry data
for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    # Check packetID, if available
    if packetID == 6:
        pass # Process data here
    
    # Check packet name
    packetName = packet.__name__
    if packetName == 'PacketCarTelemetryData'
        pass # Process data here
```

### Multi-Threaded Setup

For real-time telemetry processing with multiple threads: <br>
See [`test_programs`](main/test_programs) for more multi thread examples.

```python
from data_structures.f1_2024_struct import MetaData
from support.server import telemetryManager

# Define a worker thread function
def my_worker_thread(worker_id: int, ro_storage, stop_event):
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()
      
        # Access telemetry data
        data = snapshot.get("lastestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                # Process data here
                pass

# Initialize the class
activeThreads = telemetryManager()

# Configure metadata and network settings
activeThreads.updateMeta(MetaData)

activeThreads.updateLocalIP("127.0.0.1") # Optional. Defaults to 0.0.0.0
activeThreads.updateSendIP("192.168.1.100")  # Optional: for heartbeat destination

# Use shared memory instead of UDP (if supported by the game)
activeThreads.isSharedMemory(True)

# Add worker threads to process telemetry data concurrently
activeThreads.addWorkerThread(my_worker_thread)

# Start the telemetry system with active worker threads
activeThreads.StartTelemetry()
```

## Adding and Using a New Packet Structure

### Step 1: Create the Packet Structure File

Create a new file in [`main/data_structures/`](main/data_structures/) following the naming convention `{game}_struct.py`.

Example structure:

```python
from enum import Enum
# Swap depending on what data types you want to use
import ctypes 

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
  
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
  
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
  
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double

# Define your header packet, if required
class PacketHeader(DataTypes.STRUCTURE.value):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16.value),
        ("m_gameYear",                  DataTypes.UNSIGNED_INT8.value),
        ("m_packetId",                  DataTypes.UNSIGNED_INT8.value),
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32.value),
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64.value),
        ("m_sessionTime",               DataTypes.FLOAT.value),
        # ...
    ]

# Define any sub-packet
class CarMotionData(DataTypes.STRUCTURE.value):
    # _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT.value),
        ("m_worldVelocityX",        DataTypes.FLOAT.value),
        ("m_worldForwardDirX",      DataTypes.SIGNED_INT16.value),
        ("m_worldRightDirX",        DataTypes.SIGNED_INT16.value),
        ("m_gForceLateral",         DataTypes.FLOAT.value),
        # ...
    ]

# Define a main packet
class PacketMotionData(DataTypes.STRUCTURE.value):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
    ]

```

### Step 2: Setup MetaData

In your main script, import the new metadata:

| Syntax            | Type                                   | Description                                                                          |
| ----------------- | -------------------------------------- | ------------------------------------------------------------------------------------ |
| port              | Integer                                | UDP port data is received on                                                         |
| fullBufferSize    | Integer                                | Maximum packet size                                                                  |
| heartBeatPort     | Integer                                | UDP port to send a heart beat to                                                     |
| heartBeatFunc     | Function                               | Heart beat function                                                                  |
| handShakePort     | Integer                                | UDP port to send a hand shake to                                                     |
| handShakeFunc     | Tuple [Function, Function]             | Tuple containing start and stop hand shake functions                                 |
| decrytionFunc     | Function                               | Data decryption function                                                             |
| headerInfo        | Tuple [int, type]                      | Tuple containing, the packet size and header struct class (if protocol uses header). |
| packetIDAttribute | String                                 | An attribute in the header packet defining the packet ID                             |
| sharedMemoryName  | String                                 | Name of the shared memory segment used for data exchange                             |
| sharedMemorySize  | Integer                                | Size of the shared memory segment used for data exchange                             |
| packetInfo        | Dict [int, List [Same as headerInfo] ] | Game packet mapping - See more below                                                 |

#### PacketInfo

A Dictionary containing

- key: Packet ID or 0 if no ID
- value: Tuple of (packetSize, packetStructClass) variants.

#### PacketInfo - Standard

```python
packetInfo = {
    0: ((1349, PacketMotionData),),
    1: ((753, PacketSessionData),),
    # ...
}
```

#### PacketInfo - PacketID with multiple packets

```python
packetInfo = {
    0: ((559, TelemetryData),),
    7: ((1040, TimeStatsData),),
    8: ((1452, VehicleClassNamesData), (1164, ParticipantVehicleNamesData),),
    # ...
}
```

#### PacketInfo - No PacketID

```python
packetInfo = {
    0: ((296, PacketAData), (316, PacketBData), (344, PacketTildaData), (368, PacketCData)),
    # ...
}
```

#### Full MetaData Example

```python
# MetaData class with packet information
class MetaData:
    # standard network info
    port: int| None = 20777  # UDP port for your game
    fullBufferSize: int = 1464  # Maximum packet size

    # use if a heartbeat is needed
    heartBeatPort = 33739
    heartBeatFunc = heartBeat

    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None # tuple (startHandShakeFunc, stopHandShakeFunc)

    # use if the data needs decrypting
    decrytionFunc = decrypt_data

    # use if there is a header packet
    headerInfo: tuple[int, type] = (32, PacketHeader)  # Header size and type
    packetIDAttribute: str = "m_packetId"  # Attribute name for packet ID
    
    # use for shared memory
    sharedMemoryName: str = "Local\\SCSTelemetry" # Name of the shared memory segment
    sharedMemorySize: int = 32 * 1024 # Size of the shared memory segment in bytes

    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((1349, PacketMotionData),),  # Packet ID: ((size, packet_class),)
        # Add more packet types as needed
    }
```

### Step 3: Import and Use

In your main script, import the new metadata and use it with either mode:

```python
from data_structures.your_game_struct import MetaData as YourGameMetaData
from support.server import telemetryManager

## Setup for both modes
activeThreads = telemetryManager()
activeThreads.updateMeta(YourGameMetaData)

## Use in single-threaded mode
for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

## Or in multi-threaded mode
activeThreads.addWorkerThread(your_worker_function)
activeThreads.StartTelemetry()
```

### Step 4: Handle Packet Decoding

The system automatically handles packet decoding based on the `packetInfo` dictionary. Ensure:

- Packet sizes match exactly (use `_pack_ = 1` for correct alignment)
- Packet IDs correspond to the correct packet types
- All nested structures are properly defined

## Supported Games

### UDP
- Assetto Corsa <!-- has link -->
- BeamNG Drive <!-- has link -->
- F1 2016 (untested) <!-- has link -->
- F1 2017 <!-- has link -->
- F1 2018 <!-- has link -->
- F1 2019 <!-- has link -->
- F1 2020 <!-- has link -->
- F1 2021 <!-- has link -->
- F1 2022 <!-- has link / has document -->
- F1 2023 <!-- has link / has document -->
- F1 2024 <!-- has link / has document -->
- F1 2025 (untested) <!-- has link / has document -->
- F1 2025 (2026 dlc)(untested) <!-- has link / has document -->
- Forza Horizon 4
- Forza Horizon 5
- Forza Horizon 6
- Forza Motorsport 7 (untested)
- Forza Motorsport 8
- Gran Turismo 7
- Project Cars 2

### Shared Memory
- Euro Truck Simulator 2

## Troubleshooting

- Check that the game is configured to send telemetry data
- Check no other running game uses the same port (on xbox, if a game is in quick resume state, it may block access to a port. EG; forza horizon 5 and motorsport 8)
- Verify IP addresses are correctly configured for network communication
- Use packet capture tools to verify data transmission (wireshark, and filter based on UDP, port, incoming and source IP)
- Ensure firewall allows UDP traffic on the configured port

## Game Specific Notes
- For Microsoft Store versions of Forza games, ensure loopback is configured correctly (see [forza debug.txt](./Supporting%20Docs/forza%20debug.txt) in supporting docs)
- Euro Truck Simulator 2 requires a 'scs-sdk-plugin' to be installed in the plugins folder, see support docs for more details


## Support Documentation

### Documents

<!-- - **Data Output from F1 22 v16.docx** - Packet structures and data output for F1 2022 version 16 (official release) -->
- [Data Output from F1 22 v16.docx](./Supporting%20Docs/Data%20Output%20from%20F1%2022%20v16.docx) - Packet structures and data output for F1 2022 version 16 (official release)
- [Data Output from F1 23 v29x3.docx](./Supporting%20Docs/Data%20Output%20from%20F1%2023%20v29x3.docx) - Packet structures and data output for F1 2023 version 29x3 (official release)
- [Data Output from F1 24 v27.2x.docx](./Supporting%20Docs/Data%20Output%20from%20F1%2024%20v27.2x.docx) - Packet structures and data output for F1 2024 version 27.2x (official release)
- [Data Output from F1 25 v3.pdf](./Supporting%20Docs/Data%20Output%20from%20F1%2025%20v3.pdf) - Packet structures and data output for F1 2025 version 3 (official release)
- [Data Output from F1 25 2026 Season Pack.pdf](./Supporting%20Docs/Data%20Output%20from%20F1%2025%202026%20Season%20Pack.pdf) - Packet structures and data output for F1 2026 (official release)
- [ACSharedMemoryDocumentation.pdf](./Supporting%20Docs/ACSharedMemoryDocumentation.pdf) - Assetto Corsa shared memory documentation(official release)
- [ACCSharedMemoryDocumentationV1.8.12.pdf](./Supporting%20Docs/ACCSharedMemoryDocumentationV1.8.12.pdf) - Assetto Corsa Competizione shared memory documentation for version 1.8.12 (official release)
- [ACE_SharedFileOut_Documentation_V1.pdf](./Supporting%20Docs/ACE_SharedFileOut_Documentation_v1.pdf) - Assetto Corsa Evo shared memory documentation for version 1 (official release)

Debugging guides available in the `Supporting Docs/` folder:

- [forza debug.txt](./Supporting%20Docs/forza%20debug.txt) - Debugging setup for Forza games including local loopback configuration for Microsoft Store versions

### Links

Documentation and links to packet structures in the [`Supporting Docs/`](./Supporting%20Docs/) folder:

- Assetto Corsa - Link to [AC Socket Document](https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub) (official release)
- Beamng.drive - Link to [Protocols](https://documentation.beamng.com/modding/protocols/) (official release)
- F1 2016 - Web Archive link to [F1 2016 D-Box and UDP Telemetry Information](https://web.archive.org/web/20180302011401/http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information)
- F1 2017 - Web Archive link to [F1 2017 D-Box and UDP Output Specification](https://web.archive.org/web/20230208144303/https://forums.codemasters.com/topic/20215-f1-2017-d-box-and-udp-output-specification/)
- F1 2018 - Web Archive link to [F1 2018 UDP Specification](https://web.archive.org/web/20230208110311/https://forums.codemasters.com/topic/30601-f1-2018-udp-specification/)
- F1 2019 - Web Archive link to [F1 2019 UDP Specification](https://web.archive.org/web/20220930165800/https://forums.codemasters.com/topic/44592-f1-2019-udp-specification/)
- F1 2020 - Web Archive link to [F1 2020 UDP Specification](https://web.archive.org/web/20221127112921/https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/)
- F1 2021 - Web Archive link to [F1 2021 UDP Specification](https://web.archive.org/web/20220525102004/https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/) (dead download link)
- F1 2021 - Link to [raweceek-telemetry/f1-2021-udp](https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#data-output-from-f1-2021)
- F1 2022 - Link to [F1 22 UDP Specification](https://forums.ea.com/discussions/f1-games-franchise-discussion-en/f1-22-udp-specification/8418392)
- F1 2023 - Link to [F1 23 UDP Specification](https://forums.ea.com/discussions/f1-23-en/f1-23-udp-specification/8390745)
- F1 2024 - Link to [F1 24 UDP Specification](https://forums.ea.com/discussions/f1-24-general-discussion-en/f1-24-udp-specification/8369125)
- F1 2025 - Link to [F1®25: 2026 Season Pack UDP SPECIFICATION](https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-2026-season-pack-udp-specification/12187347)
- F1 2026 - Link to [F1®25: 2026 Season Pack UDP SPECIFICATION](https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-2026-season-pack-udp-specification/12187347)
- ETS2 - Link to [truckermudgen github](https://github.com/truckermudgeon/scs-sdk-plugin) for scs-sdk-plugin, including instructions for installation

### Other Links

- Project cars - Link to [Companion App - UDP Streaming](https://web.archive.org/web/20160826185519/http://forum.projectcarsgame.com/showthread.php?40113-HowTo-Companion-App-UDP-Streaming&s=0147744ec824a4eb44be2e778d278c49)
- Project cars - Link to [Shared Memory (API) App](https://web.archive.org/web/20180111115813/http://forum.projectcarsgame.com/showthread.php?30903-Project-CARS-Shared-Memory-or-how-do-I-make-my-own-app&highlight=shared+memory+api)
- Project cars 2 - Link to [MacManley GitHub](https://github.com/MacManley/project-cars-2-udp) - Project Cars 2 UDP