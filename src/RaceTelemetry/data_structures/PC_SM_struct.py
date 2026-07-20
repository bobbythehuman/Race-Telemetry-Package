import ctypes
from enum import Flag, IntEnum


# https://web.archive.org/web/20180111115813/http://forum.projectcarsgame.com/showthread.php?30903-Project-CARS-Shared-Memory-or-how-do-I-make-my-own-app&highlight=shared+memory+api


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


### * Data Structure

class mParticipantInfo(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        CurrentSector: ("mCurrentSector",),
    }
    _fields_ = [
        ("mIsActive",          		DataTypes.BOOL),
        ("mName",     				DataTypes.CHAR * 64),		# [ string ]
        ("mWorldPosition",			DataTypes.FLOAT * 3),		# [ UNITS = World Space  X  Y  Z ]
        ("mCurrentLapDistance",		DataTypes.FLOAT),			# [ UNITS = Metres ]   [ RANGE = 0.0f->... ]    [ UNSET = 0.0f ]
        ("mRacePosition",			DataTypes.UNSIGNED_INT8),	# [ RANGE = 1->... ]   [ UNSET = 0 ]
        ("mLapsCompleted",			DataTypes.UNSIGNED_INT8),	# [ RANGE = 0->... ]   [ UNSET = 0 ]
        ("mCurrentLap",         	DataTypes.UNSIGNED_INT8),	# [ RANGE = 0->... ]   [ UNSET = 0 ]
        ("mCurrentSector",         	DataTypes.UNSIGNED_INT8),	# [ enum (Type#4) Current Sector ]
    ]

class mTelemetryData(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs
    _enums_: dict[type, tuple[str, ...]] = {
        GameState: ("mGameState",),
        SessionState: ("mSessionState",),
        RaceState: ("mRaceState",),
        FlagColours: ("mHighestFlagColour",),
        FlagReason: ("mHighestFlagReason",),
        PitMode: ("mPitMode",),
        PitSchedule: ("mPitSchedule",),
        CarFlags: ("mCarFlags",),
        TyreFlags: ("mTyreFlags",),
        TerrainMaterial: ("mTerrain",),
        CrashDamageState: ("mCrashState",),
    }
    _fields_ = [
        # Version Number
        ("mVersion", 			DataTypes.UNSIGNED_INT8),	# [ RANGE = 0->... ]
        ("mBuildVersionNumber",	DataTypes.UNSIGNED_INT8),	# [ RANGE = 0->... ]   [ UNSET = 0 ]
        
        # Game States
        ("mGameState",			DataTypes.UNSIGNED_INT8),	# [ enum (Type#1) Game state ]
        ("mSessionState",		DataTypes.UNSIGNED_INT8),	# [ enum (Type#2) Session state ]
        ("mRaceState",			DataTypes.UNSIGNED_INT8),	# [ enum (Type#3) Race State ]
        
        # Participant Info
        ("mViewedParticipantIndex",	DataTypes.SIGNED_INT8),	# [ RANGE = 0->STORED_PARTICIPANTS_MAX ]   [ UNSET = -1 ]
        ("mNumParticipants",		DataTypes.SIGNED_INT8),	# [ RANGE = 0->STORED_PARTICIPANTS_MAX ]   [ UNSET = -1 ]
        ("mParticipantInfo",		mParticipantInfo * 64),	# [ struct (Type#13) ParticipantInfo struct ]
        
        # Unfiltered Input
        ("mUnfilteredThrottle",		DataTypes.FLOAT),	# [ RANGE = 0.0f->1.0f ]
        ("mUnfilteredBrake",		DataTypes.FLOAT),	# [ RANGE = 0.0f->1.0f ]
        ("mUnfilteredSteering",		DataTypes.FLOAT),	# [ RANGE = -1.0f->1.0f ]
        ("mUnfilteredClutch",		DataTypes.FLOAT),	# [ RANGE = 0.0f->1.0f ]
        
        # Vehicle Information
        ("mCarName",		DataTypes.CHAR * 64),	# [ string ]
        ("mCarClassName",	DataTypes.CHAR * 64),	# [ string ]
        
        # Event Information
        ("mLapsInEvent",	DataTypes.UNSIGNED_INT8),	# [ RANGE = 0->... ]   [ UNSET = 0 ]
        ("mTrackLocation",	DataTypes.CHAR * 64),		# [ string ]
        ("mTrackVariation",	DataTypes.CHAR * 64),		# [ string ]
        ("mTrackLength",	DataTypes.FLOAT),			# [ UNITS = Metres ]   [ RANGE = 0.0f->... ]    [ UNSET = 0.0f ]
        
        # Timings
        ("mLapInvalidated",					DataTypes.BOOL),	# [ UNITS = boolean ]   [ RANGE = false->true ]   [ UNSET = false ]
        ("mBestLapTime",					DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mLastLapTime",					DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mCurrentTime",					DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mSplitTimeAhead",					DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mSplitTimeBehind",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mSplitTime",						DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mEventTimeRemaining",				DataTypes.FLOAT),	# [ UNITS = milli-seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mPersonalFastestLapTime",			DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mWorldFastestLapTime",			DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mCurrentSector1Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mCurrentSector2Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mCurrentSector3Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mFastestSector1Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mFastestSector2Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mFastestSector3Time",				DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mPersonalFastestSector1Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mPersonalFastestSector2Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mPersonalFastestSector3Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mWorldFastestSector1Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mWorldFastestSector2Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mWorldFastestSector3Time",		DataTypes.FLOAT),	# [ UNITS = seconds ]   [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        
        # Flags
        ("mHighestFlagColour",	DataTypes.UNSIGNED_INT8),	# [ enum (Type#5) Flag Colour ]
        ("mHighestFlagReason",	DataTypes.UNSIGNED_INT8),	# [ enum (Type#6) Flag Reason ]
        
        # Pit Info
        ("mPitMode",		DataTypes.UNSIGNED_INT8),	# [ enum (Type#7) Pit Mode ]
        ("mPitSchedule",	DataTypes.UNSIGNED_INT8),	# [ enum (Type#8) Pit Stop Schedule ]
        
        # Car State
        ("mCarFlags",						DataTypes.UNSIGNED_INT8),	# [ enum (Type#9) Car Flags ]
        ("mOilTempCelsius",					DataTypes.FLOAT),			# [ UNITS = Celsius ]   [ UNSET = 0.0f ]
        ("mOilPressureKPa",					DataTypes.FLOAT),			# [ UNITS = Kilopascal ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mWaterTempCelsius",				DataTypes.FLOAT),			# [ UNITS = Celsius ]   [ UNSET = 0.0f ]
        ("mWaterPressureKpa",				DataTypes.FLOAT),			# [ UNITS = Kilopascal ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mFuelPressureKpa",				DataTypes.FLOAT),			# [ UNITS = Kilopascal ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mFuelLevel",						DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        ("mFuelCapacity",					DataTypes.FLOAT),			# [ UNITS = Liters ]   [ RANGE = 0.0f->1.0f ]   [ UNSET = 0.0f ]
        ("mSpeed",							DataTypes.FLOAT),			# [ UNITS = Metres per-second ]   [ RANGE = 0.0f->... ]
        ("mRpm",							DataTypes.FLOAT),			# [ UNITS = Revolutions per minute ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mMaxRpm",							DataTypes.FLOAT),			# [ UNITS = Revolutions per minute ]   [ RANGE = 0.0f->... ]   [ UNSET = 0.0f ]
        ("mBrake",							DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        ("mThrottle",						DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        ("mClutch",							DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        ("mSteering",						DataTypes.FLOAT),			# [ RANGE = -1.0f->1.0f ]
        ("mGear",							DataTypes.SIGNED_INT8),		# [ RANGE = -1 (Reverse)  0 (Neutral)  1 (Gear 1)  2 (Gear 2)  etc... ]   [ UNSET = 0 (Neutral) ]
        ("mNumGears",						DataTypes.SIGNED_INT8),		# [ RANGE = 0->... ]   [ UNSET = -1 ]
        ("mOdometerKM",						DataTypes.FLOAT),			# [ RANGE = 0.0f->... ]   [ UNSET = -1.0f ]
        ("mAntiLockActive",					DataTypes.SIGNED_INT8),		# [ UNITS = boolean ]   [ RANGE = false->true ]   [ UNSET = false ]
        ("mLastOpponentCollisionIndex",		DataTypes.SIGNED_INT8),		# [ RANGE = 0->STORED_PARTICIPANTS_MAX ]   [ UNSET = -1 ]
        ("mLastOpponentCollisionMagnitude",	DataTypes.FLOAT),			# [ RANGE = 0.0f->... ]
        ("mBoostActive",					DataTypes.BOOL),			# [ UNITS = boolean ]   [ RANGE = false->true ]   [ UNSET = false ]
        ("mBoostAmount",					DataTypes.FLOAT),			# [ RANGE = 0.0f->100.0f ]
        
        # Motion and Device Related
        ("mOrientation",			DataTypes.FLOAT * 3),	# [ UNITS = Euler Angles ]
        ("mLocalVelocity",			DataTypes.FLOAT * 3),	# [ UNITS = Metres per-second ]
        ("mWorldVelocity",			DataTypes.FLOAT * 3),	# [ UNITS = Metres per-second ]
        ("mAngularVelocity",		DataTypes.FLOAT * 3),	# [ UNITS = Radians per-second ]
        ("mLocalAcceleration",		DataTypes.FLOAT * 3),	# [ UNITS = Metres per-second ]
        ("mWorldAcceleration",		DataTypes.FLOAT * 3),	# [ UNITS = Metres per-second ]
        ("mExtentsCentre",			DataTypes.FLOAT * 3),	# [ UNITS = Local Space  X  Y  Z ]
        
        # Wheels / Tyres
        ("mTyreFlags",					DataTypes.UNSIGNED_INT8 * 4),	# [ enum (Type#10) Tyre Flags ]
        ("mTerrain",					DataTypes.UNSIGNED_INT8 * 4),	# [ enum (Type#11) Terrain Materials ]
        ("mTyreY",						DataTypes.FLOAT * 4),			# [ UNITS = Local Space  Y ]
        ("mTyreRPS",					DataTypes.FLOAT * 4),			# [ UNITS = Revolutions per second ]
        ("mTyreSlipSpeed",				DataTypes.FLOAT * 4),			# [ UNITS = Metres per-second ]
        ("mTyreTemp",					DataTypes.FLOAT * 4),			# [ UNITS = Celsius ]   [ UNSET = 0.0f ]
        ("mTyreGrip",					DataTypes.FLOAT * 4),			# [ RANGE = 0.0f->1.0f ]
        ("mTyreHeightAboveGround",		DataTypes.FLOAT * 4),			# [ UNITS = Local Space  Y ]
        ("mTyreLateralStiffness",		DataTypes.FLOAT * 4),			# [ UNITS = Lateral stiffness coefficient used in tyre deformation ]
        ("mTyreWear",					DataTypes.FLOAT * 4),			# [ RANGE = 0.0f->1.0f ]
        ("mBrakeDamage",				DataTypes.FLOAT * 4),			# [ RANGE = 0.0f->1.0f ]
        ("mSuspensionDamage",			DataTypes.FLOAT * 4),			# [ RANGE = 0.0f->1.0f ]
        ("mBrakeTempCelsius",			DataTypes.FLOAT * 4),			# [ UNITS = Celsius ]
        ("mTyreTreadTemp",				DataTypes.FLOAT * 4),			# [ UNITS = Kelvin ]
        ("mTyreLayerTemp",				DataTypes.FLOAT * 4),			# [ UNITS = Kelvin ]
        ("mTyreCarcassTemp",			DataTypes.FLOAT * 4),			# [ UNITS = Kelvin ]
        ("mTyreRimTemp",				DataTypes.FLOAT * 4),			# [ UNITS = Kelvin ]
        ("mTyreInternalAirTemp",		DataTypes.FLOAT * 4),			# [ UNITS = Kelvin ]
        
        # Car Damage
        ("mCrashState",		DataTypes.UNSIGNED_INT8),	# [ enum (Type#12) Crash Damage State ]
        ("mAeroDamage",		DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        ("mEngineDamage",	DataTypes.FLOAT),			# [ RANGE = 0.0f->1.0f ]
        
        # Weather
        ("mAmbientTemperature",		DataTypes.FLOAT),	# [ UNITS = Celsius ]   [ UNSET = 25.0f ]
        ("mTrackTemperature",		DataTypes.FLOAT),	# [ UNITS = Celsius ]   [ UNSET = 30.0f ]
        ("mRainDensity",			DataTypes.FLOAT),	# [ UNITS = How much rain will fall ]   [ RANGE = 0.0f->1.0f ]
        ("mWindSpeed",				DataTypes.FLOAT),	# [ RANGE = 0.0f->100.0f ]   [ UNSET = 2.0f ]
        ("mWindDirectionX",			DataTypes.FLOAT),	# [ UNITS = Normalised Vector X ]
        ("mWindDirectionY",			DataTypes.FLOAT),	# [ UNITS = Normalised Vector Y ]
        ("mCloudBrightness",		DataTypes.FLOAT),	# [ RANGE = 0.0f->... ]
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
    allSharedMemoryNames: str | None | dict[str, str] = "$pcars$"
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (mTelemetryData, mParticipantInfo, ),
    }
