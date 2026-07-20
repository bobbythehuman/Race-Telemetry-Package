import ctypes


# source
# https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub


class DataTypes:
    STRUCTURE = ctypes.LittleEndianStructure
    
    SIGNED_INT = ctypes.c_int
    
    BOOL = ctypes.c_bool
    FLOAT = ctypes.c_float
    CHAR = ctypes.c_wchar


### * Data Structure

# If the client subscribed himself with SUBSCRIBE_UPDATE identifier, it will receive the following structured data
class RTCarData(DataTypes.STRUCTURE):
    # _pack_ = 1 # ! Do Not Enable or data will be wrong
    _fields_ = [
        ("identifier",  DataTypes.CHAR),          # is set to char “a” , it is used to understand that the structured data is the data that the client app wants
        ("size",        DataTypes.SIGNED_INT),    # the size of the structured data in Bytes
        
        ("speed_Kmh",   DataTypes.FLOAT),
        ("speed_Mph",   DataTypes.FLOAT),
        ("speed_Ms",    DataTypes.FLOAT),
        
        ("isAbsEnabled",        DataTypes.BOOL),
        ("isAbsInAction",       DataTypes.BOOL),
        ("isTcInAction",        DataTypes.BOOL),
        ("isTcEnabled",         DataTypes.BOOL),
        ("isInPit",             DataTypes.BOOL),
        ("isEngineLimiterOn",   DataTypes.BOOL),
        
        ("accG_vertical",       DataTypes.FLOAT),
        ("accG_horizontal",     DataTypes.FLOAT),
        ("accG_frontal",        DataTypes.FLOAT),
        
        ("lapTime",     DataTypes.SIGNED_INT),
        ("lastLap",     DataTypes.SIGNED_INT),
        ("bestLap",     DataTypes.SIGNED_INT),
        ("lapCount",    DataTypes.SIGNED_INT),
        
        ("gas",         DataTypes.FLOAT),
        ("brake",       DataTypes.FLOAT),
        ("clutch",      DataTypes.FLOAT),
        ("engineRPM",   DataTypes.FLOAT),
        ("steer",       DataTypes.FLOAT),
        ("gear",        DataTypes.SIGNED_INT),
        ("cgHeight",    DataTypes.FLOAT),
        
        ("wheelAngularSpeed",           DataTypes.FLOAT * 4),
        ("slipAngle",                   DataTypes.FLOAT * 4),
        ("slipAngle_ContactPatch",      DataTypes.FLOAT * 4),
        ("slipRatio",                   DataTypes.FLOAT * 4),
        ("tyreSlip",                    DataTypes.FLOAT * 4),
        ("ndSlip",                      DataTypes.FLOAT * 4),
        ("load",                        DataTypes.FLOAT * 4),
        ("Dy",                          DataTypes.FLOAT * 4),
        ("Mz",                          DataTypes.FLOAT * 4),
        ("tyreDirtyLevel",              DataTypes.FLOAT * 4),
        
        ("camberRAD",               DataTypes.FLOAT * 4),
        ("tyreRadius",              DataTypes.FLOAT * 4),
        ("tyreLoadedRadius",        DataTypes.FLOAT * 4),
        ("suspensionHeight",        DataTypes.FLOAT * 4),
        ("carPositionNormalized",   DataTypes.FLOAT),
        ("carSlope",                DataTypes.FLOAT),
        ("carCoordinates",          DataTypes.FLOAT * 3),
    ]

# If the client subscribed himself with SUBSCRIBE_SPOT identifier, it will receive the following structured data whenever a spot event is triggered (for example for the end of a lap). 
# Differently from SUBSCRIBE_UPDATE, this event will interest all the cars in the AC session
class RTLapData(DataTypes.STRUCTURE):
    _pack_ = 1
    _fields_ = [
        ("carIdentifierNumber",     DataTypes.SIGNED_INT),
        ("lap",                     DataTypes.SIGNED_INT),
        ("driverName",              DataTypes.CHAR * 50),
        ("carName",                 DataTypes.CHAR * 50),
        ("time",                    DataTypes.SIGNED_INT),
    ]


### * Hand Shake

# The PC running Assetto Corsa will be referred as the ACServer.

# [not used in the current Remote Telemtry version by AC] In future versions it will identify the platform type of the client. This will be used to adjust a specific behaviour for each platform
# [not used in the current Remote Telemtry version by AC] In future version this field will identify the AC Remote Telemetry version that the device expects to speak with.
# This is the type of operation required by the client. The following operations are now available:
#   HANDSHAKE = 0 :         This operation identifier must be set when the client wants to start the comunication.
#   SUBSCRIBE_UPDATE = 1 :  This operation identifier must be set when the client wants to be updated from the specific ACServer.
#   SUBSCRIBE_SPOT = 2 :    This operation identifier must be set when the client wants to be updated from the specific ACServer just for SPOT Events (e.g.: the end of a lap).
#   DISMISS = 3 :           This operation identifier must be set when the client wants to leave the comunication with ACServer.

class handshaker(DataTypes.STRUCTURE):
    # _pack_ = 1
    _fields_ = [
        ("identifier",      DataTypes.SIGNED_INT),
        ("version",         DataTypes.SIGNED_INT),
        ("operationId",     DataTypes.SIGNED_INT),
    ]
    def __init__(self, operationID, identifier=1, version=1):
        super().__init__(identifier=identifier, version=version, operationId=operationID)

class handshackerResponse(DataTypes.STRUCTURE): # might be 408 or 308
    _pack_ = 1
    _fields_ = [
        ("carName",         DataTypes.CHAR * 50),     # is the name of the car that the player is driving on the AC Server
        ("driverName",      DataTypes.CHAR * 50),     # is the name of the driver running on the AC Server
        ("identifier",      DataTypes.SIGNED_INT),    # for now is just 4242, this code will identify different status, as “NOT AVAILABLE” for connection
        ("version",         DataTypes.SIGNED_INT),    # for now is set to 1, this will identify the version running on the AC Server
        ("trackName",       DataTypes.CHAR * 50),     # is the name of the track on the AC Server
        ("trackConfig",     DataTypes.CHAR * 50),     # is the track configuration
    ]

def startHandShake(socket, destination: tuple[int, int]):
    handShakeMSG = handshaker(operationID = 0)
    prepHandShake = bytes(handShakeMSG)
    
    socket.sendto(prepHandShake, destination)
        
    handShakeMSG = handshaker(operationID = 1)
    prepHandShake = bytes(handShakeMSG)
    socket.sendto(prepHandShake, destination)
    
    handShakeMSG = handshaker(operationID = 2)
    prepHandShake = bytes(handShakeMSG)
    socket.sendto(prepHandShake, destination)

def endHandShake(socket, destination: tuple[int, int]):
    handShakeMSG = handshaker(operationID = 3)
    prepHandShake = bytes(handShakeMSG)
    
    socket.sendto(prepHandShake, destination)


### * MetaData

class MetaData:
    # standard network info
    port: int | None = 9997
    
    # use if a heartbeat is needed
    heartBeatPort: int | None = None
    heartBeatFunc = None
    
    # use for itinial hand shake
    handShakePort: int | None = 9996
    handShakeFunc: tuple | None = (startHandShake, endHandShake)
    
    # use if the data needs decrypting
    decrytionFunc = None
    
    # use if there is a header packet
    headerInfo: type | None = None
    packetIDAttribute: str | None = None
    
    # use for shared memory
    allSharedMemoryNames: str | None | dict[str, str] = None
    
    # standard packet info
    packetInfo: dict[int, tuple[type, ...]] = {
        0: (RTCarData, RTLapData, handshackerResponse, ),
    }