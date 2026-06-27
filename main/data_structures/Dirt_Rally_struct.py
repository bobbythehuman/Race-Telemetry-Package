import ctypes
from enum import Enum, IntEnum


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double
    
    BYTE = ctypes.c_byte


### * Enums


### * Data Structure

class UDPPacket(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("total_time",					DataTypes.FLOAT),
        ("lap_time",					DataTypes.FLOAT),
        ("lap_distance",				DataTypes.FLOAT),
        ("total_distance",				DataTypes.FLOAT),
        ("position_x",					DataTypes.FLOAT),
        ("position_y",					DataTypes.FLOAT),
        ("position_z",					DataTypes.FLOAT),
        ("velocity",					DataTypes.FLOAT),		# Velocity (Speed) [m/s]
        ("velocity_x",					DataTypes.FLOAT),
        ("velocity_y",					DataTypes.FLOAT),
        ("velocity_z",					DataTypes.FLOAT),
        ("roll_vector_x",				DataTypes.FLOAT),
        ("roll_vector_y",				DataTypes.FLOAT),
        ("roll_vector_z",				DataTypes.FLOAT),
        ("pitch_vector_x",				DataTypes.FLOAT),
        ("pitch_vector_y",				DataTypes.FLOAT),
        ("pitch_vector_z",				DataTypes.FLOAT),
        ("suspension_position_rl",		DataTypes.FLOAT),
        ("suspension_position_rr",		DataTypes.FLOAT),
        ("suspension_position_fl",		DataTypes.FLOAT),
        ("suspension_position_fr",		DataTypes.FLOAT),
        ("suspension_velocity_rl",		DataTypes.FLOAT),
        ("suspension_velocity_rr",		DataTypes.FLOAT),
        ("suspension_velocity_fl",		DataTypes.FLOAT),
        ("suspension_velocity_fr",		DataTypes.FLOAT),
        ("wheel_velocity_rl",			DataTypes.FLOAT),
        ("wheel_velocity_rr",			DataTypes.FLOAT),
        ("wheel_velocity_fl",			DataTypes.FLOAT),
        ("wheel_velocity_fr",			DataTypes.FLOAT),
        ("throttle_input",				DataTypes.FLOAT),
        ("steering_input",				DataTypes.FLOAT),
        ("brake_input",					DataTypes.FLOAT),
        ("clutch_input",				DataTypes.FLOAT),
        ("gear",						DataTypes.FLOAT),		# Gear [0 = Neutral, 1 = 1, 2 = 2, ..., 10 = Reverse]
        ("gforce_lateral",				DataTypes.FLOAT),
        ("gforce_longitudinal",			DataTypes.FLOAT),
        ("lap",							DataTypes.FLOAT),
        ("engine_rate",					DataTypes.FLOAT),		# Speed of Engine [rpm / 10]
        
        # Possible 13 more fields here
        ("brake_temp_rl",				DataTypes.FLOAT),
        ("brake_temp_rr",				DataTypes.FLOAT),
        ("brake_temp_fl",				DataTypes.FLOAT),
        ("brake_temp_fr",				DataTypes.FLOAT),
        # Possible 5 more fields here
        ("total_laps",					DataTypes.FLOAT),
        ("track_length",				DataTypes.FLOAT),
        # Possible 1 more fields here
        ("max_rpm",						DataTypes.FLOAT),		# Maximum rpm / 10
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = 20777
    
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
        0: (UDPPacket,),
    }

