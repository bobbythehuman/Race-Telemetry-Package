import ctypes
from enum import Enum


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    UNION = ctypes.Union
    
    SIGNED_INT8 = ctypes.c_int8
    SIGNED_INT16 = ctypes.c_int16
    # SIGNED_INT32 = ctypes.c_int32
    
    UNSIGNED_INT8 = ctypes.c_uint8      # 1 byte 
    UNSIGNED_INT16 = ctypes.c_uint16
    UNSIGNED_INT32 = ctypes.c_uint32
    UNSIGNED_INT64 = ctypes.c_uint64
    
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    DOUBLE = ctypes.c_double


### Packet Header -- 26 bytes


class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_packetFormat",              DataTypes.UNSIGNED_INT16),    # 2019
        ("m_gameMajorVersion",          DataTypes.UNSIGNED_INT8),     # Game major version - "X.00"
        ("m_gameMinorVersion",          DataTypes.UNSIGNED_INT8),     # Game minor version - "1.XX"
        ("m_packetVersion",             DataTypes.UNSIGNED_INT8),     # Version of this packet type, all start from 1
        ("m_packetId",                  DataTypes.UNSIGNED_INT8),     # Identifier for the packet type, see below
        ("m_sessionUID",                DataTypes.UNSIGNED_INT64),    # Unique identifier for the session
        ("m_sessionTime",               DataTypes.FLOAT),             # Session timestamp
        ("m_frameIdentifier",           DataTypes.UNSIGNED_INT32),    # Identifier for the frame the data was retrieved on
        ("m_playerCarIndex",            DataTypes.UNSIGNED_INT8),     # Index of player's car in the array
    ]


### Motion Packet -- Rate as specified in menus -- 1343 bytes


class CarMotionData(DataTypes.STRUCTURE):
    # _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_worldPositionX",        DataTypes.FLOAT),         # World space X position
        ("m_worldPositionY",        DataTypes.FLOAT),         # World space Y position
        ("m_worldPositionZ",        DataTypes.FLOAT),         # World space Z position
        ("m_worldVelocityX",        DataTypes.FLOAT),         # Velocity in world space X
        ("m_worldVelocityY",        DataTypes.FLOAT),         # Velocity in world space Y
        ("m_worldVelocityZ",        DataTypes.FLOAT),         # Velocity in world space Z
        ("m_worldForwardDirX",      DataTypes.SIGNED_INT16),  # World space forward X direction (normalised)
        ("m_worldForwardDirY",      DataTypes.SIGNED_INT16),  # World space forward Y direction (normalised)
        ("m_worldForwardDirZ",      DataTypes.SIGNED_INT16),  # World space forward Z direction (normalised)
        ("m_worldRightDirX",        DataTypes.SIGNED_INT16),  # World space right X direction (normalised)
        ("m_worldRightDirY",        DataTypes.SIGNED_INT16),  # World space right Y direction (normalised)
        ("m_worldRightDirZ",        DataTypes.SIGNED_INT16),  # World space right Z direction (normalised)
        ("m_gForceLateral",         DataTypes.FLOAT),         # Lateral G-Force component
        ("m_gForceLongitudinal",    DataTypes.FLOAT),         # Longitudinal G-Force component
        ("m_gForceVertical",        DataTypes.FLOAT),         # Vertical G-Force component
        ("m_yaw",                   DataTypes.FLOAT),         # Yaw angle in radians
        ("m_pitch",                 DataTypes.FLOAT),         # Pitch angle in radians
        ("m_roll",                  DataTypes.FLOAT),         # Roll angle in radians
    ]


class PacketMotionData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carMotionData", CarMotionData * 20),    # Data for all cars on track
        # Extra player car ONLY data
        ("m_suspensionPosition",        DataTypes.FLOAT * 4),     # Note: All wheel arrays have the following order:
        ("m_suspensionVelocity",        DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_suspensionAcceleration",    DataTypes.FLOAT * 4),     # RL, RR, FL, FR
        ("m_wheelSpeed",                DataTypes.FLOAT * 4),     # Speed of each wheel
        ("m_wheelSlip",                 DataTypes.FLOAT * 4),     # Slip ratio for each wheel
        ("m_localVelocityX",            DataTypes.FLOAT),         # Velocity in local space
        ("m_localVelocityY",            DataTypes.FLOAT),         # Velocity in local space
        ("m_localVelocityZ",            DataTypes.FLOAT),         # Velocity in local space
        ("m_angularVelocityX",          DataTypes.FLOAT),         # Angular velocity x-component
        ("m_angularVelocityY",          DataTypes.FLOAT),         # Angular velocity y-component
        ("m_angularVelocityZ",          DataTypes.FLOAT),         # Angular velocity z-component
        ("m_angularAccelerationX",      DataTypes.FLOAT),         # Angular acceleration x-component
        ("m_angularAccelerationY",      DataTypes.FLOAT),         # Angular acceleration y-component
        ("m_angularAccelerationZ",      DataTypes.FLOAT),         # Angular acceleration z-component
        ("m_frontWheelsAngle",          DataTypes.FLOAT),         # Current front wheels angle in radians
    ]


### Session Packet -- 2 per second -- 149 bytes


class MarshalZone(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_zoneStart", DataTypes.FLOAT),         # Fraction (0..1) of way through the lap the marshal zone starts
        ("m_zoneFlag",  DataTypes.SIGNED_INT8),   # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
    ]


class PacketSessionData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                            PacketHeader),                          # Header
        ("m_weather",                           DataTypes.UNSIGNED_INT8),         # Weather - 0 = clear, 1 = light cloud, 2 = overcast, 3 = light rain, 4 = heavy rain, 5 = storm
        ("m_trackTemperature",                  DataTypes.SIGNED_INT8),           # Track temp. in degrees celsius
        ("m_airTemperature",                    DataTypes.SIGNED_INT8),           # Air temp. in degrees celsius
        ("m_totalLaps",                         DataTypes.UNSIGNED_INT8),         # Total number of laps in this race
        ("m_trackLength",                       DataTypes.UNSIGNED_INT16),        # Track length in metres
        ("m_sessionType",                       DataTypes.UNSIGNED_INT8),         # 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2, 12 = R3, 13 = Time Trial
        ("m_trackId",                           DataTypes.SIGNED_INT8),           # -1 for unknown, 0-21 for tracks, see appendix
        ("m_formula",                           DataTypes.UNSIGNED_INT8),         # Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2, 3 = F1 Generic, 4 = Beta, 5 = Supercars, 6 = Esports, 7 = F2 2021
        ("m_sessionTimeLeft",                   DataTypes.UNSIGNED_INT16),        # Time left in session in seconds
        ("m_sessionDuration",                   DataTypes.UNSIGNED_INT16),        # Session duration in seconds
        ("m_pitSpeedLimit",                     DataTypes.UNSIGNED_INT8),         # Pit speed limit in kilometres per hour
        ("m_gamePaused",                        DataTypes.UNSIGNED_INT8),         # Whether the game is paused – network game only
        ("m_isSpectating",                      DataTypes.UNSIGNED_INT8),         # Whether the player is spectating
        ("m_spectatorCarIndex",                 DataTypes.UNSIGNED_INT8),         # Index of the car being spectated
        ("m_sliProNativeSupport",               DataTypes.UNSIGNED_INT8),         # SLI Pro support, 0 = inactive, 1 = active
        ("m_numMarshalZones",                   DataTypes.UNSIGNED_INT8),         # Number of marshal zones to follow
        ("m_marshalZones",                      MarshalZone * 21),                      # List of marshal zones – max 21
        ("m_safetyCarStatus",                   DataTypes.UNSIGNED_INT8),         # 0 = no safety car, 1 = full, 2 = virtual, 3 = formation lap
        ("m_networkGame",                       DataTypes.UNSIGNED_INT8),         # 0 = offline, 1 = online
    ]


### Lap Data Packet -- Rate as specified in menus -- 843 bytes


class LapData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_lastLapTime",           DataTypes.FLOAT),             # Last lap time in seconds
        ("m_currentLapTime",        DataTypes.FLOAT),             # Current time around the lap in seconds
        ("m_bestLapTime",           DataTypes.FLOAT),             # Best lap time of the session in seconds
        ("m_sector1Time",           DataTypes.FLOAT),             # Best overall sector 3 time of the session in milliseconds
        ("m_sector2Time",           DataTypes.FLOAT),             # Lap number best overall sector 3 time achieved on
        ("m_lapDistance",           DataTypes.FLOAT),             # Distance vehicle is around current lap in metres - can, be negative if line not crossed yet
        ("m_totalDistance",         DataTypes.FLOAT),             # Total distance travelled in session in metres - can, be negative if line not crossed yet
        ("m_safetyCarDelta",        DataTypes.FLOAT),             # Delta in seconds for safety car
        ("m_carPosition",           DataTypes.UNSIGNED_INT8),     # Car race position
        ("m_currentLapNum",         DataTypes.UNSIGNED_INT8),     # Current lap number
        ("m_pitStatus",             DataTypes.UNSIGNED_INT8),     # 0 = none, 1 = pitting, 2 = in pit area
        ("m_sector",                DataTypes.UNSIGNED_INT8),     # 0 = sector1, 1 = sector2, 2 = sector3
        ("m_currentLapInvalid",     DataTypes.UNSIGNED_INT8),     # Current lap invalid - 0 = valid, 1 = invalid
        ("m_penalties",             DataTypes.UNSIGNED_INT8),     # Accumulated time penalties in seconds to be added
        ("m_gridPosition",          DataTypes.UNSIGNED_INT8),     # Grid position the vehicle started the race in
        ("m_driverStatus",          DataTypes.UNSIGNED_INT8),     # Status of driver - 0 = in garage, 1 = flying lap, 2 = in lap, 3 = out lap, 4 = on track
        ("m_resultStatus",          DataTypes.UNSIGNED_INT8),     # Result status - 0 = invalid, 1 = inactive, 2 = active, 3 = finished, 4 = didnotfinish, 5 = disqualified, 6 = not classified, 7 = retired
    ]


class PacketLapData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),                      # Header
        ("m_lapData",               LapData * 20),                      # Lap data for all cars on track
    ]


### Event Packet -- When the event occurs -- 32 bytes


class FastestLap(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8), # Vehicle index of car achieving fastest lap
        ("lapTime",     DataTypes.FLOAT),         # Lap time is in seconds
    ]


class Retirement(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of car retiring
    ]  


class TeamMateInPits(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of team mate
    ]  


class RaceWinner(DataTypes.STRUCTURE):
    _fields_ = [
        ("vehicleIdx",  DataTypes.UNSIGNED_INT8)  # Vehicle index of the race winner
    ]  


class EventDataDetails(DataTypes.UNION):
    _fields_ = [
        ("m_fastestLap",        FastestLap),
        ("m_retirement",        Retirement),
        ("m_teamMateInPits",    TeamMateInPits),
        ("m_raceWinner",        RaceWinner),
    ]


class PacketEventData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_eventStringCode",   DataTypes.UNSIGNED_INT8 * 4), # Event string code
        ("m_eventDetails",      EventDataDetails),                  # Event details - should be interpreted differently for each type
    ]


### Participants Packet -- Every 5 seconds -- 1104 bytes


class ParticipantData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_aiControlled",      DataTypes.UNSIGNED_INT8),     # Whether the vehicle is AI (1) or Human (0) controlled
        ("m_driverId",          DataTypes.UNSIGNED_INT8),     # Driver id - see appendix, 255 if network human
        ("m_teamId",            DataTypes.UNSIGNED_INT8),     # Team id - see appendix
        ("m_raceNumber",        DataTypes.UNSIGNED_INT8),     # Race number of the car
        ("m_nationality",       DataTypes.UNSIGNED_INT8),     # Nationality of the driver
        ("m_name",              DataTypes.CHAR * 48),         # Name of participant in UTF-8 format – null terminated, Will be truncated with … (U+2026) if too long
        ("m_yourTelemetry",     DataTypes.UNSIGNED_INT8),     # The player's UDP setting, 0 = restricted, 1 = public
    ]


class PacketParticipantsData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",            PacketHeader),                      # Header
        ("m_numActiveCars",     DataTypes.UNSIGNED_INT8),     # Number of active cars in the data – should match number of cars on HUD
        ("m_participants",      ParticipantData * 20),
    ]


### Car Setups Packet -- 2 per second -- 843 bytes


class CarSetupData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_frontWing",                 DataTypes.UNSIGNED_INT8),     # Front wing aero
        ("m_rearWing",                  DataTypes.UNSIGNED_INT8),     # Rear wing aero
        ("m_onThrottle",                DataTypes.UNSIGNED_INT8),     # Differential adjustment on throttle (percentage)
        ("m_offThrottle",               DataTypes.UNSIGNED_INT8),     # Differential adjustment off throttle (percentage)
        ("m_frontCamber",               DataTypes.FLOAT),             # Front camber angle (suspension geometry)
        ("m_rearCamber",                DataTypes.FLOAT),             # Rear camber angle (suspension geometry)
        ("m_frontToe",                  DataTypes.FLOAT),             # Front toe angle (suspension geometry)
        ("m_rearToe",                   DataTypes.FLOAT),             # Rear toe angle (suspension geometry)
        ("m_frontSuspension",           DataTypes.UNSIGNED_INT8),     # Front suspension
        ("m_rearSuspension",            DataTypes.UNSIGNED_INT8),     # Rear suspension
        ("m_frontAntiRollBar",          DataTypes.UNSIGNED_INT8),     # Front anti-roll bar
        ("m_rearAntiRollBar",           DataTypes.UNSIGNED_INT8),     # Front anti-roll bar
        ("m_frontSuspensionHeight",     DataTypes.UNSIGNED_INT8),     # Front ride height
        ("m_rearSuspensionHeight",      DataTypes.UNSIGNED_INT8),     # Rear ride height
        ("m_brakePressure",             DataTypes.UNSIGNED_INT8),     # Brake pressure (percentage)
        ("m_brakeBias",                 DataTypes.UNSIGNED_INT8),     # Brake bias (percentage)
        ("m_frontTyrePressure",      DataTypes.FLOAT),             # Front tyre pressure (PSI)
        ("m_rearTyrePressure",     DataTypes.FLOAT),             # Rear tyre pressure (PSI)
        ("m_ballast",                   DataTypes.UNSIGNED_INT8),     # Ballast
        ("m_fuelLoad",                  DataTypes.FLOAT),             # Fuel load
    ]


class PacketCarSetupData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                PacketHeader),              # Header
        ("m_car_setups",            CarSetupData * 20),
    ]


### Car Telemetry Packet -- Rate as specified in menus -- 1347 bytes


class CarTelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_speed",                     DataTypes.UNSIGNED_INT16),        # Speed of car in kilometres per hour
        ("m_throttle",                  DataTypes.FLOAT),                 # Amount of throttle applied (0.0 to 1.0)
        ("m_steer",                     DataTypes.FLOAT),                 # Steering (-1.0 (full lock left) to 1.0 (full lock right))
        ("m_brake",                     DataTypes.FLOAT),                 # Amount of brake applied (0.0 to 1.0)
        ("m_clutch",                    DataTypes.UNSIGNED_INT8),         # Amount of clutch applied (0 to 100)
        ("m_gear",                      DataTypes.SIGNED_INT8),           # Gear selected (1-8, N=0, R=-1)
        ("m_engineRpm",                 DataTypes.UNSIGNED_INT16),        # Engine RPM
        ("m_drs",                       DataTypes.UNSIGNED_INT8),         # 0 = off, 1 = on
        ("m_revLightsPercent",          DataTypes.UNSIGNED_INT8),         # Rev lights indicator (percentage)
        ("m_brakesTemperature",         DataTypes.UNSIGNED_INT16 * 4),    # Brakes temperature (celsius)
        ("m_tyresSurfaceTemperature",   DataTypes.UNSIGNED_INT16 * 4),     # Tyres surface temperature (celsius)
        ("m_tyresInnerTemperature",     DataTypes.UNSIGNED_INT16 * 4),     # Tyres inner temperature (celsius)
        ("m_engineTemperature",         DataTypes.UNSIGNED_INT16),        # Engine temperature (celsius)
        ("m_tyresPressure",             DataTypes.FLOAT * 4),             # Tyres pressure (PSI)
        ("m_surfaceType",               DataTypes.UNSIGNED_INT8 * 4),     # Driving surface, see appendices
    ]


class PacketCarTelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",                        PacketHeader),                      # Header
        ("m_carTelemetryData",              CarTelemetryData * 20),
        ("m_buttonStatus",                  DataTypes.UNSIGNED_INT32),    # Bit flags specifying which buttons are being pressed currently - see appendices
    ]


### Car Status Packet -- Rate as specified in menus -- 1143 bytes


class CarStatusData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_tractionControl",           DataTypes.UNSIGNED_INT8),     # Traction control - 0 = off, 1 = medium, 2 = full
        ("m_antiLockBrakes",            DataTypes.UNSIGNED_INT8),     # 0 (off) - 1 (on)
        ("m_fuelMix",                   DataTypes.UNSIGNED_INT8),     # Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
        ("m_frontBrakeBias",            DataTypes.UNSIGNED_INT8),     # Front brake bias (percentage)
        ("m_pitLimiterStatus",          DataTypes.UNSIGNED_INT8),     # Pit limiter status - 0 = off, 1 = on
        ("m_fuelInTank",                DataTypes.FLOAT),             # Current fuel mass
        ("m_fuelCapacity",              DataTypes.FLOAT),             # Fuel capacity
        ("m_fuelRemainingLaps",         DataTypes.FLOAT),             # Fuel remaining in terms of laps (value on MFD)
        ("m_maxRpm",                    DataTypes.UNSIGNED_INT16),    # Cars max RPM, point of rev limiter
        ("m_idleRpm",                   DataTypes.UNSIGNED_INT16),    # Cars idle RPM
        ("m_maxGears",                  DataTypes.UNSIGNED_INT8),     # Maximum number of gears
        ("m_drsAllowed",                DataTypes.UNSIGNED_INT8),     # 0 = not allowed, 1 = allowed
        ("m_tyresWear",                 DataTypes.UNSIGNED_INT8 * 4), # Tyre wear percentage
        ("m_actualTyreCompound",        DataTypes.UNSIGNED_INT8),     # F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1, 21 = C0, 7 = inter, 8 = wet
                                                                            # F1 Classic - 9 = dry, 10 = wet
                                                                            # F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard, 15 = wet
        ("m_visualTyreCompound",        DataTypes.UNSIGNED_INT8),     # F1 visual (can be different from actual compound) - 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                                                            # F1 Classic – same as above
                                                                            # F2 ‘19, 15 = wet, 19 – super soft, 20 = soft, 21 = medium , 22 = hard
        ("m_tyresDamage",               DataTypes.UNSIGNED_INT8 * 4), # Tyre damage (percentage)
        ("m_frontLeftWingDamage",       DataTypes.SIGNED_INT8),       # Front left wing damage (percentage)
        ("m_frontRightWingDamage",      DataTypes.SIGNED_INT8),       # Front right wing damage (percentage)
        ("m_rearWingDamage",            DataTypes.SIGNED_INT8),       # Rear wing damage (percentage)
        ("m_engineDamage",              DataTypes.SIGNED_INT8),       # Engine damage (percentage)
        ("m_gearBoxDamage",             DataTypes.SIGNED_INT8),       # Gear box damage (percentage)
        ("m_vehicleFiaFlags",           DataTypes.SIGNED_INT8),       # -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow
        ("m_ersStoreEnergy",            DataTypes.FLOAT),             # ERS energy store in Joules
        ("m_ersDeployMode",             DataTypes.UNSIGNED_INT8),     # ERS deployment mode, 0 = none, 1 = medium, 2 = hotlap, 3 = overtake
        ("m_ersHarvestedThisLapMguk",   DataTypes.FLOAT),             # ERS energy harvested this lap by MGU-K
        ("m_ersHarvestedThisLapMguh",   DataTypes.FLOAT),             # ERS energy harvested this lap by MGU-H
        ("m_ersDeployedThisLap",        DataTypes.FLOAT),             # ERS energy deployed this lap
    ]


class PacketCarStatusData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small
    _fields_ = [
        ("m_header",        PacketHeader),          # Header
        ("m_carStatusData", CarStatusData * 20),
    ]


### MetaData

class MetaData:
    # standard network info
    port: int | None = 20777
    
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
    packetIDAttribute: str | None = "m_packetId"
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (PacketMotionData,),         # Contains all motion data for player’s car – only sent while player is in control
        1: (PacketSessionData,),        # Data about the session – track, time left
        2: (PacketLapData,),            # Data about all the lap times of cars in the session
        3: (PacketEventData,),          # Various notable events that happen during a session
        4: (PacketParticipantsData,),   # List of participants in the session, mostly relevant for multiplayer
        5: (PacketCarSetupData,),       # Packet detailing car setups for cars in the race
        6: (PacketCarTelemetryData,),   # Telemetry data for all cars
        7: (PacketCarStatusData,),      # Status data for all cars
    }

