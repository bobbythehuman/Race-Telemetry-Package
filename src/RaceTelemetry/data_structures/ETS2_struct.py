import ctypes


# source
# https://github.com/truckermudgeon/scs-sdk-plugin
# https://github.com/truckermudgeon/scs-sdk-plugin/blob/master/scs-telemetry/inc/scs-telemetry-common.hpp


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


### * Data Structure

class scsTrailer(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        # Zone 1 - bools (offset 0)
        ("con_b_wheelSteerable",    DataTypes.BOOL * 16),
        ("con_b_wheelSimulated",    DataTypes.BOOL * 16),
        ("con_b_wheelPowered",      DataTypes.BOOL * 16),
        ("con_b_wheelLiftable",     DataTypes.BOOL * 16),
        ("com_b_wheelOnGround",     DataTypes.BOOL * 16),
        ("com_b_attached",          DataTypes.BOOL),
        ("_buf_b",                  DataTypes.UNSIGNED_INT8 * 3),

        # Zone 2 - uints (offset 84)
        ("com_ui_wheelSubstance",   DataTypes.UNSIGNED_INT32 * 16),
        ("con_ui_wheelCount",       DataTypes.UNSIGNED_INT32),
        
        # Zone 3 - floats (offset 152)
        ("com_f_cargoDamage",           DataTypes.FLOAT),
        ("com_f_wearChassis",           DataTypes.FLOAT),
        ("com_f_wearWheels",            DataTypes.FLOAT),
        ("com_f_wearBody",              DataTypes.FLOAT),
        ("com_f_wheelSuspDeflection",   DataTypes.FLOAT * 16),
        ("com_f_wheelVelocity",         DataTypes.FLOAT * 16),
        ("com_f_wheelSteering",         DataTypes.FLOAT * 16),
        ("com_f_wheelRotation",         DataTypes.FLOAT * 16),
        ("com_f_wheelLift",             DataTypes.FLOAT * 16),
        ("com_f_wheelLiftOffset",       DataTypes.FLOAT * 16),
        ("con_f_wheelRadius",           DataTypes.FLOAT * 16),

        # Zone 4 - float vectors (offset 616)
        ("com_fv_linearVelocityX",  DataTypes.FLOAT),
        ("com_fv_linearVelocityY",  DataTypes.FLOAT),
        ("com_fv_linearVelocityZ",  DataTypes.FLOAT),
        ("com_fv_angularVelocityX", DataTypes.FLOAT),
        ("com_fv_angularVelocityY", DataTypes.FLOAT),
        ("com_fv_angularVelocityZ", DataTypes.FLOAT),
        ("com_fv_linearAccelX",     DataTypes.FLOAT),
        ("com_fv_linearAccelY",     DataTypes.FLOAT),
        ("com_fv_linearAccelZ",     DataTypes.FLOAT),
        ("com_fv_angularAccelX",    DataTypes.FLOAT),
        ("com_fv_angularAccelY",    DataTypes.FLOAT),
        ("com_fv_angularAccelZ",    DataTypes.FLOAT),
        ("con_fv_hookPositionX",    DataTypes.FLOAT),
        ("con_fv_hookPositionY",    DataTypes.FLOAT),
        ("con_fv_hookPositionZ",    DataTypes.FLOAT),
        ("con_fv_wheelPositionX",   DataTypes.FLOAT * 16),
        ("con_fv_wheelPositionY",   DataTypes.FLOAT * 16),
        ("con_fv_wheelPositionZ",   DataTypes.FLOAT * 16),
        ("_buf_fv",                 DataTypes.UNSIGNED_INT8 * 4),
        
        # Zone 5 - doubles (offset 872)
        ("com_dp_worldX",       DataTypes.DOUBLE),
        ("com_dp_worldY",       DataTypes.DOUBLE),
        ("com_dp_worldZ",       DataTypes.DOUBLE),
        ("com_dp_rotationX",    DataTypes.DOUBLE),
        ("com_dp_rotationY",    DataTypes.DOUBLE),
        ("com_dp_rotationZ",    DataTypes.DOUBLE),
        
        # Zone 6 - strings (offset 920)
        ("con_s_id",                    DataTypes.CHAR * 64),
        ("con_s_cargoAccessoryId",      DataTypes.CHAR * 64),
        ("con_s_bodyType",              DataTypes.CHAR * 64),
        ("con_s_brandId",               DataTypes.CHAR * 64),
        ("con_s_brand",                 DataTypes.CHAR * 64),
        ("con_s_name",                  DataTypes.CHAR * 64),
        ("con_s_chainType",             DataTypes.CHAR * 64),
        ("con_s_licensePlate",          DataTypes.CHAR * 64),
        ("con_s_licensePlateCountry",   DataTypes.CHAR * 64),
        ("con_s_licensePlateCountryId", DataTypes.CHAR * 64),
    ]


class scsTelemetryMapData(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        # Zone 1 - control flags (offset 0)
        ("sdkActive",               DataTypes.BOOL),
        ("_pad1",                   DataTypes.UNSIGNED_INT8 * 3),
        ("paused",                  DataTypes.BOOL),
        ("_pad2",                   DataTypes.UNSIGNED_INT8 * 3),
        ("time",                    DataTypes.UNSIGNED_INT64),
        ("simulatedTime",           DataTypes.UNSIGNED_INT64),
        ("renderTime",              DataTypes.UNSIGNED_INT64),
        ("multiplayerTimeOffset",   DataTypes.SIGNED_INT64),

        # Zone 2 — unsigned ints (offset 40)
        # scs_values
        ("telemetry_plugin_revision",       DataTypes.UNSIGNED_INT32),
        ("version_major",                   DataTypes.UNSIGNED_INT32),
        ("version_minor",                   DataTypes.UNSIGNED_INT32),
        ("game",                            DataTypes.UNSIGNED_INT32),    # 1=ETS2, 2=ATS
        ("telemetry_version_game_major",    DataTypes.UNSIGNED_INT32),
        ("telemetry_version_game_minor",    DataTypes.UNSIGNED_INT32),
        # common_ui
        ("time_abs",    DataTypes.UNSIGNED_INT32),    # in-game minutes
        # config_ui
        ("gears",               DataTypes.UNSIGNED_INT32),
        ("gears_reverse",       DataTypes.UNSIGNED_INT32),
        ("retarderStepCount",   DataTypes.UNSIGNED_INT32),
        ("truckWheelCount",     DataTypes.UNSIGNED_INT32),
        ("selectorCount",       DataTypes.UNSIGNED_INT32),
        ("time_abs_delivery",   DataTypes.UNSIGNED_INT32),
        ("maxTrailerCount",     DataTypes.UNSIGNED_INT32),
        ("unitCount",           DataTypes.UNSIGNED_INT32),
        ("plannedDistanceKm",   DataTypes.UNSIGNED_INT32),
        # truck_ui
        ("shifterSlot",             DataTypes.UNSIGNED_INT32),
        ("retarderBrake",           DataTypes.UNSIGNED_INT32),
        ("lightsAuxFront",          DataTypes.UNSIGNED_INT32),
        ("lightsAuxRoof",           DataTypes.UNSIGNED_INT32),
        ("truck_wheelSubstance",    DataTypes.UNSIGNED_INT32 * 16),
        ("hshifterPosition",        DataTypes.UNSIGNED_INT32 * 32),
        ("hshifterBitmask",         DataTypes.UNSIGNED_INT32 * 32),
        # gameplay_ui
        ("jobDeliveredDeliveryTime",    DataTypes.UNSIGNED_INT32),
        ("jobStartingTime",             DataTypes.UNSIGNED_INT32),
        ("jobFinishedTime",             DataTypes.UNSIGNED_INT32),
        ("_buf_ui",                     DataTypes.UNSIGNED_INT8 * 48),

        # Zone 3 — signed ints (offset 500)
        ("restStop",                DataTypes.SIGNED_INT32),
        ("gear",                    DataTypes.SIGNED_INT32),
        ("gearDashboard",           DataTypes.SIGNED_INT32),
        ("hshifterResulting",       DataTypes.SIGNED_INT32 * 32),
        ("jobDeliveredEarnedXp",    DataTypes.SIGNED_INT32),
        ("_buf_i",                  DataTypes.UNSIGNED_INT8 * 56),

        # Zone 4 — floats (offset 700)
        ("scale",   DataTypes.FLOAT),
        # config_f
        ("fuelCapacity",            DataTypes.FLOAT),
        ("fuelWarningFactor",       DataTypes.FLOAT),
        ("adblueCapacity",          DataTypes.FLOAT),
        ("adblueWarningFactor",     DataTypes.FLOAT),
        ("airPressureWarning",      DataTypes.FLOAT),
        ("airPressureEmergency",    DataTypes.FLOAT),
        ("oilPressureWarning",      DataTypes.FLOAT),
        ("waterTemperatureWarning", DataTypes.FLOAT),
        ("batteryVoltageWarning",   DataTypes.FLOAT),
        ("engineRpmMax",            DataTypes.FLOAT),
        ("gearDifferential",        DataTypes.FLOAT),
        ("cargoMass",               DataTypes.FLOAT),
        ("truckWheelRadius",        DataTypes.FLOAT * 16),
        ("gearRatiosForward",       DataTypes.FLOAT * 24),
        ("gearRatiosReverse",       DataTypes.FLOAT * 8),
        ("unitMass",                DataTypes.FLOAT),
        # truck_f
        ("speed",                       DataTypes.FLOAT), # m/s
        ("engineRpm",                   DataTypes.FLOAT),
        ("userSteer",                   DataTypes.FLOAT),
        ("userThrottle",                DataTypes.FLOAT),
        ("userBrake",                   DataTypes.FLOAT),
        ("userClutch",                  DataTypes.FLOAT),
        ("gameSteer",                   DataTypes.FLOAT),
        ("gameThrottle",                DataTypes.FLOAT),
        ("gameBrake",                   DataTypes.FLOAT),
        ("gameClutch",                  DataTypes.FLOAT),
        ("cruiseControlSpeed",          DataTypes.FLOAT),
        ("airPressure",                 DataTypes.FLOAT),
        ("brakeTemperature",            DataTypes.FLOAT),
        ("fuel",                        DataTypes.FLOAT),
        ("fuelAvgConsumption",          DataTypes.FLOAT),
        ("fuelRange",                   DataTypes.FLOAT),
        ("adblue",                      DataTypes.FLOAT),
        ("oilPressure",                 DataTypes.FLOAT),
        ("oilTemperature",              DataTypes.FLOAT),
        ("waterTemperature",            DataTypes.FLOAT),
        ("batteryVoltage",              DataTypes.FLOAT),
        ("lightsDashboard",             DataTypes.FLOAT),
        ("wearEngine",                  DataTypes.FLOAT),
        ("wearTransmission",            DataTypes.FLOAT),
        ("wearCabin",                   DataTypes.FLOAT),
        ("wearChassis",                 DataTypes.FLOAT),
        ("wearWheels",                  DataTypes.FLOAT),
        ("truckOdometer",               DataTypes.FLOAT),
        ("routeDistance",               DataTypes.FLOAT),
        ("routeTime",                   DataTypes.FLOAT),
        ("speedLimit",                  DataTypes.FLOAT), # m/s
        ("truck_wheelSuspDeflection",   DataTypes.FLOAT * 16),
        ("truck_wheelVelocity",         DataTypes.FLOAT * 16),
        ("truck_wheelSteering",         DataTypes.FLOAT * 16),
        ("truck_wheelRotation",         DataTypes.FLOAT * 16),
        ("truck_wheelLift",             DataTypes.FLOAT * 16),
        ("truck_wheelLiftOffset",       DataTypes.FLOAT * 16),
        # gameplay_f
        ("jobDeliveredCargoDamage", DataTypes.FLOAT),
        ("jobDeliveredDistanceKm",  DataTypes.FLOAT),
        ("refuelAmount",            DataTypes.FLOAT),
        ("cargoDamage",             DataTypes.FLOAT),
        ("_buf_f",                  DataTypes.UNSIGNED_INT8 * 28),

        # Zone 5 — bools (offset 1500)
        ("truckWheelSteerable",         DataTypes.FLOAT * 16),
        ("truckWheelSimulated",         DataTypes.BOOL * 16),
        ("truckWheelPowered",           DataTypes.BOOL * 16),
        ("truckWheelLiftable",          DataTypes.BOOL * 16),
        ("isCargoLoaded",               DataTypes.BOOL),
        ("specialJob",                  DataTypes.BOOL),
        ("parkBrake",                   DataTypes.BOOL),
        ("motorBrake",                  DataTypes.BOOL),
        ("airPressureWarning",          DataTypes.BOOL),
        ("airPressureEmergency",        DataTypes.BOOL),
        ("fuelWarning",                 DataTypes.BOOL),
        ("adblueWarning",               DataTypes.BOOL),
        ("oilPressureWarning",          DataTypes.BOOL),
        ("waterTemperatureWarning",     DataTypes.BOOL),
        ("batteryVoltageWarning",       DataTypes.BOOL),
        ("electricEnabled",             DataTypes.BOOL),
        ("engineEnabled",               DataTypes.BOOL),
        ("wipers",                      DataTypes.BOOL),
        ("blinkerLeftActive",           DataTypes.BOOL),
        ("blinkerRightActive",          DataTypes.BOOL),
        ("blinkerLeftOn",               DataTypes.BOOL),
        ("blinkerRightOn",              DataTypes.BOOL),
        ("lightsParking",               DataTypes.BOOL),
        ("lightsBeamLow",               DataTypes.BOOL),
        ("lightsBeamHigh",              DataTypes.BOOL),
        ("lightsBeacon",                DataTypes.BOOL),
        ("lightsBrake",                 DataTypes.BOOL),
        ("lightsReverse",               DataTypes.BOOL),
        ("lightsHazard",                DataTypes.BOOL),
        ("cruiseControl",               DataTypes.BOOL),
        ("truck_wheelOnGround",         DataTypes.BOOL * 16),
        ("shifterToggle",               DataTypes.BOOL * 2),
        ("differentialLock",            DataTypes.BOOL),
        ("liftAxle",                    DataTypes.BOOL),
        ("liftAxleIndicator",           DataTypes.BOOL),
        ("trailerLiftAxle",             DataTypes.BOOL),
        ("trailerLiftAxleIndicator",    DataTypes.BOOL),
        ("jobDeliveredAutoparkUsed",    DataTypes.BOOL),
        ("jobDeliveredAutoloadUsed",    DataTypes.BOOL),
        ("_buf_b",                      DataTypes.UNSIGNED_INT8 * 25),

        # Zone 6 — float vectors (offset 1640)
        ("cabinPositionX",      DataTypes.FLOAT),
        ("cabinPositionY",      DataTypes.FLOAT),
        ("cabinPositionZ",      DataTypes.FLOAT),
        ("headPositionX",       DataTypes.FLOAT),
        ("headPositionZ",       DataTypes.FLOAT),
        ("truckHookPositionX",  DataTypes.FLOAT),
        ("truckHookPositionY",  DataTypes.FLOAT),
        ("truckHookPositionZ",  DataTypes.FLOAT),
        ("truckWheelPositionX", DataTypes.FLOAT * 16),
        ("truckWheelPositionY", DataTypes.FLOAT * 16),
        ("truckWheelPositionZ", DataTypes.FLOAT * 16),
        ("lv_accelerationX",    DataTypes.FLOAT),
        ("lv_accelerationY",    DataTypes.FLOAT),
        ("lv_accelerationZ",    DataTypes.FLOAT),
        ("av_accelerationX",    DataTypes.FLOAT),
        ("av_accelerationY",    DataTypes.FLOAT),
        ("av_accelerationZ",    DataTypes.FLOAT),
        ("accelerationX",       DataTypes.FLOAT),
        ("accelerationY",       DataTypes.FLOAT),
        ("accelerationZ",       DataTypes.FLOAT),
        ("aa_accelerationX",    DataTypes.FLOAT),
        ("aa_accelerationY",    DataTypes.FLOAT),
        ("aa_accelerationZ",    DataTypes.FLOAT),
        ("cabinAVX",            DataTypes.FLOAT),
        ("cabinAVY",            DataTypes.FLOAT),
        ("cabinAVZ",            DataTypes.FLOAT),
        ("cabinAAX",            DataTypes.FLOAT),
        ("cabinAAY",            DataTypes.FLOAT),
        ("cabinAAZ",            DataTypes.FLOAT),
        ("_buf_fv",             DataTypes.UNSIGNED_INT8 * 60),

        # Zone 7 — float placements (offset 2000)
        ("cabinOffsetX",            DataTypes.FLOAT),
        ("cabinOffsetY",            DataTypes.FLOAT),
        ("cabinOffsetZ",            DataTypes.FLOAT),
        ("cabinOffsetRotationX",    DataTypes.FLOAT),
        ("cabinOffsetRotationY",    DataTypes.FLOAT),
        ("cabinOffsetRotationZ",    DataTypes.FLOAT),
        ("headOffsetX",             DataTypes.FLOAT),
        ("headOffsetY",             DataTypes.FLOAT),
        ("headOffsetZ",             DataTypes.FLOAT),
        ("headOffsetRotationX",     DataTypes.FLOAT),
        ("headOffsetRotationY",     DataTypes.FLOAT),
        ("headOffsetRotationZ",     DataTypes.FLOAT),
        ("_buf_fp",                 DataTypes.UNSIGNED_INT8 * 152),

        # Zone 8 — double placements (offset 2200)
        ("coordinateX", DataTypes.DOUBLE),
        ("coordinateY", DataTypes.DOUBLE),
        ("coordinateZ", DataTypes.DOUBLE),
        ("rotationX",   DataTypes.DOUBLE),
        ("rotationY",   DataTypes.DOUBLE),
        ("rotationZ",   DataTypes.DOUBLE),
        ("_buf_dp",     DataTypes.UNSIGNED_INT8 * 52),

        # Zone 9 — strings (offset 2300)
        ("truckBrandId",                DataTypes.CHAR * 64),
        ("truckBrand",                  DataTypes.CHAR * 64),
        ("truckId",                     DataTypes.CHAR * 64),
        ("truckName",                   DataTypes.CHAR * 64),
        ("cargoId",                     DataTypes.CHAR * 64),
        ("cargo",                       DataTypes.CHAR * 64),
        ("cityDstId",                   DataTypes.CHAR * 64),
        ("cityDst",                     DataTypes.CHAR * 64),
        ("compDstId",                   DataTypes.CHAR * 64),
        ("compDst",                     DataTypes.CHAR * 64),
        ("citySrcId",                   DataTypes.CHAR * 64),
        ("citySrc",                     DataTypes.CHAR * 64),
        ("compSrcId",                   DataTypes.CHAR * 64),
        ("compSrc",                     DataTypes.CHAR * 64),
        ("shifterType",                 DataTypes.CHAR * 16),
        ("truckLicensePlate",           DataTypes.CHAR * 64),
        ("truckLicensePlateCountryId",  DataTypes.CHAR * 64),
        ("truckLicensePlateCountry",    DataTypes.CHAR * 64),
        ("jobMarket",                   DataTypes.CHAR * 32),
        ("fineOffence",                 DataTypes.CHAR * 32),
        ("ferrySourceName",             DataTypes.CHAR * 64),
        ("ferryTargetName",             DataTypes.CHAR * 64),
        ("ferrySourceId",               DataTypes.CHAR * 64),
        ("ferryTargetId",               DataTypes.CHAR * 64),
        ("trainSourceName",             DataTypes.CHAR * 64),
        ("trainTargetName",             DataTypes.CHAR * 64),
        ("trainSourceId",               DataTypes.CHAR * 64),
        ("trainTargetId",               DataTypes.CHAR * 64),
        ("_buf_s",                      DataTypes.UNSIGNED_INT8 * 20),

        # Zone 10 — unsigned long long (offset 4000)
        ("jobIncome",   DataTypes.UNSIGNED_INT64),
        ("_buf_ull",    DataTypes.UNSIGNED_INT8 * 192),
        
        # Zone 11 — long long (offset 4200)
        ("jobCancelledPenalty", DataTypes.SIGNED_INT64),
        ("jobDeliveredRevenue", DataTypes.SIGNED_INT64),
        ("fineAmount",          DataTypes.SIGNED_INT64),
        ("tollgatePayAmount",   DataTypes.SIGNED_INT64),
        ("ferryPayAmount",      DataTypes.SIGNED_INT64),
        ("trainPayAmount",      DataTypes.SIGNED_INT64),
        ("_buf_ll",             DataTypes.UNSIGNED_INT8 * 52),
        
        # Zone 12 — special events (offset 4300)
        ("onJob",           DataTypes.BOOL),
        ("jobFinished",     DataTypes.BOOL),
        ("jobCancelled",    DataTypes.BOOL),
        ("jobDelivered",    DataTypes.BOOL),
        ("fined",           DataTypes.BOOL),
        ("tollgate",        DataTypes.BOOL),
        ("ferry",           DataTypes.BOOL),
        ("train",           DataTypes.BOOL),
        ("refuel",          DataTypes.BOOL),
        ("refuelPayed",     DataTypes.BOOL),
        ("_buf_special",    DataTypes.UNSIGNED_INT8 * 90),
        
        # Zone 13 — substances (offset 4400)
        ("substances",  DataTypes.CHAR * 64 * 25),
        # Zone 14 — trailers (offset 6000)
        ("trailers",    scsTrailer * 10),
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = None
    
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
    allSharedMemoryNames: str | None | dict[str, str] = "Local\\SCSTelemetry"
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (scsTelemetryMapData, ),
    }