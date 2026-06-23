import ctypes
from enum import Enum, StrEnum

# source
# https://github.com/MacManley/gt7-udp

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char


### * Enums
# There is a really long list for Car list

class SURFACE_TYPE(StrEnum):
    Curb_Kerb = "C"
    Dirt = "D"
    Grass = "G"
    Sand = "S"
    Snow = "s"
    Tarmac = "T"


### * Data Structure

### Packet A -- 296 bytes -- Frequency: 60Hz (60 times a second)

class PacketAData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8 * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32),  # This value may be overriden if using a car with more then 9 gears
    ]

### Packet B -- 316 bytes -- Frequency: 60Hz (60 times a second)

class PacketBData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8 * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32),  # This value may be overriden if using a car with more then 9 gears
        
        # For Packet B
        ("wheelRotation",   DataTypes.FLOAT),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT),  # Unknown float
        ("sway",            DataTypes.FLOAT),  # X axis acceleration
        ("heave",           DataTypes.FLOAT),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT),  # Z axis acceleration
        
    ]

### Packet ~ -- 344 bytes -- Frequency: 60Hz (60 times a second)

class PacketTildaData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8 * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32),  # This value may be overriden if using a car with more then 9 gears
        
        ("wheelRotation",   DataTypes.FLOAT),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT),  # Unknown float
        ("sway",            DataTypes.FLOAT),  # X axis acceleration
        ("heave",           DataTypes.FLOAT),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT),  # Z axis acceleration
        
        # For Packet Tilda
        ("throttleFiltered",    DataTypes.UNSIGNED_INT8),     # Filtered Throttle Output
        ("brakeFiltered",       DataTypes.UNSIGNED_INT8),     # Filtered Brake Output
        ("UNKNOWNUINT81",       DataTypes.UNSIGNED_INT8),     # Unknown unsigned 8 bit integer
        ("UNKNOWNUINT82",       DataTypes.UNSIGNED_INT8),     # Unknown unsigned 8 bit integer
        ("torqueVectors",       DataTypes.FLOAT * 4),         # Torque vectoring for certain cars - Positive = driving force - Negative = braking or regenerating
        ("energyRecovery",      DataTypes.FLOAT),             # Energy being recovered to the battery
        ("UNKNOWNFLOAT11",      DataTypes.FLOAT),             # Unknown float
    ]

### Packet C -- 368 bytes -- Frequency: 60Hz (60 times a second)

class PacketCData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _enums_: dict[type, tuple[str, ...]] = {
        SURFACE_TYPE: ("surfaceType",),
    }
    _fields_ = [
        ("magic",                       DataTypes.SIGNED_INT32),  # Magic, different value defines what game is being played
        ("position",                    DataTypes.FLOAT * 3),     # Position on Track in meters in each axis
        ("worldVelocity",               DataTypes.FLOAT * 3),     # Velocity in meters for each axis
        ("rotation",                    DataTypes.FLOAT * 3),     # Rotation (Pitch/Yaw/Roll) (RANGE: -1 -> 1)
        ("orientationRelativeToNorth",  DataTypes.FLOAT),         # Orientation to North (RANGE: 1.0 (North) -> 0.0 (South))
        ("angularVelocity",             DataTypes.FLOAT * 3),     # Speed at which the car turns around axis in rad/s (RANGE: -1 -> 1)
        ("bodyHeight",                  DataTypes.FLOAT),         # Body height
        ("EngineRPM",                   DataTypes.FLOAT),         # Engine revolutions per minute

        ("iv",              DataTypes.UNSIGNED_INT8 * 4),     # IV for Salsa20 encryption/decryption
        ("fuelLevel",       DataTypes.FLOAT),                 # Fuel level of car in liters 
        ("fuelCapacity",    DataTypes.FLOAT),                 # Max fuel capacity for current car (RANGE: 100 (most cars) -> 5 (karts) -> 0 (electric cars))  
        ("speed",           DataTypes.FLOAT),                 # Speed in m/s
        ("boost",           DataTypes.FLOAT),                 # Offset by +1 (EXAMPLE: 1.0 = 0 X 100kPa, 2.0 = 1 x 100kPa) # TODO apply -1 offset (from original source)
        ("oilPressure",     DataTypes.FLOAT),                 # Oil pressure in bars
        ("waterTemp",       DataTypes.FLOAT),                 # Constantly 85
        ("oilTemp",         DataTypes.FLOAT),                 # Constantly 110
        ("tyreTemp",        DataTypes.FLOAT * 4),             # Tyre temp for all 4 tires (FL -> FR -> RL -> RR)
        
        ("packetId",            DataTypes.SIGNED_INT32),  # ID of packet
        ("lapCount",            DataTypes.SIGNED_INT16),  # Lap count
        ("totalLaps",           DataTypes.SIGNED_INT16),  # Laps to finish
        ("bestLaptime",         DataTypes.SIGNED_INT32),  # Best lap time, defaults to -1 if not set
        ("lastLaptime",         DataTypes.SIGNED_INT32),  # Previous lap time, defaults to -1 if not set
        ("dayProgression",      DataTypes.SIGNED_INT32),  # Current time of day on track in ms
        ("RaceStartPosition",   DataTypes.SIGNED_INT16),  # Position of the car before the start of the race, defaults to -1 after race start
        ("preRaceNumCars",      DataTypes.SIGNED_INT16),  # Number of cars before the race start, defaults to -1 after start of the race
        ("minAlertRPM",         DataTypes.SIGNED_INT16),  # Minimum RPM that the rev limiter displays an alert
        ("maxAlertRPM",         DataTypes.SIGNED_INT16),  # Maximum RPM that the rev limiter displays an alert
        ("calcMaxSpeed",        DataTypes.SIGNED_INT16),  # Highest possible speed achievable of the current transmission settings
        
        ("flags",           DataTypes.SIGNED_INT16), # Packet flags # TODO: Get working (from original source)
        
        ("gears",       DataTypes.UNSIGNED_INT8), # First 4 bits: Current Gear, Last 4 bits: Suggested Gear, # TODO see getCurrentGearFromByte and getSuggestedGearFromByte
        ("throttle",    DataTypes.UNSIGNED_INT8), # Throttle (RANGE: 0 -> 255)
        ("brake",       DataTypes.UNSIGNED_INT8), # Brake (RANGE: 0 -> 255)
        ("PADDING",     DataTypes.UNSIGNED_INT8), # Padding byte # * might not be needed
        
        ("roadPlane",               DataTypes.FLOAT * 3),     # Banking of the road
        ("roadPlaneDistance",       DataTypes.FLOAT),         # Distance above or below the plane, e.g a dip in the road is negative, hill is positive.
        ("wheelRPS",                DataTypes.FLOAT * 4),     # Revolutions per second of tyres in rads
        ("tyreRadius",              DataTypes.FLOAT * 4),     # Radius of the tyre in meters
        ("suspHeight",              DataTypes.FLOAT * 4),     # Suspension height of the car
        ("UNKNOWNFLOATS",           DataTypes.FLOAT * 8),     # Unknown float (from original source)
        ("clutch",                  DataTypes.FLOAT),         # Clutch (RANGE: 0.0 -> 1.0)
        ("clutchEngagement",        DataTypes.FLOAT),         # Clutch Engangement (RANGE: 0.0 -> 1.0)
        ("RPMFromClutchToGearbox",  DataTypes.FLOAT),         # Pretty much same as engine RPM, is 0 when clutch is depressed
        ("transmissionTopSpeed",    DataTypes.FLOAT),         # Top speed as gear ratio value
        ("gearRatios",              DataTypes.FLOAT  * 8),    # Gear ratios of the car up to 8
        ("carCode",                 DataTypes.SIGNED_INT32),  # This value may be overriden if using a car with more then 9 gears
        
        ("wheelRotation",   DataTypes.FLOAT),  # Calculates the wheel rotation in radians
        ("UNKNOWNFLOAT10",  DataTypes.FLOAT),  # Unknown float
        ("sway",            DataTypes.FLOAT),  # X axis acceleration
        ("heave",           DataTypes.FLOAT),  # Y axis acceleration
        ("surge",           DataTypes.FLOAT),  # Z axis acceleration
        
        ("throttleFiltered",    DataTypes.UNSIGNED_INT8),     # Filtered Throttle Output
        ("brakeFiltered",       DataTypes.UNSIGNED_INT8),     # Filtered Brake Output
        ("UNKNOWNUINT81",       DataTypes.UNSIGNED_INT8),     # Unknown unsigned 8 bit integer
        ("UNKNOWNUINT82",       DataTypes.UNSIGNED_INT8),     # Unknown unsigned 8 bit integer
        ("torqueVectors",       DataTypes.FLOAT * 4),         # Torque vectoring for certain cars - Positive = driving force - Negative = braking or regenerating
        ("energyRecovery",      DataTypes.FLOAT),             # Energy being recovered to the battery
        ("UNKNOWNFLOAT11",      DataTypes.FLOAT),             # Unknown float
        
        # For Packet C
        ("surfaceType",     DataTypes.CHAR * 4),          # The kind of surface in contact with the tyres (T: tarmac, C: curb/kerb D: Dirt/Grass)
        ("currentLap",      DataTypes.SIGNED_INT32),      # The current lap being set in milliseconds
        ("UNKNOWNFLOATS",   DataTypes.FLOAT * 3),         # Unknown float
        ("carCategory",     DataTypes.CHAR * 4),          # Null terminated string of car category (GR3, GRX etc.)
    ]


### * Heart Beat

def heartBeat(socket, destination: tuple[int, int], msg = b'C'):
    
    socket.sendto(msg, destination)
    
    # send message to destination
    # msg = packetVersion = A | B | ~
    # else packetVersion = A 

### * Decryption

# pip install pycryptodome
try:
    from Crypto.Cipher import Salsa20 as s20
except:
    print("Cant use GT7 struct! Install pycryptodome. 'pip install pycryptodome'")
import struct
def decrypt_data(raw: bytes) -> bytes:
    def detect_packet_version(data: bytes) -> str:
        size = len(data)
        return {296: 'A', 316: 'B', 344: '~', 368: 'C'}.get(size, ' ')
    
    SALSA20_KEY = b"Simulator Interface Packet GT7 ver 0.0"[:32]

    XOR_MAP = {
        'A': 0xDEADBEAF,
        'B': 0xDEADBEEF,
        '~': 0x55FABB4F,
        'C': 0xDEADBEEF,
    }
    
    version = detect_packet_version(raw)

    # Read iv1 as a little-endian uint32 from offset 0x40
    iv1int = struct.unpack_from("<I", raw, 0x40)[0]

    xor_val = XOR_MAP.get(version, 0)
    iv2int = iv1int ^ xor_val

    # IV is [iv2 as LE bytes] + [iv1 as LE bytes]  — matches C++ layout
    iv = struct.pack("<I", iv2int) + struct.pack("<I", iv1int)

    cipher = s20.new(key=SALSA20_KEY, nonce=iv)
    decrypted = cipher.decrypt(raw)
    return decrypted


### * MetaData

class MetaData:
    # standard network info
    port: int | None = 33740
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = 33739
    heartBeatFunc = heartBeat
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None
    
    # use if the data needs decrypting
    decrytionFunc = decrypt_data
    
    # use if there is a header packet
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (PacketAData, PacketBData, PacketTildaData, PacketCData,),
    }