import ctypes


# https://www.scribd.com/document/350826037/UDP-output-setup
# https://web.archive.org/web/20181117092858/http://forums.codemasters.com/discussion/52950/setting-up-udp-output-for-dirt-4


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT32 = ctypes.c_int32
    UNSIGNED_INT32 = ctypes.c_uint32
    
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double
    
    BYTE = ctypes.c_byte


### * Enums



### * Data Structure

class Mode0(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("total_time",				DataTypes.UNSIGNED_INT32),
        ("angular_velocity_x",		DataTypes.FLOAT),
        ("angular_velocity_y",		DataTypes.FLOAT),
        ("angular_velocity_z",		DataTypes.FLOAT),
        ("yaw",						DataTypes.FLOAT),
        ("pitch",					DataTypes.FLOAT),
        ("roll",					DataTypes.FLOAT),
        ("acceleration_x",			DataTypes.FLOAT),
        ("acceleration_z",			DataTypes.FLOAT),
        ("acceleration_y",			DataTypes.FLOAT),
        ("velocity_x",				DataTypes.FLOAT),
        ("velocity_y",				DataTypes.FLOAT),
        ("velocity_z",				DataTypes.FLOAT),
        ("position_x",				DataTypes.SIGNED_INT32),
        ("position_y",				DataTypes.SIGNED_INT32),
        ("position_z",				DataTypes.SIGNED_INT32),
	]

class Mode1(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("total_time",					DataTypes.FLOAT),
        ("lap_time",					DataTypes.FLOAT),
        ("lap_distance",				DataTypes.FLOAT),
        ("total_distance",				DataTypes.FLOAT),
        ("position_x",					DataTypes.FLOAT),
        ("position_y",					DataTypes.FLOAT),
        ("position_z",					DataTypes.FLOAT),
        ("speed",						DataTypes.FLOAT),
        ("velocity_x",					DataTypes.FLOAT),
        ("velocity_y",					DataTypes.FLOAT),
        ("velocity_z",					DataTypes.FLOAT),
        ("left_dir_x",					DataTypes.FLOAT),
        ("left_dir_y",					DataTypes.FLOAT),
        ("left_dir_z",					DataTypes.FLOAT),
        ("forward_dir_x",				DataTypes.FLOAT),
        ("forward_dir_y",				DataTypes.FLOAT),
        ("forward_dir_z",				DataTypes.FLOAT),
        ("suspension_position_rl",		DataTypes.FLOAT),
        ("suspension_position_rr",		DataTypes.FLOAT),
        ("suspension_position_fl",		DataTypes.FLOAT),
        ("suspension_position_fr",		DataTypes.FLOAT),
        ("suspension_velocity_rl",		DataTypes.FLOAT),
        ("suspension_velocity_rr",		DataTypes.FLOAT),
        ("suspension_velocity_fl",		DataTypes.FLOAT),
        ("suspension_velocity_fr",		DataTypes.FLOAT),
        ("wheel_patch_speed_rl",		DataTypes.FLOAT),
        ("wheel_patch_speed_rr",		DataTypes.FLOAT),
        ("wheel_patch_speed_fl",		DataTypes.FLOAT),
        ("wheel_patch_speed_fr",		DataTypes.FLOAT),
        ("throttle_input",				DataTypes.FLOAT),
        ("steering_input",				DataTypes.FLOAT),
        ("brake_input",					DataTypes.FLOAT),
        ("clutch_input",				DataTypes.FLOAT),
        ("gear",						DataTypes.FLOAT),
        ("gforce_lateral",				DataTypes.FLOAT),
        ("gforce_longitudinal",			DataTypes.FLOAT),
        ("lap",							DataTypes.FLOAT),
        ("engine_rate",					DataTypes.FLOAT),
	]

class Mode2(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("total_time",					DataTypes.FLOAT),
        ("lap_time",					DataTypes.FLOAT),
        ("lap_distance",				DataTypes.FLOAT),
        ("total_distance",				DataTypes.FLOAT),
        ("position_x",					DataTypes.FLOAT),
        ("position_y",					DataTypes.FLOAT),
        ("position_z",					DataTypes.FLOAT),
        ("speed",						DataTypes.FLOAT),
        ("velocity_x",					DataTypes.FLOAT),
        ("velocity_y",					DataTypes.FLOAT),
        ("velocity_z",					DataTypes.FLOAT),
        ("left_dir_x",					DataTypes.FLOAT),
        ("left_dir_y",					DataTypes.FLOAT),
        ("left_dir_z",					DataTypes.FLOAT),
        ("forward_dir_x",				DataTypes.FLOAT),
        ("forward_dir_y",				DataTypes.FLOAT),
        ("forward_dir_z",				DataTypes.FLOAT),
        ("suspension_position_rl",		DataTypes.FLOAT),
        ("suspension_position_rr",		DataTypes.FLOAT),
        ("suspension_position_fl",		DataTypes.FLOAT),
        ("suspension_position_fr",		DataTypes.FLOAT),
        ("suspension_velocity_rl",		DataTypes.FLOAT),
        ("suspension_velocity_rr",		DataTypes.FLOAT),
        ("suspension_velocity_fl",		DataTypes.FLOAT),
        ("suspension_velocity_fr",		DataTypes.FLOAT),
        ("wheel_patch_speed_rl",		DataTypes.FLOAT),
        ("wheel_patch_speed_rr",		DataTypes.FLOAT),
        ("wheel_patch_speed_fl",		DataTypes.FLOAT),
        ("wheel_patch_speed_fr",		DataTypes.FLOAT),
        ("throttle_input",				DataTypes.FLOAT),
        ("steering_input",				DataTypes.FLOAT),
        ("brake_input",					DataTypes.FLOAT),
        ("clutch_input",				DataTypes.FLOAT),
        ("gear",						DataTypes.FLOAT),
        ("gforce_lateral",				DataTypes.FLOAT),
        ("gforce_longitudinal",			DataTypes.FLOAT),
        ("lap",							DataTypes.FLOAT),
        ("engine_rate",					DataTypes.FLOAT),
        ("native_sli_support",			DataTypes.FLOAT),
        ("race_position",				DataTypes.FLOAT),
        ("kers_level",					DataTypes.FLOAT),
        ("kers_level_max",				DataTypes.FLOAT),
        ("drs",							DataTypes.FLOAT),
        ("traction_control",			DataTypes.FLOAT),
        ("abs",							DataTypes.FLOAT),
        ("fuel_in_tank",				DataTypes.FLOAT),
        ("fuel_capacity",				DataTypes.FLOAT),
        ("in_pits",						DataTypes.FLOAT),
        ("race_sector",					DataTypes.FLOAT),
        ("sector_time_1",				DataTypes.FLOAT),
        ("sector_time_2",				DataTypes.FLOAT),
        ("brake_temp_rl",				DataTypes.FLOAT),
        ("brake_temp_rr",				DataTypes.FLOAT),
        ("brake_temp_fl",				DataTypes.FLOAT),
        ("brake_temp_fr",				DataTypes.FLOAT),
		("tyre_pressure_rl",			DataTypes.FLOAT),
		("tyre_pressure_rr",			DataTypes.FLOAT),
		("tyre_pressure_fl",			DataTypes.FLOAT),
		("tyre_pressure_fr",			DataTypes.FLOAT),
		("laps_completed",				DataTypes.FLOAT),
        ("total_laps",					DataTypes.FLOAT),
        ("track_length",				DataTypes.FLOAT),
        ("last_lap_time",				DataTypes.FLOAT),
	]

class Mode3(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("total_time",					DataTypes.FLOAT),
        ("lap_time",					DataTypes.FLOAT),
        ("lap_distance",				DataTypes.FLOAT),
        ("total_distance",				DataTypes.FLOAT),
        ("position_x",					DataTypes.FLOAT),
        ("position_y",					DataTypes.FLOAT),
        ("position_z",					DataTypes.FLOAT),
        ("speed",						DataTypes.FLOAT),
        ("velocity_x",					DataTypes.FLOAT),
        ("velocity_y",					DataTypes.FLOAT),
        ("velocity_z",					DataTypes.FLOAT),
        ("left_dir_x",					DataTypes.FLOAT),
        ("left_dir_y",					DataTypes.FLOAT),
        ("left_dir_z",					DataTypes.FLOAT),
        ("forward_dir_x",				DataTypes.FLOAT),
        ("forward_dir_y",				DataTypes.FLOAT),
        ("forward_dir_z",				DataTypes.FLOAT),
        ("suspension_position_rl",		DataTypes.FLOAT),
        ("suspension_position_rr",		DataTypes.FLOAT),
        ("suspension_position_fl",		DataTypes.FLOAT),
        ("suspension_position_fr",		DataTypes.FLOAT),
        ("suspension_velocity_rl",		DataTypes.FLOAT),
        ("suspension_velocity_rr",		DataTypes.FLOAT),
        ("suspension_velocity_fl",		DataTypes.FLOAT),
        ("suspension_velocity_fr",		DataTypes.FLOAT),
        ("wheel_patch_speed_rl",		DataTypes.FLOAT),
        ("wheel_patch_speed_rr",		DataTypes.FLOAT),
        ("wheel_patch_speed_fl",		DataTypes.FLOAT),
        ("wheel_patch_speed_fr",		DataTypes.FLOAT),
        ("throttle_input",				DataTypes.FLOAT),
        ("steering_input",				DataTypes.FLOAT),
        ("brake_input",					DataTypes.FLOAT),
        ("clutch_input",				DataTypes.FLOAT),
        ("gear",						DataTypes.FLOAT),
        ("gforce_lateral",				DataTypes.FLOAT),
        ("gforce_longitudinal",			DataTypes.FLOAT),
        ("lap",							DataTypes.FLOAT),
        ("engine_rate",					DataTypes.FLOAT),
        ("native_sli_support",			DataTypes.FLOAT),
        ("race_position",				DataTypes.FLOAT),
        ("kers_level",					DataTypes.FLOAT),
        ("kers_level_max",				DataTypes.FLOAT),
        ("drs",							DataTypes.FLOAT),
        ("traction_control",			DataTypes.FLOAT),
        ("abs",							DataTypes.FLOAT),
        ("fuel_in_tank",				DataTypes.FLOAT),
        ("fuel_capacity",				DataTypes.FLOAT),
        ("in_pits",						DataTypes.FLOAT),
        ("race_sector",					DataTypes.FLOAT),
        ("sector_time_1",				DataTypes.FLOAT),
        ("sector_time_2",				DataTypes.FLOAT),
        ("brake_temp_rl",				DataTypes.FLOAT),
        ("brake_temp_rr",				DataTypes.FLOAT),
        ("brake_temp_fl",				DataTypes.FLOAT),
        ("brake_temp_fr",				DataTypes.FLOAT),
		("tyre_pressure_rl",			DataTypes.FLOAT),
		("tyre_pressure_rr",			DataTypes.FLOAT),
		("tyre_pressure_fl",			DataTypes.FLOAT),
		("tyre_pressure_fr",			DataTypes.FLOAT),
		("laps_completed",				DataTypes.FLOAT),
        ("total_laps",					DataTypes.FLOAT),
        ("track_length",				DataTypes.FLOAT),
        ("last_lap_time",				DataTypes.FLOAT),
        ("max_rpm",						DataTypes.FLOAT),
        ("idle_rpm",					DataTypes.FLOAT),
        ("max_gears",					DataTypes.FLOAT),
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
        0: (Mode0, Mode1, Mode2, Mode3),
    }

