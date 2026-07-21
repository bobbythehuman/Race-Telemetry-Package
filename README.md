# Race-Telemetry-Package

**A single Python package for reading real-time telemetry from a wide range of racing and driving simulation games.**

Racing sims each expose telemetry (speed, tyre temps, lap times, car position, and more) through their own UDP or shared-memory format, and every one of those formats is slightly different. Race-Telemetry-Package gives you one consistent interface for all of them, so you can build dashboards, overlays, data loggers, or motion-rig controllers without writing a separate decoder for every title.

- **One API, many games** — Assetto Corsa, BeamNG.drive, the F1 series (2016–2026), the Forza series, Gran Turismo, Project CARS 2, and more.
- **UDP and shared memory support**, depending on what each game offers.
- **Single-threaded or multi-threaded operation**, so it fits both quick scripts and always-on applications.
- **Extensible** — add support for a new game by defining its packet structure; no changes to the core package required.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Features](#features)
- [How It Works](#how-it-works)
- [Usage](#usage)
  - [Single-Threaded Mode](#single-threaded-mode)
  - [Multi-Threaded Mode](#multi-threaded-mode)
- [API Reference](#api-reference)
- [Adding Support for a New Game](#adding-support-for-a-new-game)
- [Supported Games](#supported-games)
- [Troubleshooting](#troubleshooting)
- [Game-Specific Notes](#game-specific-notes)
- [Documentation &amp; Reference Links](#documentation--reference-links)
- [Contributing](#contributing)
- [Licence](#licence)

---

## Quick Start

```shell
pip install RaceTelemetry
```

```python
from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData

# Create the manager and tell it which game protocol to expect
telemetry = telemetryManager()
telemetry.updateMeta(MetaData)

# Start pulling packets — this blocks until data arrives
for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    if packetID == 6:
        print("Received a car telemetry packet")
```

That's the whole setup for basic, single-threaded use. See [Usage](#usage) below for the multi-threaded version, and [Supported Games](#supported-games) for the full list of protocols and structure modules available.

## Installation

### Prerequisites

- Python 3.8 or later
- The telemetry-sending device (console or PC running the game) must be reachable on the network — either the same machine (loopback) or the same local network
- The game must be configured to send telemetry to the correct IP and port (UDP), or to write to shared memory, depending on the title

### Install from PyPI

```shell
pip install RaceTelemetry
```

## Features

- Single package covering multiple racing game telemetry protocols
- Single-threaded and multi-threaded operating modes
- Extensible packet structure system for adding new games without touching the core library
- Real-time UDP or shared-memory reception and decoding
- Thread-safe data storage for concurrent access from multiple worker threads

## How It Works

In multi-threaded mode, the package runs three kinds of thread:

| Thread                            | Responsibility                                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Main thread**             | Creates and manages the telemetry system, starts worker threads, and waits for a stop signal                                                |
| **Network listener thread** | Continuously receives UDP or shared-memory packets, decodes them using the game's protocol, and stores the latest data in`CentralStorage` |
| **Worker thread(s)**        | Your own code, which reads telemetry via read-only snapshots — you never touch`CentralStorage` directly                                  |

Data lives in `CentralStorage`, which is protected by thread-safe locking. Worker threads never get direct access to it; instead they receive a `ReadOnlyStorage` interface that only allows taking **immutable snapshots**. This means you get thread safety for free, without managing any locks yourself.

## Usage

### Single-Threaded Mode

A simple, blocking function that listens for packets and returns decoded telemetry as they arrive. Best for scripts and simple applications that don't need background processing.

Defined in [`main.py`](src/RaceTelemetry/main.py) as `telemetryManager.GetTelemetry()`:

- Blocks until a packet is received
- No threading overhead — the simplest way to get started

More examples: [`tests/Game_Specific`](tests/Game_Specific)

```python
from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData

# Initialise the manager
telemetry = telemetryManager()

# Tell it which game's protocol to use
telemetry.updateMeta(MetaData)

# Start receiving telemetry
for packet, packetID, headerPacket in telemetry.GetTelemetry():
    if not packet:
        continue

    # Check by packet ID, if the protocol provides one
    if packetID == 6:
        pass  # Process data here

    # Or check by packet name
    packetName = packet.__name__
    if packetName == 'PacketCarTelemetryData':
        pass  # Process data here
```

### Multi-Threaded Mode

Runs a full telemetry server with a dedicated network listener thread plus any number of worker threads, so you can process data continuously without blocking on network I/O. Best for dashboards, overlays, and long-running applications.

Defined in [`main.py`](src/RaceTelemetry/main.py) as `telemetryManager.StartTelemetry()`:

- Starts a network listener thread that continuously receives data
- Provides a thread-safe central store (`CentralStorage`)
- Lets multiple worker threads process data concurrently via read-only access

More examples: [`tests/Game_Specific`](tests/Game_Specific)

```python
from RaceTelemetry import telemetryManager
from RaceTelemetry.data_structures.F1_2024_struct import MetaData

# Define a worker thread function
def my_worker_thread(worker_id: int, ro_storage, stop_event):
    while not stop_event.is_set():
        snapshot = ro_storage.snapshot()

        # Access telemetry data
        data = snapshot.get("latestData")
        if data:
            telemetry = data.get("PacketCarTelemetryData")
            if telemetry:
                pass  # Process data here

# Initialise the manager
activeThreads = telemetryManager()

# Tell it which game's protocol to use
activeThreads.updateMeta(MetaData)

# Register one or more worker threads
activeThreads.addWorkerThread(my_worker_thread)

# Start the telemetry system — blocks until stopped
activeThreads.StartTelemetry()
```

## API Reference

| Method                 | Parameters                                                                                                                                             | Description                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `telemetryManager()` | None                                                                                                                                                   | Creates a new telemetry manager instance, which handles network communication, data storage, and threading.                                                                                               |
| `.updateMeta()`      | `MetaData` (class) — see [Adding Support for a New Game](#adding-support-for-a-new-game)                                                             | Applies game-specific metadata to configure packet structures, ports, and data handling.**Must be called before starting telemetry.**                                                               |
| `.updateLocalIP()`   | `ip` (str), e.g. `"192.168.1.100"`, `"127.0.0.1"`                                                                                                | Sets the local IP address the telemetry server listens on for incoming packets.                                                                                                                           |
| `.updateSendIP()`    | `ip` (str), e.g. `"192.168.1.100"`, `"127.0.0.1"`                                                                                                | Sets the destination IP address used for heartbeats and handshake packets.                                                                                                                                |
| `.addWorkerThread()` | `mainFunc` (callable) with signature `def worker_function(worker_id: int, ro_storage, stop_event):`                                                | Registers a worker thread function to process telemetry data concurrently. Worker threads receive read-only snapshots, keeping access thread-safe.                                                        |
| `.manualStop()`      | `target` (bool) — `True` to stop                                                                                                                  | Manually triggers a stop signal from outside the main thread or telemetry loop.                                                                                                                           |
| `.isSharedMemory()`  | `target` (bool) — `True` for shared memory, `False` for UDP                                                                                     | Switches between UDP and shared memory as the data source. Shared memory is faster but only available on the local machine.                                                                               |
| `.setEnumMode()`     | `target` (int): `0` (default) returns full enum members with name and value; `1` returns raw integer values; `2` returns enum names as strings | Configures how enum fields are represented in decoded packet data.                                                                                                                                        |
| `.GetTelemetry()`    | None                                                                                                                                                   | Yields telemetry packets one at a time, for**single-threaded** use.                                                                                                                                 |
| `.StartTelemetry()`  | None                                                                                                                                                   | Starts the telemetry system with all configured settings, creating the network listener and any registered worker threads.**Blocks until a stop signal is received** (Ctrl+C or `.manualStop()`). |

## Adding Support for a New Game

Support for a new game is added by defining its packet structure — no changes to the core package are needed.

### Step 1: Define the Packet Structure

```python
from enum import Enum
# Swap depending on the data types the game's protocol uses
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

# Define a header packet, if the protocol uses one
class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1  # May be required depending on the game
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16),
        ("m_gameYear",                  DataTypes.UNSIGNED_INT8),
        # ...
    ]

# Define any sub-packets
class CarMotionData(DataTypes.STRUCTURE):
    # _pack_ = 1  # May be required depending on the game
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT),
        ("m_worldVelocityX",        DataTypes.FLOAT),
        # ...
    ]

# Define a main packet
class PacketMotionData(DataTypes.STRUCTURE):
    _pack_ = 1  # May be required depending on the game
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 22),     # Data for all cars on track
    ]
```

### Step 2: Set Up Enums (Optional)

Create enum classes for any fields that have a defined set of values.

```python
from enum import Enum, IntEnum, StrEnum, Flag

class SessionType(IntEnum):
    UNKNOWN = 0
    PRACTICE = 1
    QUALIFYING = 2
    RACE = 3

class Gear(IntEnum):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2

class TelemetryData(DataTypes.STRUCTURE):
    # Map each enum type to the field names it applies to
    _enums_: dict[type, tuple[str, ...]] = {
        SessionType: ("session",),
        Gear: ("current_gear", "recommended_gear"),
    }
    _fields_ = [
        ("speed",               DataTypes.UNSIGNED_INT8),
        ("current_gear",        DataTypes.UNSIGNED_INT8),
        ("recommended_gear",    DataTypes.UNSIGNED_INT8),
        # ...
    ]
```

Before starting telemetry, choose how enum fields should be returned:

```python
activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)
activeThreads.addWorkerThread(displayTime)

# Mode 0 (default): return full enum members, e.g. <AC_STATUS.AC_PAUSE: 3>
activeThreads.setEnumMode(0)

# Mode 1: return raw values, e.g. 3
activeThreads.setEnumMode(1)

# Mode 2: return the enum name as a string, e.g. 'AC_PAUSE'
activeThreads.setEnumMode(2)

activeThreads.StartTelemetry()
```

### Step 3: Define the MetaData Class

| Field                 | Type                            | Description                                                                            |
| --------------------- | ------------------------------- | -------------------------------------------------------------------------------------- |
| `port`              | `int`                         | UDP port the data is received on                                                       |
| `heartBeatPort`     | `int`                         | UDP port to send a heartbeat to                                                        |
| `heartBeatFunc`     | function                        | Heartbeat function                                                                     |
| `handShakePort`     | `int`                         | UDP port to send a handshake to                                                        |
| `handShakeFunc`     | `tuple[function, function]`   | Start and stop handshake functions                                                     |
| `decrytionFunc`     | function                        | Data decryption function                                                               |
| `headerInfo`        | type                            | The header struct class, if the protocol uses one                                      |
| `packetIDAttribute` | `str`                         | The header packet attribute that identifies the packet ID                              |
| `sharedMemoryName`  | `str` or `dict[str, str]`   | Name of the shared memory segment, or a dictionary mapping packet name to segment name |
| `packetInfo`        | `dict[int, tuple[type, ...]]` | Game packet mapping — see below                                                       |

#### PacketInfo

A dictionary where:

- **key** — the packet ID, or `0` if the protocol doesn't use one
- **value** — a tuple of packet structure class(es) associated with that ID

**Standard mapping:**

```python
packetInfo = {
    0: (PacketMotionData,),
    1: (PacketSessionData,),
    # ...
}
```

**One packet ID mapping to multiple packet types:**

```python
packetInfo = {
    0: (TelemetryData,),
    7: (TimeStatsData,),
    8: (VehicleClassNamesData, ParticipantVehicleNamesData),
    # ...
}
```

**Protocols with no packet ID:**

```python
packetInfo = {
    0: (PacketAData, PacketBData, PacketTildaData, PacketCData),
    # ...
}
```

#### Full MetaData Example

```python
class MetaData:
    # Standard network info
    port: int | None = 20777  # UDP port for your game

    # Only needed if the game expects a heartbeat
    heartBeatPort: int | None = 33739
    heartBeatFunc = heartBeat

    # Only needed for an initial handshake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None  # (startHandShakeFunc, stopHandShakeFunc)

    # Only needed if the data requires decryption
    decrytionFunc = decrypt_data

    # Only needed if the protocol uses a header packet
    headerInfo: type | None = PacketHeader
    packetIDAttribute: str = "m_packetId"

    # Only needed for shared memory
    sharedMemoryName: str | None | dict[str, str] = "Local\\SCSTelemetry"

    # Standard packet mapping
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (PacketMotionData,),  # Packet ID: (packet_class,)
        # Add more packet types as needed
    }
```

### Step 4: Import and Use It

```python
from RaceTelemetry import telemetryManager
from your_game_struct import MetaData

# Setup, works for both modes
activeThreads = telemetryManager()
activeThreads.updateMeta(MetaData)

# Single-threaded use
for packet, packetID, headerPacket in activeThreads.GetTelemetry():
    if not packet:
        continue

# Or multi-threaded use
activeThreads.addWorkerThread(your_worker_function)
activeThreads.StartTelemetry()
```

### Step 5: Check Packet Decoding

Decoding is driven entirely by the `packetInfo` dictionary you defined. If packets aren't decoding correctly, check:

- Packet sizes match the protocol spec exactly (use `_pack_ = 1` for correct byte alignment)
- Packet IDs correspond to the correct packet types
- All nested structures are fully and correctly defined

## Supported Games

### UDP

| Game               | Status        |
| ------------------ | ------------- |
| Assetto Corsa      | ✅            |
| BeamNG.drive       | ✅            |
| Dirt 4             | ⚠️ Untested |
| Dirt Rally         | ⚠️ Untested |
| F1 2016            | ⚠️ Untested |
| F1 2017            | ✅            |
| F1 2018            | ✅            |
| F1 2019            | ✅            |
| F1 2020            | ✅            |
| F1 2021            | ✅            |
| F1 2022            | ✅            |
| F1 2023            | ✅            |
| F1 2024            | ✅            |
| F1 2025            | ⚠️ Untested |
| F1 2026 (2025 DLC) | ⚠️ Untested |
| Forza Horizon 4    | ✅            |
| Forza Horizon 5    | ✅            |
| Forza Horizon 6    | ✅            |
| Forza Motorsport 7 | ⚠️ Untested |
| Forza Motorsport 8 | ✅            |
| Gran Turismo 7     | ✅            |
| Project CARS       | ✅            |
| Project CARS 2     | ✅            |

### Shared Memory

| Game                       | Status        |
| -------------------------- | ------------- |
| Assetto Corsa              | ✅            |
| Assetto Corsa Competizione | ⚠️ Untested |
| Assetto Corsa EVO          | ⚠️ Untested |
| Euro Truck Simulator 2     | ✅            |
| Project CARS               | ⚠️ Untested |

Don't see your game listed? See [Adding Support for a New Game](#adding-support-for-a-new-game) — contributions of new packet structures are welcome.

## Troubleshooting

- **No data arriving?** Check that the game is actually configured to send telemetry, and that no other running game is using the same port. On Xbox, a game left in Quick Resume can hold onto a port (this has been seen with Forza Horizon 5 and Forza Motorsport 8).
- **Wrong IP?** Double-check the local and destination IP addresses configured on both the game and in your script.
- **Still nothing?** Use a packet capture tool such as Wireshark, filtering on UDP, the relevant port, and the incoming/source IP, to confirm data is actually reaching your machine.
- **Firewall blocking traffic?** Make sure your firewall allows inbound UDP traffic on the configured port.

## Game-Specific Notes

- **Forza (Microsoft Store versions):** loopback needs to be configured correctly — see [`forza debug.txt`](<./Supporting_Docs/forza%20debug.txt>) in the supporting docs.
- **Euro Truck Simulator 2:** requires the `scs-sdk-plugin` to be installed in the game's plugins folder — see the supporting docs for details.

## Documentation & Reference Links

### Official Documents

| Document                                                                                                                    | Covers                                                       |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [ACSharedMemoryDocumentation.pdf](./Supporting_Docs/ACSharedMemoryDocumentation.pdf)                                         | Assetto Corsa shared memory (official)                       |
| [ACRemoteTelemetryDocumentation.pdf](./Supporting_Docs/ACRemoteTelemetryDocumentation.pdf)                                   | Assetto Corsa UDP remote telemetry (official)                |
| [ACCSharedMemoryDocumentationV1.8.12.pdf](./Supporting_Docs/ACCSharedMemoryDocumentationV1.8.12.pdf)                         | Assetto Corsa Competizione shared memory, v1.8.12 (official) |
| [ACE_SharedFileOut_Documentation_V1.pdf](./Supporting_Docs/ACE_SharedFileOut_Documentation_v1.pdf)                           | Assetto Corsa EVO shared memory, v1 (official)               |
| [Data Output from F1 22 v16.docx](<./Supporting_Docs/Data%20Output%20from%20F1%2022%20v16.docx>)                             | F1 2022 packet structures, v16 (official)                    |
| [Data Output from F1 23 v29x3.docx](<./Supporting_Docs/Data%20Output%20from%20F1%2023%20v29x3.docx>)                         | F1 2023 packet structures, v29x3 (official)                  |
| [Data Output from F1 24 v27.2x.docx](<./Supporting_Docs/Data%20Output%20from%20F1%2024%20v27.2x.docx>)                       | F1 2024 packet structures, v27.2x (official)                 |
| [Data Output from F1 25 v3.pdf](<./Supporting_Docs/Data%20Output%20from%20F1%2025%20v3.pdf>)                                 | F1 2025 packet structures, v3 (official)                     |
| [Data Output from F1 25 2026 Season Pack.pdf](<./Supporting_Docs/Data%20Output%20from%20F1%2025%202026%20Season%20Pack.pdf>) | F1 2026 packet structures (official)                         |

More debugging guides live in [`Supporting_Docs/`](./Supporting_Docs/), including [`forza debug.txt`](<./Supporting_Docs/forza%20debug.txt>) for Forza loopback setup.

### Community & Protocol Links

| Game                          | Link                                                                                                                                                                                                                                                                                                                   | Notes                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| Assetto Corsa (UDP)           | [AC Remote Telemetry Documentation](https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub)                                                                                                                                                                                                | Official Link                       |
| Assetto Corsa (UDP)           | [AC UDP Remote Telemetry](https://www.assettocorsa.net/forum/index.php?threads/ac-udp-remote-telemetry-update-31-03-2016.222/)                                                                                                                                                                                          | PDF Download                        |
| Assetto Corsa (shared memory) | [Shared Memory Reference](https://www.assettocorsa.net/forum/index.php?threads/shared-memory-reference-25-05-2017.3352/)                                                                                                                                                                                                |                                     |
| Assetto Corsa Competizione    | [ACC Shared Memory Documentation](https://www.assettocorsa.net/forum/index.php?threads/acc-shared-memory-documentation.59965/)                                                                                                                                                                                          |                                     |
| Assetto Corsa EVO             | [Shared Memory API Documentation](https://www.assettocorsa.net/forum/index.php?threads/shared-memory-api-documentation.83659/)                                                                                                                                                                                          |                                     |
| Assetto Corsa EVO             | [ACE_SharedFileOut_Documentation_v1](https://docs.google.com/document/d/1WzqMLkW2o_C0LGcvdMRelAV31ZIifux0CSHD9k6ddz0/edit?tab=t.0)                                                                                                                                                                                      |                                     |
| BeamNG.drive                  | [Protocols](https://documentation.beamng.com/modding/protocols/)                                                                                                                                                                                                                                                        | Official Link                       |
| Dirt 4                        | [Setting up UDP output](https://web.archive.org/web/20181117092858/http://forums.codemasters.com/discussion/52950/setting-up-udp-output-for-dirt-4)                                                                                                                                                                     |                                     |
| Dirt 4                        | [Configuring UDP Output](https://www.scribd.com/document/350826037/UDP-output-setup)                                                                                                                                                                                                                                    |                                     |
| Dirt Rally                    | [UDP Telemetry](https://docs.google.com/spreadsheets/d/1UTgeE7vbnGIzDz-URRk2eBIPc_LR1vWcZklp7xD9N0Y/edit?gid=0#gid=0)                                                                                                                                                                                                   |                                     |
| Euro Truck Simulator 2        | [scs-sdk-plugin on GitHub](https://github.com/truckermudgeon/scs-sdk-plugin)                                                                                                                                                                                                                                            | Including installation instructions |
| F1 2016                       | [D-Box and UDP Telemetry Information](https://web.archive.org/web/20180302011401/http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information)                                                                                                                                                    |                                     |
| F1 2017                       | [D-Box and UDP Output Specification](https://web.archive.org/web/20230208144303/https://forums.codemasters.com/topic/20215-f1-2017-d-box-and-udp-output-specification/)                                                                                                                                                 |                                     |
| F1 2018                       | [UDP Specification](https://web.archive.org/web/20230208110311/https://forums.codemasters.com/topic/30601-f1-2018-udp-specification/)                                                                                                                                                                                   |                                     |
| F1 2019                       | [UDP Specification](https://web.archive.org/web/20220930165800/https://forums.codemasters.com/topic/44592-f1-2019-udp-specification/)                                                                                                                                                                                   |                                     |
| F1 2020                       | [UDP Specification](https://web.archive.org/web/20221127112921/https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/)                                                                                                                                                                                   |                                     |
| F1 2021                       | [UDP Specification](https://web.archive.org/web/20220525102004/https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/)                                                                                                                                                                                   | Dead download link                  |
| F1 2021                       | [raweceek-telemetry/f1-2021-udp](https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#data-output-from-f1-2021)                                                                                                                                                                                         |                                     |
| F1 2022                       | [UDP Specification](https://forums.ea.com/discussions/f1-games-franchise-discussion-en/f1-22-udp-specification/8418392)                                                                                                                                                                                                 | Official Link                       |
| F1 2023                       | [UDP Specification](https://forums.ea.com/discussions/f1-23-en/f1-23-udp-specification/8390745)                                                                                                                                                                                                                         | Official Link                       |
| F1 2024                       | [UDP Specification](https://forums.ea.com/discussions/f1-24-general-discussion-en/f1-24-udp-specification/8369125)                                                                                                                                                                                                      | Official Link                       |
| F1 2025 / F1 2026             | [2026 Season Pack UDP Specification](https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-2026-season-pack-udp-specification/12187347)                                                                                                                                                    | Official Link                       |
| Forza Horizon 4               | [Forza-data-tools on GitHub](https://github.com/richstokes/Forza-data-tools/blob/master/FH4_packetformat.dat)                                                                                                                                                                                                           |                                     |
| Forza Horizon 5               | [Data Out format](https://pastebin.com/GFbbzbg3)                                                                                                                                                                                                                                                                        | Pastebin Link                       |
| Forza Horizon 6               | [Data Out Documentation](https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation)                                                                                                                                                                                             | Official Link                       |
| Forza Motorsport 7            | [Data Out feature details](https://web.archive.org/web/20211203164310/https://forums.forzamotorsport.net/turn10_postst128499_Forza-Motorsport-7--Data-Out--feature-details.aspx)                                                                                                                                        |                                     |
| Forza Motorsport 8            | [Data Out Documentation](https://web.archive.org/web/20260515015144/https://forums.forza.net/t/data-out-feature-in-forza-motorsport/651333)                                                                                                                                                                             | Structure and Car ID                |
| Forza Motorsport 8            | [Data Out Documentation](https://support.forza.net/hc/en-us/articles/21742934024211-Forza-Motorsport-Data-Out-Documentation) - [Data Out Documentation Archive](https://web.archive.org/web/20260303125422/https://support.forzamotorsport.net/hc/en-us/articles/21742934024211-Forza-Motorsport-Data-Out-Documentation) | Just output structure               |
| Gran Turismo 7                | [gt7-udp on GitHub](https://github.com/MacManley/gt7-udp)                                                                                                                                                                                                                                                               |                                     |
| Project CARS (UDP)            | [Companion App UDP Streaming](https://web.archive.org/web/20200224094755/http://forum.projectcarsgame.com/showthread.php?40113-COMPLETE-Companion-app-UDP-streaming)                                                                                                                                                    |                                     |
| Project CARS (shared memory)  | [Shared Memory API discussion](https://web.archive.org/web/20210729083910/https://forum.projectcarsgame.com/showthread.php?30903-Project-CARS-Shared-Memory-or-how-do-I-make-my-own-app&p=984616&viewfull=1#post984616)                                                                                                 |                                     |
| Project CARS 2                | [project-cars-2-udp on GitHub](https://github.com/MacManley/project-cars-2-udp)                                                                                                                                                                                                                                         |                                     |

<!-- - Assetto Corsa (UDP) — [AC Remote Telemetry Documentation](https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub) (official), [AC UDP Remote Telemetry](https://www.assettocorsa.net/forum/index.php?threads/ac-udp-remote-telemetry-update-31-03-2016.222/) (PDF download) -->

<!-- - Assetto Corsa (shared memory) — [Shared Memory Reference](https://www.assettocorsa.net/forum/index.php?threads/shared-memory-reference-25-05-2017.3352/) -->

<!-- - Assetto Corsa Competizione — [ACC Shared Memory Documentation](https://www.assettocorsa.net/forum/index.php?threads/acc-shared-memory-documentation.59965/) -->

<!-- - Assetto Corsa EVO — [Shared Memory API Documentation](https://www.assettocorsa.net/forum/index.php?threads/shared-memory-api-documentation.83659/) -->

<!-- - BeamNG.drive — [Protocols](https://documentation.beamng.com/modding/protocols/) (official) -->

<!-- - Dirt 4 — [Configuring UDP Output](https://www.scribd.com/document/350826037/UDP-output-setup), [Setting up UDP output](https://web.archive.org/web/20181117092858/http://forums.codemasters.com/discussion/52950/setting-up-udp-output-for-dirt-4) -->

<!-- - Dirt Rally — [UDP Telemetry](https://docs.google.com/spreadsheets/d/1UTgeE7vbnGIzDz-URRk2eBIPc_LR1vWcZklp7xD9N0Y/edit?gid=0#gid=0) -->

<!-- - Euro Truck Simulator 2 — [scs-sdk-plugin on GitHub](https://github.com/truckermudgeon/scs-sdk-plugin), including installation instructions -->

<!-- - F1 2016 — [D-Box and UDP Telemetry Information](https://web.archive.org/web/20180302011401/http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information) (web archive) -->

<!-- - F1 2017 — [D-Box and UDP Output Specification](https://web.archive.org/web/20230208144303/https://forums.codemasters.com/topic/20215-f1-2017-d-box-and-udp-output-specification/) (web archive) -->

<!-- - F1 2018 — [UDP Specification](https://web.archive.org/web/20230208110311/https://forums.codemasters.com/topic/30601-f1-2018-udp-specification/) (web archive) -->

<!-- - F1 2019 — [UDP Specification](https://web.archive.org/web/20220930165800/https://forums.codemasters.com/topic/44592-f1-2019-udp-specification/) (web archive) -->

<!-- - F1 2020 — [UDP Specification](https://web.archive.org/web/20221127112921/https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/) (web archive) -->

<!-- - F1 2021 — [UDP Specification](https://web.archive.org/web/20220525102004/https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/) (web archive, dead download link), [alternative reference](https://github.com/raweceek-temeletry/f1-2021-udp?tab=readme-ov-file#data-output-from-f1-2021) -->

<!-- - F1 2022 — [UDP Specification](https://forums.ea.com/discussions/f1-games-franchise-discussion-en/f1-22-udp-specification/8418392) -->

<!-- - F1 2023 — [UDP Specification](https://forums.ea.com/discussions/f1-23-en/f1-23-udp-specification/8390745) -->

<!-- - F1 2024 — [UDP Specification](https://forums.ea.com/discussions/f1-24-general-discussion-en/f1-24-udp-specification/8369125) -->

<!-- - F1 2025 / F1 2026 — [2026 Season Pack UDP Specification](https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-2026-season-pack-udp-specification/12187347) -->

<!-- - Forza Horizon 4 — [Forza-data-tools on GitHub](https://github.com/richstokes/Forza-data-tools/blob/master/FH4_packetformat.dat) -->

<!-- - Forza Horizon 5 — [Data Out format](https://pastebin.com/GFbbzbg3) (Pastebin) -->

<!-- - Forza Horizon 6 — [Data Out Documentation](https://support.forza.net/hc/en-us/articles/51744149102611-Forza-Horizon-6-Data-Out-Documentation) -->

<!-- - Forza Motorsport 7 — [Data Out feature details](https://forums.forza.net/t/forza-motorsport-7-data-out-feature-details/74013) -->

<!-- - Forza Motorsport 8 — [Data Out feature](https://forums.forza.net/t/data-out-feature-in-forza-motorsport/651333/2) -->

<!-- - Gran Turismo 7 — [gt7-udp on GitHub](https://github.com/MacManley/gt7-udp) -->

<!-- - Project CARS (UDP) — [Companion App UDP Streaming](https://web.archive.org/web/20200224094755/http://forum.projectcarsgame.com/showthread.php?40113-COMPLETE-Companion-app-UDP-streaming) -->

<!-- - Project CARS (shared memory) — [Shared Memory API discussion](https://web.archive.org/web/20210729083910/https://forum.projectcarsgame.com/showthread.php?30903-Project-CARS-Shared-Memory-or-how-do-I-make-my-own-app&p=984616&viewfull=1#post984616) -->

<!-- - Project CARS 2 — [project-cars-2-udp on GitHub](https://github.com/MacManley/project-cars-2-udp) -->

### Other Titles

| Game                | Link                                                                                                                                                            | Notes                                                 |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| EA Sports WRC 2023  | [How to use UDP on PC](https://forums.ea.com/discussions/wrc-general-discussion-en/ea-sports%E2%84%A2-wrc---how-to-use-user-datagram-protocol-udp-on-pc/8365068) |                                                       |
| Le Mans Ultimate    | [Telemetry Socket – JSON Telemetry Plugin](https://community.lemansultimate.com/index.php?threads/telemetry-socket-%E2%80%93-json-telemetry-plugin.8229/)       |                                                       |
| RaceRoom            | [Shared Memory API](https://forum.kw-studios.com/index.php?threads/shared-memory-api.1525/)                                                                      |                                                       |
| iRacing             | [pyirsdk on GitHub](https://github.com/kutu/pyirsdk)                                                                                                             | currently unsupported due to dynamic packet structure |
| Richard Burns Rally | [rbr-udp-telem on GitHub](https://github.com/groybe/rbr-udp-telem)                                                                                               |                                                       |
| KartKraft           | [kartkraft-telemetry schema on GitHub](https://github.com/motorsportgames/kartkraft-telemetry/blob/master/Schema/Frame.fbs)                                      |                                                       |
| Project CARS 3      | likely shares a protocol with Project CARS 2, not yet confirmed                                                                                                 |                                                       |

<!-- - EA Sports WRC 2023 — [How to use UDP on PC](https://forums.ea.com/discussions/wrc-general-discussion-en/ea-sports%E2%84%A2-wrc---how-to-use-user-datagram-protocol-udp-on-pc/8365068) -->

<!-- - Le Mans Ultimate — [Telemetry Socket – JSON Telemetry Plugin](https://community.lemansultimate.com/index.php?threads/telemetry-socket-%E2%80%93-json-telemetry-plugin.8229/) -->

<!-- - RaceRoom — [Shared Memory API](https://forum.kw-studios.com/index.php?threads/shared-memory-api.1525/) -->

<!-- - iRacing — [pyirsdk on GitHub](https://github.com/kutu/pyirsdk) — currently unsupported here due to iRacing's dynamic packet structure -->

<!-- - Richard Burns Rally — [rbr-udp-telem on GitHub](https://github.com/groybe/rbr-udp-telem) -->

<!-- - KartKraft — [kartkraft-telemetry schema on GitHub](https://github.com/motorsportgames/kartkraft-telemetry/blob/master/Schema/Frame.fbs) -->

<!-- - Project CARS 3 — likely shares a protocol with Project CARS 2, not yet confirmed -->

## Contributing

Contributions are welcome, whether that's a bug fix, a new packet structure for an unsupported game, or an improvement to these docs.

- **Found a bug?** Open an issue describing what you expected to happen, what actually happened, and which game/protocol you were using.
- **Want to add a game?** Follow the steps in [Adding Support for a New Game](#adding-support-for-a-new-game) and open a pull request — please include a short test under `tests/Game_Specific` if you can.
- **Improving sources?** PRs to this README or the files in `Supporting_Docs/` are welcome.
