from __future__ import annotations
from collections.abc import Callable
import ctypes


# source
# https://github.com/kutu/pyirsdk
# https://github.com/SIMRacingApps/SIMRacingAppsSIMPluginiRacing
# https://github.com/jamatu/ArduinoRacingDash/blob/master/iRacingSLI/src/iRacingSdkWrapper/telemetry_11_23_15.pdf


# ! Iracing Dynamically creates the structure

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union


    SIGNED_INT = ctypes.c_int
    SIGNED_INT32 = ctypes.c_int32
    SIGNED_INT64 = ctypes.c_int64
    
    
    # UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64

    DOUBLE = ctypes.c_double
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    BOOL = ctypes.c_bool
    TIME = ctypes.c_time_t


### * Enums

VAR_TYPE_MAP = {
    0: ctypes.c_char,
    1: ctypes.c_bool,
    2: ctypes.c_int,
    3: ctypes.c_uint,   # bitField
    4: ctypes.c_float,
    5: ctypes.c_double,
}


### * Data Structure

class irsdk_varBuf(DataTypes.STRUCTURE):
    _fields_ = [
        ("tickCount",	DataTypes.SIGNED_INT),		# used to detect changes in data
        ("bufOffset",	DataTypes.SIGNED_INT),		# offset from header
        ("pad",			DataTypes.SIGNED_INT * 2),	# (16 byte align)
	]

class irsdk_header(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("ver",					DataTypes.SIGNED_INT),		# this api header version, see IRSDK_VER
        ("status",				DataTypes.SIGNED_INT),		# bitfield using irsdk_StatusField
        ("tickRate",			DataTypes.SIGNED_INT),		# ticks per second (60 or 360 etc)
        
        # session information, updated periodicaly
        ("sessionInfoUpdate",	DataTypes.SIGNED_INT),		# Incremented when session info changes
        ("sessionInfoLen",		DataTypes.SIGNED_INT),		# Length in bytes of session info string
        ("sessionInfoOffset",	DataTypes.SIGNED_INT),		# Session info, encoded in YAML format
        
        # State data, output at tickRate
        ("numVars",				DataTypes.SIGNED_INT),		# length of arra pointed to by varHeaderOffset
        ("varHeaderOffset",		DataTypes.SIGNED_INT),		# offset to irsdk_varHeader[numVars] array, Describes the variables received in varBuf
        
        ("numBuf",				DataTypes.SIGNED_INT),		# <= IRSDK_MAX_BUFS (3 for now)
        ("numLen",				DataTypes.SIGNED_INT),		# length in bytes for one line
        
        ("pad1",				DataTypes.SIGNED_INT * 2),	# (16 byte align)
        ("varBuf",				irsdk_varBuf * 4),				# buffers of data being written to
    ]

class irsdk_varHeader(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("type",			DataTypes.SIGNED_INT),	# irsdk_VarType
        ("offset",			DataTypes.SIGNED_INT),	# offset fron start of buffer row
        ("count",			DataTypes.SIGNED_INT),	# number of entrys (array), so length in bytes would be irsdk_VarTypeBytes[type] * count
        
        ("countAsTime",		DataTypes.BOOL),		# Incremented when session info changes
        ("pad",				DataTypes.CHAR * 3),	# (16 byte align)
        
        ("name",			DataTypes.CHAR * 32),	# Session info, encoded in YAML format
        ("desc",			DataTypes.CHAR * 64),	# length of arra pointed to by varHeaderOffset
        ("unit",			DataTypes.CHAR * 32),	# something like "kg/m^2"
    ]

class irsdk_diskSubHeader(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("sessionStartDate",	DataTypes.TIME),
        ("sessionStartTime",	DataTypes.DOUBLE),
        ("sessionEndTime",		DataTypes.DOUBLE),
        ("sessionLapCount",		DataTypes.SIGNED_INT),
        ("sessionRecordCount",	DataTypes.SIGNED_INT),
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = None
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc: Callable | None = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple[Callable, Callable] | None = None
    
    # use if the data needs decrypting
    decryptionFunc: Callable | None = None
    
    # use if there is a header packet
    headerInfo: type | None = irsdk_header
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = "Local\\IRSDKMemMapFileName"
    
    # define the receiver and decoder modes
    receiverMode: str = "shared_memory"
    decoderMode: str = "iracing_dynamic"
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (irsdk_header, irsdk_varHeader, irsdk_diskSubHeader),
    }