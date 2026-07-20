import ctypes
from enum import IntEnum


class DataTypes:
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


### * Enums

class TEAM_ID(IntEnum):
    RedBull = 0
    Ferrari = 1
    McLaren = 2
    Lotus = 3
    Mercedes = 4
    Sauber = 5
    Force_India = 6
    Williams = 7
    Toro_Rosso = 8
    Caterham = 9
    Marussia = 10
    Haas = 11
    Manor = 12

class TRACK_ID(IntEnum):
    Melbourne = 0
    Sepang = 1
    Shanghai = 2
    Sakhir_Bahrain = 3
    Catalunya = 4
    Monaco = 5
    Montreal = 6
    Silverstone = 7
    Hockenheim = 8
    Hungaroring = 9
    Spa = 10
    Monza = 11
    Singapore = 12
    Suzuka = 13
    Abu_Dhabi = 14
    Texas = 15
    Brazil = 16
    Austria = 17
    Sochi = 18
    Mexico = 19
    unused = 20
    Baka_Azerbaijan = 21


### * Data Structure

class UDPPacket(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _enums_: dict[type, tuple[str, ...]] = {
        TEAM_ID: ("m_team_info",),
        TRACK_ID: ("m_track_number",),
    }
    _fields_ = [
        ("m_time",                      DataTypes.FLOAT),
        ("m_lapTime",                   DataTypes.FLOAT),
        ("m_lapDistance",               DataTypes.FLOAT),
        ("m_totalDistance",             DataTypes.FLOAT),
        ("m_x",                         DataTypes.FLOAT),     # World space position
        ("m_y",                         DataTypes.FLOAT),     # World space position
        ("m_z",                         DataTypes.FLOAT),     # World space position
        ("m_speed",                     DataTypes.FLOAT),     # Speed of car in MPH
        ("m_xv",                        DataTypes.FLOAT),     # Velocity in world space
        ("m_yv",                        DataTypes.FLOAT),     # Velocity in world space
        ("m_zv",                        DataTypes.FLOAT),     # Velocity in world space
        ("m_xr",                        DataTypes.FLOAT),     # World space right direction
        ("m_yr",                        DataTypes.FLOAT),     # World space right direction
        ("m_zr",                        DataTypes.FLOAT),     # World space right direction
        ("m_xd",                        DataTypes.FLOAT),     # World space forward direction
        ("m_yd",                        DataTypes.FLOAT),     # World space forward direction
        ("m_zd",                        DataTypes.FLOAT),     # World space forward direction
        ("m_susp_pos_bl",               DataTypes.FLOAT),
        ("m_susp_pos_br",               DataTypes.FLOAT),
        ("m_susp_pos_fl",               DataTypes.FLOAT),
        ("m_susp_pos_fr",               DataTypes.FLOAT),
        ("m_susp_vel_bl",               DataTypes.FLOAT),
        ("m_susp_vel_br",               DataTypes.FLOAT),
        ("m_susp_vel_fl",               DataTypes.FLOAT),
        ("m_susp_vel_fr",               DataTypes.FLOAT),
        ("m_wheel_speed_bl",            DataTypes.FLOAT),
        ("m_wheel_speed_br",            DataTypes.FLOAT),
        ("m_wheel_speed_fl",            DataTypes.FLOAT),
        ("m_wheel_speed_fr",            DataTypes.FLOAT),
        ("m_throttle",                  DataTypes.FLOAT),
        ("m_steer",                     DataTypes.FLOAT),
        ("m_brake",                     DataTypes.FLOAT),
        ("m_clutch",                    DataTypes.FLOAT),
        ("m_gear",                      DataTypes.FLOAT),
        ("m_gforce_lat",                DataTypes.FLOAT),
        ("m_gforce_lon",                DataTypes.FLOAT),
        ("m_lap",                       DataTypes.FLOAT),
        ("m_engineRate",                DataTypes.FLOAT),
        ("m_sli_pro_native_support",    DataTypes.FLOAT),         # SLI Pro support
        ("m_car_position",              DataTypes.FLOAT),         # car race position
        ("m_kers_level",                DataTypes.FLOAT),         # kers energy left
        ("m_kers_max_level",            DataTypes.FLOAT),         # kers maximum energy
        ("m_drs",                       DataTypes.FLOAT),         # 0 = off, 1 = on
        ("m_traction_control",          DataTypes.FLOAT),         # 0 (off) - 2 (high)
        ("m_anti_lock_brakes",          DataTypes.FLOAT),         # 0 (off) - 1 (on)
        ("m_fuel_in_tank",              DataTypes.FLOAT),         # current fuel mass
        ("m_fuel_capacity",             DataTypes.FLOAT),         # fuel capacity
        ("m_in_pits",                   DataTypes.FLOAT),         # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                    DataTypes.FLOAT),         # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_sector1_time",              DataTypes.FLOAT),         # time of sector1 (or 0)
        ("m_sector2_time",              DataTypes.FLOAT),         # time of sector2 (or 0)
        ("m_brakes_temp",               DataTypes.FLOAT * 4),     # brakes temperature (centigrade)
        ("m_wheels_pressure",           DataTypes.FLOAT * 4),     # wheels pressure PSI
        ("m_team_info",                 DataTypes.FLOAT),         # team ID 
        ("m_total_laps",                DataTypes.FLOAT),         # total number of laps in this race
        ("m_track_size",                DataTypes.FLOAT),         # track size meters
        ("m_last_lap_time",             DataTypes.FLOAT),         # last lap time
        ("m_max_rpm",                   DataTypes.FLOAT),         # cars max RPM, at which point the rev limiter will kick in
        ("m_idle_rpm",                  DataTypes.FLOAT),         # cars idle RPM
        ("m_max_gears",                 DataTypes.FLOAT),         # maximum number of gears
        ("m_sessionType",               DataTypes.FLOAT),         # 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
        ("m_drsAllowed",                DataTypes.FLOAT),         # 0 = not allowed, 1 = allowed, -1 = invalid / unknown
        ("m_track_number",              DataTypes.FLOAT),         # -1 for unknown, 0-21 for tracks
        ("m_vehicleFIAFlags",           DataTypes.FLOAT),         # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
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

