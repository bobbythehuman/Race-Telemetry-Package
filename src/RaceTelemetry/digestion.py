import ctypes


def newChrToString(value: bytes, extra=True) -> str:
    '''
    Takes a bytes value and converts it to a string, 
    stripping any null characters and splitting on the first null character if extra is True.
    '''
    if extra:
        return bytes(value).decode("utf-8").strip("\0").split("\x00", 1)[0]
    else:
        return bytes(value).decode("utf-8").strip("\0")


def unpackArray(packet) -> list | str:
    '''
    Takes a ctypes array and converts it to a list, with any bytes values converted to strings.
    '''
    if isinstance(packet[0], bytes):
        value = newChrToString(packet)
        return value
    
    value = list(packet)

    for key, item in enumerate(value):
        if type(item) in [int, str, bool]:
            pass

        elif isinstance(item, float):
            value[key] = round(item, 5)

        elif isinstance(item, ctypes.Array):
            value[key] = unpackArray(item)
            # value[key] = newChrToString(item)

        elif isinstance(item, bytes):
            value[key] = newChrToString(item)
        
        else:
            # assume it is a class
            value[key] = dynamic_ingest(item)
            
    return value

def applyEnum(value, enumType, enumMode: int = 0):
    '''
    Receives a value and converts it into an Enum then returns a value depending on enumMode.
    '''
    if not enumType:
        return value
    try:
        if enumMode == 0:
            value = enumType(value)
        elif enumMode == 1:
            value = enumType(value).value
        elif enumMode == 2:
            value = enumType(value).name
    except ValueError:
        # If the value is not a valid enum member, keep it as is
        value = value
    
    return value

def dynamic_ingest(packet: type, enumMode: int = 0) -> type:
    '''
    Takes a packet and dynamically ingests it, converting:
    - floats to rounded floats
    - bytes values to strings 
    - ctypes arrays to lists
    - recursively ingests any nested classes
    - fields with a declared _enums_ mapped to their enum type
    '''
    attrs = {field[0]: getattr(packet, field[0]) for field in packet._fields_}
    enums = getattr(packet, "_enums_", {})

    packetName = packet.__class__.__name__
    newPacket = type(packetName, (), {})

    inverseEnums = {}
    for k,v in enums.items():
        for x in v:
            inverseEnums.setdefault(x, []).append(k)

    for source_attr, value in attrs.items():
        if isinstance(value, bool):
            pass
        elif isinstance(value, int):
            pass
        elif isinstance(value, str):
            pass
        
        elif isinstance(value, float):
            value = round(value, 5)
        
        elif isinstance(value, bytes):
            value = newChrToString(value)

        elif isinstance(value, ctypes.Array):
            value = unpackArray(value)
        
        elif value is None:
            pass
            
        else:
            # print("Unrecognised type or assuming it is a class")
            value = dynamic_ingest(value)
        
        if source_attr in inverseEnums:
            enum_type = None
            all_enum_type = inverseEnums[source_attr]
            if len(all_enum_type) > 1:
                raise ValueError(f"Multiple enum types found for attribute '{source_attr}': {all_enum_type}. Cannot determine which one to use.")
            else:
                enum_type = all_enum_type[0]
            
            if isinstance(value, list):
                value = [applyEnum(i, enum_type, enumMode) for i in value]
            else:
                value = applyEnum(value, enum_type, enumMode)

        setattr(newPacket, source_attr, value)

    return newPacket
