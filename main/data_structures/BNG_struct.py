import ctypes
from enum import Enum

# source
# https://documentation.beamng.com/modding/protocols/

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure

    SIGNED_INT = ctypes.c_int
    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_SHORT = ctypes.c_ushort

    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char

# OutGauge UDP protocol

# Items marked as `N/A` are not implemented.

class TelemetryData(DataTypes.STRUCTURE):
    _fields_ = [
        ("time",            DataTypes.UNSIGNED_INT),      # time in milliseconds (to check order) // N/A, hardcoded to 0
        ("car",             DataTypes.CHAR * 4),          # Car name // N/A, fixed value of "beam"
        ("flags",           DataTypes.UNSIGNED_SHORT),    # Info (see OG_x below)
        ("gear",            DataTypes.CHAR),              # Reverse:0, Neutral:1, First:2...
        ("plid",            DataTypes.CHAR),              # Unique ID of viewed player (0 = none) // N/A, hardcoded to 0
        ("speed",           DataTypes.FLOAT),             # M/S
        ("rpm",             DataTypes.FLOAT),             # RPM
        ("turbo",           DataTypes.FLOAT),             # BAR
        ("engTemp",         DataTypes.FLOAT),             # C
        ("fuel",            DataTypes.FLOAT),             # 0 to 1
        ("oilPressure",     DataTypes.FLOAT),             # BAR // N/A, hardcoded to 0
        ("oilTemp",         DataTypes.FLOAT),             # C
        ("dashLights",      DataTypes.UNSIGNED_INT),      # Dash lights available (see DL_x below)
        ("showLights",      DataTypes.UNSIGNED_INT),      # Dash lights currently switched on
        ("throttle",        DataTypes.FLOAT),             # 0 to 1
        ("brake",           DataTypes.FLOAT),             # 0 to 1
        ("clutch",          DataTypes.FLOAT),             # 0 to 1
        ("display1",        DataTypes.CHAR * 16),         # Usually Fuel // N/A, hardcoded to ""
        ("display2",        DataTypes.CHAR * 16),         # Usually Settings // N/A, hardcoded to ""
        ("id",              DataTypes.SIGNED_INT)         # optional - only if OutGauge ID is specified
    ]
    

# -- OG_x - bits for flags
# local OG_SHIFT =     1  -- key // N/A
# local OG_CTRL  =     2  -- key // N/A
# local OG_TURBO =  8192  -- show turbo gauge
# local OG_KM    = 16384  -- if not set - user prefers MILES
# local OG_BAR   = 32768  -- if not set - user prefers PSI

# -- DL_x - bits for dashLights and showLights
# local DL_SHIFT        = 2 ^ 0    -- shift light
# local DL_FULLBEAM     = 2 ^ 1    -- full beam
# local DL_HANDBRAKE    = 2 ^ 2    -- handbrake
# local DL_PITSPEED     = 2 ^ 3    -- pit speed limiter // N/A
# local DL_TC           = 2 ^ 4    -- tc active or switched off
# local DL_SIGNAL_L     = 2 ^ 5    -- left turn signal
# local DL_SIGNAL_R     = 2 ^ 6    -- right turn signal
# local DL_SIGNAL_ANY   = 2 ^ 7    -- shared turn signal // N/A
# local DL_OILWARN      = 2 ^ 8    -- oil pressure warning
# local DL_BATTERY      = 2 ^ 9    -- battery warning
# local DL_ABS          = 2 ^ 10   -- abs active or switched off
# local DL_SPARE        = 2 ^ 11   -- N/A

# MotionSim UDP protocol

class MotionSim(DataTypes.STRUCTURE):
    _fields_ = [
        ("format",      DataTypes.CHAR * 4),  # allows to verify if packet is the expected format, fixed value of "BNG1"
        ("posX",        DataTypes.FLOAT),     # world position of the vehicle
        ("posY",        DataTypes.FLOAT),     # world position of the vehicle
        ("posZ",        DataTypes.FLOAT),     # world position of the vehicle
        ("velX",        DataTypes.FLOAT),     # velocity of the vehicle
        ("velY",        DataTypes.FLOAT),     # velocity of the vehicle
        ("velZ",        DataTypes.FLOAT),     # velocity of the vehicle
        ("accX",        DataTypes.FLOAT),     # acceleration of the vehicle, gravity not included
        ("accY",        DataTypes.FLOAT),     # acceleration of the vehicle, gravity not included
        ("accZ",        DataTypes.FLOAT),     # acceleration of the vehicle, gravity not included
        ("upX",         DataTypes.FLOAT),     # vector components of a vector pointing "up" relative to the vehicle
        ("upY",         DataTypes.FLOAT),     # vector components of a vector pointing "up" relative to the vehicle
        ("upZ",         DataTypes.FLOAT),     # vector components of a vector pointing "up" relative to the vehicle
        ("rollPos",     DataTypes.FLOAT),     # angle of roll, pitch and yaw of the vehicle
        ("pitchPos",    DataTypes.FLOAT),     # angle of roll, pitch and yaw of the vehicle
        ("yawPos",      DataTypes.FLOAT),     # angle of roll, pitch and yaw of the vehicle
        ("rollVel",     DataTypes.FLOAT),     # angular velocities of roll, pitch and yaw of the vehicle
        ("pitchVel",    DataTypes.FLOAT),     # angular velocities of roll, pitch and yaw of the vehicle
        ("yawVel",      DataTypes.FLOAT),     # angular velocities of roll, pitch and yaw of the vehicle
        ("rollAcc",     DataTypes.FLOAT),     # angular acceleration of roll, pitch and yaw of the vehicle
        ("pitchAcc",    DataTypes.FLOAT),     # angular acceleration of roll, pitch and yaw of the vehicle
        ("yawAcc",      DataTypes.FLOAT),     # angular acceleration of roll, pitch and yaw of the vehicle
    ]


### MetaData

class MetaData:
    # standard network info
    port: int | None = 4444
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (TelemetryData, MotionSim),
    }




