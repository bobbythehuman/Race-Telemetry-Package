"""
Comprehensive PyTest suite for digestion.py

Covers:
    - new_byte_to_string
    - unpack_array
    - apply_enum
    - dynamic_ingest
    - _inverse_enums (indirectly, via dynamic_ingest)

Test types included: unit tests (happy path, edge case, error handling).
No network/database/external services are involved in this module, so no
integration/performance/mocking-of-externals sections are required - the
module is pure in-memory data transformation over ctypes structures.
"""

import ctypes
import logging
from enum import Enum
from types import SimpleNamespace

import pytest

from src.RaceTelemetry.digestion import (
    new_byte_to_string,
    unpack_array,
    apply_enum,
    dynamic_ingest,
    _inverse_enums,
)

# ===========================================================================
# Shared fixtures / helper ctypes structures & enums
# ===========================================================================


class Colour(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


class Status(Enum):
    OK = 0
    FAIL = 1


class SimplePacket(ctypes.Structure):
    """A flat packet with no nested structures and no enums."""

    _fields_ = [
        ("id", ctypes.c_int),
        ("ratio", ctypes.c_float),
        ("name", ctypes.c_char * 8),
        ("flag", ctypes.c_bool),
    ]


class EnumPacket(ctypes.Structure):
    """A packet that declares an _enums_ mapping for one of its fields."""

    _fields_ = [
        ("colour", ctypes.c_int),
        ("value", ctypes.c_int),
    ]
    _enums_ = {Colour: ["colour"]}


class MultiEnumPacket(ctypes.Structure):
    """A packet where two different enum types both claim the same field name."""

    _fields_ = [
        ("state", ctypes.c_int),
    ]
    _enums_ = {Colour: ["state"], Status: ["state"]}


class NestedPacket(ctypes.Structure):
    """A packet containing another Structure as a field."""

    _fields_ = [
        ("inner", SimplePacket),
        ("count", ctypes.c_int),
    ]


class ArrayPacket(ctypes.Structure):
    """A packet containing plain numeric arrays and a nested-array-of-structs."""

    _fields_ = [
        ("numbers", ctypes.c_int * 4),
        ("floats", ctypes.c_float * 3),
        ("matrix", (ctypes.c_int * 2) * 2),
    ]


class StructArrayPacket(ctypes.Structure):
    """A packet containing an array of nested Structures."""

    _fields_ = [
        ("items", SimplePacket * 2),
    ]


class NoFieldsPacket:
    """Deliberately NOT a ctypes.Structure - lacks `_fields_` entirely."""

    def __init__(self):
        self.name = "orphan"


# ===========================================================================
# new_byte_to_string
# ===========================================================================


class TestNewByteToString:
    """Happy path + edge cases for byte -> string conversion."""

    def test_simple_bytes_no_padding(self):
        assert new_byte_to_string(b"hello") == "hello"

    def test_strips_trailing_null_padding(self):
        # Typical ctypes fixed-length char array padded with nulls.
        assert new_byte_to_string(b"hello\x00\x00\x00") == "hello"

    def test_split_on_null_true_cuts_at_first_null(self):
        # Null in the middle: strip() only removes from the ends, so the
        # function must explicitly split on the first remaining null.
        assert new_byte_to_string(b"hello\x00world\x00", split_on_null=True) == "hello"

    def test_split_on_null_false_keeps_middle_null(self):
        # With split_on_null=False, only leading/trailing nulls are stripped;
        # any null in the middle is preserved verbatim.
        result = new_byte_to_string(b"hello\x00world\x00", split_on_null=False)
        assert result == "hello\x00world"

    def test_empty_bytes_returns_empty_string(self):
        assert new_byte_to_string(b"") == ""

    def test_all_null_bytes_returns_empty_string(self):
        assert new_byte_to_string(b"\x00\x00\x00\x00") == ""

    def test_leading_null_bytes_are_stripped(self):
        assert new_byte_to_string(b"\x00\x00foo") == "foo"

    def test_invalid_utf8_uses_replacement_character(self):
        # 0xFF is not valid UTF-8 on its own; errors="replace" should kick in
        # rather than raising UnicodeDecodeError.
        result = new_byte_to_string(b"\xffabc")
        assert "\ufffd" in result
        assert result.endswith("abc")

    def test_accepts_ctypes_array_as_input(self):
        # The function does `bytes(value)` first, so a ctypes char array
        # should work identically to a raw bytes object.
        arr = (ctypes.c_char * 8)(*b"hi\x00\x00\x00\x00\x00\x00")
        assert new_byte_to_string(arr) == "hi"


# ===========================================================================
# unpack_array
# ===========================================================================


class TestUnpackArray:
    """Happy path + edge cases for ctypes array -> list/str conversion."""

    def test_empty_list_returns_empty_list(self):
        assert unpack_array([]) == []

    def test_none_returns_empty_list(self):
        assert unpack_array(None) == []

    def test_char_array_returns_string(self):
        arr = (ctypes.c_char * 6)(*b"abc\x00\x00\x00")
        assert unpack_array(arr) == "abc"

    def test_int_array_returns_list_of_ints(self):
        arr = (ctypes.c_int * 4)(1, 2, 3, 4)
        assert unpack_array(arr) == [1, 2, 3, 4]

    def test_float_array_values_are_rounded(self):
        arr = (ctypes.c_float * 2)(1.0000001, 2.123456789)
        result = unpack_array(arr)
        assert result == [round(1.0000001, 5), round(2.123456789, 5)]

    def test_bool_array_values_pass_through(self):
        arr = (ctypes.c_bool * 3)(True, False, True)
        assert unpack_array(arr) == [True, False, True]

    def test_nested_array_is_recursively_unpacked(self):
        # (c_int * 2) * 2 -> list of lists
        arr = ((ctypes.c_int * 2) * 2)((1, 2), (3, 4))
        assert unpack_array(arr) == [[1, 2], [3, 4]]

    def test_array_of_structures_calls_dynamic_ingest(self):
        packet = StructArrayPacket()
        packet.items[0].id = 1
        packet.items[0].name = b"a"
        packet.items[1].id = 2
        packet.items[1].name = b"b"

        result = unpack_array(packet.items)

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, SimpleNamespace) for item in result)
        assert result[0].id == 1
        assert result[1].id == 2

    def test_single_element_array(self):
        arr = (ctypes.c_int * 1)(42)
        assert unpack_array(arr) == [42]

    def test_plain_python_list_of_ints_passthrough(self):
        # unpack_array is written generically enough to accept a plain list.
        assert unpack_array([1, 2, 3]) == [1, 2, 3]

    def test_plain_python_list_with_bytes_elements(self):
        # A regular (non-ctypes) list whose FIRST element is NOT bytes takes
        # the per-item path, so any later bytes element is converted
        # individually via new_byte_to_string rather than the whole-array
        # path (which only triggers when packet[0] itself is bytes).
        assert unpack_array([1, b"foo\x00bar"]) == [1, "foo"]

    def test_list_whose_first_element_is_bytes_treats_whole_list_as_bytes(self):
        # When packet[0] is bytes, unpack_array assumes the ENTIRE packet
        # represents a byte string (as with a ctypes char array) and calls
        # new_byte_to_string directly on it - this only works for something
        # bytes()-constructible, i.e. a real ctypes char array in practice.
        arr = (ctypes.c_char * 4)(*b"hi\x00\x00")
        assert unpack_array(arr) == "hi"


# ===========================================================================
# apply_enum
# ===========================================================================


class TestApplyEnum:
    """Happy path + edge cases for enum resolution."""

    def test_no_enum_type_returns_value_unchanged(self):
        assert apply_enum(99, None, enumMode=0) == 99

    def test_enum_mode_0_returns_enum_member(self):
        assert apply_enum(1, Colour, enumMode=0) is Colour.GREEN

    def test_enum_mode_1_returns_underlying_value(self):
        assert apply_enum(1, Colour, enumMode=1) == 1

    def test_enum_mode_2_returns_member_name(self):
        assert apply_enum(1, Colour, enumMode=2) == "GREEN"

    def test_invalid_enum_value_logs_warning_and_returns_original(self, caplog):
        # 99 is not a member of Colour - the function should swallow the
        # ValueError, log a warning, and return the raw value untouched.
        with caplog.at_level(logging.WARNING):
            result = apply_enum(99, Colour, enumMode=0)
        assert result == 99
        assert "not a valid enum member" in caplog.text

    def test_unrecognised_enum_mode_leaves_value_untouched(self):
        # enumMode values other than 0/1/2 fall through all branches with no
        # conversion applied at all (not even an enum lookup attempt).
        assert apply_enum(1, Colour, enumMode=5) == 1

    @pytest.mark.parametrize(
        "enum_mode,expected",
        [
            (0, Colour.RED),
            (1, 0),
            (2, "RED"),
        ],
    )
    def test_enum_modes_parametrized(self, enum_mode, expected):
        assert apply_enum(0, Colour, enumMode=enum_mode) == expected


# ===========================================================================
# _inverse_enums
# ===========================================================================


class TestInverseEnums:
    """Tests for the cached reverse enum-name lookup helper."""

    def test_builds_reverse_mapping_from_enums_attribute(self):
        inverse = _inverse_enums(EnumPacket)
        assert inverse == {"colour": [Colour]}

    def test_class_without_enums_attribute_returns_empty_dict(self):
        assert _inverse_enums(SimplePacket) == {}

    def test_result_is_cached_between_calls(self):
        # lru_cache means repeated calls for the same class return the
        # identical (same id) object rather than rebuilding it.
        first = _inverse_enums(EnumPacket)
        second = _inverse_enums(EnumPacket)
        assert first is second

    def test_multiple_enum_types_for_same_field_are_both_recorded(self):
        inverse = _inverse_enums(MultiEnumPacket)
        assert set(inverse["state"]) == {Colour, Status}


# ===========================================================================
# dynamic_ingest
# ===========================================================================


class TestDynamicIngest:
    """Happy path + edge cases for full packet -> SimpleNamespace ingestion."""

    def test_flat_packet_all_field_types(self):
        packet = SimplePacket(id=42, ratio=1.23456789, name=b"abc", flag=True)
        result = dynamic_ingest(packet)

        assert isinstance(result, SimpleNamespace)
        assert result.__name__ == "SimplePacket"
        assert result.id == 42
        assert result.ratio == round(1.23456789, 5)
        assert result.name == "abc"
        assert result.flag is True

    def test_packet_without_fields_attribute_logs_error_and_returns_stub(self, caplog):
        with caplog.at_level(logging.ERROR):
            result = dynamic_ingest(NoFieldsPacket())

        # Only __name__ should be set - no other attributes are copied over.
        assert result.__name__ == "NoFieldsPacket"
        assert not hasattr(result, "name")
        assert "doesnt contain a _field_ attribute" in caplog.text

    def test_enum_field_is_resolved_to_enum_member_by_default(self):
        packet = EnumPacket(colour=1, value=5)
        result = dynamic_ingest(packet)
        assert result.colour is Colour.GREEN
        assert result.value == 5

    def test_enum_field_respects_enum_mode_argument(self):
        packet = EnumPacket(colour=2, value=0)
        result = dynamic_ingest(packet, enumMode=2)
        assert result.colour == "BLUE"

    def test_invalid_enum_value_on_a_field_is_kept_as_raw_int(self, caplog):
        packet = EnumPacket(colour=999, value=0)
        with caplog.at_level(logging.WARNING):
            result = dynamic_ingest(packet)
        assert result.colour == 999

    def test_multiple_enum_types_for_one_field_raises_value_error(self):
        packet = MultiEnumPacket(state=0)
        with pytest.raises(ValueError, match="Multiple enum types found"):
            dynamic_ingest(packet)

    def test_nested_structure_field_is_recursively_ingested(self):
        packet = NestedPacket(count=3)
        packet.inner.id = 7
        packet.inner.name = b"nested"

        result = dynamic_ingest(packet)

        assert result.count == 3
        assert isinstance(result.inner, SimpleNamespace)
        assert result.inner.id == 7
        assert result.inner.name == "nested"

    def test_array_fields_are_unpacked_via_unpack_array(self):
        packet = ArrayPacket()
        packet.numbers[:] = [1, 2, 3, 4]
        packet.floats[:] = [1.111111, 2.222222, 3.333333]
        packet.matrix[0][:] = [1, 2]
        packet.matrix[1][:] = [3, 4]

        result = dynamic_ingest(packet)

        assert result.numbers == [1, 2, 3, 4]
        assert result.floats == [round(1.111111, 5), round(2.222222, 5), round(3.333333, 5)]
        assert result.matrix == [[1, 2], [3, 4]]

    def test_array_of_structures_is_ingested_as_list_of_namespaces(self):
        packet = StructArrayPacket()
        packet.items[0].id = 1
        packet.items[0].name = b"a"
        packet.items[1].id = 2
        packet.items[1].name = b"b"

        result = dynamic_ingest(packet)

        assert isinstance(result.items, list)
        assert len(result.items) == 2
        assert result.items[0].id == 1
        assert result.items[1].id == 2

    def test_enum_applied_across_list_of_values(self):
        # When a field with an _enums_ mapping resolves to a *list* (e.g. it
        # came from an array), each element should individually be passed
        # through apply_enum.
        class EnumArrayPacket(ctypes.Structure):
            _fields_ = [("colours", ctypes.c_int * 3)]
            _enums_ = {Colour: ["colours"]}

        packet = EnumArrayPacket()
        packet.colours[:] = [0, 1, 2]

        result = dynamic_ingest(packet)

        assert result.colours == [Colour.RED, Colour.GREEN, Colour.BLUE]

    def test_two_independent_packets_do_not_leak_state(self):
        # Regression-style test: ingesting one packet shouldn't mutate or
        # leave stray attributes on another separately-created namespace.
        p1 = SimplePacket(id=1, name=b"one")
        p2 = SimplePacket(id=2, name=b"two")

        r1 = dynamic_ingest(p1)
        r2 = dynamic_ingest(p2)

        assert r1.id == 1 and r1.name == "one"
        assert r2.id == 2 and r2.name == "two"
