from __future__ import annotations
from collections.abc import Callable
from . import _dataTypes
from enum import Flag, IntEnum


# source
# https://github.com/kwstudios-sweden/r3e-api

class DataTypes:
    STRUCTURE = _dataTypes.STRUCTURE

    SIGNED_INT32 = _dataTypes.SIGNED_INT32
    DOUBLE = _dataTypes.DOUBLE
    SINGLE = _dataTypes.FLOAT
    CHAR = _dataTypes.CHAR


### * Enums

class VersionMajor(IntEnum):
    R3E_VERSION_MAJOR = 3

class VersionMinor(IntEnum):
    R3E_VERSION_MINOR = 6

class GameMode(IntEnum):
    Unavailable = -1
    TrackTest = 0
    LeaderboardChallenge = 1
    Competition = 2
    SingleRace = 3
    Championship = 4
    Multiplayer = 5
    MultiplayerRanked = 6
    TryBeforeYouBuy = 7

class Session(IntEnum):
    Unavailable = -1
    Practice = 0
    Qualify = 1
    Race = 2
    Warmup = 3

class SessionPhase(IntEnum):
    Unavailable = -1
    Garage = 1          # MP race start countdown in garage
    Gridwalk = 2        # Gridwalk or track walkthrough
    Formation = 3       # Formation lap, rolling start etc.
    Countdown = 4       # Countdown to race is ongoing
    Green = 5           # Race is ongoing
    Checkered = 6       # End of session

class StartMode(IntEnum):
    Unavailable = -1
    Standing = 0
    Rolling = 1
    Formation = 2

class StartPhase(IntEnum):
    Unavailable = -1
    Waiting = 0         # Waiting for the car's own start group: on the grid, on the formation lap or rolling to the line
    Corridor = 1        # The car's start group leader is in the start corridor, the group's green is imminent
    Green = 2           # The car's start group has gone green

class Control(IntEnum):
    Unavailable = -1
    Player = 0          # Controlled by the actual player
    AI = 1              # Controlled by AI
    Remote = 2          # Controlled by a network entity of some sort
    Replay = 3          # Controlled by a replay or ghost

class PitWindow(IntEnum):
    Unavailable = -1
    Disabled = 0        # Pit stops are not enabled for this session
    Closed = 1          # Pit stops are enabled, but you're not allowed to perform one right now
    Open = 2            # Allowed to perform a pit stop now
    Stopped = 3         # Currently performing the pit stop changes (changing driver, etc.)
    Completed = 4       # After the current mandatory pitstop have been completed

class PitStopStatus(IntEnum):
    Unavailable = -1        # No mandatory pitstops
    UnservedTwoTyres = 0    # Mandatory pitstop for two tyres not served yet
    UnservedFourTyres = 1   # Mandatory pitstop for four tyres not served yet
    Served = 2              # Mandatory pitstop served

class FinishStatus(IntEnum):
    Unavailable = -1    # N/A
    Nothing = 0         # Still on track, not finished - cant be none in python
    Finished = 1        # Finished session normally
    DNF = 2             # Did not finish
    DNQ = 3             # Did not qualify
    DNS = 4             # Did not start
    DQ = 5              # Disqualified

class SessionLengthFormat(IntEnum):
    Unavailable = -1    # N/A
    TimeBased = 0
    LapBased = 1
    TimeAndLapBased = 2 # Time and lap based session means there will be an extra lap after the time has run out

class PitMenuSelection(IntEnum):
    Unavailable = -1    # Pit menu unavailable
    Preset = 0          # Pit menu preset
    Penalty = 1         # Pit menu actions
    Driverchange = 2
    Fuel = 3
    Fronttires = 4
    Reartires = 5
    Body = 6
    Frontwing = 7
    Rearwing = 8
    Suspension = 9
    ButtonTop = 10      # Pit menu buttons
    ButtonBottom = 11
    Max = 12            # Pit menu nothing selected

class TireType(IntEnum):
    Unavailable = -1
    Option = 0
    Prime = 1

class TireSubtype(IntEnum):
    Unavailable = -1
    Primary = 0
    Alternate = 1
    Soft = 2
    Medium = 3
    Hard = 4

class MtrlType(IntEnum):
    Unavailable = -1
    Nothing = 0
    Tarmac = 1
    Grass = 2
    Dirt = 3
    Gravel = 4
    Rumble = 5
    Concrete = 6

class EngineType(IntEnum):
    COMBUSTION = 0
    ELECTRIC = 1
    HYBRID = 2


### * Data Structure

class RaceDuration_SignedInt32(DataTypes.STRUCTURE):
    _fields_ = [
        ("Race1",   DataTypes.SIGNED_INT32),
        ("Race2",   DataTypes.SIGNED_INT32),
        ("Race3",   DataTypes.SIGNED_INT32),
    ]

class Vector3_Double(DataTypes.STRUCTURE):
    _fields_ = [
        ("X",   DataTypes.DOUBLE),
        ("Y",   DataTypes.DOUBLE),
        ("Z",   DataTypes.DOUBLE),
    ]

class Vector3_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("X",   DataTypes.SINGLE),
        ("Y",   DataTypes.SINGLE),
        ("Z",   DataTypes.SINGLE),
    ]

class Orientation_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("Pitch",   DataTypes.SINGLE),
        ("Yaw",     DataTypes.SINGLE),
        ("Roll",    DataTypes.SINGLE),
    ]

class SectorStarts_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("Sector1",     DataTypes.SINGLE),
        ("Sector2",     DataTypes.SINGLE),
        ("Sector3",     DataTypes.SINGLE),
    ]

class Sectors_SignedInt32(DataTypes.STRUCTURE):
    _fields_ = [
        ("Sector1",     DataTypes.SIGNED_INT32),
        ("Sector2",     DataTypes.SIGNED_INT32),
        ("Sector3",     DataTypes.SIGNED_INT32),
    ]

class Sectors_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("Sector1",     DataTypes.SINGLE),
        ("Sector2",     DataTypes.SINGLE),
        ("Sector3",     DataTypes.SINGLE),
    ]

class TireData_Double(DataTypes.STRUCTURE):
    _fields_ = [
        ("FrontLeft",     DataTypes.DOUBLE),
        ("FrontRight",    DataTypes.DOUBLE),
        ("RearLeft",      DataTypes.DOUBLE),
        ("RearRight",     DataTypes.DOUBLE),
    ]

class TireData_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("FrontLeft",     DataTypes.SINGLE),
        ("FrontRight",    DataTypes.SINGLE),
        ("RearLeft",      DataTypes.SINGLE),
        ("RearRight",     DataTypes.SINGLE),
    ]

class TireData_SignedInt32(DataTypes.STRUCTURE):
    _fields_ = [
        ("FrontLeft",     DataTypes.SIGNED_INT32),
        ("FrontRight",    DataTypes.SIGNED_INT32),
        ("RearLeft",      DataTypes.SIGNED_INT32),
        ("RearRight",     DataTypes.SIGNED_INT32),
    ]

class TireTemperature_Single(DataTypes.STRUCTURE):
    _fields_ = [
        ("Left",    DataTypes.SINGLE),
        ("Center",  DataTypes.SINGLE),
        ("Right",   DataTypes.SINGLE),
    ]

class TireTempInformation(DataTypes.STRUCTURE):
    _fields_ = [
        ("CurrentTemp",     TireTemperature_Single),
        ("OptimalTemp",     DataTypes.SINGLE),
        ("ColdTemp",        DataTypes.SINGLE),
        ("HotTemp",         DataTypes.SINGLE),
    ]

class TireData_TireTempInfo(DataTypes.STRUCTURE):
    _fields_ = [
        ("FrontLeft",     TireTempInformation),
        ("FrontRight",    TireTempInformation),
        ("RearLeft",      TireTempInformation),
        ("RearRight",     TireTempInformation),
    ]

class BrakeTemp(DataTypes.STRUCTURE):
    _fields_ = [
        ("CurrentTemp",     DataTypes.SINGLE),
        ("OptimalTemp",     DataTypes.SINGLE),
        ("ColdTemp",        DataTypes.SINGLE),
        ("HotTemp",         DataTypes.SINGLE),
    ]

class TireData_BrakeTemp(DataTypes.STRUCTURE):
    _fields_ = [
        ("FrontLeft",     BrakeTemp),
        ("FrontRight",    BrakeTemp),
        ("RearLeft",      BrakeTemp),
        ("RearRight",     BrakeTemp),
    ]


class PlayerData(DataTypes.STRUCTURE):
    _fields_ = [
        ("UserId",     DataTypes.SIGNED_INT32),     # Player user id
        
        # Virtual physics time
        ("GameSimulationTicks",     DataTypes.SIGNED_INT32),    # Unit: Ticks (1 tick = 1/400th of a second)
        ("GameSimulationTime",      DataTypes.DOUBLE),          # Unit: Seconds
        
        # Car world/local space position
        ("Position",            Vector3_Double),
        ("Velocity",            Vector3_Double),  # Unit: Meter per second (m/s)
        ("LocalVelocity",       Vector3_Double),  # Unit: Meter per second (m/s)
        ("Acceleration",        Vector3_Double),  # Unit: Meter per second squared (m/s^2)
        ("LocalAcceleration",   Vector3_Double),  # Unit: Meter per second squared (m/s^2)
        
        # Car body orientation
        ("Orientation",             Vector3_Double),  # Unit: Euler angles
        ("Rotation",                Vector3_Double),  # Car body rotation
        ("AngularAcceleration",     Vector3_Double),  # Car body angular acceleration (torque divided by inertia)
        
        # Car world/local space angular velocity
        ("AngularVelocity",         Vector3_Double),  # Unit: Radians per second
        ("LocalAngularVelocity",    Vector3_Double),  # Unit: Unit: Radians per second
        
        ("LocalGforce",     Vector3_Double),  # Driver g-force local to car
        
        ("SteeringForce",       DataTypes.DOUBLE),  # Total steering force coming through steering bars
        
        # Force feedback output before the maximum-force clamp, as the in-game FFB graph plots it:
        # +/-1.0 = device full scale, beyond that the wheel clips. Same sign as SteeringForce.
        # Without a force feedback wheel: SteeringForce * car FFB multiplier / FFB steer force input max.
        ("SteeringForcePercentage",     DataTypes.DOUBLE),  # Total steering force coming through steering bars
        
        ("EngineTorque",    DataTypes.DOUBLE),  # Current engine torque
        
        # Current downforce
        ("CurrentDownforce",    DataTypes.DOUBLE),  # Unit: Newtons (N)
        
        # Currently unused
        ("Voltage",     DataTypes.DOUBLE),
        ("ErsLevel",    DataTypes.DOUBLE),
        ("PowerMguH",   DataTypes.DOUBLE),
        ("PowerMguK",   DataTypes.DOUBLE),
        ("TorqueMguK",  DataTypes.DOUBLE),
        
        # Car setup (radians, meters, meters per second)
        ("SuspensionDeflection",    TireData_Double),
        ("SuspensionVelocity",      TireData_Double),
        ("Camber",                  TireData_Double),
        ("RideHeight",              TireData_Double),
        
        ("FrontWingHeight",     DataTypes.DOUBLE),
        ("FrontRollAngle",      DataTypes.DOUBLE),
        ("RearRollAngle",       DataTypes.DOUBLE),
        ("ThirdSpringSuspensionDeflectionFront",    DataTypes.DOUBLE),
        ("ThirdSpringSuspensionVelocityFront",      DataTypes.DOUBLE),
        ("ThirdSpringSuspensionDeflectionRear",     DataTypes.DOUBLE),
        ("ThirdSpringSuspensionVelocityRear",       DataTypes.DOUBLE),
        
        # Reserved data
        ("Unused1",     DataTypes.DOUBLE),
        ("Unused2",     DataTypes.DOUBLE),
        ("Unused3",     DataTypes.DOUBLE),
        
    ]

class Flags(DataTypes.STRUCTURE):
    _fields_ = [
        # Whether yellow flag is currently active
        ("Yellow",      DataTypes.SIGNED_INT32),    # -1 = no data, 0 = not active, 1 = active
        
        # Whether yellow flag was caused by current slot
        ("YellowCausedIt",  DataTypes.SIGNED_INT32),    # -1 = no data, 0 = didnt cause it, 1 = caused it
        
        # Whether overtake of car in front by current slot is allowed under yellow flag
        ("YellowOvertake",  DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not allowed, 1 = allowed
        
        # Whether you have gained positions illegaly under yellow flag to give back
        ("YellowPositionsGained",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = no positions gained, n = number of positions gained
        
        ("SectorYellow",    Sectors_SignedInt32),   # Yellow flag for each sector; -1 = no data, 0 = not active, 1 = active
        
        # Distance into track for closest yellow, -1.0 if no yellow flag exists
        ("ClosestYellowDistanceIntoTrack",  DataTypes.SINGLE),  # Unit: Meters (m)
        
        # Whether blue flag is currently active
        ("Blue",    DataTypes.SIGNED_INT32),    # -1 = no data, 0 = not active, 1 = active
        
        # Whether black flag is currently active
        ("Black",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not active, 1 = active
        
        # Whether green flag is currently active
        ("Green",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not active, 1 = active
        
        # Whether checkered flag is currently active
        ("Checkered",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not active, 1 = active
        
        # Whether white flag is currently active
        ("White",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not active, 1 = active
        
        # Whether black and white flag is currently active and reason
        ("BlackAndWhite",   DataTypes.SIGNED_INT32),  # -1 = no data, 0 = not active, 1 = blue flag 1st warnings, 2 = blue flag 2nd warnings, 3 = wrong way, 4 = cutting track
    ]

class CarDamage(DataTypes.STRUCTURE):
    _fields_ = [
        ("Engine",          DataTypes.SINGLE),  # Range: 0.0 - 1.0, Note: -1.0 = N/A
        ("Transmission",    DataTypes.SINGLE),  # Range: 0.0 - 1.0, Note: -1.0 = N/A
        
        # Note: A bit arbitrary at the moment. 0.0 doesn't necessarily mean completely destroyed.
        ("Aerodynamics",    DataTypes.SINGLE),  # Range: 0.0 - 1.0, Note: -1.0 = N/A
        ("Suspension",      DataTypes.SINGLE),  # Range: 0.0 - 1.0, Note: -1.0 = N/A
        
        # Reserved data
        ("Unused1",          DataTypes.SINGLE),
        ("Unused2",          DataTypes.SINGLE),
    ]

class PitMenuState(DataTypes.STRUCTURE):
    _fields_ = [
        ("Preset",      DataTypes.SIGNED_INT32),  # Pit menu preset
        
        # Pit menu actions
        ("Penalty",         DataTypes.SIGNED_INT32),
        ("Driverchange",    DataTypes.SIGNED_INT32),
        ("Fuel",            DataTypes.SIGNED_INT32),
        ("FrontTires",      DataTypes.SIGNED_INT32),
        ("RearTires",       DataTypes.SIGNED_INT32),
        ("Body",            DataTypes.SIGNED_INT32),
        ("FrontWing",       DataTypes.SIGNED_INT32),
        ("RearWing",        DataTypes.SIGNED_INT32),
        ("Suspension",      DataTypes.SIGNED_INT32),
        
        # Pit menu buttons
        ("ButtonTop",       DataTypes.SIGNED_INT32),
        ("ButtonBottom",    DataTypes.SIGNED_INT32),
    ]

class CutTrackPenalties(DataTypes.STRUCTURE):
    _fields_ = [
        # -1.0 = none pending, otherwise penalty time dep on penalty type 
        # (drive-through active = 0.0, stop-and-go = time to stay, slow-down = time left to give back etc)
        ("DriveThrough",    DataTypes.SINGLE),
        ("StopAndGo",       DataTypes.SINGLE),
        ("PitStop",         DataTypes.SINGLE),
        ("TimeDeduction",   DataTypes.SINGLE),
        ("SlowDown",        DataTypes.SINGLE),
    ]

class DRS(DataTypes.STRUCTURE):
    _fields_ = [
        # If DRS is equipped and allowed
        ("Equipped",    DataTypes.SIGNED_INT32),  # 0 = No, 1 = Yes, -1 = N/A
        
        # Got DRS activation left
        ("Available",   DataTypes.SIGNED_INT32),  # 0 = No, 1 = Yes, -1 = N/A
        
        # Number of DRS activations left this lap
        # Note: In sessions with 'endless' amount of drs activations per lap this value starts at int32::max
        ("NumActivationsLeft",  DataTypes.SIGNED_INT32),  # -1 = N/A
        
        # DRS engaged
        ("Engaged",     DataTypes.SIGNED_INT32),  # 0 = No, 1 = Yes, -1 = N/A
    ]

class PushToPass(DataTypes.STRUCTURE):
    _fields_ = [
        ("Available",           DataTypes.SIGNED_INT32), # PTP system exists = 1, N/A = -1. (for applicable systems 2 = charging, 3 = charged)
        ("Engaged",             DataTypes.SIGNED_INT32),
        ("AmountLeft",          DataTypes.SIGNED_INT32),
        ("EngagedTimeLeft",     DataTypes.SINGLE),
        ("WaitTimeLeft",        DataTypes.SINGLE),
    ]

class AidSettings(DataTypes.STRUCTURE):
    _fields_ = [
        ("Abs",             DataTypes.SIGNED_INT32),  # ABS; -1 = N/A, 0 = off, 1 = on, 5 = currently active
        ("Tc",              DataTypes.SIGNED_INT32),  # TC; -1 = N/A, 0 = off, 1 = on, 5 = currently active
        ("Esp",             DataTypes.SIGNED_INT32),  # ESP; -1 = N/A, 0 = off, 1 = on low, 2 = on medium, 3 = on high, 5 = currently active
        ("Countersteer",    DataTypes.SIGNED_INT32),  # Countersteer; -1 = N/A, 0 = off, 1 = on, 5 = currently active
        ("Cornering",       DataTypes.SIGNED_INT32),  # Cornering; -1 = N/A, 0 = off, 1 = on, 5 = currently active
    ]

class DriverInfo(DataTypes.STRUCTURE):
    _enums_: dict[type, tuple[str, ...]] = {
        EngineType: ("EngineType",),
    }
    _fields_ = [
        ("Name",                    DataTypes.CHAR * 64), # UTF-8
        ("CarNumber",               DataTypes.SIGNED_INT32),
        ("ClassId",                 DataTypes.SIGNED_INT32),
        ("ModelId",                 DataTypes.SIGNED_INT32),
        ("TeamId",                  DataTypes.SIGNED_INT32), 
        ("LiveryId",                DataTypes.SIGNED_INT32), 
        ("ManufacturerId",          DataTypes.SIGNED_INT32), 
        ("UserId",                  DataTypes.SIGNED_INT32), 
        ("SlotId",                  DataTypes.SIGNED_INT32), 
        ("ClassPerformanceIndex",   DataTypes.SIGNED_INT32), 
        ("EngineType",              DataTypes.SIGNED_INT32),  # Note: See the EngineType enum
        ("CarWidth",                DataTypes.SINGLE), 
        ("CarLength",               DataTypes.SINGLE), 
        ("Rating",                  DataTypes.SINGLE), 
        ("Reputation",              DataTypes.SINGLE), 
        
        # Reserved data
        ("Unused1",     DataTypes.SINGLE), 
        ("Unused2",     DataTypes.SINGLE), 
    ]

class DriverData(DataTypes.STRUCTURE):
    _enums_: dict[type, tuple[str, ...]] = {
        FinishStatus: ("FinishStatus",),
        PitStopStatus: ("PitStopStatus",),
        TireType: ("TireTypeFront", "TireTypeRear",),
        TireSubtype: ("TireSubtypeFront", "TireSubtypeRear",),
        StartPhase: ("StartPhase",),
    }
    _fields_ = [
        ("DriverInfo",      DriverInfo),
        
        ("FinishStatus",            DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.FinishStatus enum
        ("Place",                   DataTypes.SIGNED_INT32),
        ("PlaceClass",              DataTypes.SIGNED_INT32),    # Based on performance index
        ("LapDistance",             DataTypes.SINGLE),
        ("LapDistanceFraction",     DataTypes.SINGLE),
        ("Position",                Vector3_Single),
        ("TrackSector",             DataTypes.SIGNED_INT32),
        ("CompletedLaps",           DataTypes.SIGNED_INT32),
        ("CurrentLapValid",         DataTypes.SIGNED_INT32),
        ("LapTimeCurrentSelf",      DataTypes.SINGLE),
        ("SectorTimeCurrentSelf",   Sectors_Single),
        ("SectorTimePreviousSelf",  Sectors_Single),
        ("SectorTimeBestSelf",      Sectors_Single),
        
        ("TimeDeltaFront",      DataTypes.SINGLE),
        ("TimeDeltaBehind",     DataTypes.SINGLE),
        
        ("PitStopStatus",   DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.PitStopStatus enum
        ("InPitlane",       DataTypes.SIGNED_INT32),
        ("NumPitstops",     DataTypes.SIGNED_INT32),
        ("Penalties",       CutTrackPenalties),
        ("CarSpeed",        DataTypes.SINGLE),
        
        # Note: See the R3E.Constant.TireType enum
        ("TireTypeFront",       DataTypes.SIGNED_INT32),
        ("TireTypeRear",        DataTypes.SIGNED_INT32),
        
        # Note: See the R3E.Constant.TireSubtype enum
        ("TireSubtypeFront",    DataTypes.SIGNED_INT32),
        ("TireSubtypeRear",     DataTypes.SIGNED_INT32),
        
        ("BasePenaltyWeight",   DataTypes.SINGLE),
        ("AidPenaltyWeight",    DataTypes.SINGLE),
        ("DrsState",            DataTypes.SIGNED_INT32),    # -1 unavailable, 0 = not engaged, 1 = engaged
        ("PtpState",            DataTypes.SIGNED_INT32),
        ("VirtualEnergy",       DataTypes.SINGLE),          # -1.0 unavailable, 0.0 - 1.0 tank factor
        ("PenaltyType",         DataTypes.SIGNED_INT32),    # -1 unavailable, DriveThrough = 0, StopAndGo = 1, Pitstop = 2, Time = 3, Slowdown = 4, Disqualify = 5
        
        # Based on the PenaltyType you can assume the reason is:

        # DriveThroughPenaltyInvalid = 0,
        # DriveThroughPenaltyCutTrack = 1,
        # DriveThroughPenaltyPitSpeeding = 2,
        # DriveThroughPenaltyFalseStart = 3,
        # DriveThroughPenaltyIgnoredBlue = 4,
        # DriveThroughPenaltyDrivingTooSlow = 5,
        # DriveThroughPenaltyIllegallyPassedBeforeGreen = 6,
        # DriveThroughPenaltyIllegallyPassedBeforeFinish = 7,
        # DriveThroughPenaltyIllegallyPassedBeforePitEntrance = 8,
        # DriveThroughPenaltyIgnoredSlowDown = 9,
        # DriveThroughPenaltyMax = 10

        # StopAndGoPenaltyInvalid = 0,
        # StopAndGoPenaltyCutTrack1st = 1,
        # StopAndGoPenaltyCutTrackMult = 2,
        # StopAndGoPenaltyYellowFlagOvertake = 3,
        # StopAndGoPenaltyVirtualEnergy = 4,
        # StopAndGoPenaltyMax = 5

        # PitstopPenaltyInvalid = 0,
        # PitstopPenaltyIgnoredPitstopWindow = 1,
        # PitstopPenaltyMax = 2

        # ServableTimePenaltyInvalid = 0,
        # ServableTimePenaltyServedMandatoryPitstopLate = 1,
        # ServableTimePenaltyIgnoredMinimumPitstopDuration = 2,
        # ServableTimePenaltyMax = 3

        # SlowDownPenaltyInvalid = 0,
        # SlowDownPenaltyCutTrack1st = 1,
        # SlowDownPenaltyCutTrackMult = 2,
        # SlowDownPenaltyMax = 3

        # DisqualifyPenaltyInvalid = -1,
        # DisqualifyPenaltyFalseStart = 0,
        # DisqualifyPenaltyPitlaneSpeeding = 1,
        # DisqualifyPenaltyWrongWay = 2,
        # DisqualifyPenaltyEnteringPitsUnderRed = 3,
        # DisqualifyPenaltyExitingPitsUnderRed = 4,
        # DisqualifyPenaltyFailedDriverChange = 5,
        # DisqualifyPenaltyThreeDriveThroughsInLap = 6,
        # DisqualifyPenaltyLappedFieldMultipleTimes = 7,
        # DisqualifyPenaltyIgnoredDriveThroughPenalty = 8,
        # DisqualifyPenaltyIgnoredStopAndGoPenalty = 9,
        # DisqualifyPenaltyIgnoredPitStopPenalty = 10,
        # DisqualifyPenaltyIgnoredTimePenalty = 11,
        # DisqualifyPenaltyExcessiveCutting = 12,
        # DisqualifyPenaltyIgnoredBlueFlag = 13,
        # DisqualifyPenaltyMax = 14
        
        ("PenaltyReason",   DataTypes.SIGNED_INT32),
        
        ("EngineState",     DataTypes.SIGNED_INT32), # -1 unavailable, 0 = ignition off, 1 = ignition on but not running, 2 = ignition on and starter running, 3 = ignition on and running
        
        # Car body orientation
        ("Orientation",     Vector3_Single),    # Unit: Euler angles
        
        # Race start group the car belongs to (staggered starts release groups separately)
        ("StartGroup",      DataTypes.SIGNED_INT32),    # Note: 0-based, -1 = N/A (not a race session)
        
        # Where the car is in its own start procedure
        ("StartPhase",      DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.StartPhase enum. A later start group can still be waiting while SessionPhase is already green
        
        # The car's slot in its start group's formation order (0 = group leader)
        ("FormationSlot",      DataTypes.SIGNED_INT32),    # Note: -1 = N/A or not in the formation order (e.g. pit lane start, retired)
        
    ]


class Shared(DataTypes.STRUCTURE):
    _pack_ = 1
    _enums_: dict[type, tuple[str, ...]] = {
        GameMode: ("GameMode",),
        Session: ("SessionType",),
        SessionPhase: ("SessionPhase",),
        StartMode: ("StartMode",),
        PitWindow: ("PitWindowStatus",),
        FinishStatus: ("FinishStatus",),
        Control: ("ControlType",),
        TireType: ("TireType", "TireTypeFront", "TireTypeRear",),
        TireSubtype: ("TireSubtypeFront", "TireSubtypeRear",),
        MtrlType: ("TireOnMtrl",),
        SessionLengthFormat: ("SessionLengthFormat",),
        PitMenuSelection: ("PitMenuSelection",),
    }
    _fields_ = [
        ####################################################
        # Version
        ####################################################
        
        ("VersionMajor",        DataTypes.SIGNED_INT32),
        ("VersionMinor",     	DataTypes.SIGNED_INT32),
        ("AllDriversOffset",    DataTypes.SIGNED_INT32),	# Offset to NumCars variable
        ("DriverDataSize",		DataTypes.SIGNED_INT32),    # Size of DriverData
        
        ####################################################
        # Game State
        ####################################################
        
        ("GameMode",			DataTypes.SIGNED_INT32),	# Note: See the R3E.Constant.GameMode enum
        ("GamePaused",			DataTypes.SIGNED_INT32),
        ("GameInMenus",         DataTypes.SIGNED_INT32),
        ("GameInReplay",        DataTypes.SIGNED_INT32),
        ("GameUsingVr",         DataTypes.SIGNED_INT32),
        ("GamePlayerInGarage",  DataTypes.SIGNED_INT32),
        
        ####################################################
        # High Detail
        ####################################################
        
        ("Player",  PlayerData),    # High precision data for player's vehicle only
        
        ####################################################
        # Event And Session
        ####################################################
        
        ("TrackName",       DataTypes.CHAR * 64), # UTF-8
        ("LayoutName",      DataTypes.CHAR * 64), # UTF-8
        
        ("TrackId",     DataTypes.SIGNED_INT32),
        ("LayoutId",    DataTypes.SIGNED_INT32),
        
        ("LayoutLength",        DataTypes.SINGLE),      # Layout length in meters
        ("SectorStartFactors",  SectorStarts_Single),
        
        # Race session durations
        # Note: Index 0-2 = race 1-3
        # Note: Value -1 = N/A
        # Note: If both laps and minutes are more than 0, race session starts with minutes then adds laps
        ("RaceSessionLaps",     RaceDuration_SignedInt32),
        ("RaceSessionMinutes",  RaceDuration_SignedInt32),
        
        # The current race event index, for championships with multiple events
        ("EventIndex",      DataTypes.SIGNED_INT32),    # Note: 0-indexed, -1 = N/A
        
        # Which session the player is in (practice, qualifying, race, etc.)
        ("SessionType",     DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.Session enum
        
        # The current iteration of the current type of session (second qualifying session, etc.)
        ("SessionIteration",    DataTypes.SIGNED_INT32),    # Note: 1 = first, 2 = second etc, -1 = N/A
        
        ("SessionLengthFormat",     DataTypes.SIGNED_INT32),    # If the session is time based, lap based or time based with an extra lap at the end
        
        ("SessionPitSpeedLimit",    DataTypes.SINGLE),  # Unit: Meter per second (m/s)
        
        # Which phase the current session is in (gridwalk, countdown, green flag, etc.)
        ("SessionPhase",    DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.SessionPhase enum
        
        # Which phase start lights are in; -1 = unavailable, 0 = off, 1-5 = redlight on and counting down, 6 = greenlight on
        ("StartLights",     DataTypes.SIGNED_INT32),    # Note: See the r3e_session_phase enum
        
        ("TireWearActive",  DataTypes.SIGNED_INT32),    # -1 = no data available, 0 = not active, 1 = active, 2 = 2x, 3 = 3x, 4 = 4x
        ("FuelUseActive",   DataTypes.SIGNED_INT32),    # -1 = no data available, 0 = not active, 1 = active, 2 = 2x, 3 = 3x, 4 = 4x
        ("NumberOfLaps",    DataTypes.SIGNED_INT32),    # Total number of laps in the race, or -1 if player is not in race mode (practice, test mode, etc.)
        
        # Amount of time and time remaining for the current session
        # Note: Only available in time-based sessions, -1.0 = N/A
        ("SessionTimeDuration",     DataTypes.SINGLE),  # Units: Seconds
        ("SessionTimeRemaining",    DataTypes.SINGLE),
        
        ("MaxIncidentPoints",   DataTypes.SIGNED_INT32),    # Server max incident points, -1 = N/A
        
        # How the race is started
        ("StartMode",           DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.StartMode enum, -1 = N/A (not a race session)
        
        # Number of race start groups released separately (1 = single start)
        ("StartGroupCount",     DataTypes.SIGNED_INT32),    # Note: -1 = N/A (not a race session)
        
        ####################################################
        # Pit
        ####################################################
        
        # Current status of the pit stop
        ("PitWindowStatus",     DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.PitWindow enum
        
        # The minute/lap from which you're obligated to pit (-1 = N/A)
        ("PitWindowStart",      DataTypes.SIGNED_INT32),    # Unit: Minutes in time-based sessions, otherwise lap
        
        # The minute/lap into which you need to have pitted (-1 = N/A)
        ("PitWindowEnd",        DataTypes.SIGNED_INT32),    # Unit: Minutes in time-based sessions, otherwise lap
        
        ("InPitlane",           DataTypes.SIGNED_INT32),    # If current vehicle is in pitline (-1 = N/A)
        
        # What is currently selected in pit menu, and array of states 
        # (preset/buttons: -1 = not selectable, 1 = selectable) (actions: -1 = N/A, 0 = unmarked for fix, 1 = marked for fix)
        ("PitMenuSelection",    DataTypes.SIGNED_INT32),
        ("PitMenuState",        PitMenuState),
        
        # Current vehicle pit state 
        # (-1 = N/A, 0 = None, 1 = Requested stop, 2 = Entered pitlane heading for pitspot, 3 = Stopped at pitspot, 4 = Exiting pitspot heading for pit exit)
        ("PitState",    DataTypes.SIGNED_INT32),
        
        # Current vehicle pitstop actions duration
        ("PitTotalDuration",    DataTypes.SINGLE),
        ("PitElapsedTime",      DataTypes.SINGLE),
        
        # Current vehicle pit action 
        # (-1 = N/A, 0 = None, 1 = Preparing, 
        # (combination of 2 = Penalty serve, 4 = Driver change, 8 = Refueling, 16 = Front tires, 32 = Rear tires, 64 = Body, 128 = Front wing, 256 = Rear wing, 512 = Suspension))
        ("PitAction",   DataTypes.SIGNED_INT32),
        
        ("NumPitstopsPerformed",    DataTypes.SIGNED_INT32), # Number of pitstops the current vehicle has performed (-1 = N/A)
        
        ("PitMinDurationTotal",     DataTypes.SINGLE),
        ("PitMinDurationLeft",      DataTypes.SINGLE),
        
        ####################################################
        # Scoring & Timings
        ####################################################
        
        ("Flags",      Flags),
        
        ("Position",            DataTypes.SIGNED_INT32), # Current position (1 = first place)
        ("PositionClass",       DataTypes.SIGNED_INT32), # Based on performance index
        ("FinishStatus",        DataTypes.SIGNED_INT32), # Note: See the R3E.Constant.FinishStatus enum
        ("CutTrackWarnings",    DataTypes.SIGNED_INT32), # Total number of cut track warnings (-1 = N/A)
        ("Penalties",           CutTrackPenalties), # The number of penalties the car currently has pending of each type (-1 = N/A)
        
        # Total number of penalties pending for the car
        ("NumPenalties",    DataTypes.SIGNED_INT32), # Note: See the 'penalties' field
        
        # How many laps the player has completed. If this value is 6, the player is on his 7th lap. -1 = n/a
        ("CompletedLaps",           DataTypes.SIGNED_INT32),
        ("CurrentLapValid",         DataTypes.SIGNED_INT32),
        ("TrackSector",             DataTypes.SIGNED_INT32),
        ("LapDistance",             DataTypes.SINGLE),
        ("LapDistanceFraction",     DataTypes.SINGLE),      # fraction of lap completed, 0.0-1.0, -1.0 = N/A
        
        ("LapTimeBestLeader",       DataTypes.SINGLE),  # The current best lap time for the leader of the session (-1.0 = N/A)
        ("LapTimeBestLeaderClass",  DataTypes.SINGLE),  # The current best lap time for the leader of the player's class in the current session (-1.0 = N/A)
        
        # Sector times of fastest lap by anyone in session
        ("SectorTimesSessionBestLap",   Sectors_Single),    # Unit: Seconds (-1.0 = N/A)
        ("LapTimeBestSelf",             DataTypes.SINGLE),  # Unit: Seconds (-1.0 = N/A)
        ("SectorTimesBestSelf",         Sectors_Single),
        ("LapTimePreviousSelf",         DataTypes.SINGLE),  # Unit: Seconds (-1.0 = N/A)
        ("SectorTimesPreviousSelf",     Sectors_Single),
        ("LapTimeCurrentSelf",          DataTypes.SINGLE),  # Unit: Seconds (-1.0 = N/A)
        ("SectorTimesCurrentSelf",      Sectors_Single),
        ("LapTimeDeltaLeader",          DataTypes.SINGLE),  # The time delta between the player's time and the leader of the current session (-1.0 = N/A)
        ("LapTimeDeltaLeaderClass",     DataTypes.SINGLE),  # The time delta between the player's time and the leader of the player's class in the current session (-1.0 = N/A)
        
        # Time delta between the player and the car placed in front (-1.0 = N/A)
        ("TimeDeltaFront",      DataTypes.SINGLE),  # Units: Seconds
        
        # Time delta between the player and the car placed behind (-1.0 = N/A)
        ("TimeDeltaBehind",     DataTypes.SINGLE),  # Units: Seconds
        
        # Time delta between this car's current laptime and this car's best laptime
        ("TimeDeltaBestSelf",   DataTypes.SINGLE),  # Unit: Seconds (-1000.0 = N/A)
        
        # Best time for each individual sector no matter lap
        ("BestIndividualSectorTimeSelf",            Sectors_Single),    # Unit: Seconds (-1.0 = N/A)
        ("BestIndividualSectorTimeLeader",          Sectors_Single),
        ("BestIndividualSectorTimeLeaderClass",     Sectors_Single),
        ("IncidentPoints",                          DataTypes.SIGNED_INT32),
        
        ("LapValidState",   DataTypes.SIGNED_INT32),    # -1 = N/A, 0 = this and next lap valid, 1 = this lap invalid, 2 = this and next lap invalid
        ("PrevLapValid",    DataTypes.SIGNED_INT32),    # -1 = N/A, 0 = invalid, 1 = valid
        
        ("DischargeRate",   DataTypes.SINGLE),  # -1.0 = N/A, 0.0 - 1.0
        ("BrakeRegen",      DataTypes.SINGLE),
        
        ("Unused1",     DataTypes.SINGLE),  # Reserved data
        
        ####################################################
        # Vehicle information
        ####################################################
        
        ("VehicleInfo",     DriverInfo),
        ("PlayerName",      DataTypes.CHAR * 64), # UTF-8
        
        ####################################################
        # Vehicle State
        ####################################################
        
        # Which controller is currently controlling the player's car (AI, player, remote, etc.)
        ("ControlType",     DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.Control enum
        ("CarSpeed",        DataTypes.SINGLE),          # Unit: Meter per second (m/s)
        ("EngineRps",       DataTypes.SINGLE),          # Unit: Radians per second (rad/s)
        ("MaxEngineRps",    DataTypes.SINGLE),
        ("UpshiftRps",      DataTypes.SINGLE),
        ("Gear",            DataTypes.SIGNED_INT32),    # -2 = N/A, -1 = reverse, 0 = neutral, 1 = first gear, ...
        ("NumGears",        DataTypes.SIGNED_INT32),    # -1 = N/A
        ("CarCgLocation",   Sectors_Single),            # Physical location of car's center of gravity in world space (X, Y, Z) (Y = up)
        
        # Pitch, yaw, roll
        ("CarOrientation",  Orientation_Single),    # Unit: Radians (rad)
        
        # Acceleration in three axes (X, Y, Z) of car body in local-space.
        # From car center, +X=left, +Y=up, +Z=back.
        ("LocalAcceleration",   Sectors_Single),    # Unit: Meter per second squared (m/s^2)
        
        # Unit: Kilograms (kg)
        ("TotalMass",   DataTypes.SINGLE),    # Note: Car + penalty weight + fuel
        
        # Unit: Liters (l)
        # Note: Fuel per lap show estimation when not enough data, then max recorded fuel per lap
        # Note: Not valid for remote players
        ("FuelLeft",        DataTypes.SINGLE),
        ("FuelCapacity",    DataTypes.SINGLE),
        ("FuelPerLap",      DataTypes.SINGLE),
        
        # Unit: Mega-Joule (MJ)
        # Note: -1.0f when not enough data, then max recorded virtual energy per lap
        # Note: Not valid for remote players
        ("VirtualEnergyLeft",       DataTypes.SINGLE),
        ("VirtualEnergyCapacity",   DataTypes.SINGLE),
        ("VirtualEnergyPerLap",     DataTypes.SINGLE),
        
        # Unit: Celsius (C)
        # Note: Not valid for AI or remote players
        ("EngineTemp",      DataTypes.SINGLE),
        ("EngineOilTemp",   DataTypes.SINGLE),
        
        # Unit: Kilopascals (KPa)
        # Note: Not valid for AI or remote players
        ("FuelPressure",    DataTypes.SINGLE),
        
        # Unit: Kilopascals (KPa)
        # Note: Not valid for AI or remote players
        ("EngineOilPressure",   DataTypes.SINGLE),
        
        # Unit: (Bar)
        # Note: Not valid for AI or remote players (-1.0 = N/A)
        ("TurboPressure",   DataTypes.SINGLE),
        
        # How pressed the throttle pedal is
        # Range: 0.0 - 1.0 (-1.0 = N/A)
        # Note: Not valid for AI or remote players
        ("Throttle",        DataTypes.SINGLE),
        ("ThrottleRaw",     DataTypes.SINGLE),
        
        # How pressed the brake pedal is
        # Range: 0.0 - 1.0 (-1.0 = N/A)
        # Note: Not valid for AI or remote players
        ("Brake",       DataTypes.SINGLE),
        ("BrakeRaw",    DataTypes.SINGLE),
        
        # How pressed the clutch pedal is
        # Range: 0.0 - 1.0 (-1.0 = N/A)
        # Note: Not valid for AI or remote players
        ("Clutch",      DataTypes.SINGLE),
        ("ClutchRaw",   DataTypes.SINGLE),
        
        # How much the steering wheel is turned
        # Range: -1.0 - 1.0
        # Note: Not valid for AI or remote players
        ("SteerInputRaw",   DataTypes.SINGLE),
        
        # How many degrees in steer lock (center to full lock)
        # Note: Not valid for AI or remote players
        ("SteerLockDegrees",    DataTypes.SIGNED_INT32),
        
        # How many degrees in wheel range (degrees full left to full right)
        # Note: Not valid for AI or remote players
        ("SteerWheelRangeDegrees",  DataTypes.SIGNED_INT32),
        
        ("AidSettings",     AidSettings),               # Aid settings
        ("Drs",             DRS),                       # DRS data
        ("PitLimiter",      DataTypes.SIGNED_INT32),    # Pit limiter (-1 = N/A, 0 = inactive, 1 = active)
        ("PushToPass",      PushToPass),                # Push to pass data
        
        # How much the vehicle's brakes are biased towards the back wheels (0.3 = 30%, etc.) (-1.0 = N/A)
        ("BrakeBias",   DataTypes.SINGLE),  # Note: Not valid for AI or remote players
        
        ("DrsNumActivationsTotal",  DataTypes.SIGNED_INT32),    # DRS activations available in total (-1 = N/A or endless)
        ("PtpNumActivationsTotal",  DataTypes.SIGNED_INT32),    # PTP activations available in total (-1 = N/A, or there's no restriction per lap, or endless)
        
        # Battery state of charge
        ("BatterySoC",  DataTypes.SINGLE),  # Range: 0.0 - 100.0 (-1.0 = N/A)
        
        # Brake water tank (-1.0 = N/A)
        ("WaterLeft",   DataTypes.SINGLE),  # Unit: Liters (l)
        
        ("AbsSetting",  DataTypes.SIGNED_INT32),    # -1.0 = N/A
        ("HeadLights",  DataTypes.SIGNED_INT32),    # -1 = N/A or dont exist on car, 0 = ignition off or headlights off, 1 = on, 2 = strobing
        
        # -1 = N/A, 0 = set to Auto, 180 - 1800 = set to Manual
        ("SteerWheelMaxRotation",   DataTypes.SIGNED_INT32),    # Note: Not valid for AI or remote players
        
        ####################################################
        # Tires
        ####################################################
        
        # Which type of tires the player's car has (option, prime, etc.)
        ("TireType",    DataTypes.SIGNED_INT32),    # Note: See the R3E.Constant.TireType enum, deprecated - use the values further down instead
        
        # Rotation speed
        ("TireRps",     TireData_Single),   # Uint: Radians per second
        
        # Wheel speed
        ("TireSpeed",       TireData_Single),       # Uint: Meters per second
        ("TireGrip",        TireData_Single),       # Range: 0.0 - 1.0 (-1.0 = N/A)
        ("TireWear",        TireData_Single),       # Range: 0.0 - 1.0 (-1.0 = N/A)
        ("TireFlatspot",    TireData_SignedInt32),  # (-1 = N/A, 0 = false, 1 = true)
        
        # Unit: Kilopascals (KPa) (-1.0 = N/A)
        ("TirePressure",    TireData_Single),    # Note: Not valid for AI or remote players
        
        # Percentage of dirt on tire (-1.0 = N/A)
        ("TireDirt",    TireData_Single),    # Range: 0.0 - 1.0
        
        # Current temperature of three points across the tread of the tire (-1.0 = N/A)
        # Optimum temperature
        # Cold temperature
        # Hot temperature
        # Unit: Celsius (C)
        # Note: Not valid for AI or remote players
        ("TireTemp",    TireData_TireTempInfo),
        
        
        # Which type of tires the car has (option, prime, etc.)
        # Note: See the R3E.Constant.TireType enum
        ("TireTypeFront",   DataTypes.SIGNED_INT32),
        ("TireTypeRear",    DataTypes.SIGNED_INT32),
        
        # Which subtype of tires the car has
        # Note: See the R3E.Constant.TireSubtype enum
        ("TireSubtypeFront",    DataTypes.SIGNED_INT32),
        ("TireSubtypeRear",     DataTypes.SIGNED_INT32),
        
        # Current brake temperature (-1.0 = N/A)
        # Optimum temperature
        # Cold temperature
        # Hot temperature
        # Unit: Celsius (C)
        # Note: Not valid for AI or remote players
        ("BrakeTemp",   TireData_BrakeTemp),
        
        # Brake pressure (-1.0 = N/A)
        # Unit: Kilo Newtons (kN)
        # Note: Not valid for AI or remote players
        ("BrakePressure",   TireData_Single),
        
        # -1.0 = N/A
        ("TractionControlSetting",      DataTypes.SIGNED_INT32),
        ("EngineMapSetting",            DataTypes.SIGNED_INT32),
        ("EngineBrakeSetting",          DataTypes.SIGNED_INT32),
        
        ("TractionControlPercent",  DataTypes.SINGLE),  # -1.0 = N/A, 0.0 -> 100.0 percent
        
        # Which type of material under player car tires (tarmac, gravel, etc.)
        ("TireOnMtrl",  TireData_SignedInt32),  # Note: See the R3E.Constant.MtrlType enum
        
        # Tire load (N)
        ("TireLoad",    TireData_Single),   # -1.0 = N/A
        
        ####################################################
        # Damage
        ####################################################
        
        # The current state of various parts of the car
        ("CarDamage",   CarDamage),     # Note: Not valid for AI or remote players
        
        ####################################################
        # Driver Info
        ####################################################
        
        ("NumCars",     DataTypes.SIGNED_INT32),    # Number of cars (including the player) in the race
        ("DriverData",  DriverData * 128),          # Contains name and basic vehicle info for all drivers in place order
        
        ####################################################
        # Start procedure (current vehicle), added in 3.6
        # Note: All -1 = N/A unless the current vehicle is waiting for its start group's green
        ####################################################
        
        # Speed the current vehicle should hold. For the start group leader this is the leader's speed limit
        ("FormationSpeedLimit",     DataTypes.SINGLE),  # Unit: Meter per second (m/s)
        
        # Below this speed the start group leader counts as too slow (leader only)
        ("FormationPaceFloor",      DataTypes.SINGLE),  # Unit: Meter per second (m/s)
        
        # Lap distance where the start corridor begins
        ("StartCorridorLapDistance",    DataTypes.SINGLE),  # Unit: Meters (m)
        
        ("FormationSide",   DataTypes.SIGNED_INT32),    # Side of the track the current vehicle should keep (0 = left, 1 = right)
        
        # Slot id of the car the current vehicle should follow (-1 = none, e.g. start group leader)
        ("FormationFollowSlotId",   DataTypes.SIGNED_INT32),    # Note: Matches DriverInfo.SlotId in DriverData
        
        # Time left until the current vehicle may leave the pit lane after a delayed pit lane start
        ("PitlaneStartDelayRemaining",  DataTypes.SINGLE),  # Unit: Seconds
        
        # Start offence recorded against the current vehicle, penalised when its start group goes green
        ("StartPenaltyPending",     DataTypes.SIGNED_INT32),      # Note: 0 = none, 1 = jumped the start, 2 = wrong side of the track
    ]


### * MetaData

class MetaData:
    # standard network info
    port: int | None = None
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc: Callable | None = None
    
    # use for itinial hand shake
    handShakePort: int | None = None
    handShakeFunc: tuple[Callable, Callable] | None = None
    
    # use if the data needs decrypting
    decryptionFunc: Callable | None = None
    
    # use if there is a header packet
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = "$R3E"

    # define the receiver and decoder modes
    receiverMode: str = "shared_memory"

    # Common data attributes
    commonFieldMap = {
        "speed": "CarSpeed",
        "engineRPM": "EngineRps",
        "gear": "Gear",
        "throttle": "Throttle",
        "brake": "Brake",
        "clutch": "Clutch",
        "steering": "SteerInputRaw",
    }
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (Shared, ),
    }
