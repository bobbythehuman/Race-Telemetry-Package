import ctypes
from enum import Enum

# source
# https://www.assettocorsa.net/forum/index.php?threads/acc-shared-memory-documentation.59965/

class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    FLOAT = ctypes.c_float
    
    BOOL = ctypes.c_bool
    DOUBLE = ctypes.c_double
    CHAR = ctypes.c_wchar
    # a = ctypes.c_w
    

# The following members change at each graphic step. They all refer to the player’s car. 
class SPageFilePhysicsData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("packetId",            DataTypes.SIGNED_INT.value),    # Current step index
        ("gas",                 DataTypes.FLOAT.value),         # Gas pedal input value (from -0 to 1.0)
        ("brake",               DataTypes.FLOAT.value),         # Brake pedal input value (from -0 to 1.0)
        ("fuel",                DataTypes.FLOAT.value),         # Amount of fuel remaining in kg
        ("gear",                DataTypes.SIGNED_INT.value),    # Current gear
        ("rpm",                 DataTypes.SIGNED_INT.value),    # Engine revolutions per minute
        ("steerAngle",          DataTypes.FLOAT.value),         # Steering input value (from -1.0 to 1.0)
        ("speedKmh",            DataTypes.FLOAT.value),         # Car speed in km/h
        ("velocity",            DataTypes.FLOAT.value * 3),     # Car velocity vector in global coordinates
        ("accG",                DataTypes.FLOAT.value * 3),     # Car acceleration vector in global coordinates
        ("wheelSlip",           DataTypes.FLOAT.value * 4),     # Tyre slip for each tyre [FL, FR, RL, RR]
        # ("wheelLoad",           DataTypes.FLOAT.value * 4),     # Wheel load for each tyre [FL, FR, RL, RR]
        ("wheelPressure",       DataTypes.FLOAT.value * 4),     # Tyre pressure [FL, FR, RL, RR]
        ("wheelAngularSpeed",   DataTypes.FLOAT.value * 4),     # Wheel angular speed in rad/s [FL, FR, RL, RR]
        # ("tyreWear",            DataTypes.FLOAT.value * 4),     # Tyre wear [FL, FR, RL, RR]
        # ("tyreDirtyLevel",      DataTypes.FLOAT.value * 4),     # Dirt accumulated on tyre surface [FL, FR, RL, RR]
        ("TyreCoreTemp",        DataTypes.DOUBLE.value * 4),     # Tyre rubber core temperature [FL, FR, RL, RR]
        # ("camberRAD",           DataTypes.FLOAT.value * 4),     # Wheels camber in radians [FL, FR, RL, RR]
        ("suspensionTravel",    DataTypes.FLOAT.value * 4),     # Suspension travel [FL, FR, RL, RR]
        # ("drs",                 DataTypes.FLOAT.value),         # DRS on
        ("tc",                  DataTypes.FLOAT.value),         # TC in action
        ("heading",             DataTypes.FLOAT.value),         # Car yaw orientation
        ("pitch",               DataTypes.FLOAT.value),         # Car pitch orientation
        
        ("roll",                DataTypes.FLOAT.value),         # Car roll orientation 
        # ("cgHeight",            DataTypes.FLOAT.value),         # Centre of gravity height 
        ("carDamage",           DataTypes.FLOAT.value * 5),     # Car damage: front 0, rear 1, left 2, right 3, centre 4 
        # ("numberOfTyresOut",    DataTypes.SIGNED_INT.value),    # Number of tyres out of track 
        ("pitLimiterOn",        DataTypes.SIGNED_INT.value),    # Pit limiter is on
        ("abs",                 DataTypes.FLOAT.value),         # ABS in action
        # ("kersCharge",          DataTypes.FLOAT.value),         # Not used in ACC
        # ("kersInput",           DataTypes.FLOAT.value),         # Not used in ACC
        ("autoshifterOn",       DataTypes.SIGNED_INT.value),    # Automatic transmission on
        # ("rideHeight",          DataTypes.FLOAT.value * 2),     # Ride height: 0 front, 1 rear
        ("turboBoost",          DataTypes.FLOAT.value),         # Car turbo level
        # ("ballast",             DataTypes.FLOAT.value),         # Car ballast in kg / Not implemented
        # ("airDensity ",         DataTypes.FLOAT.value),         # Air density
        ("airTemp",             DataTypes.FLOAT.value),         # Air temperature
        ("roadTemp",            DataTypes.FLOAT.value),         # Road temperature 
        ("localAngularVel",     DataTypes.FLOAT.value * 3),     # Car angular velocity vector in local coordinates
        ("finalFF",             DataTypes.FLOAT.value),         # Force feedback signal 
        # ("performanceMeter",    DataTypes.FLOAT.value),         # Not used in ACC
        # ("engineBrake",         DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("ersRecoveryLevel",    DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("ersPowerLevel",       DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("ersHeatCharging",     DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("ersIsCharging",       DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("kersCurrentKJ",       DataTypes.FLOAT.value),         # Not used in ACC
        # ("drsAvailable",        DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("drsEnabled",          DataTypes.SIGNED_INT.value),    # Not used in ACC
        ("brakeTemp",           DataTypes.FLOAT.value * 4),     # Brake discs temperatures 
        ("clutch",              DataTypes.FLOAT.value),         # Clutch pedal input value (from -0 to 1.0)
        # ("tyreTempI",           DataTypes.FLOAT.value * 4),     # Not used in ACC
        # ("tyreTempM",           DataTypes.FLOAT.value * 4),     # Not used in ACC
        # ("tyreTempO",           DataTypes.FLOAT.value * 4),     # Not used in ACC
        ("isAIControlled",      DataTypes.SIGNED_INT.value),    # Car is controlled by the AI 
        ("tyreContactPoint",    DataTypes.FLOAT.value * 4 * 3), # Tyre contact point global coordinates [FL, FR, RL, RR] [x,y,z]
        ("tyreContactNormal",   DataTypes.FLOAT.value * 4 * 3), # Tyre contact normal [FL, FR, RL, RR] [x,y,z]
        ("tyreContactHeading",  DataTypes.FLOAT.value * 4 * 3), # Tyre contact heading [FL, FR, RL, RR] [x,y,z]
        ("brakeBias",           DataTypes.FLOAT.value),         # Front brake bias, see Appendix 4
        ("localVelocity",       DataTypes.FLOAT.value * 3),     # Car velocity vector in local coordinates
        # ("P2PActivation",       DataTypes.SIGNED_INT.value),    # Not used in ACC 
        # ("P2PStatus",           DataTypes.SIGNED_INT.value),    # Not used in ACC 
        # ("currentMaxRpm",       DataTypes.FLOAT.value),         # Maximum engine rpm 
        # ("mz",                  DataTypes.FLOAT.value * 4),     # Not shown in ACC
        
        # ("fx",                  DataTypes.FLOAT.value * 4),     # Not shown in ACC
        # ("fy",                  DataTypes.FLOAT.value * 4),     # Not shown in ACC
        ("slipRatio",           DataTypes.FLOAT.value * 4),     # Tyre slip ratio [FL, FR, RL, RR] in radians
        ("slipAngle",           DataTypes.FLOAT.value * 4),     # Tyre slip angle [FL, FR, RL, RR]
        # ("tcinAction",          DataTypes.SIGNED_INT.value),    # TC in action
        # ("absInAction",         DataTypes.SIGNED_INT.value),    # ABS in action
        # ("suspensionDamage",    DataTypes.FLOAT.value * 4),     # Suspensions damage levels [FL, FR, RL, RR]
        # ("tyreTemp",            DataTypes.FLOAT.value * 4),     # Tyres core temperatures [FL, FR, RL, RR]
        ("waterTemp",           DataTypes.FLOAT.value),         # Water Temperature
        ("brakePressure",       DataTypes.FLOAT.value * 4),     # Brake pressure [FL, FR, RL, RR] see Appendix 2
        ("frontBrakeCompound",  DataTypes.SIGNED_INT.value),    # Brake pad compund front
        ("rearBrakeCompound",   DataTypes.SIGNED_INT.value),    # Brake pad compund rear
        ("padLife",             DataTypes.FLOAT.value * 4),     # Brake pad wear [FL, FR, RL, RR]
        ("discLife",            DataTypes.FLOAT.value * 4),     # Brake disk wear [FL, FR, RL, RR]
        ("ignitionOn",          DataTypes.SIGNED_INT.value),    # Ignition switch set to on?
        ("starterEngineOn",     DataTypes.SIGNED_INT.value),    # Starter Switch set to on?
        ("isEngineRunning",     DataTypes.SIGNED_INT.value),    # Engine running?
        ("kerbVibration",       DataTypes.FLOAT.value),         # vibrations sent to the FFB, could be used for motion rigs
        ("slipVibrations",      DataTypes.FLOAT.value),         # vibrations sent to the FFB, could be used for motion rigs
        ("gVibrations",         DataTypes.FLOAT.value),         # vibrations sent to the FFB, could be used for motion rigs
        ("absVibrations",       DataTypes.FLOAT.value),         # vibrations sent to the FFB, could be used for motion rigs
    ]

# The following members are updated at each graphical step. They mostly refer to player’s car
# except for carCoordinates and carID, which refer to the cars currently on track.
class SPageFileGraphicData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("packetId",                DataTypes.SIGNED_INT.value),        # Current step index
        # ("status",                  DataTypes.FLOAT.value),         # See enums ACC_STATUS
        # ("session",                 DataTypes.FLOAT.value),         # See enums ACC_SESSION_TYPE
        ("currentTime",             DataTypes.CHAR.value * 15),         # Current lap time in wide character
        ("lastTime",                DataTypes.CHAR.value * 15),         # Last lap time in wide character
        ("bestTime",                DataTypes.CHAR.value * 15),         # Best lap time in wide character 
        ("split",                   DataTypes.CHAR.value * 15),         # Last split time in wide character
        ("completedLaps",           DataTypes.SIGNED_INT.value),        # No of completed laps
        ("position",                DataTypes.SIGNED_INT.value),        # Current player position 
        ("iCurrentTime",            DataTypes.SIGNED_INT.value),        # Current lap time in milliseconds
        ("iLastTime",               DataTypes.SIGNED_INT.value),        # Last lap time in milliseconds
        ("iBestTime",               DataTypes.SIGNED_INT.value),        # Best lap time in milliseconds
        ("sessionTimeLeft",         DataTypes.FLOAT.value),             # Session time left
        ("distanceTraveled",        DataTypes.FLOAT.value),             # Distance travelled in the current stint 
        ("isInPit",                 DataTypes.SIGNED_INT.value),        # Car is pitting 
        ("currentSectorIndex",      DataTypes.SIGNED_INT.value),        # Current track sector
        ("lastSectorTime",          DataTypes.SIGNED_INT.value),        # Last sector time in milliseconds 
        ("numberOfLaps",            DataTypes.SIGNED_INT.value),        # Number of completed laps
        ("tyreCompound",            DataTypes.CHAR.value * 33),         # Tyre compound used
        # ("replayTimeMultiplier",    DataTypes.FLOAT.value),             # Not used in ACC
        ("normalizedCarPosition",   DataTypes.FLOAT.value),             # Car position on track spline (0.0 start to 1.0 finish) 
        ("activeCars",              DataTypes.SIGNED_INT.value),        # Number of cars on track
        ("carCoordinates",          DataTypes.FLOAT.value * 60 * 3),    # Coordinates of cars on track
        ("carID",                   DataTypes.SIGNED_INT.value),        # Car IDs of cars on track
        ("playerCarID",             DataTypes.SIGNED_INT.value),        # Player Car ID
        ("penaltyTime",             DataTypes.FLOAT.value),             # Penalty time to wait
        # ("flag",                    DataTypes.SIGNED_INT.value),    # See enums ACC_FLAG_TYPE
        # ("penalty",                 DataTypes.SIGNED_INT.value),    # See enums ACC_PENALTY_TYPE
        ("idealLineOn",             DataTypes.SIGNED_INT.value),        # Ideal line on 
        ("isInPitLane",             DataTypes.SIGNED_INT.value),        # Car is in pit lane
        ("surfaceGrip",             DataTypes.FLOAT.value),             # Ideal line friction coefficient 
        ("mandatoryPitDone",        DataTypes.SIGNED_INT.value),        # Mandatory pit is completed 
        ("windSpeed",               DataTypes.FLOAT.value),             # Wind speed in m/s
        ("windDirection",           DataTypes.FLOAT.value),             # wind direction in radians
        ("isSetupMenuVisible",      DataTypes.SIGNED_INT.value),        # Car is working on setup
        
        ("mainDisplayIndex",            DataTypes.SIGNED_INT.value),    # current car main display index, see Appendix 1
        ("secondaryDisplyIndex",        DataTypes.SIGNED_INT.value),    # current car secondary display index
        ("TC",                          DataTypes.SIGNED_INT.value),    # Traction control level 
        ("TCCUT",                       DataTypes.SIGNED_INT.value),    # Traction control cut level
        ("EngineMap",                   DataTypes.SIGNED_INT.value),    # Current engine map
        ("ABS",                         DataTypes.SIGNED_INT.value),    # ABS level 
        ("fuelXLap",                    DataTypes.FLOAT.value),         # Average fuel consumed per lap in liters 
        ("rainLights",                  DataTypes.SIGNED_INT.value),    # Rain lights on
        ("flashingLights",              DataTypes.SIGNED_INT.value),    # Flashing lights on
        ("lightsStage",                 DataTypes.SIGNED_INT.value),    # Current lights stage 
        ("exhaustTemperature",          DataTypes.FLOAT.value),         # Exhaust temperature
        ("wiperLV",                     DataTypes.SIGNED_INT.value),    # Current wiper stage
        ("driverStintTotalTimeLeft",    DataTypes.SIGNED_INT.value),    # Time the driver is allowed to drive/race (ms)
        ("driverStintTimeLeft",         DataTypes.SIGNED_INT.value),    # Time the driver is allowed to drive/stint (ms)
        ("rainTyres",                   DataTypes.SIGNED_INT.value),    # Are rain tyres equipped
        ("sessionIndex",                DataTypes.SIGNED_INT.value),
        ("usedFuel",                    DataTypes.FLOAT.value),         # Used fuel since last time refueling
        ("deltaLapTime",                DataTypes.CHAR.value * 15),     # Delta time in wide character
        ("iDeltaLapTime",               DataTypes.SIGNED_INT.value),    # Delta time time in milliseconds
        ("estimatedLapTime",            DataTypes.CHAR.value * 15),     # Estimated lap time in milliseconds
        ("iEstimatedLapTime",           DataTypes.SIGNED_INT.value),    # Estimated lap time in wide character
        ("isDeltaPositive",             DataTypes.SIGNED_INT.value),    # Delta positive (1) or negative (0)
        ("iSplit",                      DataTypes.SIGNED_INT.value),    # Last split time in milliseconds
        ("isValidLap",                  DataTypes.SIGNED_INT.value),    # Check if Lap is valid for timing
        ("fuelEstimatedLaps",           DataTypes.FLOAT.value),         # Laps possible with current fuel level
        ("trackStatus",                 DataTypes.CHAR.value * 33),     # Status of track 
        ("missingMandatoryPits",        DataTypes.SIGNED_INT.value),    # Mandatory pitstops the player still has to do
        ("Clock",                       DataTypes.FLOAT.value),         # Time of day in seconds
        ("directionLightsLeft",         DataTypes.SIGNED_INT.value),    # Is Blinker left on
        ("directionLightsRight",        DataTypes.SIGNED_INT.value),    # Is Blinker right on
        ("GlobalYellow",                DataTypes.SIGNED_INT.value),    # Yellow Flag is out?
        ("GlobalYellow1",               DataTypes.SIGNED_INT.value),    # Yellow Flag in Sector 1 is out?
        ("GlobalYellow2",               DataTypes.SIGNED_INT.value),    # Yellow Flag in Sector 2 is out?
        ("GlobalYellow3",               DataTypes.SIGNED_INT.value),    # Yellow Flag in Sector 3 is out?
        ("GlobalWhite",                 DataTypes.SIGNED_INT.value),    # White Flag is out?
        ("GlobalGreen",                 DataTypes.SIGNED_INT.value),    # Green Flag is out?
        ("GlobalChequered",             DataTypes.SIGNED_INT.value),    # Checkered Flag is out?
        ("GlobalRed",                   DataTypes.SIGNED_INT.value),    # Red Flag is out?
        ("mfdTyreSet",                  DataTypes.SIGNED_INT.value),    # num of tyre set on the MFD
        ("mfdFuelToAdd",                DataTypes.FLOAT.value),         # How much fuel to add on the MFD
        ("mfdTyrePressureLF",           DataTypes.FLOAT.value),         # Tyre pressure left front on the MFD
        
        ("mfdTyrePressureRF",       DataTypes.FLOAT.value),         # Tyre pressure right front on the MFD
        ("mfdTyrePressureLR",       DataTypes.FLOAT.value),         # Tyre pressure left rear on the MFD
        ("mfdTyrePressureRR",       DataTypes.FLOAT.value),         # Tyre pressure right rear on the MFD
        # ("trackGripStatus",         DataTypes.SIGNED_INT.value),    # See enums ACC_TRACK_GRIP_STATUS
        # ("rainIntensity",           DataTypes.SIGNED_INT.value),    # See enums ACC_RAIN_INTENSITY
        # ("rainIntensityIn10min",    DataTypes.FLOAT.value),         # See enums ACC_RAIN_INTENSITY
        # ("rainIntensityIn30min",    DataTypes.FLOAT.value),         # See enums ACC_RAIN_INTENSITY
        ("currentTyreSet",          DataTypes.SIGNED_INT.value),    # Tyre Set currently in use
        ("strategyTyreSet",         DataTypes.SIGNED_INT.value),    # Next Tyre set per strategy
        ("gapAhead",                DataTypes.SIGNED_INT.value),    # Distance in ms to car in front
        ("gapBehind",               DataTypes.SIGNED_INT.value),    # Distance in ms to car behind
    ]

# The following members are initialized when the instance starts and never changes until the
# instance is closed. 
class SPageFileStaticData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("smVersion",                   DataTypes.CHAR.value * 15),     # Shared memory version
        ("acVersion",                   DataTypes.CHAR.value * 15),     # Assetto Corsa version
        ("numberOfSessions",            DataTypes.SIGNED_INT.value),    # Number of sessions 
        ("numCars",                     DataTypes.SIGNED_INT.value),    # Number of cars 
        ("carModel",                    DataTypes.CHAR.value * 33),     # Player car model see Appendix 2
        ("track",                       DataTypes.CHAR.value * 33),     # Track name
        ("playerName",                  DataTypes.CHAR.value * 33),     # Player name
        ("playerSurname",               DataTypes.CHAR.value * 33),     # Player surname 
        ("playerNick",                  DataTypes.CHAR.value * 33),     # Player nickname
        ("sectorCount",                 DataTypes.SIGNED_INT.value),    # Number of sectors 
        # ("maxTorque",                   DataTypes.FLOAT.value),         # Not shown in ACC 
        # ("maxPower",                    DataTypes.FLOAT.value),         # Not shown in ACC 
        ("maxRpm",                      DataTypes.SIGNED_INT.value),    # Maximum rpm 
        ("maxFuel",                     DataTypes.FLOAT.value),         # Maximum fuel tank capacity
        # ("suspensionMaxTravel",         DataTypes.FLOAT.value * 4),     # Not shown in ACC 
        # ("tyreRadius",                  DataTypes.FLOAT.value * 4),     # Not shown in ACC 
        # ("maxTurboBoost",               DataTypes.FLOAT.value),         # Maximum turbo boost 
        # ("deprecated_1",                DataTypes.SIGNED_INT.value),
        # ("deprecated_2",                DataTypes.FLOAT.value),
        ("penaltiesEnabled",            DataTypes.SIGNED_INT.value),    # Penalties enabled
        ("aidFuelRate",                 DataTypes.FLOAT.value),         # Fuel consumption rate
        ("aidTireRate",                 DataTypes.FLOAT.value),         # Tyre wear rate
        ("aidMechanicalDamage",         DataTypes.FLOAT.value),         # Mechanical damage rate
        ("AllowTyreBlankets",           DataTypes.FLOAT.value),         # Not allowed in Blancpain endurance series 
        ("aidStability",                DataTypes.FLOAT.value),         # Stability control used
        ("aidAutoclutch",               DataTypes.SIGNED_INT.value),    # Auto clutch used 
        ("aidAutoBlip",                 DataTypes.SIGNED_INT.value),    # Always true in ACC
        # ("hasDRS",                      DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("hasERS",                      DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("hasKERS",                     DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("kersMaxJ",                    DataTypes.FLOAT.value),         # Not used in ACC
        # ("engineBrakeSettingsCount",    DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("ersPowerControllerCount",     DataTypes.SIGNED_INT.value),    # Not used in ACC
        # ("trackSplineLength",           DataTypes.FLOAT.value),         # Not used in ACC
        # ("trackConfiguration",          DataTypes.CHAR.value),          # Not used in ACC
        # ("ersMaxJ",                     DataTypes.FLOAT.value),         # Not used in ACC
        
        ("isTimedRace",             DataTypes.SIGNED_INT.value),    # Not used in ACC
        ("hasExtraLap",             DataTypes.SIGNED_INT.value),    # Not used in ACC
        ("carSkin",                 DataTypes.CHAR.value * 33),     # Not used in ACC
        ("reversedGridPositions",   DataTypes.SIGNED_INT.value),    # Not used in ACC
        ("PitWindowStart",          DataTypes.SIGNED_INT.value),    # Pit window opening time
        ("PitWindowEnd",            DataTypes.SIGNED_INT.value),    # Pit windows closing time
        ("isOnline",                DataTypes.SIGNED_INT.value),    # If is a multiplayer session
        ("dryTyresName",            DataTypes.CHAR.value * 33),     # Name of the dry tyres
        ("wetTyresName",            DataTypes.CHAR.value * 33),     # Name of the wet tyres
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
    allSharedMemoryNames: str | None | dict[str, str] = {
            "SPageFilePhysicsData": "Local\\acpmf_physics",
            "SPageFileGraphicData": "Local\\acpmf_graphics",
            "SPageFileStaticData": "Local\\acpmf_static",
        }
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (SPageFilePhysicsData, SPageFileGraphicData, SPageFileStaticData, ),
    }