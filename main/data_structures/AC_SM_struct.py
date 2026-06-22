import ctypes
from enum import Enum, IntEnum


class DataTypes(Enum):
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    
    BOOL = ctypes.c_bool
    FLOAT = ctypes.c_float
    # CHAR = ctypes.c_char
    CHAR = ctypes.c_wchar


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
class SPageFileStaticData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("smVersion",                   DataTypes.CHAR.value * 15),     # Version of the Shared Memory structure
        ("acVersion",                   DataTypes.CHAR.value * 15),     # Version of Assetto Corsa
        ("numberOfSessions",            DataTypes.SIGNED_INT.value),    # Number of sessions in this instance
        ("numCars",                     DataTypes.SIGNED_INT.value),    # Max number of possible cars on track
        ("carModel",                    DataTypes.CHAR.value * 33),     # Name of the player’s car
        ("track",                       DataTypes.CHAR.value * 33),     # Name of the track
        ("playerName",                  DataTypes.CHAR.value * 33),     # Name of the player
        ("playerSurname",               DataTypes.CHAR.value * 33),     # Surname of the player
        ("playerNick",                  DataTypes.CHAR.value * 33),     # Nickname of the player
        ("sectorCount",                 DataTypes.SIGNED_INT.value),    # Number of track sectors
        ("maxTorque",                   DataTypes.FLOAT.value),         # Max torque value of the player’s car
        ("maxPower",                    DataTypes.FLOAT.value),         # Max power value of the player’s car
        ("maxRpm",                      DataTypes.SIGNED_INT.value),    # Max rpm value of the player’s car
        ("maxFuel",                     DataTypes.FLOAT.value),         # Max fuel value of the player’s car
        ("suspensionMaxTravel",         DataTypes.FLOAT.value * 4),     # Max travel distance of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreRadius",                  DataTypes.FLOAT.value * 4),     # Radius of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("maxTurboBoost",               DataTypes.FLOAT.value),         # Max turbo boost value of the player’s car
        ("deprecated_1",                DataTypes.FLOAT.value),         # Do not use it
        ("deprecated_2",                DataTypes.FLOAT.value),         # Do not use it
        ("penaltiesEnabled",            DataTypes.SIGNED_INT.value),    # Cut penalties enabled: 1 (true) or 0 (false)
        ("aidFuelRate",                 DataTypes.FLOAT.value),         # Fuel consumption rate: 0 (no cons), 1 (normal), 2 (double cons) etc.
        ("aidTireRate",                 DataTypes.FLOAT.value),         # Tire wear rate: 0 (no wear), 1 (normal), 2 (double wear) etc.
        ("aidMechanicalDamage",         DataTypes.FLOAT.value),         # Damage rate: 0 (no damage) to 1 (normal)
        ("AllowTyreBlankets",           DataTypes.SIGNED_INT.value),    # Player starts with hot (optimal temp) tyres: 1 (true) or 0 (false)
        ("aidStability",                DataTypes.FLOAT.value),         # Stability aid: 0 (no aid) to 1 (full aid)
        ("aidAutoclutch",               DataTypes.SIGNED_INT.value),    # If player’s car has the “auto clutch” feature enabled : 0 or 1
        ("aidAutoBlip",                 DataTypes.SIGNED_INT.value),    # If player’s car has the “auto blip” feature enabled : 0 or 1
        ("hasDRS",                      DataTypes.SIGNED_INT.value),    # If player’s car has the “DRS” system: 0 or 1
        ("hasERS",                      DataTypes.SIGNED_INT.value),    # If player’s car has the “ERS” system: 0 or 1
        ("hasKERS",                     DataTypes.SIGNED_INT.value),    # If player’s car has the “KERS” system: 0 or 1
        ("kersMaxJ",                    DataTypes.FLOAT.value),         # Max KERS Joule value of the player’s car
        ("engineBrakeSettingsCount",    DataTypes.SIGNED_INT.value),    # Count of possible engine brake settings of the player’s car
        ("ersPowerControllerCount",     DataTypes.SIGNED_INT.value),    # Count of the possible power controllers of the player’s car
        ("trackSplineLength",           DataTypes.FLOAT.value),         # Length of the spline of the selected track
        ("trackConfiguration",          DataTypes.CHAR.value * 33),     # Name of the track’s layout (only multi-layout tracks)
        ("ersMaxJ",                     DataTypes.FLOAT.value),         # Max ERS Joule value of the player’s car
        ("isTimedRace",                 DataTypes.SIGNED_INT.value),    # 1 if the race is a timed one
        ("hasExtraLap",                 DataTypes.SIGNED_INT.value),    # 1 if the timed race is set with an extra lap
        ("carSkin",                     DataTypes.CHAR.value * 33),     # Name of the used skin
        ("reversedGridPositions",       DataTypes.SIGNED_INT.value),    # How many positions are going to be swapped in the second race
        ("PitWindowStart",              DataTypes.SIGNED_INT.value),    # Pit window is open on Lap/Minute
        ("PitWindowEnd",                DataTypes.SIGNED_INT.value),    # Pit window is closed on Lap/Minute
    ]

# The following members change at each graphic step. They all refer to the player’s car.
class SPageFilePhysicsData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("packetId",            DataTypes.SIGNED_INT.value),    # Index of the shared memory’s current step
        ("gas",                 DataTypes.FLOAT.value),         # Value of gas pedal: 0 to 1 (fully pressed)
        ("brake",               DataTypes.FLOAT.value),         # Value of brake pedal: 0 to 1 (fully pressed)
        ("fuel",                DataTypes.FLOAT.value),         # Liters of fuel in the car
        ("gear",                DataTypes.SIGNED_INT.value),    # Selected gear (0 is reverse, 1 is neutral, 2 is first gear )
        ("rpm",                 DataTypes.SIGNED_INT.value),    # Value of rpm
        ("steerAngle",          DataTypes.FLOAT.value),         # Angle of steer
        ("speedKmh",            DataTypes.FLOAT.value),         # Speed in Km/h
        ("velocity",            DataTypes.FLOAT.value * 3),     # Velocity for each axis (world related) [x, y, z]
        ("accG",                DataTypes.FLOAT.value * 3),     # G-force for each axis (local related) [x, y, z]
        ("wheelSlip",           DataTypes.FLOAT.value * 4),     # Spin speed of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelLoad",           DataTypes.FLOAT.value * 4),     # Load on each tyre (in N) [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelPressure",       DataTypes.FLOAT.value * 4),     # Pressure of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("wheelAngularSpeed",   DataTypes.FLOAT.value * 4),     # Angular speed of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreWear",            DataTypes.FLOAT.value * 4),     # Current wear of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreDirtyLevel",      DataTypes.FLOAT.value * 4),     # Dirt level on each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("TyreCoreTemp",        DataTypes.FLOAT.value * 4),     # Core temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("camberRAD",           DataTypes.FLOAT.value * 4),     # Camber of each tyre in Radian [Front Left, Front Right, Rear Left, Rear Right]
        ("suspensionTravel",    DataTypes.FLOAT.value * 4),     # Suspension travel for each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("drs",                 DataTypes.FLOAT.value),         # If DRS is present and enabled: 0 (false) or 1 (true)
        ("tc",                  DataTypes.FLOAT.value),         # Slip ratio limit for the traction control (if enabled)
        ("heading",             DataTypes.FLOAT.value),         # Heading of the car on world coordinates
        ("pitch",               DataTypes.FLOAT.value),         # Pitch of the car on world coordinates
        ("roll",                DataTypes.FLOAT.value),         # Roll of the car on world coordinates
        ("cgHeight",            DataTypes.FLOAT.value),         # Height of Center of Gravity
        ("carDamage",           DataTypes.FLOAT.value * 5),     # Level of damage for each car section (only first 4 are valid)
        ("numberOfTyresOut",    DataTypes.SIGNED_INT.value),    # How many tyres are allowed to stay out of the track to not receive a penalty
        ("pitLimiterOn",        DataTypes.SIGNED_INT.value),    # If pit limiter is enabled: 0 (false) or 1 (true)
        ("abs",                 DataTypes.FLOAT.value),         # Slip ratio limit for the ABS (if enabled)
        ("kersCharge",          DataTypes.FLOAT.value),         # KERS/ERS battery charge: 0 to 1
        ("kersInput",           DataTypes.FLOAT.value),         # KERS/ERS input to engine: 0 to 1
        ("autoshifterOn",       DataTypes.SIGNED_INT.value),    # If auto shifter is enabled: 0 (false) or 1 (true)
        ("rideHeight",          DataTypes.FLOAT.value * 2),     # Right heights: front and rear
        ("turboBoost",          DataTypes.FLOAT.value),         # Turbo boost
        ("ballast",             DataTypes.FLOAT.value),         # Kilograms of ballast added to the car (only in multiplayer)
        ("airDensity ",         DataTypes.FLOAT.value),         # Air density
        ("airTemp",             DataTypes.FLOAT.value),         # Ambient temperature
        ("roadTemp",            DataTypes.FLOAT.value),         # Road temperature 
        ("localAngularVel",     DataTypes.FLOAT.value * 3),     # Angular velocity of the car [x, y, z]
        ("finalFF",             DataTypes.FLOAT.value),         # Current Force Feedback value;
        ("performanceMeter",    DataTypes.FLOAT.value),         # Performance meter compared to the best lap
        ("engineBrake",         DataTypes.SIGNED_INT.value),    # Engine brake setting
        ("ersRecoveryLevel",    DataTypes.SIGNED_INT.value),    # ERS recovery level
        ("ersPowerLevel",       DataTypes.SIGNED_INT.value),    # ERS selected power controller
        ("ersHeatCharging",     DataTypes.SIGNED_INT.value),    # ERS changing: 0 (Motor) or 1 (Battery)
        ("ersIsCharging",       DataTypes.SIGNED_INT.value),    # If ERS battery is recharging: 0 (false) or 1 (true)
        ("kersCurrentKJ",       DataTypes.FLOAT.value),         # KERS/ERS KiloJoule spent during the lap
        ("drsAvailable",        DataTypes.SIGNED_INT.value),    # If DRS is available (DRS zone): 0 (false) or 1 (true)
        ("drsEnabled",          DataTypes.SIGNED_INT.value),    # If DRS is enabled: 0 (false) or 1 (true)
        ("brakeTemp",           DataTypes.FLOAT.value * 4),     # Brake temp for each tire [Front Left, Front Right, Rear Left, Rear Right]
        ("clutch",              DataTypes.FLOAT.value),         # Value of clutch pedal: 0 to 1 (fully pressed)
        ("tyreTempI",           DataTypes.FLOAT.value * 4),     # Inner temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreTempM",           DataTypes.FLOAT.value * 4),     # Middle temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("tyreTempO",           DataTypes.FLOAT.value * 4),     # Outer temperature of each tyre [Front Left, Front Right, Rear Left, Rear Right]
        ("isAIControlled",      DataTypes.SIGNED_INT.value),    # AI controlled car: 0 (human) or 1 (AI)
        ("tyreContactPoint",    DataTypes.FLOAT.value * 4 * 3), # Vector for contact point of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("tyreContactNormal",   DataTypes.FLOAT.value * 4 * 3), # Vector for contact normal of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("tyreContactHeading",  DataTypes.FLOAT.value * 4 * 3), # Vector for contact heading of each tyre [Front Left, Front Right, Rear Left, Rear Right][x, y, z]
        ("brakeBias",           DataTypes.FLOAT.value),         # Brake bias from 0 (rear) to 1 (front)
        ("localVelocity",       DataTypes.FLOAT.value * 3),     # Vector for local velocity
    ]

# The following members change at each graphical step. They all refer to the player’s car.
class SPageFileGraphicData(DataTypes.STRUCTURE.value):
    # _pack_ = 1
    _fields_ = [
        ("packetId",                DataTypes.SIGNED_INT.value),        # Index of the shared memory’s current step
        ("status",                  DataTypes.SIGNED_INT.value),        # Status of the instance: AC_OFF 0, AC_REPLAY 1, AC_LIVE 2, AC_PAUSE 3
        ("session",                 DataTypes.SIGNED_INT.value),        # Session type: AC_UNKNOWN -1, AC_PRACTICE 0, AC_QUALIFY 1, AC_RACE 2, AC_HOTLAP 3, AC_TIME_ATTACK 4, AC_DRIFT 5, AC_DRAG 6
        ("currentTime",             DataTypes.CHAR.value * 15),         # Current lap time
        ("lastTime",                DataTypes.CHAR.value * 15),         # Last lap time
        ("bestTime",                DataTypes.CHAR.value * 15),         # Best lap time
        ("split",                   DataTypes.CHAR.value * 15),         # Time in sector
        ("completedLaps",           DataTypes.SIGNED_INT.value),        # Number of completed laps by the player
        ("position",                DataTypes.SIGNED_INT.value),        # Current player position (standings)
        ("iCurrentTime",            DataTypes.SIGNED_INT.value),        # Current lap time
        ("iLastTime",               DataTypes.SIGNED_INT.value),        # Last lap time
        ("iBestTime",               DataTypes.SIGNED_INT.value),        # Best lap time
        ("sessionTimeLeft",         DataTypes.FLOAT.value),             # Time left until session is closed
        ("distanceTraveled",        DataTypes.FLOAT.value),             # Distance traveled during the instance
        ("isInPit",                 DataTypes.SIGNED_INT.value),        # If player’s car is stopped in the pit: 0 (false) or 1 (true)
        ("currentSectorIndex",      DataTypes.SIGNED_INT.value),        # Current sector index
        ("lastSectorTime",          DataTypes.SIGNED_INT.value),        # Last sector time
        ("numberOfLaps",            DataTypes.SIGNED_INT.value),        # Number of laps needed to close the session
        ("tyreCompound",            DataTypes.CHAR.value * 33),         # Current tyre compound
        ("replayTimeMultiplier",    DataTypes.FLOAT.value),             # Replay multiplier
        ("normalizedCarPosition",   DataTypes.FLOAT.value),             # Car position on the track’s spline
        ("carCoordinates",          DataTypes.FLOAT.value * 3),         # Car position on world coordinates [x, y, z]
        ("penaltyTime",             DataTypes.FLOAT.value),             # Time of penalty
        ("flag",                    DataTypes.SIGNED_INT.value),        # Type of flag being shown: AC_NO_FLAG 0, AC_BLUE_FLAG 1, AC_YELLOW_FLAG 2, AC_BLACK_FLAG 3, AC_WHITE_FLAG 4, AC_CHECKERED_FLAG 5, AC_PENALTY_FLAG 6
        ("idealLineOn",             DataTypes.SIGNED_INT.value),        # If ideal line is enabled: 0 (false) or 1 (true)
        ("isInPitLane",             DataTypes.SIGNED_INT.value),        # If player’s car is in the pitlane: 0 (false) or 1 (true)
        ("surfaceGrip",             DataTypes.FLOAT.value),             # Current grip of the track’s surface
        ("mandatoryPitDone",        DataTypes.SIGNED_INT.value),        # Set to 1 if the player has done the mandatory pit
        ("windSpeed",               DataTypes.FLOAT.value),             # Speed of the wind on the current session
        ("windDirection",           DataTypes.FLOAT.value),             # Direction of the wind (0-359) on the current session
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