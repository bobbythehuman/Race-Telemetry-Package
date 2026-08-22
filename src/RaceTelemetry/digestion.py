"""
Dynamic ctypes packet ingestion.

Converts ctypes Structures/Unions (and nested Structures/Unions/Arrays within
them) into plain Python objects (SimpleNamespace), applying these
transformations along the way:

- bytes fields  -> decoded, null-terminated strings
- float fields  -> rounded floats
- ctypes Arrays -> lists (or a string, if the array holds bytes)
- fields declared in a packet's `_enums_` mapping -> resolved Enum values
- nested Structures/Unions -> recursively ingested SimpleNamespace objects
"""

from __future__ import annotations
import ctypes
import logging
from enum import Enum
from functools import lru_cache
from types import SimpleNamespace
from typing import Any

# ---------------------------------------------------------------------------
# Other Setups
# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared value conversion
# ---------------------------------------------------------------------------


def _convert_value(value: Any) -> Any:
    """
    Applies the standard set of conversions to a single value:
    leave primitives as-is, round floats, decode bytes, unpack ctypes
    Arrays, and recursively ingest anything else (assumed to be a
    nested ctypes Structure/Union).

    Shared by `unpack_array` and `dynamic_ingest` so the conversion
    rules only need to be maintained in one place.
    """

    if isinstance(value, (str, int, bool)):
        # no transformation need to be done
        return value

    elif isinstance(value, float):
        # round float numbers
        return round(value, 5)

    elif isinstance(value, bytes):
        # convert bytes to a string
        return new_byte_to_string(value)

    elif isinstance(value, ctypes.Array):
        # manage each item in array seperatly
        return unpack_array(value)

    elif value is None:
        return value

    else:
        # Anything left over is assumed to be a nested Structure/Union.
        LOGGER.info("Unknown value, assuming it is a class %r", value)
        return dynamic_ingest(value)


# ---------------------------------------------------------------------------
# Bytes to strings
# ---------------------------------------------------------------------------


def new_byte_to_string(value: bytes, split_on_null: bool = True) -> str:
    """
    Takes a bytes value and converts it to a string, stripping any null
    characters and splitting on the first null character if
    split_on_null is True.
    """

    toBytes = bytes(value)
    decodedValue = toBytes.decode("utf-8", errors="replace")
    strippedValue = decodedValue.strip("\0")

    if not split_on_null:
        return strippedValue

    splitValue = strippedValue.split("\x00", 1)
    firstSegment = splitValue[0]

    return firstSegment


# ---------------------------------------------------------------------------
# Unpack arrays
# ---------------------------------------------------------------------------


def unpack_array(packet) -> list | str:
    """
    Takes a ctypes array and converts it to a list, with any bytes
    values converted to strings. If the array itself holds raw bytes
    (a char array), a single decoded string is returned instead of a
    list of byte values.
    """
    if not packet:
        # return empty packets
        LOGGER.debug("Received empty packet %r", packet)
        return []

    if isinstance(packet[0], bytes):
        # if array contains bytes convert array to string
        value = new_byte_to_string(packet)
        return value

    newArray = []
    for item in packet:
        newItem = _convert_value(item)
        newArray.append(newItem)

    return newArray


# ---------------------------------------------------------------------------
# Apply enums
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def _inverse_enums(packet_cls) -> dict:
    """
    Builds a {field_name: [enum_type, ...]} mapping from a packet
    class's `_enums_` attribute, so a given field name can be looked
    up to find which Enum type (if any) applies to it.
    """
    enums = getattr(packet_cls, "_enums_", {})
    inverse = {}
    for k, v in enums.items():
        for x in v:
            inverse.setdefault(x, []).append(k)
    return inverse


def apply_enum(value: Any, enumType: type[Enum] | None, enumMode: int = 0) -> Any:
    """
    Receives a value and converts it into an Enum, then returns a
    value depending on enum_mode (see EnumMode for the options).
    If the value isn't a valid member of enum_type, it's returned
    unchanged and a warning is logged.
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
        LOGGER.warning("[ENUM] [Warning]\tvalue %r is not a valid enum member of %r", value, enumType)
        # If the value is not a valid enum member, keep it as is
        pass

    return value


# ---------------------------------------------------------------------------
# Dynamic ingestion
# ---------------------------------------------------------------------------


def dynamic_ingest(packet: ctypes.Structure | ctypes.Union | SimpleNamespace | None, enumMode: int = 0) -> SimpleNamespace | None:
    """
    Takes a packet and dynamically ingests it, converting:
    - floats to rounded floats
    - bytes values to strings
    - ctypes arrays to lists
    - recursively ingests any nested classes
    - fields with a declared _enums_ mapped to their enum type
    """

    if not packet:
        return None

    packetName = packet.__class__.__name__
    newPacket = SimpleNamespace()
    newPacket.__name__ = packetName

    if not hasattr(packet, "_fields_"):
        LOGGER.error("Packet %r doesnt contain a _field_ attribute", packetName)
        return newPacket

    attrs = {field[0]: getattr(packet, field[0]) for field in packet._fields_}

    # reverse enum dictionary so attribute references an enum
    inverseEnums = _inverse_enums(packet.__class__)

    for source_attr, value in attrs.items():
        # TODO check if value references the parent if so return None or empty array

        value = _convert_value(value)

        if source_attr in inverseEnums:
            all_enum_type = inverseEnums.get(source_attr)

            if len(all_enum_type) > 1:
                LOGGER.critical("Multiple enum types found for attribute '%r': %r. Cannot determine which one to use.", source_attr, all_enum_type)
                raise ValueError(f"Multiple enum types found for attribute '{source_attr}': {all_enum_type}. Cannot determine which one to use.")

            enum_type = all_enum_type[0]

            if isinstance(value, list):
                value = [apply_enum(i, enum_type, enumMode) for i in value]
            else:
                value = apply_enum(value, enum_type, enumMode)

        setattr(newPacket, source_attr, value)

    return newPacket
