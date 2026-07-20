import ctypes
from enum import Flag, IntEnum

'''
packet information from
https://github.com/MacManley/project-cars-2-udp
and
https://web.archive.org/web/20220818194601/https://www.projectcarsgame.com/two/wp-content/uploads/sites/4/2018/01/sms_udp_definitions.hh
however this is outdated and the only one accessable from:
https://web.archive.org/web/20230201014848/https://www.projectcarsgame.com/two/project-cars-2-api/#1526544680534-1e10fcf7-b72a

'''

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    # UNION = ctypes.Union

    SIGNED_BYTE = ctypes.c_byte
    SIGNED_SHORT = ctypes.c_short

    UNSIGNED_INT = ctypes.c_uint
    UNSIGNED_INT16 = ctypes.c_uint16
    # UNSIGNED_INT16 = ctypes.c_uint8
    UNSIGNED_BYTE = ctypes.c_ubyte
    UNSIGNED_SHORT = ctypes.c_ushort

    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    SHORT = ctypes.c_short


### * Enums

class PacketName(IntEnum):
    Telemetry = 0
    Race_Data = 1
    Participants_Data = 2
    Timings_Data = 3
    Game_Data = 4
    Weather_State = 5
    Vehicle_Names = 6
    Time_Stats = 7
    Participants_Vehicle_Name = 8

class GameState(IntEnum):
    Exited = 0
    FrontEnd = 1
    Playing = 2
    Paused = 3
    InMenuTimeTicking = 4
    Restarting = 5
    Replay = 6
    FrontEndReplay = 7

class SessionState(IntEnum):
    Invalid = 0
    Practice = 1
    Test = 2
    Qualify = 3
    FormationLap = 4
    Race = 5
    TimeAttack = 6

class RaceState(IntEnum):
    Invalid = 0
    NotStarted = 1
    Racing = 2
    Finished = 3
    DSQ = 4
    Retired = 5
    DNF = 6

class FlagColours(IntEnum):
    Nothing = 0
    Green = 1
    Blue = 2
    WhiteSlowCar = 3
    WhiteFinalLap = 4
    Red = 5
    Yellow = 6
    DoubleYellow = 7
    BlackAndWhite = 8
    BlackOrangeCircle = 9
    Black = 10
    Chequered = 11

class FlagReason(IntEnum):
    Nothing = 0
    SoloCrash = 1
    VehicleCrash = 2
    VehicleObstruction = 3

class PitMode(IntEnum):
    Nothing = 0
    DrivingIntoPits = 1
    InPit = 2
    DrivingOutPits = 3
    InGarage = 4
    DrivingOutGarage = 5

class PitSchedule(IntEnum):
    Nothing = 0
    PlayerRequested = 1
    EngineerRequested = 2
    PitScheduleDamageRequested = 3
    PitScheduleMandatory = 4
    PitScheduleDriveThrough = 5
    PitScheduleStopGo = 6
    PitSchedulePitspotOccupied = 7

class TerrainMaterial(IntEnum):
    TerrainRoad = 0
    TerrainLowGripRoad = 1
    TerrainBumpyRoad1 = 2
    TerrainBumpyRoad2 = 3
    TerrainBumpyRoad3 = 4
    TerrainMarbles = 5
    TerrainGrassyBerms = 6
    TerrainGrass = 7
    TerrainGravel = 8
    TerrainBumpyGravel = 9
    TerrainRumbleStrips = 10
    TerrainDrains = 11
    TerrainTyrewalls = 12
    TerrainCementwalls = 13
    TerrainGuardrails = 14
    TerrainSand = 15
    TerrainBumpySand = 16
    TerrainDirt = 17
    TerrainBumpyDirt = 18
    TerrainDirtRoad = 19
    TerrainBumpyDirtRoad = 20
    TerrainPavement = 21
    TerrainDirtBank = 22
    TerrainWood = 23
    TerrainDryVerge = 24
    TerrainExitRumbleStrips = 25
    TerrainGrasscrete = 26
    TerrainLongGrass = 27
    TerrainSlopeGrass = 28
    TerrainCobbles = 29
    TerrainSandRoad = 30
    TerrainBakedClay = 31
    TerrainAstroturf = 32
    TerrainSnowhalf = 33
    TerrainSnowfull = 34
    TerrainDamagedRoad1 = 35
    TerrainTrainTrackRoad = 36
    TerrainBumpycobbles = 37
    TerrainAriesOnly = 38
    TerrainOrionOnly = 39
    TerrainB1rumbles = 40
    TerrainB2rumbles = 41
    TerrainRoughSandMedium = 42
    TerrainRoughSandHeavy = 43
    TerrainSnowwalls = 44
    TerrainIceRoad = 45
    TerrainRunoffRoad = 46
    TerrainIllegalStrip = 47
    TerrainPaintConcrete = 48
    TerrainPaintConcreteIllegal = 49
    TerrainRallyTarmac = 50

class CrashDamageState(IntEnum):
    Nothing = 0
    CrashDamageOfftrack = 1
    CrashDamageLargeProp = 2
    CrashDamageSpinning = 3
    CrashDamageRolling = 4

class CarFlags(Flag):
    Car_Headlight = 1
    Car_Engine_Active = 2
    Car_Engine_Warning = 4
    Car_Speed_Limit = 8
    Car_ABS = 16
    Car_Handbrake = 32

class TyreFlags(Flag):
    Tyre_Attached = 1
    Tyre_Inflated = 2
    Tyre_Is_On_Ground = 4

class DPadButton(Flag):
    Up = 1
    Down = 2
    Left = 4
    Right = 8

class JoyPadButton(Flag):
    Menu = 16
    Action = 32
    Left_Stick_Down = 64
    Right_Stick_Down = 128
    Left_Bumper = 256
    Right_Bumper = 512
    A_Button = 4096
    B_Button = 8192
    Y_Button = 32768
    X_Button = 16384


### * Data Structure

### Packet Header

#   Description: 
#    Base definitions of udp packet structure
#    The data definition mostly follows the data set for the Shared memory, so it is strongly suggested to have a look to the
#    latest shared memory header if you have problem decoding any data.

class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        PacketName: ("mPacketType",),
    }
    _fields_ = [
        ("mPacketNumber",           DataTypes.UNSIGNED_INT),     # Counter reflecting all the packets that have been sent during the game run
        ("mCategoryPacketNumber",   DataTypes.UNSIGNED_INT),     # Counter of the packet groups belonging to the given category
        ("mPartialPacketIndex",     DataTypes.UNSIGNED_BYTE),    # If the data from this class had to be sent in several packets, the index number
        ("mPartialPacketNumber",    DataTypes.UNSIGNED_BYTE),    # If the data from this class had to be sent in several packets, the total number
        ("mPacketType",             DataTypes.UNSIGNED_BYTE),    # What is the type of this packet (see EUDPStreamerPacketHanlderType for details)
        ("mPacketVersion",          DataTypes.UNSIGNED_BYTE),    # What is the version of protocol for this handler, to be bumped with data structure change
    ]


### Telemetry Packet -- Packet 0

#   Telemetry data for the viewed participant. 
#   Frequency: Each tick of the UDP streamer how it is set in the options
#   When it is sent: in race

class TelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (556 instead of at least 564 bytes)
    _enums_: dict[type, tuple[str, ...]] = {
        TerrainMaterial: ("sTerrain",),
        CrashDamageState: ("sCrashState",),
        CarFlags: ("sCarFlags",),
        TyreFlags: ("sTyreFlags",),
        DPadButton: ("sDPad",),
        JoyPadButton: ("sJoyPad",),
    }
    _fields_ = [
        ("s_header",                    PacketHeader),

        ("sViewedParticipantIndex",     DataTypes.SIGNED_BYTE),     # Index of currently viewed car 

        ("sUnfilteredThrottle",         DataTypes.UNSIGNED_BYTE),   # Unfiltered throttle input (RANGE: 0 -> 255)
        ("sUnfilteredBrake",            DataTypes.UNSIGNED_BYTE),   # Unfiltered brake input (RANGE: 0 -> 255)
        ("sUnfilteredSteering",         DataTypes.SIGNED_BYTE),     # Unfiltered steering input (RANGE: -127 -> 127)
        ("sUnfilteredClutch",           DataTypes.UNSIGNED_BYTE),   # Unfiltered clutch input (RANGE: 0 -> 255)

        ("sCarFlags",                   DataTypes.UNSIGNED_BYTE),   # Flags for different car states
        ("sOilTempCelsius",             DataTypes.SIGNED_SHORT),    # Oil temp in degrees Celsius
        ("sOilPressureKPa",             DataTypes.UNSIGNED_SHORT),  # Oil pressure in kPa
        ("sWaterTempCelsius",           DataTypes.SIGNED_SHORT),    # Water temp in degrees Celsius
        ("sWaterPressureKpa",           DataTypes.UNSIGNED_SHORT),  # Water pressure in kPa
        ("sFuelPressureKpa",            DataTypes.UNSIGNED_SHORT),  # Fuel pressure in kPa
        ("sFuelCapacity",               DataTypes.UNSIGNED_BYTE),   # Fuel capacity
        ("sBrake",                      DataTypes.UNSIGNED_BYTE),   # Filtered brake input (RANGE: 0 -> 255) 
        ("sThrottle",                   DataTypes.UNSIGNED_BYTE),   # Filtered throttle input (RANGE: 0 -> 255)
        ("sClutch",                     DataTypes.UNSIGNED_BYTE),   # Filtered clutch input (RANGE: 0 -> 255) 
        ("sFuelLevel",                  DataTypes.FLOAT),           # Current fuel level as a fraction of 1 (RANGE: 0.0f -> 1.0f)
        ("sSpeed",                      DataTypes.FLOAT),           # Speed in m/s
        ("sRpm",                        DataTypes.UNSIGNED_SHORT),  # RPM of drivetrain
        ("sMaxRpm",                     DataTypes.UNSIGNED_SHORT),  # Maximum RPM
        ("sSteering",                   DataTypes.SIGNED_BYTE),     # Filtered steering input (- = left, + = right) (RANGE: -127 -> 127)
        ("sGearNumGears",               DataTypes.UNSIGNED_BYTE),   # Data for number of gears in the car and currently selected gear
        ("sBoostAmount",                DataTypes.UNSIGNED_BYTE),   # Current amount of boost as a percentage
        ("sCrashState",                 DataTypes.UNSIGNED_BYTE),   # Crash damage state of car
        ("sOdometerKM",                 DataTypes.FLOAT),           # Odomoter of the car in km

        ("sOrientation",                DataTypes.FLOAT * 3),       # Orientation of car in Euler Angles
        ("sLocalVelocity",              DataTypes.FLOAT * 3),       # Local velocity of car in m/s
        ("sWorldVelocity",              DataTypes.FLOAT * 3),       # Velocity of the car relative to the world in m/s
        ("sAngularVelocity",            DataTypes.FLOAT * 3),       # Angular Velocity of the car in rads^-1
        ("sLocalAcceleration",          DataTypes.FLOAT * 3),       # Local acceleration of the car in m/s
        ("sWorldAcceleration",          DataTypes.FLOAT * 3),       # Acceleration of the car relative to the world in m/s
        ("sExtentsCentre",              DataTypes.FLOAT * 3),       # Centre position of the world

        ("sTyreFlags",                  DataTypes.UNSIGNED_BYTE * 4),   # Flags related to each tyre
        ("sTerrain",                    DataTypes.UNSIGNED_BYTE * 4),   # Current terrain type in contact with each tyre
        ("sTyreY",                      DataTypes.FLOAT * 4),           # Local tyre Y position
        ("sTyreRPS",                    DataTypes.FLOAT * 4),           # Anglular velocity of each wheel in rps
        ("sTyreTemp",                   DataTypes.UNSIGNED_BYTE * 4),   # Temperature of each tyre in degrees Celsius
        ("sTyreHeightAboveGround",      DataTypes.FLOAT * 4),           # Height of each tyre above the ground in meters
        ("sTyreWear",                   DataTypes.UNSIGNED_BYTE * 4),   # Wear of each tyre as a fraction of 255
        ("sBrakeDamage",                DataTypes.UNSIGNED_BYTE * 4),   # Brake damage for each wheel as a fraction of 255
        ("sSuspensionDamage",           DataTypes.UNSIGNED_BYTE * 4),   # Suspension damage at wheel as a fraction of 255
        ("sBrakeTempCelsius",           DataTypes.SIGNED_SHORT * 4),    # Temperature of each wheels brake in degrees Celsius
        ("sTyreTreadTemp",              DataTypes.UNSIGNED_SHORT * 4),  # Temperature of the tread for each tyre in Kelvins
        ("sTyreLayerTemp",              DataTypes.UNSIGNED_SHORT * 4),  # Temperature of the layer for each tyre in Kelvins
        ("sTyreCarcassTemp",            DataTypes.UNSIGNED_SHORT * 4),  # Temperature of the carcass for each tyre in Kelvins
        ("sTyreRimTemp",                DataTypes.UNSIGNED_SHORT * 4),  # Temperature of the rim for each tyre in Kelvins
        ("sTyreInternalAirTemp",        DataTypes.UNSIGNED_SHORT * 4),  # Temperature of the air in each tyre in Kelvins
        ("sTyreTempLeft",               DataTypes.UNSIGNED_SHORT * 4),  # Temperature on the left side for each tyre in Kelvins
        ("sTyreTempCenter",             DataTypes.UNSIGNED_SHORT * 4),  # Temperature in the centre for each tyre in Kelvins
        ("sTyreTempRight",              DataTypes.UNSIGNED_SHORT * 4),  # Temperature on the right side for each tyre in Kelvins
        ("sWheelLocalPositionY",        DataTypes.FLOAT * 4),           # Position of wheel relative to car
        ("sRideHeight",                 DataTypes.FLOAT * 4),           # Ride height of the car at each wheel in meters
        ("sSuspensionTravel",           DataTypes.FLOAT * 4),           # Travel of the suspension of each wheel in meters
        ("sSuspensionVelocity",         DataTypes.FLOAT * 4),           # Velocity of pushrod deflection at each wheel in m/s
        ("sSuspensionRideHeight",       DataTypes.UNSIGNED_SHORT * 4),  # Ride height of the suspension at each wheel in cm
        ("sAirPressure",                DataTypes.UNSIGNED_SHORT * 4),  # Air pressure of each tyre in centibar

        ("sEngineSpeed",                DataTypes.FLOAT),               # Speed of the enging in rads^-1
        ("sEngineTorque",               DataTypes.FLOAT),               # Torque of the engine in Nm
        ("sWings",                      DataTypes.UNSIGNED_BYTE * 2),   # How much wing is being used on the car (RANGE: 0 -> 255)
        ("sHandBrake",                  DataTypes.UNSIGNED_BYTE),       # Amount of handbrake applied as a fraction of 255

        ("sAeroDamage",                 DataTypes.UNSIGNED_BYTE),       # Damage to the aero as a fraction of 255
        ("sEngineDamage",               DataTypes.UNSIGNED_BYTE),       # Damage to the engine of the car as a fraction of 255

        ("sJoyPad",                     DataTypes.UNSIGNED_INT),        # Button input
        ("sDPad",                       DataTypes.UNSIGNED_BYTE),       # DPad input
        ("sTyreCompound",               DataTypes.CHAR * 40 * 4),       # Tyre compound name of each tyre
        ("sTurboBoostPressure",         DataTypes.FLOAT),               # Turbo boost pressure
        ("sFullPosition",               DataTypes.FLOAT * 3),           # Position of the viewed participant
        ("sBrakeBias",                  DataTypes.UNSIGNED_BYTE),       # Brake bias being used on the car as a fraction of 255
        ("sTickCount",                  DataTypes.UNSIGNED_INT),        # Game tick count
    ]


### Race Packet -- Packet 1

#   Race stats data.
#   Frequency: Logaritmic decrease
#   When it is sent: Counter resets on entering InRace state and again each time any of the values changes

class RaceData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sWorldFastestLapTime",            DataTypes.FLOAT),           # Fastest global laptime (FORMAT: SECONDS.MILLISECONDS)
        ("sPersonalFastestLapTime",         DataTypes.FLOAT),           # Fastest personal laptime (FORMAT: SECONDS.MILLISECONDS)
        ("sPersonalFastestSector1Time",     DataTypes.FLOAT),           # Fastest personal sector 1 time (FORMAT: SECONDS.MILLISECONDS)
        ("sPersonalFastestSector2Time",     DataTypes.FLOAT),           # Fastest personal sector 2 time (FORMAT: SECONDS.MILLISECONDS)
        ("sPersonalFastestSector3Time",     DataTypes.FLOAT),           # Fastest personal sector 3 time (FORMAT: SECONDS.MILLISECONDS)
        ("sWorldFastestSector1Time",        DataTypes.FLOAT),           # Fastest global sector 1 time (FORMAT: SECONDS.MILLISECONDS)
        ("sWorldFastestSector2Time",        DataTypes.FLOAT),           # Fastest global sector 2 time (FORMAT: SECONDS.MILLISECONDS)
        ("sWorldFastestSector3Time",        DataTypes.FLOAT),           # Fastest global sector 3 time (FORMAT: SECONDS.MILLISECONDS)
        ("sTrackLength",                    DataTypes.FLOAT),           # Track length in meters
        ("sTrackLocation",                  DataTypes.CHAR * 64),       # Track location
        ("sTrackVariation",                 DataTypes.CHAR * 64),       # Track variation
        ("sTranslatedTrackLocation",        DataTypes.CHAR * 64),       # Translated track location
        ("sTranslatedTrackVariation",       DataTypes.CHAR * 64),       # Translated track variation
        ("sLapsTimeInEvent",                DataTypes.UNSIGNED_SHORT),  # Contains lap number for lap based session or quantized session duration (number of 5mins) for timed sessions, the top bit is 1 for timed sessions
        ("sEnforcedPitStopLap",             DataTypes.SIGNED_BYTE),     # Mandatory pit stop lap
    ]


### Participants Packet -- Packet 2

#   Participant names data.
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#   The sParticipantsChangedTimestamp represent last time the participants has changed and is to be used to sync
#   this information with the rest of the participant related packets

class ParticipantsData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT),
        ("sName",                           DataTypes.CHAR * 64 * 16),      # Player Name
        ("sNationality",                    DataTypes.UNSIGNED_INT * 16),   # Player Nationality
        ("sIndex",                          DataTypes.UNSIGNED_SHORT * 16), # Session unique index in MP races
    ]


### Timings Packet -- Packet 3

#   Participant timings data. 
#   Frequency: Each tick of the UDP streamer how it is set in the options.
#   When it is sent: in race

class ParticipantsInfo(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _enums_: dict[type, tuple[str, ...]] = {
        RaceState: ("sRaceState",),
        FlagColours: ("sFlagColour",),  # sHighestFlag is split
        FlagReason: ("sFlagReason",),   # sHighestFlag is split
        PitMode: ("sPitMode",),         # sPitModeSchedule is split
        PitSchedule: ("sPitSchedule",), # sPitModeSchedule is split
    }
    _fields_ = [
        ("sWorldPosition",          DataTypes.SIGNED_SHORT * 3),
        ("sOrientation",            DataTypes.SIGNED_SHORT * 3),    # Quantized heading (-PI .. +PI) , Quantized pitch (-PI / 2 .. +PI / 2),  Quantized bank (-PI .. +PI)
        ("sCurrentLapDistance",     DataTypes.UNSIGNED_SHORT),      # Distance in current lap
        ("sRacePosition",           DataTypes.UNSIGNED_BYTE),       # Race position, + top bit shows if the participant is active or not
        ("sSector",                 DataTypes.UNSIGNED_BYTE),       # current sector + extra precision bits for x/z position
        # ("sHighestFlag",            DataTypes.UNSIGNED_BYTE),         # Flag color and reason - sHighestFlag is split into enum 4 bit / enum 4 bit
        ("sFlagColour",             DataTypes.UNSIGNED_BYTE, 4),    # Flag color - sHighestFlag is split into enum 4 bit / enum 4 bit
        ("sFlagReason",             DataTypes.UNSIGNED_BYTE, 4),    # Flag reason - sHighestFlag is split into enum 4 bit / enum 4 bit
        # ("sPitModeSchedule",        DataTypes.UNSIGNED_BYTE),         # Pit mode and pit schedule - sPitModeSchedule is split into enum 4 bit / enum 4 bit
        ("sPitMode",                DataTypes.UNSIGNED_BYTE, 4),    # Pit mode - sPitModeSchedule is split into enum 4 bit / enum 4 bit
        ("sPitSchedule",            DataTypes.UNSIGNED_BYTE, 4),    # Pit schedule - sPitModeSchedule is split into enum 4 bit / enum 4 bit
        ("sCarIndex",               DataTypes.UNSIGNED_SHORT),      # top bit shows if particpant is a human player or not
        ("sRaceState",              DataTypes.UNSIGNED_BYTE),       # race state flags & invalidated lap indication
        ("sCurrentLap",             DataTypes.UNSIGNED_BYTE),       # Current lap
        ("sCurrentTime",            DataTypes.FLOAT),               # Current lap time
        ("sCurrentSectorTime",      DataTypes.FLOAT),               # Current sector time
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_SHORT),      # Matches sIndex from ParticipantsData
    ]

class TimingsData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sNumParticipants",                DataTypes.SIGNED_BYTE),     # Number of participants
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT),
        ("sEventTimeRemaining",             DataTypes.FLOAT),           # Time remaining in the event
        ("sSplitTimeAhead",                 DataTypes.FLOAT),           # Split time to car ahead
        ("sSplitTimeBehind",                DataTypes.FLOAT),           # Split time to car behind
        ("sSplitTime",                      DataTypes.FLOAT),           # Split time
        ("sParticipants",                   ParticipantsInfo * 32),
        ("sLocalParticipantIndex",          DataTypes.UNSIGNED_SHORT),  # Identifies which participant is the local player
        ("sTickCount",                      DataTypes.UNSIGNED_INT),    # Tick count of game
    ]


### Game State Packet -- Packet 4

#   Game State. 
#   Frequency: Each 5s while being in Main Menu, Each 10s while being in race + on each change Main Menu<->Race several times.
#   the frequency in Race is increased in case of weather timer being faster  up to each 5s for 30x time progression
#   When it is sent: Always

class GameStateData(DataTypes.STRUCTURE):
    _pack_ = 1
    _enums_: dict[type, tuple[str, ...]] = {
        GameState: ("mGameState",),         # mGameState is split
        SessionState: ("mSessionState",),   # mGameState is split
    }
    _fields_ = [
        ("s_header",                PacketHeader),
        ("mBuildVersionNumber",     DataTypes.UNSIGNED_SHORT),      # Build version number
        # ("mGameState",              DataTypes.UNSIGNED_BYTE),         # Game state
        ("mGameState",              DataTypes.UNSIGNED_BYTE, 4),    # Game state - mGameState is split into enum 4 bit / enum 4 bit
        ("mSessionState",           DataTypes.UNSIGNED_BYTE, 4),    # Session state - mGameState is split into enum 4 bit / enum 4 bit
        ("sAmbientTemperature",     DataTypes.SIGNED_BYTE),         # Ambient temperature
        ("sTrackTemperature",       DataTypes.SIGNED_BYTE),         # Track temperature
        ("sRainDensity",            DataTypes.UNSIGNED_BYTE),       # Rain density (RANGE: 0 -> 255)
        ("sSnowDensity",            DataTypes.UNSIGNED_BYTE),       # Snow density (RANGE: 0 -> 255) (will be same as sRainDensity on non-snow tracks)
        ("sWindSpeed",              DataTypes.SIGNED_BYTE),         # Wind speed
        ("sWindDirectionX",         DataTypes.SIGNED_BYTE),         # Wind direction in X Direction
        ("sWindDirectionY",         DataTypes.SIGNED_BYTE),         # Wind Direction in Y Direction
        ("paddingD",                DataTypes.SHORT),
    ]


### Time Stats Packet -- Packet 7

#   Participant Stats and records
#   Frequency: When entering the race and each time any of the values change, so basically each time any of the participants crosses a sector boundary.
#   When it is sent: In Race

class ParticipantStatsInfo(DataTypes.STRUCTURE):
    _fields_ = [
        ("sFastestLapTime",         DataTypes.FLOAT),           # Fastest lap of the selected participant
        ("sLastLapTime",            DataTypes.FLOAT),           # Last lap time of the selected participant
        ("sLastSectorTime",         DataTypes.FLOAT),           # The last logged sector time of the selected participant
        ("sFastestSector1Time",     DataTypes.FLOAT),           # Fastest S1 time of the selected participant
        ("sFastestSector2Time",     DataTypes.FLOAT),           # Fastest S2 time of the selected participant
        ("sFastestSector3Time",     DataTypes.FLOAT),           # Fastest S3 time of the selected participant
        ("sRankType",               DataTypes.UNSIGNED_INT16),  # Which safety rank the competitor is
        ("sStrength",               DataTypes.UNSIGNED_INT16),  # Strength of the competitor
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_INT16),  # Index of viewed participant (matches sIndex from participantsdata)
    ]

class ParticipantsStats(DataTypes.STRUCTURE):
    _fields_ = [
        ("sParticipants",   ParticipantStatsInfo * 32),
    ]

class TimeStatsData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT),
        ("sStats",                          ParticipantsStats),
    ]


### Participants Vehicle Names Packet / Vehicle Class Names Packet -- Packet 8

#   Participant Vehicle names
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#	The sParticipantsChangedTimestamp represent last time the participants has changed and is  to be used to sync 
#	this information with the rest of the participant related packets
#   Note: This data is always sent with at least 2 packets. The 1-(n-1) holds the vehicle name for each participant
#	The last one holding the class names.

class VehicleInfo(DataTypes.STRUCTURE):
    _fields_ = [
        ("sIndex",  DataTypes.UNSIGNED_SHORT),  # Index
        ("sClass",  DataTypes.UNSIGNED_INT),    # Vehicle class
        ("sName",   DataTypes.CHAR * 64),       # Vehicle name
    ]

class ParticipantVehicleNamesData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",        PacketHeader),
        ("sVehicleInfo",    VehicleInfo * 16),
    ]

class ClassInfo(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("sClassIndex", DataTypes.UNSIGNED_INT),    # Index of class
        ("sName",       DataTypes.CHAR * 20),       # Class name
    ]

class VehicleClassNamesData(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("s_header",    PacketHeader),
        ("sClassInfo",  ClassInfo * 60),
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = 5606
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple | None = None
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: type | None = PacketHeader
    packetIDAttribute: str | None = 'mPacketType'
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = "$pcars2$"
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (TelemetryData,),
        1: (RaceData,),
        2: (ParticipantsData,),
        3: (TimingsData,),
        4: (GameStateData,),
        7: (TimeStatsData,),
        8: (VehicleClassNamesData, ParticipantVehicleNamesData),
    }




