"""
Test suite for digestion.py

Run with:
    pip install pytest --break-system-packages   # if not already installed
    pytest test_digestion.py -v
"""

import ctypes
import enum
from typing import Any
import pytest

from ..src.RaceTelemetry.digestion import (
    newChrToString,
    unpackArray,
    applyEnum,
    dynamic_ingest,
)
from .test_resources import (
    testPacket1,
    testPacket2,
    metaData,
    SubPacket,
    FullPacket,
    full_packet_byte,
    full_unpacked_packet,
    SubHeaderPacket,
    HeaderPacket,
    header_packet_byte,
    header_unpacked_packet,
)

# ---------------------------------------------------------------------------
# newChrToString
# ---------------------------------------------------------------------------


class TestNewChrToString:

    def test_extra_true_splits_on_first_null(self):
        raw = b"hello\x00world\x00"
        assert newChrToString(raw, extra=True) == "hello"

    def test_extra_false_stripped_ends_only(self):
        raw = b"hello\x00world\x00"
        # strip("\0") only removes leading/trailing nulls, not embedded ones
        assert newChrToString(raw, extra=False) == "hello\x00world"

    def test_no_null_bytes(self):
        raw = b"plain text"
        assert newChrToString(raw, extra=True) == "plain text"
        assert newChrToString(raw, extra=False) == "plain text"

    def test_ctypes_char_array_input(self):
        buf = ctypes.create_string_buffer(b"abc", 10)  # 'abc' + null padding
        assert newChrToString(buf.raw, extra=True) == "abc"


# ---------------------------------------------------------------------------
# unpackArray
# ---------------------------------------------------------------------------


class TestUnpackArray:

    def test_char_array_becomes_string(self):
        arr = (ctypes.c_char * 10)(*b"hi\x00\x00\x00\x00\x00\x00\x00\x00")
        result = unpackArray(arr)
        assert result == "hi"

    def test_int_array_becomes_list(self):
        arr = (ctypes.c_int * 4)(1, 2, 3, 4)
        assert unpackArray(arr) == [1, 2, 3, 4]

    def test_float_array_rounded(self):
        arr = (ctypes.c_float * 2)(1.123456789, 2.0)
        result = unpackArray(arr)
        assert result[1] == 2.0
        assert result[0] == round(result[0], 5)  # already rounded, no more than 5dp
        assert abs(result[0] - 1.12346) < 1e-4

    def test_nested_ctypes_array(self):
        Inner = ctypes.c_int * 2
        arr = (Inner * 2)((1, 2), (3, 4))
        assert unpackArray(arr) == [[1, 2], [3, 4]]

    def test_array_of_bytes_elements(self):
        # array whose *elements* are individual bytes objects (e.g. char arrays nested
        # inside a struct array) rather than the array itself being a char array
        class Small(ctypes.Structure):
            _fields_ = [("name", ctypes.c_char * 4)]

        arr = (Small * 2)((b"ab\x00\x00",), (b"cd\x00\x00",))
        result = unpackArray(arr)
        # each element is a Structure -> goes through dynamic_ingest branch
        assert result[0].name == "ab"
        assert result[1].name == "cd"


# ---------------------------------------------------------------------------
# applyEnum
# ---------------------------------------------------------------------------


class Colour(enum.IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2


class Tire(enum.StrEnum):
    FRONT_LEFT = "FL"
    FRONT_RIGHT = "FR"
    REAR_LEFT = "RL"
    REAR_RIGHT = "RR"


class Button(enum.Flag):
    NONE = 0
    A = 1
    B = 2
    C = 4
    D = 8


class TestApplyEnum:

    @pytest.mark.parametrize(
        "operand1, operand2, operand3, expected",
        [
            (5, None, 0, 5),
            (5, None, 1, 5),
            (5, None, 2, 5),
            ("FL", None, 0, "FL"),
            ("FL", None, 1, "FL"),
            ("FL", None, 2, "FL"),
        ],
    )
    def test_no_enum_type_returns_value_unchanged(
        self,
        operand1: Any,
        operand2: Any,
        operand3: Any,
        expected: Any,
    ):
        assert applyEnum(operand1, operand2, enumMode=operand3) == expected

    @pytest.mark.parametrize(
        "operand1, operand2, operand3, expected",
        [
            (1, Colour, 0, Colour.GREEN),
            (2, Colour, 0, Colour.BLUE),
            ("FL", Tire, 0, Tire.FRONT_LEFT),
            ("RR", Tire, 0, Tire.REAR_RIGHT),
            (2, Button, 0, Button.B),
            (8, Button, 0, Button.D),
            (6, Button, 0, Button.B | Button.C),
        ],
    )
    def test_enum_mode_0_returns_enum_member(
        self,
        operand1: Any,
        operand2: Any,
        operand3: Any,
        expected: Any,
    ):
        assert applyEnum(operand1, operand2, enumMode=operand3) == expected

    @pytest.mark.parametrize(
        "operand1, operand2, operand3, expected",
        [
            (1, Colour, 1, 1),
            (2, Colour, 1, 2),
            ("FL", Tire, 1, "FL"),
            ("RR", Tire, 1, "RR"),
            (2, Button, 1, 2),
            (8, Button, 1, 8),
            (6, Button, 1, 6),
        ],
    )
    def test_enum_mode_1_returns_enum_value(
        self,
        operand1: Any,
        operand2: Any,
        operand3: Any,
        expected: Any,
    ):
        assert applyEnum(operand1, operand2, enumMode=operand3) == expected

    @pytest.mark.parametrize(
        "operand1, operand2, operand3, expected",
        [
            (1, Colour, 2, "GREEN"),
            (2, Colour, 2, "BLUE"),
            ("FL", Tire, 2, "FRONT_LEFT"),
            ("RR", Tire, 2, "REAR_RIGHT"),
            (2, Button, 2, "B"),
            (8, Button, 2, "D"),
            (6, Button, 2, "B|C"),
        ],
    )
    def test_enum_mode_2_returns_enum_name(
        self,
        operand1: Any,
        operand2: Any,
        operand3: Any,
        expected: Any,
    ):
        assert applyEnum(operand1, operand2, enumMode=operand3) == expected

    @pytest.mark.parametrize(
        "operand1, operand2, operand3, expected",
        [
            (-1, Colour, 0, -1),
            (-1, Colour, 1, -1),
            (-1, Colour, 2, -1),
            (99, Colour, 0, 99),
            (99, Colour, 1, 99),
            (99, Colour, 2, 99),
            ("Red", Colour, 0, "Red"),
            ("Red", Colour, 1, "Red"),
            ("Red", Colour, 2, "Red"),
            ("FF", Tire, 0, "FF"),
            ("FF", Tire, 1, "FF"),
            ("FF", Tire, 2, "FF"),
            (3, Tire, 0, 3),
            (3, Tire, 1, 3),
            (3, Tire, 2, 3),
            (16, Button, 0, 16),
            (16, Button, 1, 16),
            (16, Button, 2, 16),
            (20, Button, 0, 20),
            (20, Button, 1, 20),
            (20, Button, 2, 20),
            ("A", Button, 0, "A"),
            ("A", Button, 1, "A"),
            ("A", Button, 2, "A"),
        ],
    )
    def test_invalid_value_falls_back_to_original(
        self,
        operand1: Any,
        operand2: Any,
        operand3: Any,
        expected: Any,
    ):
        assert applyEnum(operand1, operand2, enumMode=operand3) == expected


# ---------------------------------------------------------------------------
# dynamic_ingest
# ---------------------------------------------------------------------------


class TestDynamicIngest:

    def test_plain_fields(self):
        class Simple(ctypes.Structure):
            _fields_ = [
                ("a", ctypes.c_int),
                ("b", ctypes.c_float),
                ("name", ctypes.c_char * 8),
            ]

        p = Simple(a=42, b=3.14159265, name=b"bob")
        result = dynamic_ingest(p)

        assert result.a == 42
        assert result.b == round(3.14159265, 5)
        assert result.name == "bob"

    def test_nested_struct(self):
        class Inner(ctypes.Structure):
            _fields_ = [("x", ctypes.c_int)]

        class Outer(ctypes.Structure):
            _fields_ = [("inner", Inner), ("y", ctypes.c_int)]

        p = Outer(inner=Inner(x=7), y=9)
        result = dynamic_ingest(p)

        assert result.y == 9
        assert result.inner.x == 7

    def test_ctypes_array_field(self):
        class WithArray(ctypes.Structure):
            _fields_ = [("values", ctypes.c_int * 3)]

        p = WithArray(values=(ctypes.c_int * 3)(1, 2, 3))
        result = dynamic_ingest(p)
        assert result.values == [1, 2, 3]

    def test_enum_mapping_single_field(self):
        class WithEnum(ctypes.Structure):
            _fields_ = [("colour", ctypes.c_int)]
            _enums_ = {Colour: ["colour"]}

        p = WithEnum(colour=2)
        result = dynamic_ingest(p, enumMode=2)
        assert result.colour == "BLUE"

    def test_enum_mapping_on_list_field(self):
        class WithEnumArray(ctypes.Structure):
            _fields_ = [("colours", ctypes.c_int * 2)]
            _enums_ = {Colour: ["colours"]}

        p = WithEnumArray(colours=(ctypes.c_int * 2)(0, 1))
        result = dynamic_ingest(p, enumMode=2)
        assert result.colours == ["RED", "GREEN"]

    def test_multiple_enum_types_for_same_attr_raises(self):
        class Shape(enum.IntEnum):
            SQUARE = 0
            CIRCLE = 1

        class Conflicting(ctypes.Structure):
            _fields_ = [("value", ctypes.c_int)]
            # both Colour and Shape claim "value" -> ambiguous
            _enums_ = {Colour: ["value"], Shape: ["value"]}

        p = Conflicting(value=0)
        with pytest.raises(ValueError, match="Multiple enum types found"):
            dynamic_ingest(p)

    def test_bool_and_str_passthrough(self):
        # bool/str aren't ctypes field types directly usable this simply in all
        # versions, so we simulate via a class exposing the same _fields_/getattr
        # contract dynamic_ingest relies on, without requiring real ctypes typing.
        class FakePacket:
            _fields_ = [("flag",), ("label",)]
            flag = True
            label = "already-a-string"

        result = dynamic_ingest(FakePacket())
        assert result.flag is True
        assert result.label == "already-a-string"

    def test_none_passthrough(self):
        class WithNone(ctypes.Structure):
            _fields_ = [("ptr", ctypes.c_void_p)]

        p = WithNone(ptr=None)
        result = dynamic_ingest(p)
        assert result.ptr is None

    def test_full_packet_ingestion(self):
        result1 = dynamic_ingest(full_unpacked_packet, enumMode=0)
        result2 = dynamic_ingest(header_unpacked_packet, enumMode=0)


result1 = dynamic_ingest(full_unpacked_packet, enumMode=0)
result2 = dynamic_ingest(header_unpacked_packet, enumMode=0)


class TestFullPacketIngestion:

    def test_full_packet_boolean(self):
        assert result1.flag is True

    def test_full_packet_signed_integers(self):
        assert result1.byte_val == -12
        assert result1.short_val == -1000
        assert result1.int_val == -100000
        assert result1.long_val == -123456
        assert result1.longlong_val == -1234567890123
        assert result1.ssize_val == -42

    def test_full_packet_unsigned_integers(self):
        assert result1.ubyte_val == 200
        assert result1.ushort_val == 40000
        assert result1.uint_val == 3000000000
        assert result1.ulong_val == 123456
        assert result1.ulonglong_val == 12345678901234
        assert result1.size_val == 999

    def test_full_packet_explicitly_sized_integers(self):
        assert result1.int8_val == -5
        assert result1.uint8_val == 250
        assert result1.int16_val == -30000
        assert result1.uint16_val == 60000
        assert result1.int32_val == -2000000000
        assert result1.uint32_val == 4000000000
        assert result1.int64_val == -9000000000000000000
        assert result1.uint64_val == 18000000000000000000

    def test_full_packet_floats(self):
        assert result1.float_val == 3.14159
        assert result1.double_val == 2.71828
        assert result1.longdouble_val == 1.41421

    def test_full_packet_characters(self):
        assert result1.char_val == "Z"
        assert result1.wchar_val == "W"
        assert result1.char_arr == "hello"
        assert result1.wchar_arr == "hi"

    def test_full_packet_arrays(self):
        assert result1.int_arr == [10, 20, 30, 40]

    def test_full_packet_nested_structures(self):
        assert result1.nested.sub_id == 7
        assert result1.nested.sub_flag == True
        assert result1.nested_arr[0].sub_id == 1
        assert result1.nested_arr[0].sub_flag == False
        assert result1.nested_arr[1].sub_id == 2
        assert result1.nested_arr[1].sub_flag == True

    def test_full_packet_bitfields(self):
        assert result1.bit_a == 5
        assert result1.bit_b == 17
        assert result1.bit_c == 12345

    def test_full_packet_pointer_fields(self):
        assert result1.void_ptr == None
        assert result1.char_ptr == None
        assert result1.wchar_ptr == None

    def test_header_packet_fields(self):
        assert result2.header.header_id == 1
        assert result2.header.packetNum == 28


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
    # --disable-warnings
