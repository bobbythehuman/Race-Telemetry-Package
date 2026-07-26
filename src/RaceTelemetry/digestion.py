import ctypes
from struct import pack
import warnings
import logging

from types import SimpleNamespace
from functools import lru_cache

# ---------------------------------------------------------------------------
# Other Setups
# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bytes to strings
# ---------------------------------------------------------------------------


def new_byte_to_string(value: bytes, extra=True) -> str:
    """
    Takes a bytes value and converts it to a string,
    stripping any null characters and splitting on the first null character if extra is True.
    """

    toBytes = bytes(value)
    decodedValue = toBytes.decode("utf-8", errors="replace")
    strippedValue = decodedValue.strip("\0")

    if not extra:
        return strippedValue

    splitValue = strippedValue.split("\x00", 1)
    cutValue = splitValue[0]

    return cutValue


# ---------------------------------------------------------------------------
# Unpack arrays
# ---------------------------------------------------------------------------


def unpack_array(packet) -> list | str:
    """
    Takes a ctypes array and converts it to a list, with any bytes values converted to strings.
    """
    if not packet:
        # return empty packets
        return packet

    if isinstance(packet[0], bytes):
        # if array contains bytes convert array to string
        value = new_byte_to_string(packet)
        return value

    value = list(packet)

    for key, item in enumerate(value):
        if isinstance(item, (int, str, bool)):
            # no transformation need to be done
            pass

        elif isinstance(item, float):
            # round float numbers
            value[key] = round(item, 5)

        elif isinstance(item, ctypes.Array):
            # manage each item in array seperatly
            value[key] = unpack_array(item)

        elif isinstance(item, bytes):
            # convert bytes to a string
            value[key] = new_byte_to_string(item)

        else:
            # assume it is a class
            LOGGER.info("Unknown value, assuming it is a class %r" % item)
            value[key] = dynamic_ingest(item)

    return value


# ---------------------------------------------------------------------------
# Apply enums
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def _inverse_enums(packet_cls):
    enums = getattr(packet_cls, "_enums_", {})
    inverse = {}
    for k, v in enums.items():
        for x in v:
            inverse.setdefault(x, []).append(k)
    return inverse


def apply_enum(value, enumType, enumMode: int = 0):
    """
    Receives a value and converts it into an Enum then returns a value depending on enumMode.
    """
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
        LOGGER.warning("[msg=ENUM] [Warning]\tvalue %s is not a valid enum member of %s" % (value, enumType))
        # If the value is not a valid enum member, keep it as is
        pass

    return value


# ---------------------------------------------------------------------------
# Dynamic ingestion
# ---------------------------------------------------------------------------


def dynamic_ingest(packet: type, enumMode: int = 0) -> type:
    """
    Takes a packet and dynamically ingests it, converting:
    - floats to rounded floats
    - bytes values to strings
    - ctypes arrays to lists
    - recursively ingests any nested classes
    - fields with a declared _enums_ mapped to their enum type
    """
    packetName = packet.__class__.__name__

    if not hasattr(packet, "_field_"):
        LOGGER.error("Packet %s doesnt contain a _field_ attribute" % packet.__name__)
        return type(packetName, (), {})

    attrs = {field[0]: getattr(packet, field[0]) for field in packet._fields_}

    newPacket = type(packetName, (), {})
    # newPacket = SimpleNamespace()

    # reverse enum dictionary so attribute references an enum
    inverseEnums = _inverse_enums(packet.__class__)

    for source_attr, value in attrs.items():
        # check if value references the parent if so return None or empty array

        if isinstance(value, (str, int, bool)):
            pass

        elif isinstance(value, float):
            # round float numbers
            value = round(value, 5)

        elif isinstance(value, bytes):
            # convert bytes to a string
            value = new_byte_to_string(value)

        elif isinstance(value, ctypes.Array):
            # manage each item in array seperatly
            value = unpack_array(value)

        elif value is None:
            pass

        else:
            # assume it is a class
            LOGGER.info("Unknown value, assuming it is a class %r" % value)
            value = dynamic_ingest(value)

        if source_attr in inverseEnums:
            enum_type = None
            all_enum_type = inverseEnums[source_attr]

            if len(all_enum_type) > 1:
                LOGGER.critical("Multiple enum types found for attribute '%s': %s. Cannot determine which one to use." % (source_attr, all_enum_type))
                raise ValueError(f"Multiple enum types found for attribute '{source_attr}': {all_enum_type}. Cannot determine which one to use.")
            else:
                enum_type = all_enum_type[0]

            if isinstance(value, list):
                value = [apply_enum(i, enum_type, enumMode) for i in value]
            else:
                value = apply_enum(value, enum_type, enumMode)

        setattr(newPacket, source_attr, value)

    return newPacket
