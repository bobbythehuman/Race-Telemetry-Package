# data_structures/ctypes_types.py
import ctypes
import platform

STRUCTURE = ctypes.LittleEndianStructure

SIGNED_INT = ctypes.c_int

SIGNED_INT8 = ctypes.c_int8
UNSIGNED_UINT8 = ctypes.c_uint8
SIGNED_INT16 = ctypes.c_int16
UNSIGNED_UINT16 = ctypes.c_uint16
SIGNED_INT32 = ctypes.c_int32
UNSIGNED_UINT32 = ctypes.c_uint32
SIGNED_INT64 = ctypes.c_int64
UNSIGNED_UINT64 = ctypes.c_uint64

BOOL = ctypes.c_bool
FLOAT = ctypes.c_float
DOUBLE = ctypes.c_double

SIGNED_SHORT = ctypes.c_short
UNSIGNED_SHORT = ctypes.c_ushort

CHAR = ctypes.c_char


if platform.system() == "Windows":
    WCHAR = ctypes.c_wchar
elif platform.system() == "Linux":
    WCHAR = ctypes.c_char
