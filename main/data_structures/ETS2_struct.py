import ctypes
from enum import Enum

# source
# https://github.com/truckermudgeon/scs-sdk-plugin
# https://github.com/truckermudgeon/scs-sdk-plugin/blob/master/scs-telemetry/inc/scs-telemetry-common.hpp

class DataTypes(Enum):
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


class scsTrailer(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        # Zone 1 - bools (offset 0)
        ("con_b_wheelSteerable",    DataTypes.BOOL.value * 16),
        ("con_b_wheelSimulated",    DataTypes.BOOL.value * 16),
        ("con_b_wheelPowered",      DataTypes.BOOL.value * 16),
        ("con_b_wheelLiftable",     DataTypes.BOOL.value * 16),
        ("com_b_wheelOnGround",     DataTypes.BOOL.value * 16),
        ("com_b_attached",          DataTypes.BOOL.value),
        ("_buf_b",                  DataTypes.UNSIGNED_INT8.value * 3),

        # Zone 2 - uints (offset 84)
        ("com_ui_wheelSubstance",   DataTypes.UNSIGNED_INT32.value * 16),
        ("con_ui_wheelCount",       DataTypes.UNSIGNED_INT32.value),
        
        # Zone 3 - floats (offset 152)
        ("com_f_cargoDamage",           DataTypes.FLOAT.value),
        ("com_f_wearChassis",           DataTypes.FLOAT.value),
        ("com_f_wearWheels",            DataTypes.FLOAT.value),
        ("com_f_wearBody",              DataTypes.FLOAT.value),
        ("com_f_wheelSuspDeflection",   DataTypes.FLOAT.value * 16),
        ("com_f_wheelVelocity",         DataTypes.FLOAT.value * 16),
        ("com_f_wheelSteering",         DataTypes.FLOAT.value * 16),
        ("com_f_wheelRotation",         DataTypes.FLOAT.value * 16),
        ("com_f_wheelLift",             DataTypes.FLOAT.value * 16),
        ("com_f_wheelLiftOffset",       DataTypes.FLOAT.value * 16),
        ("con_f_wheelRadius",           DataTypes.FLOAT.value * 16),

        # Zone 4 - float vectors (offset 616)
        ("com_fv_linearVelocityX",  DataTypes.FLOAT.value),
        ("com_fv_linearVelocityY",  DataTypes.FLOAT.value),
        ("com_fv_linearVelocityZ",  DataTypes.FLOAT.value),
        ("com_fv_angularVelocityX", DataTypes.FLOAT.value),
        ("com_fv_angularVelocityY", DataTypes.FLOAT.value),
        ("com_fv_angularVelocityZ", DataTypes.FLOAT.value),
        ("com_fv_linearAccelX",     DataTypes.FLOAT.value),
        ("com_fv_linearAccelY",     DataTypes.FLOAT.value),
        ("com_fv_linearAccelZ",     DataTypes.FLOAT.value),
        ("com_fv_angularAccelX",    DataTypes.FLOAT.value),
        ("com_fv_angularAccelY",    DataTypes.FLOAT.value),
        ("com_fv_angularAccelZ",    DataTypes.FLOAT.value),
        ("con_fv_hookPositionX",    DataTypes.FLOAT.value),
        ("con_fv_hookPositionY",    DataTypes.FLOAT.value),
        ("con_fv_hookPositionZ",    DataTypes.FLOAT.value),
        ("con_fv_wheelPositionX",   DataTypes.FLOAT.value * 16),
        ("con_fv_wheelPositionY",   DataTypes.FLOAT.value * 16),
        ("con_fv_wheelPositionZ",   DataTypes.FLOAT.value * 16),
        ("_buf_fv",                 DataTypes.UNSIGNED_INT8.value * 4),
        
        # Zone 5 - doubles (offset 872)
        ("com_dp_worldX",       DataTypes.DOUBLE.value),
        ("com_dp_worldY",       DataTypes.DOUBLE.value),
        ("com_dp_worldZ",       DataTypes.DOUBLE.value),
        ("com_dp_rotationX",    DataTypes.DOUBLE.value),
        ("com_dp_rotationY",    DataTypes.DOUBLE.value),
        ("com_dp_rotationZ",    DataTypes.DOUBLE.value),
        
        # Zone 6 - strings (offset 920)
        ("con_s_id",                    DataTypes.CHAR.value * 64),
        ("con_s_cargoAccessoryId",      DataTypes.CHAR.value * 64),
        ("con_s_bodyType",              DataTypes.CHAR.value * 64),
        ("con_s_brandId",               DataTypes.CHAR.value * 64),
        ("con_s_brand",                 DataTypes.CHAR.value * 64),
        ("con_s_name",                  DataTypes.CHAR.value * 64),
        ("con_s_chainType",             DataTypes.CHAR.value * 64),
        ("con_s_licensePlate",          DataTypes.CHAR.value * 64),
        ("con_s_licensePlateCountry",   DataTypes.CHAR.value * 64),
        ("con_s_licensePlateCountryId", DataTypes.CHAR.value * 64),
    ]


class scsTelemetryMapData(DataTypes.STRUCTURE.value):
    _pack_ = 1
    _fields_ = [
        # Zone 1 - control flags (offset 0)
        ("sdkActive",               DataTypes.BOOL.value),
        ("_pad1",                   DataTypes.UNSIGNED_INT8.value * 3),
        ("paused",                  DataTypes.BOOL.value),
        ("_pad2",                   DataTypes.UNSIGNED_INT8.value * 3),
        ("time",                    DataTypes.UNSIGNED_INT64.value),
        ("simulatedTime",           DataTypes.UNSIGNED_INT64.value),
        ("renderTime",              DataTypes.UNSIGNED_INT64.value),
        ("multiplayerTimeOffset",   DataTypes.SIGNED_INT64.value),

        # Zone 2 — unsigned ints (offset 40)
        # scs_values
        ("telemetry_plugin_revision",       DataTypes.UNSIGNED_INT32.value),
        ("version_major",                   DataTypes.UNSIGNED_INT32.value),
        ("version_minor",                   DataTypes.UNSIGNED_INT32.value),
        ("game",                            DataTypes.UNSIGNED_INT32.value),    # 1=ETS2, 2=ATS
        ("telemetry_version_game_major",    DataTypes.UNSIGNED_INT32.value),
        ("telemetry_version_game_minor",    DataTypes.UNSIGNED_INT32.value),
        # common_ui
        ("time_abs",    DataTypes.UNSIGNED_INT32.value),    # in-game minutes
        # config_ui
        ("gears",               DataTypes.UNSIGNED_INT32.value),
        ("gears_reverse",       DataTypes.UNSIGNED_INT32.value),
        ("retarderStepCount",   DataTypes.UNSIGNED_INT32.value),
        ("truckWheelCount",     DataTypes.UNSIGNED_INT32.value),
        ("selectorCount",       DataTypes.UNSIGNED_INT32.value),
        ("time_abs_delivery",   DataTypes.UNSIGNED_INT32.value),
        ("maxTrailerCount",     DataTypes.UNSIGNED_INT32.value),
        ("unitCount",           DataTypes.UNSIGNED_INT32.value),
        ("plannedDistanceKm",   DataTypes.UNSIGNED_INT32.value),
        # truck_ui
        ("shifterSlot",             DataTypes.UNSIGNED_INT32.value),
        ("retarderBrake",           DataTypes.UNSIGNED_INT32.value),
        ("lightsAuxFront",          DataTypes.UNSIGNED_INT32.value),
        ("lightsAuxRoof",           DataTypes.UNSIGNED_INT32.value),
        ("truck_wheelSubstance",    DataTypes.UNSIGNED_INT32.value * 16),
        ("hshifterPosition",        DataTypes.UNSIGNED_INT32.value * 32),
        ("hshifterBitmask",         DataTypes.UNSIGNED_INT32.value * 32),
        # gameplay_ui
        ("jobDeliveredDeliveryTime",    DataTypes.UNSIGNED_INT32.value),
        ("jobStartingTime",             DataTypes.UNSIGNED_INT32.value),
        ("jobFinishedTime",             DataTypes.UNSIGNED_INT32.value),
        ("_buf_ui",                     DataTypes.UNSIGNED_INT8.value * 48),

        # Zone 3 — signed ints (offset 500)
        ("restStop",                DataTypes.SIGNED_INT32.value),
        ("gear",                    DataTypes.SIGNED_INT32.value),
        ("gearDashboard",           DataTypes.SIGNED_INT32.value),
        ("hshifterResulting",       DataTypes.SIGNED_INT32.value * 32),
        ("jobDeliveredEarnedXp",    DataTypes.SIGNED_INT32.value),
        ("_buf_i",                  DataTypes.UNSIGNED_INT8.value * 56),

        # Zone 4 — floats (offset 700)
        ("scale",   DataTypes.FLOAT.value),
        # config_f
        ("fuelCapacity",            DataTypes.FLOAT.value),
        ("fuelWarningFactor",       DataTypes.FLOAT.value),
        ("adblueCapacity",          DataTypes.FLOAT.value),
        ("adblueWarningFactor",     DataTypes.FLOAT.value),
        ("airPressureWarning",      DataTypes.FLOAT.value),
        ("airPressureEmergency",    DataTypes.FLOAT.value),
        ("oilPressureWarning",      DataTypes.FLOAT.value),
        ("waterTemperatureWarning", DataTypes.FLOAT.value),
        ("batteryVoltageWarning",   DataTypes.FLOAT.value),
        ("engineRpmMax",            DataTypes.FLOAT.value),
        ("gearDifferential",        DataTypes.FLOAT.value),
        ("cargoMass",               DataTypes.FLOAT.value),
        ("truckWheelRadius",        DataTypes.FLOAT.value * 16),
        ("gearRatiosForward",       DataTypes.FLOAT.value * 24),
        ("gearRatiosReverse",       DataTypes.FLOAT.value * 8),
        ("unitMass",                DataTypes.FLOAT.value),
        # truck_f
        ("speed",                       DataTypes.FLOAT.value), # m/s
        ("engineRpm",                   DataTypes.FLOAT.value),
        ("userSteer",                   DataTypes.FLOAT.value),
        ("userThrottle",                DataTypes.FLOAT.value),
        ("userBrake",                   DataTypes.FLOAT.value),
        ("userClutch",                  DataTypes.FLOAT.value),
        ("gameSteer",                   DataTypes.FLOAT.value),
        ("gameThrottle",                DataTypes.FLOAT.value),
        ("gameBrake",                   DataTypes.FLOAT.value),
        ("gameClutch",                  DataTypes.FLOAT.value),
        ("cruiseControlSpeed",          DataTypes.FLOAT.value),
        ("airPressure",                 DataTypes.FLOAT.value),
        ("brakeTemperature",            DataTypes.FLOAT.value),
        ("fuel",                        DataTypes.FLOAT.value),
        ("fuelAvgConsumption",          DataTypes.FLOAT.value),
        ("fuelRange",                   DataTypes.FLOAT.value),
        ("adblue",                      DataTypes.FLOAT.value),
        ("oilPressure",                 DataTypes.FLOAT.value),
        ("oilTemperature",              DataTypes.FLOAT.value),
        ("waterTemperature",            DataTypes.FLOAT.value),
        ("batteryVoltage",              DataTypes.FLOAT.value),
        ("lightsDashboard",             DataTypes.FLOAT.value),
        ("wearEngine",                  DataTypes.FLOAT.value),
        ("wearTransmission",            DataTypes.FLOAT.value),
        ("wearCabin",                   DataTypes.FLOAT.value),
        ("wearChassis",                 DataTypes.FLOAT.value),
        ("wearWheels",                  DataTypes.FLOAT.value),
        ("truckOdometer",               DataTypes.FLOAT.value),
        ("routeDistance",               DataTypes.FLOAT.value),
        ("routeTime",                   DataTypes.FLOAT.value),
        ("speedLimit",                  DataTypes.FLOAT.value), # m/s
        ("truck_wheelSuspDeflection",   DataTypes.FLOAT.value * 16),
        ("truck_wheelVelocity",         DataTypes.FLOAT.value * 16),
        ("truck_wheelSteering",         DataTypes.FLOAT.value * 16),
        ("truck_wheelRotation",         DataTypes.FLOAT.value * 16),
        ("truck_wheelLift",             DataTypes.FLOAT.value * 16),
        ("truck_wheelLiftOffset",       DataTypes.FLOAT.value * 16),
        # gameplay_f
        ("jobDeliveredCargoDamage", DataTypes.FLOAT.value),
        ("jobDeliveredDistanceKm",  DataTypes.FLOAT.value),
        ("refuelAmount",            DataTypes.FLOAT.value),
        ("cargoDamage",             DataTypes.FLOAT.value),
        ("_buf_f",                  DataTypes.UNSIGNED_INT8.value * 28),

        # Zone 5 — bools (offset 1500)
        ("truckWheelSteerable",         DataTypes.FLOAT.value * 16),
        ("truckWheelSimulated",         DataTypes.BOOL.value * 16),
        ("truckWheelPowered",           DataTypes.BOOL.value * 16),
        ("truckWheelLiftable",          DataTypes.BOOL.value * 16),
        ("isCargoLoaded",               DataTypes.BOOL.value),
        ("specialJob",                  DataTypes.BOOL.value),
        ("parkBrake",                   DataTypes.BOOL.value),
        ("motorBrake",                  DataTypes.BOOL.value),
        ("airPressureWarning",          DataTypes.BOOL.value),
        ("airPressureEmergency",        DataTypes.BOOL.value),
        ("fuelWarning",                 DataTypes.BOOL.value),
        ("adblueWarning",               DataTypes.BOOL.value),
        ("oilPressureWarning",          DataTypes.BOOL.value),
        ("waterTemperatureWarning",     DataTypes.BOOL.value),
        ("batteryVoltageWarning",       DataTypes.BOOL.value),
        ("electricEnabled",             DataTypes.BOOL.value),
        ("engineEnabled",               DataTypes.BOOL.value),
        ("wipers",                      DataTypes.BOOL.value),
        ("blinkerLeftActive",           DataTypes.BOOL.value),
        ("blinkerRightActive",          DataTypes.BOOL.value),
        ("blinkerLeftOn",               DataTypes.BOOL.value),
        ("blinkerRightOn",              DataTypes.BOOL.value),
        ("lightsParking",               DataTypes.BOOL.value),
        ("lightsBeamLow",               DataTypes.BOOL.value),
        ("lightsBeamHigh",              DataTypes.BOOL.value),
        ("lightsBeacon",                DataTypes.BOOL.value),
        ("lightsBrake",                 DataTypes.BOOL.value),
        ("lightsReverse",               DataTypes.BOOL.value),
        ("lightsHazard",                DataTypes.BOOL.value),
        ("cruiseControl",               DataTypes.BOOL.value),
        ("truck_wheelOnGround",         DataTypes.BOOL.value * 16),
        ("shifterToggle",               DataTypes.BOOL.value * 2),
        ("differentialLock",            DataTypes.BOOL.value),
        ("liftAxle",                    DataTypes.BOOL.value),
        ("liftAxleIndicator",           DataTypes.BOOL.value),
        ("trailerLiftAxle",             DataTypes.BOOL.value),
        ("trailerLiftAxleIndicator",    DataTypes.BOOL.value),
        ("jobDeliveredAutoparkUsed",    DataTypes.BOOL.value),
        ("jobDeliveredAutoloadUsed",    DataTypes.BOOL.value),
        ("_buf_b",                      DataTypes.UNSIGNED_INT8.value * 25),

        # Zone 6 — float vectors (offset 1640)
        ("cabinPositionX",      DataTypes.FLOAT.value),
        ("cabinPositionY",      DataTypes.FLOAT.value),
        ("cabinPositionZ",      DataTypes.FLOAT.value),
        ("headPositionX",       DataTypes.FLOAT.value),
        ("headPositionZ",       DataTypes.FLOAT.value),
        ("truckHookPositionX",  DataTypes.FLOAT.value),
        ("truckHookPositionY",  DataTypes.FLOAT.value),
        ("truckHookPositionZ",  DataTypes.FLOAT.value),
        ("truckWheelPositionX", DataTypes.FLOAT.value * 16),
        ("truckWheelPositionY", DataTypes.FLOAT.value * 16),
        ("truckWheelPositionZ", DataTypes.FLOAT.value * 16),
        ("lv_accelerationX",    DataTypes.FLOAT.value),
        ("lv_accelerationY",    DataTypes.FLOAT.value),
        ("lv_accelerationZ",    DataTypes.FLOAT.value),
        ("av_accelerationX",    DataTypes.FLOAT.value),
        ("av_accelerationY",    DataTypes.FLOAT.value),
        ("av_accelerationZ",    DataTypes.FLOAT.value),
        ("accelerationX",       DataTypes.FLOAT.value),
        ("accelerationY",       DataTypes.FLOAT.value),
        ("accelerationZ",       DataTypes.FLOAT.value),
        ("aa_accelerationX",    DataTypes.FLOAT.value),
        ("aa_accelerationY",    DataTypes.FLOAT.value),
        ("aa_accelerationZ",    DataTypes.FLOAT.value),
        ("cabinAVX",            DataTypes.FLOAT.value),
        ("cabinAVY",            DataTypes.FLOAT.value),
        ("cabinAVZ",            DataTypes.FLOAT.value),
        ("cabinAAX",            DataTypes.FLOAT.value),
        ("cabinAAY",            DataTypes.FLOAT.value),
        ("cabinAAZ",            DataTypes.FLOAT.value),
        ("_buf_fv",             DataTypes.UNSIGNED_INT8.value * 60),

        # Zone 7 — float placements (offset 2000)
        ("cabinOffsetX",            DataTypes.FLOAT.value),
        ("cabinOffsetY",            DataTypes.FLOAT.value),
        ("cabinOffsetZ",            DataTypes.FLOAT.value),
        ("cabinOffsetRotationX",    DataTypes.FLOAT.value),
        ("cabinOffsetRotationY",    DataTypes.FLOAT.value),
        ("cabinOffsetRotationZ",    DataTypes.FLOAT.value),
        ("headOffsetX",             DataTypes.FLOAT.value),
        ("headOffsetY",             DataTypes.FLOAT.value),
        ("headOffsetZ",             DataTypes.FLOAT.value),
        ("headOffsetRotationX",     DataTypes.FLOAT.value),
        ("headOffsetRotationY",     DataTypes.FLOAT.value),
        ("headOffsetRotationZ",     DataTypes.FLOAT.value),
        ("_buf_fp",                 DataTypes.UNSIGNED_INT8.value * 152),

        # Zone 8 — double placements (offset 2200)
        ("coordinateX", DataTypes.DOUBLE.value),
        ("coordinateY", DataTypes.DOUBLE.value),
        ("coordinateZ", DataTypes.DOUBLE.value),
        ("rotationX",   DataTypes.DOUBLE.value),
        ("rotationY",   DataTypes.DOUBLE.value),
        ("rotationZ",   DataTypes.DOUBLE.value),
        ("_buf_dp",     DataTypes.UNSIGNED_INT8.value * 52),

        # Zone 9 — strings (offset 2300)
        ("truckBrandId",                DataTypes.CHAR.value * 64),
        ("truckBrand",                  DataTypes.CHAR.value * 64),
        ("truckId",                     DataTypes.CHAR.value * 64),
        ("truckName",                   DataTypes.CHAR.value * 64),
        ("cargoId",                     DataTypes.CHAR.value * 64),
        ("cargo",                       DataTypes.CHAR.value * 64),
        ("cityDstId",                   DataTypes.CHAR.value * 64),
        ("cityDst",                     DataTypes.CHAR.value * 64),
        ("compDstId",                   DataTypes.CHAR.value * 64),
        ("compDst",                     DataTypes.CHAR.value * 64),
        ("citySrcId",                   DataTypes.CHAR.value * 64),
        ("citySrc",                     DataTypes.CHAR.value * 64),
        ("compSrcId",                   DataTypes.CHAR.value * 64),
        ("compSrc",                     DataTypes.CHAR.value * 64),
        ("shifterType",                 DataTypes.CHAR.value * 16),
        ("truckLicensePlate",           DataTypes.CHAR.value * 64),
        ("truckLicensePlateCountryId",  DataTypes.CHAR.value * 64),
        ("truckLicensePlateCountry",    DataTypes.CHAR.value * 64),
        ("jobMarket",                   DataTypes.CHAR.value * 32),
        ("fineOffence",                 DataTypes.CHAR.value * 32),
        ("ferrySourceName",             DataTypes.CHAR.value * 64),
        ("ferryTargetName",             DataTypes.CHAR.value * 64),
        ("ferrySourceId",               DataTypes.CHAR.value * 64),
        ("ferryTargetId",               DataTypes.CHAR.value * 64),
        ("trainSourceName",             DataTypes.CHAR.value * 64),
        ("trainTargetName",             DataTypes.CHAR.value * 64),
        ("trainSourceId",               DataTypes.CHAR.value * 64),
        ("trainTargetId",               DataTypes.CHAR.value * 64),
        ("_buf_s",                      DataTypes.UNSIGNED_INT8.value * 20),

        # Zone 10 — unsigned long long (offset 4000)
        ("jobIncome",   DataTypes.UNSIGNED_INT64.value),
        ("_buf_ull",    DataTypes.UNSIGNED_INT8.value * 192),
        
        # Zone 11 — long long (offset 4200)
        ("jobCancelledPenalty", DataTypes.SIGNED_INT64.value),
        ("jobDeliveredRevenue", DataTypes.SIGNED_INT64.value),
        ("fineAmount",          DataTypes.SIGNED_INT64.value),
        ("tollgatePayAmount",   DataTypes.SIGNED_INT64.value),
        ("ferryPayAmount",      DataTypes.SIGNED_INT64.value),
        ("trainPayAmount",      DataTypes.SIGNED_INT64.value),
        ("_buf_ll",             DataTypes.UNSIGNED_INT8.value * 52),
        
        # Zone 12 — special events (offset 4300)
        ("onJob",           DataTypes.BOOL.value),
        ("jobFinished",     DataTypes.BOOL.value),
        ("jobCancelled",    DataTypes.BOOL.value),
        ("jobDelivered",    DataTypes.BOOL.value),
        ("fined",           DataTypes.BOOL.value),
        ("tollgate",        DataTypes.BOOL.value),
        ("ferry",           DataTypes.BOOL.value),
        ("train",           DataTypes.BOOL.value),
        ("refuel",          DataTypes.BOOL.value),
        ("refuelPayed",     DataTypes.BOOL.value),
        ("_buf_special",    DataTypes.UNSIGNED_INT8.value * 90),
        
        # Zone 13 — substances (offset 4400)
        ("substances",  DataTypes.CHAR.value * 64 * 25),
        # Zone 14 — trailers (offset 6000)
        ("trailers",    scsTrailer * 10),
    ]


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
    headerInfo: tuple[int, type | None] = (0, None)
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = "Local\\SCSTelemetry"
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (scsTelemetryMapData, ),
    }