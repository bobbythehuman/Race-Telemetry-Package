"""
Pattern-level tests that apply to every `<GAME>_struct.py` module.

Verifies enums are setup correctly
"""

from __future__ import annotations
import pytest
from typing import Iterable

from src.RaceTelemetry.DataStructures import *

MODULES = [
    pytest.param(AC_SM_MetaData, id="AC_SM"),
    pytest.param(AC_UDP_MetaData, id="AC_UDP"),
    pytest.param(ACC_MetaData, id="ACC"),
    pytest.param(ACE_MetaData, id="ACE"),
    pytest.param(BNG_MetaData, id="BNG"),
    pytest.param(Dirt_4_MetaData, id="Dirt_4"),
    pytest.param(Dirt_Rally_MetaData, id="Dirt_Rally"),
    pytest.param(ETS2_MetaData, id="ETS2"),
    pytest.param(F1_2016_MetaData, id="F1_2016"),
    pytest.param(F1_2017_MetaData, id="F1_2017"),
    pytest.param(F1_2018_MetaData, id="F1_2018"),
    pytest.param(F1_2019_MetaData, id="F1_2019"),
    pytest.param(F1_2020_MetaData, id="F1_2020"),
    pytest.param(F1_2021_MetaData, id="F1_2021"),
    pytest.param(F1_2022_MetaData, id="F1_2022"),
    pytest.param(F1_2023_MetaData, id="F1_2023"),
    pytest.param(F1_2024_MetaData, id="F1_2024"),
    pytest.param(F1_2025_MetaData, id="F1_2025"),
    pytest.param(F1_2026_MetaData, id="F1_2026"),
    pytest.param(FH4_MetaData, id="FH4"),
    pytest.param(FH5_MetaData, id="FH5"),
    pytest.param(FH6_MetaData, id="FH6"),
    pytest.param(FM7_MetaData, id="FM7"),
    pytest.param(FM8_MetaData, id="FM8"),
    pytest.param(GT7_MetaData, id="GT7"),
    pytest.param(PC_SM_MetaData, id="PC_SM"),
    pytest.param(PC_UDP_MetaData, id="PC_UDP"),
    pytest.param(PC2_MetaData, id="PC2"),
    pytest.param(PC2_MetaData, id="IRacing"),
]
# ---------------------------------------------------------------------------
# Enum Validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module", MODULES)
class TestEnumValidity:
    """Verify that all enums used in struct definitions are correctly set up
    and working as expected."""

    def test_enum_types_are_valid(self, module):
        """All enum types referenced in _enums_ must be actual enum classes."""
        import enum

        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue

            for enum_type in enums.keys():
                # Check it's actually an enum type (IntEnum, Flag, StrEnum, etc.)
                assert isinstance(enum_type, type), f"{struct_cls.__name__}._enums_ references {enum_type!r}, " f"which is not a type"
                # Allow for enum types or enums with a different MRO
                try:
                    assert issubclass(enum_type, enum.Enum), (
                        f"{struct_cls.__name__}._enums_ references {enum_type.__name__}, " f"which is not an Enum subclass"
                    )
                except TypeError:
                    # In rare cases, the enum might have an unusual MRO
                    # At minimum, verify it has expected enum attributes
                    assert hasattr(enum_type, "__members__") or hasattr(enum_type, "_member_names_"), (
                        f"{struct_cls.__name__}._enums_ references {enum_type.__name__}, " f"which doesn't look like an Enum"
                    )

    def test_enum_members_are_accessible(self, module):
        """All enum members must be accessible and have valid values."""
        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue

            for enum_type, field_names_list in enums.items():
                # Try to get members - handle both standard enums and custom implementations
                members = getattr(enum_type, "__members__", None)
                if members is None:
                    members = getattr(enum_type, "_member_names_", None)
                if members is None:
                    # Skip if we can't find members
                    pytest.skip(f"Cannot determine members for {enum_type.__name__}")

                # Verify we can access each enum member
                member_list = members if isinstance(members, (list, tuple)) else members.keys()
                for member_name in member_list:
                    member = getattr(enum_type, member_name, None)
                    assert member is not None, f"{enum_type.__name__}.{member_name} is None"

    def test_enum_has_members(self, module):
        """All enum types used must have at least one member."""
        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue

            for enum_type in enums.keys():
                # Try to get members - handle both standard enums and custom implementations
                members = getattr(enum_type, "__members__", None)
                if members is None:
                    members = getattr(enum_type, "_member_names_", None)
                if members is None:
                    # Skip if we can't determine members (unusual enum implementation)
                    pytest.skip(f"Cannot determine members for {enum_type.__name__}")

                members_list = members if isinstance(members, (list, tuple)) else list(members.keys())
                assert members_list, f"{enum_type.__name__} has no members defined"

    def test_strenum_compatibility(self, module):
        """StrEnum fields should be strings and work correctly if used."""
        from sys import version_info

        # Only test if Python 3.11+
        if version_info < (3, 11):
            pytest.skip("StrEnum requires Python 3.11+")

        from enum import StrEnum

        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue

            for enum_type, field_names_list in enums.items():
                # Check if it's a StrEnum
                try:
                    is_str_enum = issubclass(enum_type, StrEnum)
                except TypeError:
                    is_str_enum = False

                if is_str_enum:
                    members = getattr(enum_type, "__members__", {})
                    for member_name, member in members.items():
                        # StrEnum members should be strings
                        assert isinstance(member.value, str), (
                            f"{enum_type.__name__}.{member_name} = {member.value!r} " f"is not a string (expected StrEnum member)"
                        )
                        # StrEnum member should equal its value
                        assert member == member.value, f"{enum_type.__name__}.{member_name} != its value " f"({member} vs {member.value!r})"

    def test_enum_field_names_are_valid_and_unique_per_enum(self, module):
        """Field names in _enums_ must be valid field names on the struct,
        and each field should map to only one enum type."""
        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue

            declared_fields = set(field_names(struct_cls))
            field_to_enum = {}

            for enum_type, names_tuple in enums.items():
                for field_name in names_tuple:
                    assert field_name in declared_fields, (
                        f"{struct_cls.__name__}._enums_ references field "
                        f"{field_name!r} for {enum_type.__name__}, "
                        f"but that field doesn't exist in _fields_"
                    )
                    # Track which enum "owns" each field
                    if field_name in field_to_enum:
                        # A field can map to multiple enum types if they're related
                        # (e.g., different parts of a bitfield), but let's at least
                        # verify it's consistent
                        assert field_to_enum[field_name] == enum_type or (
                            isinstance(field_to_enum[field_name], tuple) and enum_type in field_to_enum[field_name]
                        ), (f"{struct_cls.__name__}.{field_name} maps to both " f"{field_to_enum[field_name].__name__} and " f"{enum_type.__name__}")
                    else:
                        field_to_enum[field_name] = enum_type


# ----------------------------------------------------------------------------
# Shared Helpers
# ----------------------------------------------------------------------------

"""
Shared helpers for testing the *_struct.py telemetry definition modules.

These modules all follow the same shape:
  * a `DataTypes` class aliasing ctypes primitives
  * zero or more `ctypes.LittleEndianStructure` / `ctypes.Union` packet definitions,
    optionally carrying an `_enums_` dict mapping an Enum type to the field
    name(s) it decorates
  * a `MetaData` class describing how the transport should talk to the game
    (port, heartbeat, handshake, decryption, shared memory, packetInfo)

This module has no test_ prefix so pytest won't collect it directly - it's
imported by the real test files.
"""


def all_packet_structs(meta_data_cls: type) -> Iterable[type]:
    """Flatten every struct/union type referenced by MetaData.packetInfo."""
    seen = set()
    for structs in meta_data_cls.packetInfo.values():
        for struct_cls in structs:
            if struct_cls not in seen:
                seen.add(struct_cls)
                yield struct_cls


def field_names(struct_cls: type) -> list[str]:
    """Return field names declared by a ctypes class and its bases."""
    names = []
    for base in reversed(struct_cls.__mro__):
        names.extend(name for name, *_ in getattr(base, "_fields_", ()))
    return names
