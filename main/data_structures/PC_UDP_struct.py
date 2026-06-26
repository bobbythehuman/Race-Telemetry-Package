import ctypes
from enum import Enum, Flag, IntEnum

'''
udp
https://docs.google.com/spreadsheets/d/1UTgeE7vbnGIzDz-URRk2eBIPc_LR1vWcZklp7xD9N0Y/edit?gid=293667394#gid=293667394
https://web.archive.org/web/20160826185519/http://forum.projectcarsgame.com/showthread.php?40113-HowTo-Companion-App-UDP-Streaming&s=0147744ec824a4eb44be2e778d278c49
https://web.archive.org/web/20180111115541/http://forum.projectcarsgame.com/showthread.php?40113-COMPLETE-Companion-app-UDP-streaming
'''

class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    # UNION = ctypes.Union

    SIGNED_INT16 = ctypes.c_int16
    SIGNED_INT8 = ctypes.c_int8
    
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT8 = ctypes.c_uint8

    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    BOOL = ctypes.c_bool


### * Enums

class PacketName(IntEnum):
    TelemetryData = 0
    ParticipantInfoStrings = 1
    ParticipantInfoStringsAdditional = 2

class GameState(IntEnum):
    GAME_EXITED  = 0
    GAME_FRONT_END = 1
    GAME_INGAME_PLAYING = 2
    GAME_INGAME_PAUSED = 3

class SessionState(IntEnum):
    SESSION_INVALID  = 0
    SESSION_PRACTICE = 1
    SESSION_TEST = 2
    SESSION_QUALIFY = 3
    SESSION_FORMATION_LAP = 4
    SESSION_RACE = 5
    SESSION_TIME_ATTACK = 6

class RaceState(IntEnum):
    RACESTATE_INVALID = 0
    RACESTATE_NOT_STARTED = 1
    RACESTATE_RACING = 2
    RACESTATE_FINISHED = 3
    RACESTATE_DISQUALIFIED = 4
    RACESTATE_RETIRED = 5
    RACESTATE_DNF = 6

class CurrentSector(IntEnum):
    SECTOR_INVALID = 0
    SECTOR_START = 0
    SECTOR_SECTOR1 = 0
    SECTOR_SECTOR2 = 0
    SECTOR_FINISH = 0
    SECTOR_STOP = 0

class FlagColours(IntEnum):
    FLAG_COLOUR_NONE  = 0			# Not used for actual flags, only for some query functions
    FLAG_COLOUR_GREEN = 1			# End of danger zone, or race started
    FLAG_COLOUR_BLUE = 2			# Faster car wants to overtake the participant
    FLAG_COLOUR_WHITE = 3			# Approaching a slow car
    FLAG_COLOUR_YELLOW = 4			# Danger on the racing surface itself
    FLAG_COLOUR_DOUBLE_YELLOW = 5	# Danger that wholly or partly blocks the racing surface
    FLAG_COLOUR_BLACK = 6			# Participant disqualified
    FLAG_COLOUR_CHEQUERED = 7		# Chequered flag

class FlagReason(IntEnum):
    FLAG_REASON_NONE  = 0
    FLAG_REASON_SOLO_CRASH = 1
    FLAG_REASON_VEHICLE_CRASH = 2
    FLAG_REASON_VEHICLE_OBSTRUCTION = 3

class PitMode(IntEnum):
    PIT_MODE_NONE  = 0
    PIT_MODE_DRIVING_INTO_PITS = 1
    PIT_MODE_IN_PIT = 2
    PIT_MODE_DRIVING_OUT_OF_PITS = 3
    PIT_MODE_IN_GARAGE = 4

class PitSchedule(IntEnum):
    PIT_SCHEDULE_NONE  = 0			# Nothing scheduled
    PIT_SCHEDULE_STANDARD = 1		# Used for standard pit sequence
    PIT_SCHEDULE_DRIVE_THROUGH = 2	# Used for drive-through penalty
    PIT_SCHEDULE_STOP_GO = 3		# Used for stop-go penalty

class CarFlags(Flag):
    CAR_HEADLIGHT = 1
    CAR_ENGINE_ACTIVE = 2
    CAR_ENGINE_WARNING = 4
    CAR_SPEED_LIMITER = 8
    CAR_ABS = 16
    CAR_HANDBRAKE = 32
    CAR_STABILITY = 64
    CAR_TRACTION_CONTROL = 128

class TyreFlags(Flag):
    TYRE_ATTACHED = 1
    TYRE_INFLATED = 2
    TYRE_IS_ON_GROUND = 4

class TerrainMaterial(IntEnum):
    TERRAIN_ROAD = 0
    TERRAIN_LOW_GRIP_ROAD = 1
    TERRAIN_BUMPY_ROAD1 = 2
    TERRAIN_BUMPY_ROAD2 = 3
    TERRAIN_BUMPY_ROAD3 = 4
    TERRAIN_MARBLES = 5
    TERRAIN_GRASSY_BERMS = 6
    TERRAIN_GRASS = 7
    TERRAIN_GRAVEL = 8
    TERRAIN_BUMPY_GRAVEL = 9
    TERRAIN_RUMBLE_STRIPS = 10
    TERRAIN_DRAINS = 11
    TERRAIN_TYREWALLS = 12
    TERRAIN_CEMENTWALLS = 13
    TERRAIN_GUARDRAILS = 14
    TERRAIN_SAND = 15
    TERRAIN_BUMPY_SAND = 16
    TERRAIN_DIRT = 17
    TERRAIN_BUMPY_DIRT = 18
    TERRAIN_DIRT_ROAD = 19
    TERRAIN_BUMPY_DIRT_ROAD = 20
    TERRAIN_PAVEMENT = 21
    TERRAIN_DIRT_BANK = 22
    TERRAIN_WOOD = 23
    TERRAIN_DRY_VERGE = 24
    TERRAIN_EXIT_RUMBLE_STRIPS = 25
    TERRAIN_GRASSCRETE = 26
    TERRAIN_LONG_GRASS = 27
    TERRAIN_SLOPE_GRASS = 28
    TERRAIN_COBBLES = 29
    TERRAIN_SAND_ROAD = 30
    TERRAIN_BAKED_CLAY = 31
    TERRAIN_ASTROTURF = 32
    TERRAIN_SNOWHALF = 33
    TERRAIN_SNOWFULL = 34

class CrashDamageState(IntEnum):
    CRASH_DAMAGE_NONE  = 0
    CRASH_DAMAGE_OFFTRACK = 1
    CRASH_DAMAGE_LARGE_PROP = 2
    CRASH_DAMAGE_SPINNING = 3
    CRASH_DAMAGE_ROLLING = 4

class DPadButton(Flag):
    Up = 1
    Down = 2
    Left = 4
    Right = 8

class JoyPadButton(Flag):
    Start = 16
    Back = 32
    Left_Stick_Down = 64
    Right_Stick_Down = 128
    Left_Bumper = 256
    Right_Bumper = 512
    A_Button = 4096
    B_Button = 8192
    X_Button = 16384
    Y_Button = 32768


### * Data Structure

class sParticipantInfo(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        CurrentSector: ("sSector",),
    }
    _fields_ = [
        ("sWorldPosition",			DataTypes.SIGNED_INT16 * 3),	# 0
        ("sCurrentLapDistance",		DataTypes.UNSIGNED_INT16),		# 6
        ("sRacePosition",			DataTypes.UNSIGNED_INT8),		# 8
        ("sLapsCompleted",			DataTypes.UNSIGNED_INT8),		# 9
        ("sCurrentLap",				DataTypes.UNSIGNED_INT8),		# 10
        ("sSector",					DataTypes.UNSIGNED_INT8),		# 11
        ("sLastSectorTime",			DataTypes.FLOAT),				# 14
    ]

class sParticipantInfoStrings(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        PacketName: ("sPacketType",),
    }
    _fields_ = [
        ("sBuildVersionNumber", DataTypes.UNSIGNED_INT16),  # 0
        # ("sPacketType",         DataTypes.UNSIGNED_INT8),   # 2
        ("sPacketType",         DataTypes.UNSIGNED_INT8, 2),   # 2
        ("sSequenceNumber",     DataTypes.UNSIGNED_INT8, 6),   # 2
        ("sCarName",            DataTypes.CHAR * 64),       # 3
        ("sCarClassName",       DataTypes.CHAR * 64),       # 67
        ("sTrackLocation",      DataTypes.CHAR * 64),       # 131
        ("sTrackVariation",     DataTypes.CHAR * 64),       # 195
        ("sName",               DataTypes.CHAR * 16 * 64),  # 259
        ("sFastestLapTime",     DataTypes.FLOAT * 16),      # 1283
    ]

class sParticipantInfoStringsAdditional(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        PacketName: ("sPacketType",),
    }
    _fields_ = [
        ("sBuildVersionNumber", DataTypes.UNSIGNED_INT16),  # 0
        # ("sPacketType",         DataTypes.UNSIGNED_INT8),   # 2
        ("sPacketType",         DataTypes.UNSIGNED_INT8, 2),   # 2
        ("sSequenceNumber",     DataTypes.UNSIGNED_INT8, 6),   # 2
        ("sOffset",             DataTypes.UNSIGNED_INT8),   # 3
        ("sName",               DataTypes.CHAR * 16 * 64),  # 4
    ]

class sTelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        PacketName: ("sPacketType",),
        GameState: ("sGameState",),         # sGameSessionState is split
        SessionState: ("sSessionState",),   # sGameSessionState is split
        JoyPadButton: ("sJoyPad",),
        FlagColours: ("sFlagColour",),  # sHighestFlag is split
        FlagReason: ("sFlagReason",),   # sHighestFlag is split
        PitMode: ("sPitMode",),         # sPitModeSchedule is split
        PitSchedule: ("sPitSchedule",), # sPitModeSchedule is split
        CarFlags: ("sCarFlags",),
        CrashDamageState: ("sCrashState",),
        TyreFlags: ("sTyreFlags",),
        TerrainMaterial: ("sTerrain",),
        DPadButton: ("sDPad",),
    }
    _fields_ = [
        ("sBuildVersionNumber", DataTypes.UNSIGNED_INT16),  # 0
        # ("sPacketType",         DataTypes.UNSIGNED_INT8),   # 2
        ("sPacketType",         DataTypes.UNSIGNED_INT8, 2),   # 2
        ("sSequenceNumber",     DataTypes.UNSIGNED_INT8, 6),   # 2
        
        # Game States
        # ("sGameSessionState",   DataTypes.UNSIGNED_INT8),   # 3
        ("sGameState",   DataTypes.UNSIGNED_INT8, 4),   # 3
        ("sSessionState",   DataTypes.UNSIGNED_INT8, 4),   # 3
        
        # Participant Info
        ("sViewedParticipantIndex", DataTypes.SIGNED_INT8), # 4
        ("sNumParticipants",        DataTypes.SIGNED_INT8), # 5
        
        # Unfiltered Input
        ("sUnfilteredThrottle",     DataTypes.UNSIGNED_INT8),   # 6
        ("sUnfilteredBrake",        DataTypes.UNSIGNED_INT8),   # 7
        ("sUnfilteredSteering",     DataTypes.SIGNED_INT8),     # 8
        ("sUnfilteredClutch",       DataTypes.UNSIGNED_INT8),   # 9
        ("sRaceStateFlags",         DataTypes.UNSIGNED_INT8),   # 10
        
        # Event Information
        ("sLapsInEvent",    DataTypes.UNSIGNED_INT8),   # 11
        
        # Timings
        ("sBestLapTime",                    DataTypes.FLOAT),   # 12
        ("sLastLapTime",                    DataTypes.FLOAT),   # 16
        ("sCurrentTime",                    DataTypes.FLOAT),   # 20
        ("sSplitTimeAhead",                 DataTypes.FLOAT),   # 24
        ("sSplitTimeBehind",                DataTypes.FLOAT),   # 28
        ("sSplitTime",                      DataTypes.FLOAT),   # 32
        ("sEventTimeRemaining",             DataTypes.FLOAT),   # 36
        ("sPersonalFastestLapTime",         DataTypes.FLOAT),   # 40
        ("sWorldFastestLapTime",            DataTypes.FLOAT),   # 44
        ("sCurrentSector1Time",             DataTypes.FLOAT),   # 48
        ("sCurrentSector2Time",             DataTypes.FLOAT),   # 52
        ("sCurrentSector3Time",             DataTypes.FLOAT),   # 56
        ("sFastestSector1Time",             DataTypes.FLOAT),   # 60
        ("sFastestSector2Time",             DataTypes.FLOAT),   # 64
        ("sFastestSector3Time",             DataTypes.FLOAT),   # 68
        ("sPersonalFastestSector1Time",     DataTypes.FLOAT),   # 72
        ("sPersonalFastestSector2Time",     DataTypes.FLOAT),   # 76
        ("sPersonalFastestSector3Time",     DataTypes.FLOAT),   # 80
        ("sWorldFastestSector1Time",        DataTypes.FLOAT),   # 84
        ("sWorldFastestSector2Time",        DataTypes.FLOAT),   # 88
        ("sWorldFastestSector3Time",        DataTypes.FLOAT),   # 92
        
        ("sJoyPad",     DataTypes.UNSIGNED_INT16),  # 96
        
        # Flags
        # ("sHighestFlag",    DataTypes.UNSIGNED_INT8),   # 98
        ("sFlagColour",     DataTypes.UNSIGNED_INT8, 4),   # 98
        ("sFlagReason",      DataTypes.UNSIGNED_INT8, 4),   # 98
        
        # ("sPitModeSchedule",    DataTypes.UNSIGNED_INT8),   # 99
        ("sPitMode",        DataTypes.UNSIGNED_INT8, 4),   # 99
        ("sPitSchedule",    DataTypes.UNSIGNED_INT8, 4),   # 99
        
        ("sOilTempCelsius",         DataTypes.SIGNED_INT16),    # 100
        ("sOilPressureKPa",         DataTypes.UNSIGNED_INT16),  # 102
        ("sWaterTempCelsius",       DataTypes.SIGNED_INT16),    # 104
        ("sWaterPressureKpa",       DataTypes.UNSIGNED_INT16),  # 106
        ("sFuelPressureKpa",        DataTypes.UNSIGNED_INT16),  # 108
        ("sCarFlags",               DataTypes.UNSIGNED_INT8),   # 110
        ("sFuelCapacity",           DataTypes.UNSIGNED_INT8),   # 111
        ("sBrake",                  DataTypes.UNSIGNED_INT8),   # 112
        ("sThrottle",               DataTypes.UNSIGNED_INT8),   # 113
        ("sClutch",                 DataTypes.UNSIGNED_INT8),   # 114
        ("sSteering",               DataTypes.SIGNED_INT8),   # 115
        ("sFuelLevel",              DataTypes.FLOAT),           # 116
        ("sSpeed",                  DataTypes.FLOAT),           # 120
        ("sRpm",                    DataTypes.UNSIGNED_INT16),  # 124
        ("sMaxRpm",                 DataTypes.UNSIGNED_INT16),  # 126
        ("sGearNumGears",           DataTypes.UNSIGNED_INT8),   # 128
        ("sBoostAmount",            DataTypes.UNSIGNED_INT8),   # 129
        ("sEnforcedPitStopLap",     DataTypes.SIGNED_INT8),     # 130
        ("sCrashState",             DataTypes.UNSIGNED_INT8),   # 131
        
        ("sOdometerKM",             DataTypes.FLOAT),		# 132
        ("sOrientation",            DataTypes.FLOAT * 3),	# 136
        ("sLocalVelocity",          DataTypes.FLOAT * 3),	# 148
        ("sWorldVelocity",          DataTypes.FLOAT * 3),	# 160
        ("sAngularVelocity",        DataTypes.FLOAT * 3),	# 172
        ("sLocalAcceleration",      DataTypes.FLOAT * 3),	# 184
        ("sWorldAcceleration",      DataTypes.FLOAT * 3),	# 196
        ("sExtentsCentre",          DataTypes.FLOAT * 3),	# 208
        
        # Wheels / Tyres
        ("sTyreFlags",					DataTypes.UNSIGNED_INT8 * 4),	# 220
        ("sTerrain",					DataTypes.UNSIGNED_INT8 * 4),	# 224
        ("sTyreY",						DataTypes.FLOAT * 4),			# 228
        ("sTyreRPS",					DataTypes.FLOAT * 4),			# 244
        ("sTyreSlipSpeed",				DataTypes.FLOAT * 4),			# 260
        ("sTyreTemp",					DataTypes.UNSIGNED_INT8 * 4),	# 276
        ("sTyreGrip",					DataTypes.UNSIGNED_INT8 * 4),	# 280
        ("sTyreHeightAboveGround",		DataTypes.FLOAT * 4),			# 284
        ("sTyreLateralStiffness",		DataTypes.FLOAT * 4),			# 300
        ("sTyreWear",					DataTypes.UNSIGNED_INT8 * 4),	# 316
        ("sBrakeDamage",				DataTypes.UNSIGNED_INT8 * 4),	# 320
        ("sSuspensionDamage",			DataTypes.UNSIGNED_INT8 * 4),	# 324
        ("sBrakeTempCelsius",			DataTypes.SIGNED_INT16 * 4),	# 328
        ("sTyreTreadTemp",				DataTypes.UNSIGNED_INT16 * 4),	# 336
        ("sTyreLayerTemp",				DataTypes.UNSIGNED_INT16 * 4),	# 344
        ("sTyreCarcassTemp",			DataTypes.UNSIGNED_INT16 * 4),	# 352
        ("sTyreRimTemp",				DataTypes.UNSIGNED_INT16 * 4),	# 360
        ("sTyreInternalAirTemp",		DataTypes.UNSIGNED_INT16 * 4),	# 368
        ("sWheelLocalPositionY",		DataTypes.FLOAT * 4),			# 376
        ("sRideHeight",					DataTypes.FLOAT * 4),			# 392
        ("sSuspensionTravel",			DataTypes.FLOAT * 4),			# 408
        ("sSuspensionVelocity",			DataTypes.FLOAT * 4),			# 424
        ("sAirPressure",				DataTypes.UNSIGNED_INT16 * 4),	# 440
        
        # Extras
        ("sEngineSpeed",	DataTypes.FLOAT),	# 448
        ("sEngineTorque",	DataTypes.FLOAT),	# 452
        
        # Car Damage
        ("sAeroDamage",		DataTypes.UNSIGNED_INT8),	# 456
        ("sEngineDamage",	DataTypes.UNSIGNED_INT8),	# 457
        
        # Weather
        ("sAmbientTemperature",		DataTypes.SIGNED_INT8),		# 458
        ("sTrackTemperature",		DataTypes.SIGNED_INT8),		# 459
        ("sRainDensity",			DataTypes.UNSIGNED_INT8),	# 460
        ("sWindSpeed",				DataTypes.SIGNED_INT8),		# 461
        ("sWindDirectionX",			DataTypes.SIGNED_INT8),		# 462
        ("sWindDirectionY",			DataTypes.SIGNED_INT8),		# 463
        
        ("sParticipantInfo",	sParticipantInfo * 56),	# 464, 56*16=896
        
        ("sTrackLength",	DataTypes.FLOAT),				# 1360
        ("sWings",			DataTypes.UNSIGNED_INT8 * 2),	# 1364
        ("sDPad",			DataTypes.UNSIGNED_INT8),		# 1366
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
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (sTelemetryData, sParticipantInfoStrings, sParticipantInfoStringsAdditional),
    }
