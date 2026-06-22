import ctypes
from enum import Enum

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
    UNSIGNED_BYTE = ctypes.c_ubyte
    UNSIGNED_SHORT = ctypes.c_ushort

    FLOAT = ctypes.c_float
    CHAR = ctypes.c_char
    SHORT = ctypes.c_short


### Packet Header
#
#   Description: 
#    Base definitions of udp packet structure
#    The data definition mostly follows the data set for the Shared memory, so it is strongly suggested to have a look to the
#    latest shared memory header if you have problem decoding any data.
#

class PacketHeader(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs
    _fields_ = [
        ("mPacketNumber",           DataTypes.UNSIGNED_INT),     # Counter reflecting all the packets that have been sent during the game run
        ("mCategoryPacketNumber",   DataTypes.UNSIGNED_INT),     # Counter of the packet groups belonging to the given category
        ("mPartialPacketIndex",     DataTypes.UNSIGNED_BYTE),    # If the data from this class had to be sent in several packets, the index number
        ("mPartialPacketNumber",    DataTypes.UNSIGNED_BYTE),    # If the data from this class had to be sent in several packets, the total number
        ("mPacketType",             DataTypes.UNSIGNED_BYTE),    # What is the type of this packet (see EUDPStreamerPacketHanlderType for details)
        ("mPacketVersion",          DataTypes.UNSIGNED_BYTE),    # What is the version of protocol for this handler, to be bumped with data structure change
    ]


### Telemetry Packet -- Packet 0

#
#   Telemetry data for the viewed participant. 
#   Frequency: Each tick of the UDP streamer how it is set in the options
#   When it is sent: in race
#

class TelemetryData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (556 instead of at least 564 bytes)
    _fields_ = [
        ("s_header",                    PacketHeader),

        ("sViewedParticipantIndex",     DataTypes.SIGNED_BYTE),

        ("sUnfilteredThrottle",         DataTypes.UNSIGNED_BYTE),
        ("sUnfilteredBrake",            DataTypes.UNSIGNED_BYTE),
        ("sUnfilteredSteering",         DataTypes.SIGNED_BYTE),
        ("sUnfilteredClutch",           DataTypes.UNSIGNED_BYTE),

        ("sCarFlags",                   DataTypes.UNSIGNED_BYTE),
        ("sOilTempCelsius",             DataTypes.SIGNED_SHORT),
        ("sOilPressureKPa",             DataTypes.UNSIGNED_SHORT),
        ("sWaterTempCelsius",           DataTypes.SIGNED_SHORT),
        ("sWaterPressureKpa",           DataTypes.UNSIGNED_SHORT),
        ("sFuelPressureKpa",            DataTypes.UNSIGNED_SHORT),
        ("sFuelCapacity",               DataTypes.UNSIGNED_BYTE),
        ("sBrake",                      DataTypes.UNSIGNED_BYTE),
        ("sThrottle",                   DataTypes.UNSIGNED_BYTE),
        ("sClutch",                     DataTypes.UNSIGNED_BYTE),
        ("sFuelLevel",                  DataTypes.FLOAT),
        ("sSpeed",                      DataTypes.FLOAT),
        ("sRpm",                        DataTypes.UNSIGNED_SHORT),
        ("sMaxRpm",                     DataTypes.UNSIGNED_SHORT),
        ("sSteering",                   DataTypes.SIGNED_BYTE),
        ("sGearNumGears",               DataTypes.UNSIGNED_BYTE),
        ("sBoostAmount",                DataTypes.UNSIGNED_BYTE),
        ("sCrashState",                 DataTypes.UNSIGNED_BYTE),
        ("sOdometerKM",                 DataTypes.FLOAT),

        ("sOrientation",                DataTypes.FLOAT * 3),
        ("sLocalVelocity",              DataTypes.FLOAT * 3),
        ("sWorldVelocity",              DataTypes.FLOAT * 3),
        ("sAngularVelocity",            DataTypes.FLOAT * 3),
        ("sLocalAcceleration",          DataTypes.FLOAT * 3),
        ("sWorldAcceleration",          DataTypes.FLOAT * 3),
        ("sExtentsCentre",              DataTypes.FLOAT * 3),

        ("sTyreFlags",                  DataTypes.UNSIGNED_BYTE * 4),
        ("sTerrain",                    DataTypes.UNSIGNED_BYTE * 4),
        ("sTyreY",                      DataTypes.FLOAT * 4),
        ("sTyreRPS",                    DataTypes.FLOAT * 4),
        ("sTyreTemp",                   DataTypes.UNSIGNED_BYTE * 4),
        ("sTyreHeightAboveGround",      DataTypes.FLOAT * 4),
        ("sTyreWear",                   DataTypes.UNSIGNED_BYTE * 4),
        ("sBrakeDamage",                DataTypes.UNSIGNED_BYTE * 4),
        ("sSuspensionDamage",           DataTypes.UNSIGNED_BYTE * 4),
        ("sBrakeTempCelsius",           DataTypes.SIGNED_SHORT * 4),
        ("sTyreTreadTemp",              DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreLayerTemp",              DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreCarcassTemp",            DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreRimTemp",                DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreInternalAirTemp",        DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreTempLeft",               DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreTempCenter",             DataTypes.UNSIGNED_SHORT * 4),
        ("sTyreTempRight",              DataTypes.UNSIGNED_SHORT * 4),
        ("sWheelLocalPositionY",        DataTypes.FLOAT * 4),
        ("sRideHeight",                 DataTypes.FLOAT * 4),
        ("sSuspensionTravel",           DataTypes.FLOAT * 4),
        ("sSuspensionVelocity",         DataTypes.FLOAT * 4),
        ("sSuspensionRideHeight",       DataTypes.UNSIGNED_SHORT * 4),
        ("sAirPressure",                DataTypes.UNSIGNED_SHORT * 4),

        ("sEngineSpeed",                DataTypes.FLOAT),
        ("sEngineTorque",               DataTypes.FLOAT),
        ("sWings",                      DataTypes.UNSIGNED_BYTE * 2),
        ("sHandBrake",                  DataTypes.UNSIGNED_BYTE),

        ("sAeroDamage",                 DataTypes.UNSIGNED_BYTE),
        ("sEngineDamage",               DataTypes.UNSIGNED_BYTE),

        ("sJoyPad0",                    DataTypes.UNSIGNED_INT),
        ("sDPad",                       DataTypes.UNSIGNED_BYTE),
        ("sTyreCompound",               DataTypes.CHAR * 40 * 4),
        ("sTurboBoostPressure",         DataTypes.FLOAT),
        ("sFullPosition",               DataTypes.FLOAT * 3),
        ("sBrakeBias",                  DataTypes.UNSIGNED_BYTE),
        ("sTickCount",                  DataTypes.UNSIGNED_INT),
    ]


### Race Packet -- Packet 1

#
#   Race stats data.
#   Frequency: Logaritmic decrease
#   When it is sent: Counter resets on entering InRace state and again each time any of the values changes
#

class RaceData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sWorldFastestLapTime",            DataTypes.FLOAT),
        ("sPersonalFastestLapTime",         DataTypes.FLOAT),
        ("sPersonalFastestSector1Time",     DataTypes.FLOAT),
        ("sPersonalFastestSector2Time",     DataTypes.FLOAT),
        ("sPersonalFastestSector3Time",     DataTypes.FLOAT),
        ("sWorldFastestSector1Time",        DataTypes.FLOAT),
        ("sWorldFastestSector2Time",        DataTypes.FLOAT),
        ("sWorldFastestSector3Time",        DataTypes.FLOAT),
        ("sTrackLength",                    DataTypes.FLOAT),
        ("sTrackLocation",                  DataTypes.CHAR * 64),
        ("sTrackVariation",                 DataTypes.CHAR * 64),
        ("sTranslatedTrackLocation",        DataTypes.CHAR * 64),
        ("sTranslatedTrackVariation",       DataTypes.CHAR * 64),
        ("sLapsTimeInEvent",                DataTypes.UNSIGNED_SHORT),
        ("sEnforcedPitStopLap",             DataTypes.SIGNED_BYTE),
    ]


### Participants Packet -- Packet 2

#
#   Participant names data.
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#   The sParticipantsChangedTimestamp represent last time the participants has changed and is to be used to sync
#   this information with the rest of the participant related packets
#

class ParticipantsData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT),
        ("sName",                           DataTypes.CHAR * 64 * 16),
        ("sNationality",                    DataTypes.UNSIGNED_INT * 16),
        ("sIndex",                          DataTypes.UNSIGNED_SHORT * 16),
    ]


### Timings Packet -- Packet 3

#
#   Participant timings data. 
#   Frequency: Each tick of the UDP streamer how it is set in the options.
#   When it is sent: in race
#

class ParticipantsInfo(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _fields_ = [
        ("sWorldPosition",          DataTypes.SIGNED_SHORT * 3),
        ("sOrientation",            DataTypes.SIGNED_SHORT * 3),
        ("sCurrentLapDistance",     DataTypes.UNSIGNED_SHORT),
        ("sRacePosition",           DataTypes.UNSIGNED_BYTE),
        ("sSector",                 DataTypes.UNSIGNED_BYTE),
        ("sHighestFlag",            DataTypes.UNSIGNED_BYTE),
        ("sPitModeSchedule",        DataTypes.UNSIGNED_BYTE),
        ("sCarIndex",               DataTypes.UNSIGNED_SHORT),
        ("sRaceState",              DataTypes.UNSIGNED_BYTE),
        ("sCurrentLap",             DataTypes.UNSIGNED_BYTE),
        ("sCurrentTime",            DataTypes.FLOAT),
        ("sCurrentSectorTime",      DataTypes.FLOAT),
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_SHORT),
    ]


class TimingsData(DataTypes.STRUCTURE):
    _pack_ = 1 # !!REQUIRED - is required or error occurs - Buffer size too small (1059 instead of at least 1192 bytes)
    _fields_ = [
        ("s_header",                        PacketHeader),
        ("sNumParticipants",                DataTypes.SIGNED_BYTE),
        ("sParticipantsChangedTimestamp",   DataTypes.UNSIGNED_INT),
        ("sEventTimeRemaining",             DataTypes.FLOAT),
        ("sSplitTimeAhead",                 DataTypes.FLOAT),
        ("sSplitTimeBehind",                DataTypes.FLOAT),
        ("sSplitTime",                      DataTypes.FLOAT),
        ("sParticipants",                   ParticipantsInfo * 32),
        ("sLocalParticipantIndex",          DataTypes.UNSIGNED_SHORT),
        ("sTickCount",                      DataTypes.UNSIGNED_INT),
    ]


### Game State Packet -- Packet 4

#
#   Game State. 
#   Frequency: Each 5s while being in Main Menu, Each 10s while being in race + on each change Main Menu<->Race several times.
#   the frequency in Race is increased in case of weather timer being faster  up to each 5s for 30x time progression
#   When it is sent: Always
#

class GameStateData(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("s_header",                PacketHeader),
        ("mBuildVersionNumber",     DataTypes.UNSIGNED_SHORT),
        ("mGameState",              DataTypes.CHAR),
        ("sAmbientTemperature",     DataTypes.SIGNED_BYTE),
        ("sTrackTemperature",       DataTypes.SIGNED_BYTE),
        ("sRainDensity",            DataTypes.UNSIGNED_BYTE),
        ("sSnowDensity",            DataTypes.UNSIGNED_BYTE),
        ("sWindSpeed",              DataTypes.SIGNED_BYTE),
        ("sWindDirectionX",         DataTypes.SIGNED_BYTE),
        ("sWindDirectionY",         DataTypes.SIGNED_BYTE),
        ("paddingD",                DataTypes.SHORT),
    ]


### Time Stats Packet -- Packet 7

#
#   Participant Stats and records
#   Frequency: When entering the race and each time any of the values change, so basically each time any of the participants crosses a sector boundary.
#   When it is sent: In Race
#

class ParticipantStatsInfo(DataTypes.STRUCTURE):
    _fields_ = [
        ("sFastestLapTime",         DataTypes.FLOAT),
        ("sLastLapTime",            DataTypes.FLOAT),
        ("sLastSectorTime",         DataTypes.FLOAT),
        ("sFastestSector1Time",     DataTypes.FLOAT),
        ("sFastestSector2Time",     DataTypes.FLOAT),
        ("sFastestSector3Time",     DataTypes.FLOAT),
        ("sParticipantOnlineRep",   DataTypes.UNSIGNED_INT),
        ("sMPParticipantIndex",     DataTypes.UNSIGNED_SHORT),
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

#
#   Participant Vehicle names
#   Frequency: Logarithmic decrease
#   When it is sent: Counter resets on entering InRace state and again each  the participants change. 
#	The sParticipantsChangedTimestamp represent last time the participants has changed and is  to be used to sync 
#	this information with the rest of the participant related packets
#   Note: This data is always sent with at least 2 packets. The 1-(n-1) holds the vehicle name for each participant
#	The last one holding the class names.

class VehicleInfo(DataTypes.STRUCTURE):
    _fields_ = [
        ("sIndex",  DataTypes.UNSIGNED_SHORT),
        ("sClass",  DataTypes.UNSIGNED_INT),
        ("sName",   DataTypes.CHAR * 64),
    ]


class ParticipantVehicleNamesData(DataTypes.STRUCTURE):
    _fields_ = [
        ("s_header",        PacketHeader),
        ("sVehicleInfo",    VehicleInfo * 16),
    ]


class ClassInfo(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("sClassIndex", DataTypes.UNSIGNED_INT),
        ("sName",       DataTypes.CHAR * 20),
    ]


class VehicleClassNamesData(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("s_header",    PacketHeader),
        ("sClassInfo",  ClassInfo * 60),
    ]

### MetaData

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




