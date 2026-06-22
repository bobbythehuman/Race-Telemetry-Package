import ctypes
from enum import Enum

# source
# https://forums.forza.net/t/data-out-telemetry-variables-and-structure/535984/2
# https://pastebin.com/GFbbzbg3

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT8 = ctypes.c_uint8
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    
    FLOAT = ctypes.c_float


class DashData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("IsRaceOn",            DataTypes.SIGNED_INT32),  # 1 when race is on. = 0 when in menus/race stopped
        # Can overflow to 0 eventually      
        ("TimestampMS",         DataTypes.UNSIGNED_INT32),          
        ("EngineMaxRpm",        DataTypes.FLOAT),
        ("EngineIdleRpm",       DataTypes.FLOAT),
        ("CurrentEngineRpm",    DataTypes.FLOAT),
        # In the car's local space; X = right, Y = up, Z = forward
        ("AccelerationX",       DataTypes.FLOAT),
        ("AccelerationY",       DataTypes.FLOAT),
        ("AccelerationZ",       DataTypes.FLOAT),
        # In the car's local space; X = right, Y = up, Z = forward
        ("VelocityX",           DataTypes.FLOAT),
        ("VelocityY",           DataTypes.FLOAT),
        ("VelocityZ",           DataTypes.FLOAT),
        # In the car's local space; X = pitch, Y = yaw, Z = roll
        ("AngularVelocityX",    DataTypes.FLOAT),
        ("AngularVelocityY",    DataTypes.FLOAT),
        ("AngularVelocityZ",    DataTypes.FLOAT),
        
        ("Yaw",                 DataTypes.FLOAT),
        ("Pitch",               DataTypes.FLOAT),
        ("Roll",                DataTypes.FLOAT),
        # Suspension travel normalized: 0.0f = max stretch; 1.0 = max compression
        ("NormalizedSuspensionTravelFrontLeft",     DataTypes.FLOAT),
        ("NormalizedSuspensionTravelFrontRight",    DataTypes.FLOAT),
        ("NormalizedSuspensionTravelRearLeft",      DataTypes.FLOAT),
        ("NormalizedSuspensionTravelRearRight",     DataTypes.FLOAT),
        # Tire normalized slip ratio, = 0 means 100% grip and |ratio| > 1.0 means loss of grip.
        ("TireSlipRatioFrontLeft",          DataTypes.FLOAT),
        ("TireSlipRatioFrontRight",         DataTypes.FLOAT),
        ("TireSlipRatioRearLeft",           DataTypes.FLOAT),
        ("TireSlipRatioRearRight",          DataTypes.FLOAT),
        # Wheels rotation speed radians/sec. 
        ("WheelRotationSpeedFrontLeft",     DataTypes.FLOAT),
        ("WheelRotationSpeedFrontRight",    DataTypes.FLOAT),
        ("WheelRotationSpeedRearLeft",      DataTypes.FLOAT),
        ("WheelRotationSpeedRearRight",     DataTypes.FLOAT),
        # 1 when wheel is on rumble strip, = 0 when off.
        ("WheelOnRumbleStripFrontLeft",     DataTypes.SIGNED_INT32),
        ("WheelOnRumbleStripFrontRight",    DataTypes.SIGNED_INT32),
        ("WheelOnRumbleStripRearLeft",      DataTypes.SIGNED_INT32),
        ("WheelOnRumbleStripRearRight",     DataTypes.SIGNED_INT32),
        # from 0 to 1, where 1 is the deepest puddle
        ("WheelInPuddleDepthFrontLeft",     DataTypes.FLOAT),
        ("WheelInPuddleDepthFrontRight",    DataTypes.FLOAT),
        ("WheelInPuddleDepthRearLeft",      DataTypes.FLOAT),
        ("WheelInPuddleDepthRearRight",     DataTypes.FLOAT),
        # Non-dimensional surface rumble values passed to controller force feedback
        ("SurfaceRumbleFrontLeft",          DataTypes.FLOAT),
        ("SurfaceRumbleFrontRight",         DataTypes.FLOAT),
        ("SurfaceRumbleRearLeft",           DataTypes.FLOAT),
        ("SurfaceRumbleRearRight",          DataTypes.FLOAT),
        # Tire normalized slip angle, = 0 means 100% grip and |angle| > 1.0 means loss of grip.
        ("TireSlipAngleFrontLeft",          DataTypes.FLOAT),
        ("TireSlipAngleFrontRight",         DataTypes.FLOAT),
        ("TireSlipAngleRearLeft",           DataTypes.FLOAT),
        ("TireSlipAngleRearRight",          DataTypes.FLOAT),
        # Tire normalized combined slip, = 0 means 100% grip and |slip| > 1.0 means loss of grip.
        ("TireCombinedSlipFrontLeft",       DataTypes.FLOAT),
        ("TireCombinedSlipFrontRight",      DataTypes.FLOAT),
        ("TireCombinedSlipRearLeft",        DataTypes.FLOAT),
        ("TireCombinedSlipRearRight",       DataTypes.FLOAT),
        # Actual suspension travel in meters
        ("SuspensionTravelMetersFrontLeft",     DataTypes.FLOAT),
        ("SuspensionTravelMetersFrontRight",    DataTypes.FLOAT),
        ("SuspensionTravelMetersRearLeft",      DataTypes.FLOAT),
        ("SuspensionTravelMetersRearRight",     DataTypes.FLOAT),
        
        ("CarOrdinal",              DataTypes.SIGNED_INT32),  # Unique ID of the car make/model
        ("CarClass",                DataTypes.SIGNED_INT32),  # Between 0 (D -- worst cars) and 7 (X class -- best cars) inclusive      
        ("CarPerformanceIndex",     DataTypes.SIGNED_INT32),  # Between 100 (worst car) and 999 (best car) inclusive
        ("DrivetrainType",          DataTypes.SIGNED_INT32),  # 0 = FWD, 1 = RWD, 2 = AWD
        ("NumCylinders",            DataTypes.SIGNED_INT32),  # Number of cylinders in the engine
        
        ("CarCategory",     DataTypes.SIGNED_INT32),
        ("Unknown1",        DataTypes.SIGNED_INT32),
        ("Unknown2",        DataTypes.SIGNED_INT32),
        
        # Dash data
        ("PositionX",           DataTypes.FLOAT),
        ("PositionY",           DataTypes.FLOAT),
        ("PositionZ",           DataTypes.FLOAT),
        ("Speed",               DataTypes.FLOAT),
        ("Power",               DataTypes.FLOAT),
        ("Torque",              DataTypes.FLOAT),
        ("TireTempFrontLeft",   DataTypes.FLOAT),
        ("TireTempFrontRight",  DataTypes.FLOAT),
        ("TireTempRearLeft",    DataTypes.FLOAT),
        ("TireTempRearRight",   DataTypes.FLOAT),
        ("Boost",               DataTypes.FLOAT),
        ("Fuel",                DataTypes.FLOAT),
        ("DistanceTraveled",    DataTypes.FLOAT),
        ("BestLap",             DataTypes.FLOAT),
        ("LastLap",             DataTypes.FLOAT),
        ("CurrentLap",          DataTypes.FLOAT),
        ("CurrentRaceTime",     DataTypes.FLOAT),
        
        ("LapNumber",       DataTypes.UNSIGNED_INT16),
        ("RacePosition",    DataTypes.UNSIGNED_INT8),
        ("Accel",           DataTypes.UNSIGNED_INT8),
        ("Brake",           DataTypes.UNSIGNED_INT8),
        ("Clutch",          DataTypes.UNSIGNED_INT8),
        ("HandBrake",       DataTypes.UNSIGNED_INT8),
        ("Gear",            DataTypes.UNSIGNED_INT8),
        ("Steer",           DataTypes.SIGNED_INT8),
        ("NormalizedDrivingLine",           DataTypes.SIGNED_INT8),
        ("NormalizedAIBrakeDifference",     DataTypes.SIGNED_INT8),
    ]

### MetaData

class MetaData:
    # standard network info
    port: int | None = 5300
    
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
        0: (DashData,),
    }