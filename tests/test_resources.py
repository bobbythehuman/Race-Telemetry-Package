import ctypes
import enum
from tracemalloc import stop

# ---------------------------------------------------------------------------
# CentralStorage
# ---------------------------------------------------------------------------

class testPacket1(ctypes.Structure):  # 4 bytes
    _fields_ = [
        ("field1", ctypes.c_int),
    ]


class testPacket2(ctypes.Structure):  # 8 bytes
    _fields_ = [
        ("field2", ctypes.c_float),
        ("field3", ctypes.c_bool),
    ]


# ---------------------------------------------------------------------------
# TelemetryManager - Tests for the __construct_packet method
# ---------------------------------------------------------------------------

class SubPacket(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("sub_id", ctypes.c_uint16),
        ("sub_flag", ctypes.c_bool),
    ]


class FullPacket(ctypes.LittleEndianStructure):
    _pack_ = 1  # no padding, so the byte layout is fully deterministic
    _fields_ = [
        # --- booleans ---
        ("flag", ctypes.c_bool),
        # --- signed integers ---
        ("byte_val", ctypes.c_byte),
        ("short_val", ctypes.c_short),
        ("int_val", ctypes.c_int),
        ("long_val", ctypes.c_long),
        ("longlong_val", ctypes.c_longlong),
        ("ssize_val", ctypes.c_ssize_t),
        # --- unsigned integers ---
        ("ubyte_val", ctypes.c_ubyte),
        ("ushort_val", ctypes.c_ushort),
        ("uint_val", ctypes.c_uint),
        ("ulong_val", ctypes.c_ulong),
        ("ulonglong_val", ctypes.c_ulonglong),
        ("size_val", ctypes.c_size_t),
        # --- explicitly-sized ints (aliases, but worth including) ---
        ("int8_val", ctypes.c_int8),
        ("uint8_val", ctypes.c_uint8),
        ("int16_val", ctypes.c_int16),
        ("uint16_val", ctypes.c_uint16),
        ("int32_val", ctypes.c_int32),
        ("uint32_val", ctypes.c_uint32),
        ("int64_val", ctypes.c_int64),
        ("uint64_val", ctypes.c_uint64),
        # --- floating point ---
        ("float_val", ctypes.c_float),
        ("double_val", ctypes.c_double),
        ("longdouble_val", ctypes.c_longdouble),
        # --- characters ---
        ("char_val", ctypes.c_char),  # single byte
        ("wchar_val", ctypes.c_wchar),  # single wide char, size varies
        ("char_arr", ctypes.c_char * 8),  # fixed-size byte string field
        ("wchar_arr", ctypes.c_wchar * 8),  # fixed-size wide-string field
        # --- arrays of a primitive type ---
        ("int_arr", ctypes.c_int * 4),
        # --- nested structure, and an array of nested structures ---
        ("nested", SubPacket),
        ("nested_arr", SubPacket * 2),
        # --- bitfields (packed into the backing c_uint32) ---
        ("bit_a", ctypes.c_uint32, 3),
        ("bit_b", ctypes.c_uint32, 5),
        ("bit_c", ctypes.c_uint32, 24),
        # --- pointers: included for completeness only, see note above ---
        ("void_ptr", ctypes.c_void_p),
        ("char_ptr", ctypes.c_char_p),
        ("wchar_ptr", ctypes.c_wchar_p),
    ]

full_packet_byte = b"\x01\xf4\x18\xfc`y\xfe\xff\xc0\x1d\xfe\xff5\xfb\x04\x8e\xe0\xfe\xff\xff\xd6\xff\xff\xff\xff\xff\xff\xff\xc8@\x9c\x00^\xd0\xb2@\xe2\x01\x00\xf2/\xces:\x0b\x00\x00\xe7\x03\x00\x00\x00\x00\x00\x00\xfb\xfa\xd0\x8a`\xea\x00l\xca\x88\x00(k\xee\x00\x00|\x1d\xaf\x93\x19\x83\x00\x00\x08\xc5\xa1\xd8\xcc\xf9\xd0\x0fI@iW\x14\x8b\n\xbf\x05@Z\x05\x7ff\x9e\xa0\xf6?ZW\x00hello\x00\x00\x00h\x00i\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x14\x00\x00\x00\x1e\x00\x00\x00(\x00\x00\x00\x07\x00\x01\x01\x00\x00\x02\x00\x01\x8d90\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

full_unpacked_packet = FullPacket.from_buffer_copy(full_packet_byte)

# ---------------------------------------------------------------------------
# TelemetryManager - Tests for the __retrieve_packet method
# ---------------------------------------------------------------------------


class SubHeaderPacket(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("header_id", ctypes.c_ushort),
        ("packetNum", ctypes.c_ushort),
    ]


class HeaderPacket(ctypes.LittleEndianStructure):
    _pack_ = 1  # no padding, so the byte layout is fully deterministic
    _fields_ = [
        # --- booleans ---
        ("header", SubHeaderPacket),
        ("flag", ctypes.c_bool),
        # --- signed integers ---
        ("byte_val", ctypes.c_byte),
        ("short_val", ctypes.c_short),
        ("int_val", ctypes.c_int),
        ("long_val", ctypes.c_long),
        ("longlong_val", ctypes.c_longlong),
        ("ssize_val", ctypes.c_ssize_t),
        # --- unsigned integers ---
        ("ubyte_val", ctypes.c_ubyte),
        ("ushort_val", ctypes.c_ushort),
        ("uint_val", ctypes.c_uint),
        ("ulong_val", ctypes.c_ulong),
        ("ulonglong_val", ctypes.c_ulonglong),
        ("size_val", ctypes.c_size_t),
    ]


header_packet_byte = b"\x01\x00\x1c\x00\x01\xf4\x18\xfc`y\xfe\xff\xc0\x1d\xfe\xff5\xfb\x04\x8e\xe0\xfe\xff\xff\xd6\xff\xff\xff\xff\xff\xff\xff\xc8@\x9c\x00^\xd0\xb2@\xe2\x01\x00\xf2/\xces:\x0b\x00\x00\xe7\x03\x00\x00\x00\x00\x00\x00"

subheader_unpacked_packet = SubHeaderPacket.from_buffer_copy(header_packet_byte[0:8])
header_unpacked_packet = HeaderPacket.from_buffer_copy(header_packet_byte)


class metaData:
    port = 1234
    packetIDAttribute = "packetID"

    headerInfo: type | None = SubHeaderPacket
    packetIDAttribute: str | None = "header_id"

    packetInfo: dict[int, tuple[type, ...]] = {
        0: (testPacket1, testPacket2),
        1: (HeaderPacket,),
    }

# ---------------------------------------------------------------------------
# TelemetryManager - Tests for addWorkerThread method
# ---------------------------------------------------------------------------

def func1():
    print("FUNC1")
    
def func2(argInput):
    pass

def func3(worker_id, ro_storage, stop_event):
    print(worker_id)
    a = ro_storage
    b = stop_event

def func4(worker_id, ro_storage, stop_event, argInput):
    pass

class workerClass:
    def workerFunc(self):
        pass