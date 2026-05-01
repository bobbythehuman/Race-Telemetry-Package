import ctypes
from enum import Enum


class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    # SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8      # 1 byte 
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double
    
    BYTE = ctypes.c_byte


class UDPPacket(DataTypes.STRUCTURE.value):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_time",                      DataTypes.FLOAT.value),
        ("m_lapTime",                   DataTypes.FLOAT.value),
        ("m_lapDistance",               DataTypes.FLOAT.value),
        ("m_totalDistance",             DataTypes.FLOAT.value),
        ("m_x",                         DataTypes.FLOAT.value),     # World space position
        ("m_y",                         DataTypes.FLOAT.value),     # World space position
        ("m_z",                         DataTypes.FLOAT.value),     # World space position
        ("m_speed",                     DataTypes.FLOAT.value),     # Speed of car in MPH
        ("m_xv",                        DataTypes.FLOAT.value),     # Velocity in world space
        ("m_yv",                        DataTypes.FLOAT.value),     # Velocity in world space
        ("m_zv",                        DataTypes.FLOAT.value),     # Velocity in world space
        ("m_xr",                        DataTypes.FLOAT.value),     # World space right direction
        ("m_yr",                        DataTypes.FLOAT.value),     # World space right direction
        ("m_zr",                        DataTypes.FLOAT.value),     # World space right direction
        ("m_xd",                        DataTypes.FLOAT.value),     # World space forward direction
        ("m_yd",                        DataTypes.FLOAT.value),     # World space forward direction
        ("m_zd",                        DataTypes.FLOAT.value),     # World space forward direction
        ("m_susp_pos_bl",               DataTypes.FLOAT.value),
        ("m_susp_pos_br",               DataTypes.FLOAT.value),
        ("m_susp_pos_fl",               DataTypes.FLOAT.value),
        ("m_susp_pos_fr",               DataTypes.FLOAT.value),
        ("m_susp_vel_bl",               DataTypes.FLOAT.value),
        ("m_susp_vel_br",               DataTypes.FLOAT.value),
        ("m_susp_vel_fl",               DataTypes.FLOAT.value),
        ("m_susp_vel_fr",               DataTypes.FLOAT.value),
        ("m_wheel_speed_bl",            DataTypes.FLOAT.value),
        ("m_wheel_speed_br",            DataTypes.FLOAT.value),
        ("m_wheel_speed_fl",            DataTypes.FLOAT.value),
        ("m_wheel_speed_fr",            DataTypes.FLOAT.value),
        ("m_throttle",                  DataTypes.FLOAT.value),
        ("m_steer",                     DataTypes.FLOAT.value),
        ("m_brake",                     DataTypes.FLOAT.value),
        ("m_clutch",                    DataTypes.FLOAT.value),
        ("m_gear",                      DataTypes.FLOAT.value),
        ("m_gforce_lat",                DataTypes.FLOAT.value),
        ("m_gforce_lon",                DataTypes.FLOAT.value),
        ("m_lap",                       DataTypes.FLOAT.value),
        ("m_engineRate",                DataTypes.FLOAT.value),
        ("m_sli_pro_native_support",    DataTypes.FLOAT.value),         # SLI Pro support
        ("m_car_position",              DataTypes.FLOAT.value),         # car race position
        ("m_kers_level",                DataTypes.FLOAT.value),         # kers energy left
        ("m_kers_max_level",            DataTypes.FLOAT.value),         # kers maximum energy
        ("m_drs",                       DataTypes.FLOAT.value),         # 0 = off, 1 = on
        ("m_traction_control",          DataTypes.FLOAT.value),         # 0 (off) - 2 (high)
        ("m_anti_lock_brakes",          DataTypes.FLOAT.value),         # 0 (off) - 1 (on)
        ("m_fuel_in_tank",              DataTypes.FLOAT.value),         # current fuel mass
        ("m_fuel_capacity",             DataTypes.FLOAT.value),         # fuel capacity
        ("m_in_pits",                   DataTypes.FLOAT.value),         # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                    DataTypes.FLOAT.value),         # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_sector1_time",              DataTypes.FLOAT.value),         # time of sector1 (or 0)
        ("m_sector2_time",              DataTypes.FLOAT.value),         # time of sector2 (or 0)
        ("m_brakes_temp",               DataTypes.FLOAT.value * 4),     # brakes temperature (centigrade)
        ("m_wheels_pressure",           DataTypes.FLOAT.value * 4),     # wheels pressure PSI
        ("m_team_info",                 DataTypes.FLOAT.value),         # team ID 
        ("m_total_laps",                DataTypes.FLOAT.value),         # total number of laps in this race
        ("m_track_size",                DataTypes.FLOAT.value),         # track size meters
        ("m_last_lap_time",             DataTypes.FLOAT.value),         # last lap time
        ("m_max_rpm",                   DataTypes.FLOAT.value),         # cars max RPM, at which point the rev limiter will kick in
        ("m_idle_rpm",                  DataTypes.FLOAT.value),         # cars idle RPM
        ("m_max_gears",                 DataTypes.FLOAT.value),         # maximum number of gears
        ("m_sessionType",               DataTypes.FLOAT.value),         # 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
        ("m_drsAllowed",                DataTypes.FLOAT.value),         # 0 = not allowed, 1 = allowed, -1 = invalid / unknown
        ("m_track_number",              DataTypes.FLOAT.value),         # -1 for unknown, 0-21 for tracks
        ("m_vehicleFIAFlags",           DataTypes.FLOAT.value),         # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]



### MetaData

class MetaData:
    # standard network info
    port: int = 20777
    fullBufferSize: int = 260
    
    # use if a heartbeat is needed
    heartBeatPort = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort = None
    handShakeFunc = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    
    # standard packet info
    packetInfo: dict[int, tuple[tuple[int, type], ...]] = {
        0: ((260, UDPPacket),),
    }

