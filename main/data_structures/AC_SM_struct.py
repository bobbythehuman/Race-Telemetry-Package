import ctypes
from enum import Enum, IntEnum


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    
    BOOL = ctypes.c_bool
    FLOAT = ctypes.c_float
    # CHAR = ctypes.c_char
    CHAR = ctypes.c_wchar
    a = ctypes


class AC_STATUS(IntEnum):
    AC_OFF = 0
    AC_REPLAY = 1
    AC_LIVE = 2
    AC_PAUSE = 3

class AC_SESSION_TYPE(IntEnum):
    AC_UNKNOWN = -1
    AC_PRACTICE = 0
    AC_QUALIFY = 1
    AC_RACE = 2
    AC_HOTLAP = 3
    AC_TIME_ATTACK = 4
    AC_DRIFT = 5
    AC_DRAG = 6

class AC_FLAG_TYPE(IntEnum):
    AC_NO_FLAG = 0
    AC_BLUE_FLAG = 1
    AC_YELLOW_FLAG = 2
    AC_BLACK_FLAG = 3
    AC_WHITE_FLAG = 4
    AC_CHECKERED_FLAG = 5
    AC_PENALTY_FLAG = 6


# The following members are initialized when the instance starts and never changes until the instance is closed.
class SPageFileStaticData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("smVersion",                   DataTypes.CHAR * 15),     # Version of the Shared Memory structure
        ("acVersion",                   DataTypes.CHAR * 15),     # Version of Assetto Corsa
        ("numberOfSessions",            DataTypes.SIGNED_INT),    # Number of sessions in this instance
        ("numCars",                     DataTypes.SIGNED_INT),    # Max number of possible cars on track
        ("carModel",                    DataTypes.CHAR * 33),     # Name of the player’s car
        ("track",                       DataTypes.CHAR * 33),     # Name of the track
        ("playerName",                  DataTypes.CHAR * 33),     # Name of the player
        ("playerSurname",               DataTypes.CHAR * 33),     # Surname of the player
        ("playerNick",                  DataTypes.CHAR * 33),     # Nickname of the player
        ("sectorCount",                 DataTypes.SIGNED_INT),    # Number of track sectors
        ("maxTorque",                   DataTypes.FLOAT),         # Max torque value of the player’s car
        ("maxPower",                    DataTypes.FLOAT),         # Max power value of the player’s car
        ("maxRpm",                      DataTypes.SIGNED_INT),    # Max rpm value of the player’s car
        ("maxFuel",                     DataTypes.FLOAT),         # Max fuel value of the player’s car
        ("suspensionMaxTravel",         DataTypes.FLOAT * 4),     # Max travel distance of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreRadius",                  DataTypes.FLOAT * 4),     # Radius of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("maxTurboBoost",               DataTypes.FLOAT),         # Max turbo boost value of the player’s car
        ("deprecated_1",                DataTypes.FLOAT),         # Do not use it
        ("deprecated_2",                DataTypes.FLOAT),         # Do not use it
        ("penaltiesEnabled",            DataTypes.SIGNED_INT),    # Cut penalties enabled: 1 (true) or 0 (false)
        ("aidFuelRate",                 DataTypes.FLOAT),         # Fuel consumption rate: 0 (no cons), 1 (normal), 2 (double cons) etc.
        ("aidTireRate",                 DataTypes.FLOAT),         # Tire wear rate: 0 (no wear), 1 (normal), 2 (double wear) etc.
        ("aidMechanicalDamage",         DataTypes.FLOAT),         # Damage rate: 0 (no damage) to 1 (normal)
        ("AllowTyreBlankets",           DataTypes.SIGNED_INT),    # Player starts with hot (optimal temp) tyres: 1 (true) or 0 (false)
        ("aidStability",                DataTypes.FLOAT),         # Stability aid: 0 (no aid) to 1 (full aid)
        ("aidAutoclutch",               DataTypes.SIGNED_INT),    # If player’s car has the “auto clutch” feature enabled : 0 or 1
        ("aidAutoBlip",                 DataTypes.SIGNED_INT),    # If player’s car has the “auto blip” feature enabled : 0 or 1
        ("hasDRS",                      DataTypes.SIGNED_INT),    # If player’s car has the “DRS” system: 0 or 1
        ("hasERS",                      DataTypes.SIGNED_INT),    # If player’s car has the “ERS” system: 0 or 1
        ("hasKERS",                     DataTypes.SIGNED_INT),    # If player’s car has the “KERS” system: 0 or 1
        ("kersMaxJ",                    DataTypes.FLOAT),         # Max KERS Joule value of the player’s car
        ("engineBrakeSettingsCount",    DataTypes.SIGNED_INT),    # Count of possible engine brake settings of the player’s car
        ("ersPowerControllerCount",     DataTypes.SIGNED_INT),    # Count of the possible power controllers of the player’s car
        ("trackSplineLength",           DataTypes.FLOAT),         # Length of the spline of the selected track
        ("trackConfiguration",          DataTypes.CHAR * 33),     # Name of the track’s layout (only multi-layout tracks)
        ("ersMaxJ",                     DataTypes.FLOAT),         # Max ERS Joule value of the player’s car
        ("isTimedRace",                 DataTypes.SIGNED_INT),    # 1 if the race is a timed one
        ("hasExtraLap",                 DataTypes.SIGNED_INT),    # 1 if the timed race is set with an extra lap
        ("carSkin",                     DataTypes.CHAR * 33),     # Name of the used skin
        ("reversedGridPositions",       DataTypes.SIGNED_INT),    # How many positions are going to be swapped in the second race
        ("PitWindowStart",              DataTypes.SIGNED_INT),    # Pit window is open on Lap/Minute
        ("PitWindowEnd",                DataTypes.SIGNED_INT),    # Pit window is closed on Lap/Minute
    ]

# The following members change at each graphic step. They all refer to the player’s car.
class SPageFilePhysicsData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("packetId",            DataTypes.SIGNED_INT),    # Index of the shared memory’s current step
        ("gas",                 DataTypes.FLOAT),         # Value of gas pedal: 0 to 1 (fully pressed)
        ("brake",               DataTypes.FLOAT),         # Value of brake pedal: 0 to 1 (fully pressed)
        ("fuel",                DataTypes.FLOAT),         # Liters of fuel in the car
        ("gear",                DataTypes.SIGNED_INT),    # Selected gear (0 is reverse, 1 is neutral, 2 is first gear )
        ("rpm",                 DataTypes.SIGNED_INT),    # Value of rpm
        ("steerAngle",          DataTypes.FLOAT),         # Angle of steer
        ("speedKmh",            DataTypes.FLOAT),         # Speed in Km/h
        ("velocity",            DataTypes.FLOAT * 3),     # Velocity for each axis (world related) [x, y, z]
        ("accG",                DataTypes.FLOAT * 3),     # G-force for each axis (local related) [x, y, z]
        ("wheelSlip",           DataTypes.FLOAT * 4),     # Spin speed of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelLoad",           DataTypes.FLOAT * 4),     # Load on each tyre (in N) [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelPressure",       DataTypes.FLOAT * 4),     # Pressure of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelAngularSpeed",   DataTypes.FLOAT * 4),     # Angular speed of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreWear",            DataTypes.FLOAT * 4),     # Current wear of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreDirtyLevel",      DataTypes.FLOAT * 4),     # Dirt level on each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("TyreCoreTemp",        DataTypes.FLOAT * 4),     # Core temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("camberRAD",           DataTypes.FLOAT * 4),     # Camber of each tyre in Radian [Front Left, Front Right, Rear Left, Rear Right]
        ("suspensionTravel",    DataTypes.FLOAT * 4),     # Suspension travel for each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("drs",                 DataTypes.FLOAT),         # If DRS is present and enabled: 0 (false) or 1 (true)
        ("tc",                  DataTypes.FLOAT),         # Slip ratio limit for the traction control (if enabled)
        ("heading",             DataTypes.FLOAT),         # Heading of the car on world coordinates
        ("pitch",               DataTypes.FLOAT),         # Pitch of the car on world coordinates
        ("roll",                DataTypes.FLOAT),         # Roll of the car on world coordinates
        ("cgHeight",            DataTypes.FLOAT),         # Height of Center of Gravity
        ("carDamage",           DataTypes.FLOAT * 5),     # Level of damage for each car section (only first 4 are valid)
        ("numberOfTyresOut",    DataTypes.SIGNED_INT),    # How many tyres are allowed to stay out of the track to not receive a penalty
        ("pitLimiterOn",        DataTypes.SIGNED_INT),    # If pit limiter is enabled: 0 (false) or 1 (true)
        ("abs",                 DataTypes.FLOAT),         # Slip ratio limit for the ABS (if enabled)
        ("kersCharge",          DataTypes.FLOAT),         # KERS/ERS battery charge: 0 to 1
        ("kersInput",           DataTypes.FLOAT),         # KERS/ERS input to engine: 0 to 1
        ("autoshifterOn",       DataTypes.SIGNED_INT),    # If auto shifter is enabled: 0 (false) or 1 (true)
        ("rideHeight",          DataTypes.FLOAT * 2),     # Right heights: front and rear
        ("turboBoost",          DataTypes.FLOAT),         # Turbo boost
        ("ballast",             DataTypes.FLOAT),         # Kilograms of ballast added to the car (only in multiplayer)
        ("airDensity ",         DataTypes.FLOAT),         # Air density
        ("airTemp",             DataTypes.FLOAT),         # Ambient temperature
        ("roadTemp",            DataTypes.FLOAT),         # Road temperature 
        ("localAngularVel",     DataTypes.FLOAT * 3),     # Angular velocity of the car [x, y, z]
        ("finalFF",             DataTypes.FLOAT),         # Current Force Feedback value;
        ("performanceMeter",    DataTypes.FLOAT),         # Performance meter compared to the best lap
        ("engineBrake",         DataTypes.SIGNED_INT),    # Engine brake setting
        ("ersRecoveryLevel",    DataTypes.SIGNED_INT),    # ERS recovery level
        ("ersPowerLevel",       DataTypes.SIGNED_INT),    # ERS selected power controller
        ("ersHeatCharging",     DataTypes.SIGNED_INT),    # ERS changing: 0 (Motor) or 1 (Battery)
        ("ersIsCharging",       DataTypes.SIGNED_INT),    # If ERS battery is recharging: 0 (false) or 1 (true)
        ("kersCurrentKJ",       DataTypes.FLOAT),         # KERS/ERS KiloJoule spent during the lap
        ("drsAvailable",        DataTypes.SIGNED_INT),    # If DRS is available (DRS zone): 0 (false) or 1 (true)
        ("drsEnabled",          DataTypes.SIGNED_INT),    # If DRS is enabled: 0 (false) or 1 (true)
        ("brakeTemp",           DataTypes.FLOAT * 4),     # Brake temp for each tire [Front Left, Front Right, Rear Left, Rear Right]
        ("clutch",              DataTypes.FLOAT),         # Value of clutch pedal: 0 to 1 (fully pressed)
        ("tyreTempI",           DataTypes.FLOAT * 4),     # Inner temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreTempM",           DataTypes.FLOAT * 4),     # Middle temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreTempO",           DataTypes.FLOAT * 4),     # Outer temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("isAIControlled",      DataTypes.SIGNED_INT),    # AI controlled car: 0 (human) or 1 (AI)
        ("tyreContactPoint",    DataTypes.FLOAT * 4 * 3), # Vector for contact point of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("tyreContactNormal",   DataTypes.FLOAT * 4 * 3), # Vector for contact normal of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("tyreContactHeading",  DataTypes.FLOAT * 4 * 3), # Vector for contact heading of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("brakeBias",           DataTypes.FLOAT),         # Brake bias from 0 (rear) to 1 (front)
        ("localVelocity",       DataTypes.FLOAT * 3),     # Vector for local velocity
    ]

# The following members change at each graphical step. They all refer to the player’s car.
class SPageFileGraphicData(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("packetId",                DataTypes.SIGNED_INT),        # Index of the shared memory’s current step
        ("status",                  DataTypes.SIGNED_INT),        # Status of the instance: AC_OFF 0, AC_REPLAY 1, AC_LIVE 2, AC_PAUSE 3
        # ("status",                  AC_STATUS),        # Status of the instance: AC_OFF 0, AC_REPLAY 1, AC_LIVE 2, AC_PAUSE 3
        ("session",                 DataTypes.SIGNED_INT),        # Session type: AC_UNKNOWN -1, AC_PRACTICE 0, AC_QUALIFY 1, AC_RACE 2, AC_HOTLAP 3, AC_TIME_ATTACK 4, AC_DRIFT 5, AC_DRAG 6
        ("currentTime",             DataTypes.CHAR * 15),         # Current lap time
        ("lastTime",                DataTypes.CHAR * 15),         # Last lap time
        ("bestTime",                DataTypes.CHAR * 15),         # Best lap time
        ("split",                   DataTypes.CHAR * 15),         # Time in sector
        ("completedLaps",           DataTypes.SIGNED_INT),        # Number of completed laps by the player
        ("position",                DataTypes.SIGNED_INT),        # Current player position (standings)
        ("iCurrentTime",            DataTypes.SIGNED_INT),        # Current lap time
        ("iLastTime",               DataTypes.SIGNED_INT),        # Last lap time
        ("iBestTime",               DataTypes.SIGNED_INT),        # Best lap time
        ("sessionTimeLeft",         DataTypes.FLOAT),             # Time left until session is closed
        ("distanceTraveled",        DataTypes.FLOAT),             # Distance traveled during the instance
        ("isInPit",                 DataTypes.SIGNED_INT),        # If player’s car is stopped in the pit: 0 (false) or 1 (true)
        ("currentSectorIndex",      DataTypes.SIGNED_INT),        # Current sector index
        ("lastSectorTime",          DataTypes.SIGNED_INT),        # Last sector time
        ("numberOfLaps",            DataTypes.SIGNED_INT),        # Number of laps needed to close the session
        ("tyreCompound",            DataTypes.CHAR * 33),         # Current tyre compound
        ("replayTimeMultiplier",    DataTypes.FLOAT),             # Replay multiplier
        ("normalizedCarPosition",   DataTypes.FLOAT),             # Car position on the track’s spline
        ("carCoordinates",          DataTypes.FLOAT * 3),         # Car position on world coordinates [x, y, z]
        ("penaltyTime",             DataTypes.FLOAT),             # Time of penalty
        ("flag",                    DataTypes.SIGNED_INT),        # Type of flag being shown: AC_NO_FLAG 0, AC_BLUE_FLAG 1, AC_YELLOW_FLAG 2, AC_BLACK_FLAG 3, AC_WHITE_FLAG 4, AC_CHECKERED_FLAG 5, AC_PENALTY_FLAG 6
        ("idealLineOn",             DataTypes.SIGNED_INT),        # If ideal line is enabled: 0 (false) or 1 (true)
        ("isInPitLane",             DataTypes.SIGNED_INT),        # If player’s car is in the pitlane: 0 (false) or 1 (true)
        ("surfaceGrip",             DataTypes.FLOAT),             # Current grip of the track’s surface
        ("mandatoryPitDone",        DataTypes.SIGNED_INT),        # Set to 1 if the player has done the mandatory pit
        ("windSpeed",               DataTypes.FLOAT),             # Speed of the wind on the current session
        ("windDirection",           DataTypes.FLOAT),             # Direction of the wind (0-359) on the current session
    ]


### MetaData

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
    allSharedMemoryNames: str | None | dict[str, str] = {
            "SPageFileStaticData": "Local\\acpmf_static",
            "SPageFilePhysicsData": "Local\\acpmf_physics",
            "SPageFileGraphicData": "Local\\acpmf_graphics"
        }
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (SPageFileStaticData, SPageFilePhysicsData, SPageFileGraphicData),
    }