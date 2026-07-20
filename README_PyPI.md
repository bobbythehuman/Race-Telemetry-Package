# Race-Telemetry-Package

A single telemetry package that can extract UDP and shared memory data from multiple racing games including:
Assetto Corsa, BeamNG Drive, F1 2016 to F1 2026, Forza Horizon, Forza Motorsport, Gran Turismo, Project Cars 2, and more.

# Installation

```Shell
pip install RaceTelemetry
```

## Features

- Single package for multiple racing game telemetry protocols
- Support for both single-threaded and multi-threaded operation modes
- Extensible packet structure system for adding new games
- Real-time UDP or shared memory data reception and decoding
- Thread-safe data storage for concurrent access

## Architecture

The multi-threaded system uses the following architecture:

- **Main Thread**: Creates and manages the telemetry system, starts worker threads, waits for stop signal
- **Network Listener Thread**: Continuously receives UDP or shared memory packets, and decodes them according to the game protocol.
- **Worker Threads**: User-defined threads that access telemetry data via read-only snapshots, preventing accidental data mutation

## Setup

### Prerequisites

- Python 3.9+
- On the same local network as the gaming device (or loopback for same device)
- For UDP telemetry: Game configured to send telemetry data to the correct IP and port
- For shared memory telemetry: Game configured to write telemetry data to shared memory (if supported)

### Single-Threaded Setup

The single-threaded mode provides a simple, blocking function that listens for UDP packets and returns decoded telemetry data.
This is suitable for applications that don't require concurrent processing or real-time worker threads.

For basic telemetry extraction without threading:

```python
from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData

# Initialize the class
telemetry = telemetryManager()

# Configure metadata and network settings
telemetry.updateMeta(MetaData)

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

The multi-threaded mode runs a full telemetry server with separate threads for network listening and data processing.
This allows for real-time data processing while continuously receiving new packets.

For real-time telemetry processing with multiple threads:

```python
from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData

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

# Add worker threads to process telemetry data concurrently
activeThreads.addWorkerThread(my_worker_thread)

# Start the telemetry system with active worker threads
activeThreads.StartTelemetry()
```

## Config Options

| Systax             | Parameters                                                                                                                                                                                                 | Description                                                                                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| telemetryManager() | None                                                                                                                                                                                                       | Initialize and create a new telemetry manager instance. This manages all network communication, data storage, and threading.                                                                             |
| .updateMeta()      | `MetaData` (class): see [Adding and Using a New Packet Structure](#adding-and-using-a-new-packet-structure) for details                                                                                   | Apply game-specific metadata to configure packet structures, ports, and data handling.<br />**Must be called before starting telemetry.**                                                          |
| .updateLocalIP()   | `ip` (str): e.g., `"192.168.1.100"`, `"127.0.0.1"`                                                                                                                                                   | Set the local IP address that the telemetry server listens on for incoming packets.                                                                                                                      |
| .updateSendIP()    | `ip` (str): e.g., `"192.168.1.100"`, `"127.0.0.1"`                                                                                                                                                   | Set the destination IP address for sending heartbeats and handshake packets.                                                                                                                             |
| .addWorkerThread() | `mainFunc` (callable): A function with the signature: <br />``def worker_function(worker_id: int, ro_storage, stop_event):``                                                                             | Register a worker thread function to process telemetry data concurrently. Worker threads receive read-only snapshots of the data, ensuring thread safety.                                                |
| .manualStop()      | `target` (bool): `True` to stop                                                                                                                                                                       | Manually trigger a stop signal from outside the main thread or telemetryloop.                                                                                                                            |
| .isSharedMemory()  | `target` (bool): <br />- `True` to use shared memory, <br />- `False` to use UDP                                                                                                                   | Toggle between UDP and shared memory as the telemetry data source. Shared memory is faster but only available on the local machine.                                                                      |
| .setEnumMode()     | `target` (int): Enum handling mode: <br />- `0` (default): Return full enum members with both name and value, <br />- `1`: Return raw integer values, <br />- `2`: Return enum names as strings | Configure how enum fields are handled in packet data. Affects what values are returned for fields with enum types.                                                                                       |
| .GetTelemetry()    | None                                                                                                                                                                                                       | Retrieve telemetry packets one at a time in a generator pattern. Use this for**single-threaded** applications                                                                                      |
| .StartTelemetry()  | None                                                                                                                                                                                                       | Start the telemetry system with all configured settings. Creates and starts the network listener thread and all worker threads.**Blocks until a stop signal is received** (Ctrl+C or manual stop). |

## Adding and Using a New Packet Structure

### Step 1: Create the Packet Structure File

Example structure:

```python
from enum import Enum
# Swap depending on what data types you want to use
import ctypes 

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
  
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
  
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
  
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char

# Define your header packet, if required
class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16),
        ("m_gameYear",                  DataTypes.UNSIGNED_INT8),
        # ...
    ]

# Define any sub-packet
class CarMotionData(DataTypes.STRUCTURE):
    # _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT),
        ("m_worldVelocityX",        DataTypes.FLOAT),
        # ...
    ]

# Define a main packet
class PacketMotionData(DataTypes.STRUCTURE):
    _pack_ = 1 # This may be required depening on the game
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),    # Data for all cars on track
    ]
```

### Step 2: Setup Enums (Optional)

Create enum classes for any fields that have a defined set of values.

```python
from enum import Enum, IntEnum, StrEnum, Flag

# Create an enum
class Gear(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2

class Gear(IntEnum):
    NEUTRAL = "N"
    FIRST = "ONE"
    SECOND = "TWO"

class Gear(Flag):
    NEUTRAL = 1
    FIRST = 2
    SECOND = 4
    SECOND = 8

class TelemetryData(DataTypes.STRUCTURE):
    # Setup enums, field pairing as a dictionary for dynamic ingestion
    _enums_: dict[type, tuple[str, ...]] = {
        SESSION_TYPE: ("session",),
        GEAR: ("current_gear", "recommended_gear",),
    }
    _fields_ = [
        ("speed",               DataTypes.UNSIGNED_INT8),
        ("current_gear",        DataTypes.UNSIGNED_INT8),
        ("recommended_gear",    DataTypes.UNSIGNED_INT8),
        # ...
    ]
```

Before starting the telemetry, set the enum mode in your main script:

```python
activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displayTime)

# Default is mode 0 (no special handling). Returns all enums members (<AC_STATUS.AC_PAUSE: 3>).
activeThreads.setEnumMode(0)

# Mode 1: Leave fields as raw values. Returns enum values / raw values (3).
activeThreads.setEnumMode(1)

# Mode 2: Convert fields to their enum type. Returns enum name ('AC_PAUSE').
activeThreads.setEnumMode(2)

activeThreads.StartTelemetry()
```

### Step 3: Setup MetaData

In your main script, import the new metadata:

| Syntax            | Type                       | Description                                                                                        |
| ----------------- | -------------------------- | -------------------------------------------------------------------------------------------------- |
| port              | Integer                    | UDP port data is received on                                                                       |
| heartBeatPort     | Integer                    | UDP port to send a heart beat to                                                                   |
| heartBeatFunc     | Function                   | Heart beat function                                                                                |
| handShakePort     | Integer                    | UDP port to send a hand shake to                                                                   |
| handShakeFunc     | Tuple [Function, Function] | Tuple containing start and stop hand shake functions                                               |
| decrytionFunc     | Function                   | Data decryption function                                                                           |
| headerInfo        | Type                       | The header struct class (if protocol uses header).                                                 |
| packetIDAttribute | String                     | An attribute in the header packet defining the packet ID                                           |
| sharedMemoryName  | String or Dict[Str, Str]   | Name of shared memory segment or a dictionary, with the key as packet name and value as SM segment |
| packetInfo        | Dict [Int, List [Type] ]   | Game packet mapping - See more below                                                               |

#### PacketInfo

A Dictionary containing

- key: Packet ID or 0 if no ID
- value: Tuple of packetStructClass variants.

#### PacketInfo - Standard

```python
packetInfo = {
    0: (PacketMotionData,),
    1: (PacketSessionData,),
    # ...
}
```

#### PacketInfo - PacketID with multiple packets

```python
packetInfo = {
    0: (TelemetryData,),
    7: (TimeStatsData,),
    8: (VehicleClassNamesData, ParticipantVehicleNamesData),
    # ...
}
```

#### PacketInfo - No PacketID

```python
packetInfo = {
    0: (PacketAData, PacketBData, PacketTildaData, PacketCData),
    # ...
}
```

#### Full MetaData Example

```python
# MetaData class with packet information
class MetaData:
    # standard network info
    port: int| None = 20777  # UDP port for your game

    # use if a heartbeat is needed
    heartBeatPort: int | None = 33739
    heartBeatFunc = heartBeat

    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None # tuple (startHandShakeFunc, stopHandShakeFunc)

    # use if the data needs decrypting
    decrytionFunc = decrypt_data

    # use if there is a header packet
    headerInfo: type | None = PacketHeader  # Header type
    packetIDAttribute: str = "m_packetId"  # Attribute name for packet ID
  
    # use for shared memory
    sharedMemoryName: str | None | dict[str, str] = "Local\\SCSTelemetry" # Names of the shared memory segment

    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (PacketMotionData,),  # Packet ID: (packet_class,)
        # Add more packet types as needed
    }
```

### Step 4: Import and Use

In your main script, import the new metadata and use it with either mode:

```python
from RaceTelemetry import telemetryManager

from your_game_struct import MetaData

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

### Step 5: Handle Packet Decoding

The system automatically handles packet decoding based on the `packetInfo` dictionary. Ensure:

- Packet sizes match exactly (use `_pack_ = 1` for correct alignment)
- Packet IDs correspond to the correct packet types
- All nested structures are properly defined

## Supported Games

### UDP

- Assetto Corsa
- BeamNG Drive
- Dirt 4 (untested)
- Dirt Rally (untested)
- F1 2016 (untested)
- F1 2017
- F1 2018
- F1 2019
- F1 2020
- F1 2021
- F1 2022
- F1 2023
- F1 2024
- F1 2025 (untested)
- F1 2026 (2025 dlc) (untested)
- Forza Horizon 4
- Forza Horizon 5
- Forza Horizon 6
- Forza Motorsport 7 (untested)
- Forza Motorsport 8
- Gran Turismo 7
- Project Cars
- Project Cars 2

### Shared Memory

- Assetto Corsa
- Assetto Corsa Competizione (untested)
- Assetto Corsa Evo (untested)
- Euro Truck Simulator 2
- Project Cars (untested)

## Troubleshooting

- Check that the game is configured to send telemetry data
- Check no other running game uses the same port (on xbox, if a game is in quick resume state, it may block access to a port. EG; forza horizon 5 and motorsport 8)
- Verify IP addresses are correctly configured for network communication
- Use packet capture tools to verify data transmission (wireshark, and filter based on UDP, port, incoming and source IP)
- Ensure firewall allows UDP traffic on the configured port

## Game Specific Notes

- For Microsoft Store versions of Forza games, ensure loopback is configured correctly
- Euro Truck Simulator 2 requires a 'scs-sdk-plugin' to be installed in the plugins folder
