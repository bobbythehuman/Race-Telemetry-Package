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


def unpackArray(packet):
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


def dynamic_ingest(packet: type) -> type:
    '''
    Takes a packet and dynamically ingests it, converting any bytes values to strings and any ctypes arrays to lists.
    '''
    attrs = {field[0]: getattr(packet, field[0]) for field in packet._fields_}

    packetName = packet.__class__.__name__
    newPacket = type(packetName, (), {})

    for source_attr, value in attrs.items():

        if isinstance(value, int):
            pass
        elif isinstance(value, str):
            pass
        elif isinstance(value, bool):
            pass
        
        elif isinstance(value, float):
            value = round(value, 5)
        
        elif isinstance(value, bytes):
            value = newChrToString(value)

        elif isinstance(value, ctypes.Array):
            value = unpackArray(value)

        else:
            # print("Unrecognised type or assuming it is a class")
            value = dynamic_ingest(value)
            # continue

        setattr(newPacket, source_attr, value)

    return newPacket
