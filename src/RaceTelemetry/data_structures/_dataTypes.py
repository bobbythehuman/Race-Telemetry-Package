# data_structures/ctypes_types.py
import ctypes
import platform

STRUCTURE = ctypes.LittleEndianStructure
UNION = ctypes.Union

SIGNED_INT = ctypes.c_int
SIGNED_INT8 = ctypes.c_int8
SIGNED_INT16 = ctypes.c_int16
SIGNED_INT32 = ctypes.c_int32
SIGNED_INT64 = ctypes.c_int64

UNSIGNED_UINT = ctypes.c_uint
UNSIGNED_UINT8 = ctypes.c_uint8
UNSIGNED_UINT16 = ctypes.c_uint16
UNSIGNED_UINT32 = ctypes.c_uint32
UNSIGNED_UINT64 = ctypes.c_uint64

BOOL = ctypes.c_bool
FLOAT = ctypes.c_float
DOUBLE = ctypes.c_double

SIGNED_BYTE = ctypes.c_byte
UNSIGNED_UBYTE = ctypes.c_ubyte

SIGNED_SHORT = ctypes.c_short
UNSIGNED_USHORT = ctypes.c_ushort

TIME_T = ctypes.c_time_t

CHAR = ctypes.c_char

if platform.system() == "Windows":
    WCHAR = ctypes.c_wchar
elif platform.system() == "Linux":
    WCHAR = ctypes.c_char
