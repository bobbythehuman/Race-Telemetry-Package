import ctypes
from enum import Enum


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


### Motion Packet -- Rate as specified in menus -- 1341 bytes


class CarUDPData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_worldPosition",         DataTypes.FLOAT * 3),     # world co-ordinates of vehicle
        ("m_lastLapTime",           DataTypes.FLOAT),
        ("m_currentLapTime",        DataTypes.FLOAT),
        ("m_bestLapTime",           DataTypes.FLOAT),
        ("m_sector1Time",           DataTypes.FLOAT),
        ("m_sector2Time",           DataTypes.FLOAT),
        ("m_lapDistance",           DataTypes.FLOAT),
        ("m_driverId",              DataTypes.BYTE),
        ("m_teamId",                DataTypes.BYTE),
        ("m_carPosition",           DataTypes.BYTE),          # track positions of vehicle
        ("m_currentLapNum",         DataTypes.BYTE),
        ("m_tyreCompound",          DataTypes.BYTE),          # compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
        ("m_inPits",                DataTypes.BYTE),          # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                DataTypes.BYTE),          # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",     DataTypes.BYTE),          # current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",             DataTypes.BYTE),          # accumulated time penalties in seconds to be added
    ]


class UDPPacket(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_time",                      DataTypes.FLOAT),
        ("m_lapTime",                   DataTypes.FLOAT),
        ("m_lapDistance",               DataTypes.FLOAT),
        ("m_totalDistance",             DataTypes.FLOAT),
        ("m_x",                         DataTypes.FLOAT),         # World space position
        ("m_y",                         DataTypes.FLOAT),         # World space position
        ("m_z",                         DataTypes.FLOAT),         # World space position
        ("m_speed",                     DataTypes.FLOAT),         # Speed of car in MPH
        ("m_xv",                        DataTypes.FLOAT),         # Velocity in world space
        ("m_yv",                        DataTypes.FLOAT),         # Velocity in world space
        ("m_zv",                        DataTypes.FLOAT),         # Velocity in world space
        ("m_xr",                        DataTypes.FLOAT),         # World space right direction
        ("m_yr",                        DataTypes.FLOAT),         # World space right direction
        ("m_zr",                        DataTypes.FLOAT),         # World space right direction
        ("m_xd",                        DataTypes.FLOAT),         # World space forward direction
        ("m_yd",                        DataTypes.FLOAT),         # World space forward direction
        ("m_zd",                        DataTypes.FLOAT),         # World space forward direction
        ("m_susp_pos",                  DataTypes.FLOAT * 4),     # Note: All wheel arrays have the order:
        ("m_susp_vel",                  DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_wheel_speed",               DataTypes.FLOAT * 4),
        ("m_throttle",                  DataTypes.FLOAT),
        ("m_steer",                     DataTypes.FLOAT),
        ("m_brake",                     DataTypes.FLOAT),
        ("m_clutch",                    DataTypes.FLOAT),
        ("m_gear",                      DataTypes.FLOAT),
        ("m_gforce_lat",                DataTypes.FLOAT),
        ("m_gforce_lon",                DataTypes.FLOAT),
        ("m_lap",                       DataTypes.FLOAT),
        ("m_engineRate",                DataTypes.FLOAT),
        ("m_sli_pro_native_support",    DataTypes.FLOAT),     # SLI Pro support
        ("m_car_position",              DataTypes.FLOAT),     # car race position
        ("m_kers_level",                DataTypes.FLOAT),     # kers energy left
        ("m_kers_max_level",            DataTypes.FLOAT),     # kers maximum energy
        ("m_drs",                       DataTypes.FLOAT),     # 0 = off, 1 = on
        ("m_traction_control",          DataTypes.FLOAT),     # 0 (off) - 2 (high)
        ("m_anti_lock_brakes",          DataTypes.FLOAT),     # 0 (off) - 1 (on)
        ("m_fuel_in_tank",              DataTypes.FLOAT),     # current fuel mass
        ("m_fuel_capacity",             DataTypes.FLOAT),     # fuel capacity
        ("m_in_pits",                   DataTypes.FLOAT),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                    DataTypes.FLOAT),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_sector1_time",              DataTypes.FLOAT),     # time of sector1 (or 0)
        ("m_sector2_time",              DataTypes.FLOAT),     # time of sector2 (or 0)
        ("m_brakes_temp",               DataTypes.FLOAT * 4), # brakes temperature (centigrade)
        ("m_tyres_pressure",            DataTypes.FLOAT * 4), # tyres pressure PSI
        ("m_team_info",                 DataTypes.FLOAT),     # team ID 
        ("m_total_laps",                DataTypes.FLOAT),     # total number of laps in this race
        ("m_track_size",                DataTypes.FLOAT),     # track size meters
        ("m_last_lap_time",             DataTypes.FLOAT),     # last lap time
        ("m_max_rpm",                   DataTypes.FLOAT),     # cars max RPM, at which point the rev limiter will kick in
        ("m_idle_rpm",                  DataTypes.FLOAT),     # cars idle RPM
        ("m_max_gears",                 DataTypes.FLOAT),     # maximum number of gears
        ("m_sessionType",               DataTypes.FLOAT),     # 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
        ("m_drsAllowed",                DataTypes.FLOAT),     # 0 = not allowed, 1 = allowed, -1 = invalid / unknown
        ("m_track_number",              DataTypes.FLOAT),     # -1 for unknown, 0-21 for tracks
        ("m_vehicleFIAFlags",           DataTypes.FLOAT),     # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
        ("m_era",                       DataTypes.FLOAT),     # era, 2017 (modern) or 1980 (classic)
        ("m_engine_temperature",        DataTypes.FLOAT),     # engine temperature (centigrade)
        ("m_gforce_vert",               DataTypes.FLOAT),     # vertical g-force component
        ("m_ang_vel_x",                 DataTypes.FLOAT),     # angular velocity x-component
        ("m_ang_vel_y",                 DataTypes.FLOAT),     # angular velocity y-component
        ("m_ang_vel_z",                 DataTypes.FLOAT),     # angular velocity z-component
        ("m_tyres_temperature",         DataTypes.BYTE * 4),  # tyres temperature (centigrade)
        ("m_tyres_wear",                DataTypes.BYTE * 4),  # tyre wear percentage
        ("m_tyre_compound",             DataTypes.BYTE),      # compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
        ("m_front_brake_bias",          DataTypes.BYTE),      # front brake bias (percentage)
        ("m_fuel_mix",                  DataTypes.BYTE),      # fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ("m_currentLapInvalid",         DataTypes.BYTE),      # current lap invalid - 0 = valid, 1 = invalid
        ("m_tyres_damage",              DataTypes.BYTE * 4),  # tyre damage (percentage)
        ("m_front_left_wing_damage",    DataTypes.BYTE),      # front left wing damage (percentage)
        ("m_front_right_wing_damage",   DataTypes.BYTE),      # front right wing damage (percentage)
        ("m_rear_wing_damage",          DataTypes.BYTE),      # rear wing damage (percentage)
        ("m_engine_damage",             DataTypes.BYTE),      # engine damage (percentage)
        ("m_gear_box_damage",           DataTypes.BYTE),      # gear box damage (percentage)
        ("m_exhaust_damage",            DataTypes.BYTE),      # exhaust damage (percentage)
        ("m_pit_limiter_status",        DataTypes.BYTE),      # pit limiter status – 0 = off, 1 = on
        ("m_pit_speed_limit",           DataTypes.BYTE),      # pit speed limit in mph
        ("m_session_time_left",         DataTypes.FLOAT),     # time left in session in seconds 
        ("m_rev_lights_percent",        DataTypes.BYTE),      # rev lights indicator (percentage)
        ("m_is_spectating",             DataTypes.BYTE),      # whether the player is spectating
        ("m_spectator_car_index",       DataTypes.BYTE),      # index of the car being spectated
        # Car data
        ("m_num_cars",              DataTypes.BYTE),      # number of cars in data
        ("m_player_car_index",      DataTypes.BYTE),      # index of player's car in the array
        ("m_car_data",              CarUDPData * 20),           # data for all cars on track
        ("m_yaw",                   DataTypes.FLOAT),
        ("m_pitch",                 DataTypes.FLOAT),
        ("m_roll",                  DataTypes.FLOAT),
        ("m_x_local_velocity",      DataTypes.FLOAT),     # Velocity in local space
        ("m_y_local_velocity",      DataTypes.FLOAT),     # Velocity in local space
        ("m_z_local_velocity",      DataTypes.FLOAT),     # Velocity in local space
        ("m_susp_acceleration",     DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_ang_acc_x",             DataTypes.FLOAT),     # angular acceleration x-component
        ("m_ang_acc_y",             DataTypes.FLOAT),     # angular acceleration x-component
        ("m_ang_acc_z",             DataTypes.FLOAT),     # angular acceleration x-component
    ]



### MetaData

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

