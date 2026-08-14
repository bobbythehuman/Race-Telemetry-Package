"""
Pattern-level tests that apply to every `<GAME>_struct.py` module.

MetaData should follow the same pattern across every game,
while the packet data structures themselves are game-specific.
"""

from __future__ import annotations

import ctypes
from typing import Iterable
from collections.abc import Callable

import pytest

# import BNG_struct
# import ETS2_struct
# import F1_2019_struct
# import GT7_struct
from ..src.RaceTelemetry.DataStructures import *

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
    # pytest.param(PC_UDP_MetaData, id="PC_UDP"),
    # pytest.param(PC2_MetaData, id="PC2"),
]


# ---------------------------------------------------------------------------
# MetaData shape
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module", MODULES)
class TestMetaDataPattern:
    """Every module's MetaData must expose the same attributes with the same
    broad types, since the transport layer (UDPTransport/SharedMemoryTransport)
    reads these generically without knowing which game it's talking to."""

    def test_has_all_expected_attributes(self, module):
        meta = module
        expected_attrs = {
            "port",
            "heartBeatPort",
            "heartBeatFunc",
            "handShakePort",
            "handShakeFunc",
            "decryptionFunc",
            "headerInfo",
            "packetIDAttribute",
            "allSharedMemoryNames",
            "packetInfo",
        }
        missing = expected_attrs - set(vars(meta))
        assert not missing, f"MetaData is missing expected attributes: {missing}"

    def test_port_is_int_or_none(self, module):
        assert module.port is None or isinstance(module.port, int)

    def test_heartbeat_port_and_func_are_consistent_types(self, module):
        meta = module
        assert meta.heartBeatPort is None or isinstance(meta.heartBeatPort, int)
        assert meta.heartBeatFunc is None or isinstance(meta.heartBeatFunc, Callable)

    def test_handshake_func_is_none_or_a_pair_of_callables(self, module):
        handShakeFunc = module.handShakeFunc
        if handShakeFunc is None:
            return
        assert isinstance(handShakeFunc, tuple)
        assert len(handShakeFunc) == 2
        assert all(isinstance(f, Callable) for f in handShakeFunc)

    def test_decryption_func_is_none_or_callable(self, module):
        decryptionFunc = module.decryptionFunc
        assert decryptionFunc is None or isinstance(decryptionFunc, Callable)

    def test_header_info_and_packet_id_attribute_travel_together(self, module):
        """If a header type is declared, the packetIDAttribute must actually
        exist on it (and vice versa - no dangling attribute name without a
        header type to look it up on)."""
        meta = module
        if meta.headerInfo is None:
            assert meta.packetIDAttribute is None
            return

        assert isinstance(meta.packetIDAttribute, str) and meta.packetIDAttribute
        assert is_ctypes_struct_or_union(meta.headerInfo)
        assert meta.packetIDAttribute in field_names(meta.headerInfo), (
            f"packetIDAttribute {meta.packetIDAttribute!r} is not a field on " f"headerInfo {meta.headerInfo.__name__}"
        )

    def test_shared_memory_names_is_none_str_or_dict(self, module):
        names = module.allSharedMemoryNames
        assert names is None or isinstance(names, (str, dict))

    def test_packet_info_is_a_dict_of_int_to_tuple_of_struct_types(self, module):
        packetInfo = module.packetInfo
        assert isinstance(packetInfo, dict)
        assert packetInfo, "packetInfo should not be empty"

        for packet_id, structs in packetInfo.items():
            assert isinstance(packet_id, int)
            assert isinstance(structs, tuple)
            assert structs, f"packetInfo[{packet_id}] has no structs"
            for struct_cls in structs:
                assert is_ctypes_struct_or_union(struct_cls), (
                    f"packetInfo[{packet_id}] contains {struct_cls!r}, " "which is not a ctypes Structure/Union"
                )


# ---------------------------------------------------------------------------
# Structure sanity (applies to every struct referenced from packetInfo)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module", MODULES)
class TestPacketStructSanity:
    def test_every_referenced_struct_is_instantiable(self, module):
        for struct_cls in all_packet_structs(module):
            instance = struct_cls()  # should zero-initialise without raising
            assert instance is not None

    def test_every_referenced_struct_has_positive_size(self, module):
        for struct_cls in all_packet_structs(module):
            assert ctypes.sizeof(struct_cls) > 0

    def test_every_referenced_struct_has_at_least_one_field(self, module):
        for struct_cls in all_packet_structs(module):
            assert len(struct_cls._fields_) > 0, f"{struct_cls.__name__} has no fields"

    def test_no_duplicate_field_names(self, module):
        """
        A field name declared twice in `_fields_` silently shadows the
        earlier one at the class-attribute level (see
        struct_test_utils.duplicate_field_names). Both copies still occupy
        space in the wire layout, but only the *last* one is ever readable
        by name - the earlier field becomes a dead byte range nobody can see.
        This is real data loss for whichever field got shadowed, so it's
        treated as a hard failure rather than a warning.
        """
        offenders = {}
        for struct_cls in all_packet_structs(module):
            dupes = duplicate_field_names(struct_cls)
            if dupes:
                offenders[struct_cls.__name__] = dupes
        assert not offenders, "Duplicate field name(s) found - the earlier field(s) are " f"silently unreadable: {offenders}"

    def test_enums_dict_only_references_real_field_names(self, module):
        """`_enums_` is a hint to downstream code about which fields should be
        interpreted as a particular Enum/Flag. If it references a field name
        that was renamed or removed, that's a silent bug - this test catches it."""
        for struct_cls in all_packet_structs(module):
            enums = getattr(struct_cls, "_enums_", None)
            if not enums:
                continue
            declared_fields = set(field_names(struct_cls))
            for enum_type, names in enums.items():
                for name in names:
                    assert name in declared_fields, (
                        f"{struct_cls.__name__}._enums_ references field "
                        f"{name!r} for {enum_type.__name__}, but that field "
                        f"doesn't exist in _fields_"
                    )

    def test_packed_structs_have_no_padding_gaps(self, module):
        """Any struct explicitly opting into `_pack_ = 1` should genuinely be
        byte-packed with no alignment gaps between fields.

        Structs with duplicate field names are skipped here - offset lookup
        by name is meaningless for a shadowed field, and that defect is
        already reported (more precisely) by test_no_duplicate_field_names.
        """
        for struct_cls in all_packet_structs(module):
            if getattr(struct_cls, "_pack_", None) == 1 and not duplicate_field_names(struct_cls):
                assert_no_padding_gaps(struct_cls)

    def test_field_offsets_are_monotonically_non_decreasing(self, module):
        """Regardless of packing, fields must appear in the byte layout in
        the same order they're declared in _fields_ - a shuffled field would
        otherwise pass every other check silently.

        Structs with duplicate field names are skipped for the same reason
        as above.
        """
        for struct_cls in all_packet_structs(module):
            if duplicate_field_names(struct_cls):
                continue
            offsets = [getattr(struct_cls, name).offset for name in field_names(struct_cls)]
            assert offsets == sorted(offsets), f"{struct_cls.__name__} fields are not laid out in " "declaration order"


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


def field_names(struct_cls: type) -> list[str]:
    """Return the declared field names of a ctypes Structure/Union."""
    return [name for name, *_ in struct_cls._fields_]


def field_offset(struct_cls: type, name: str) -> int:
    """Byte offset of a named field, via the class-level ctypes descriptor."""
    return getattr(struct_cls, name).offset


def assert_no_padding_gaps(struct_cls: type) -> None:
    """
    For a structure declared with `_pack_ = 1`, fields are laid out back to
    back with no alignment padding. This walks `_fields_` in order and
    verifies each field's real offset equals the running total of the sizes
    of the fields before it - i.e. nothing silently shifted due to a type
    change introducing alignment padding despite `_pack_ = 1` being set.
    """
    assert getattr(struct_cls, "_pack_", None) == 1, (
        f"{struct_cls.__name__} is not declared with _pack_ = 1; " "this check only makes sense for packed structures."
    )
    running_offset = 0
    for name, field_type, *_ in struct_cls._fields_:
        actual = field_offset(struct_cls, name)
        assert actual == running_offset, (
            f"{struct_cls.__name__}.{name}: expected offset {running_offset}, "
            f"got {actual} (unexpected gap/overlap of {actual - running_offset} bytes)"
        )
        running_offset += ctypes.sizeof(field_type)


def duplicate_field_names(struct_cls: type) -> set[str]:
    """
    Names that appear more than once in `_fields_`.

    ctypes silently allows this: each entry still consumes its own bytes in
    the layout, but the *class attribute* for that name ends up pointing at
    whichever entry was declared last - so the earlier field(s) become
    permanently unreadable/unwritable by name (`instance.name` always
    resolves to the last declaration). This is almost never intentional.
    """
    names = field_names(struct_cls)
    seen, dupes = set(), set()
    for name in names:
        if name in seen:
            dupes.add(name)
        seen.add(name)
    return dupes


def all_packet_structs(meta_data_cls: type) -> Iterable[type]:
    """Flatten every struct/union type referenced by MetaData.packetInfo."""
    seen = set()
    for structs in meta_data_cls.packetInfo.values():
        for struct_cls in structs:
            if struct_cls not in seen:
                seen.add(struct_cls)
                yield struct_cls


def is_ctypes_struct_or_union(obj: object) -> bool:
    return isinstance(obj, type) and issubclass(obj, (ctypes.Structure, ctypes.Union, ctypes.LittleEndianStructure, ctypes.BigEndianStructure))
