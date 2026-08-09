"""
Pytest suite for router.py: PacketRouter.

IMPORTANT — package layout:
`router.py` uses a relative import (`from .digestion import dynamic_ingest`)
and a `RaceTelemetry.main` reference under TYPE_CHECKING, so it must live
inside a package. Place this test file so that the following exists:

    RaceTelemetry/
        __init__.py
        router.py        <- the file under test
        config.py         <- TelemetryConfig (used for the integration tests)
        digestion.py       <- must exist at runtime; see stub below if you
                               don't already have a real implementation
    test_router.py         <- this file, next to the RaceTelemetry/ folder

If you don't have a real `digestion.py` yet, this minimal stub is enough to
run these tests (they monkeypatch `dynamic_ingest` directly in most cases
anyway, so the real implementation's behaviour isn't required):

    # RaceTelemetry/digestion.py
    def dynamic_ingest(raw_packet, enum_mode=0):
        return raw_packet

Run with:  pytest test_router.py -v
"""

# from __future__ import annotations

import ctypes
import logging
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ..src.RaceTelemetry.router import PacketRouter

# from RaceTelemetry.router import PacketRouter

# --------------------------------------------------------------------------
# ctypes packet structures used across the suite
# --------------------------------------------------------------------------


class HeaderStruct(ctypes.Structure):
    _fields_ = [("pid", ctypes.c_uint8)]  # size 1


class SmallPacket(ctypes.Structure):
    _fields_ = [("value", ctypes.c_uint16)]  # size 2


class BigPacket(ctypes.Structure):
    _fields_ = [("value", ctypes.c_uint32)]  # size 4


class SameSizeAsSmallA(ctypes.Structure):
    _fields_ = [("a", ctypes.c_uint16)]  # size 2


class SameSizeAsSmallB(ctypes.Structure):
    _fields_ = [("b", ctypes.c_int16)]  # size 2


class EmptyPacket(ctypes.Structure):
    _fields_ = []  # size 0


class CombinedPacket(ctypes.Structure):
    _fields_ = [("raw", ctypes.c_uint8 * 3)]  # size 3 == 1-byte header + 2-byte payload


class NotACtypesStruct:
    """A plain class -- not a ctypes.Structure -- to trigger TypeError paths."""


# --------------------------------------------------------------------------
# Helpers / fixtures
# --------------------------------------------------------------------------


def make_config(**overrides) -> SimpleNamespace:
    """
    Build a minimal duck-typed config object. PacketRouter only touches a
    handful of attributes, so a SimpleNamespace is sufficient and keeps
    these as true unit tests independent of TelemetryConfig.
    """
    defaults = dict(
        active_metadata=None,
        packet_info=None,
        header_packet=None,
        packet_id_attr=None,
        enum_mode=0,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.fixture
def identity_ingest(monkeypatch):
    """Replace dynamic_ingest with a pass-through so raw ctypes structs
    flow straight through unchanged -- convenient for most tests."""

    def _identity(raw_packet, enum_mode=0):
        return raw_packet

    monkeypatch.setattr("RaceTelemetry.src.RaceTelemetry.router.dynamic_ingest", _identity)
    return _identity


@pytest.fixture
def router(identity_ingest):
    cfg = make_config()
    return PacketRouter(cfg)


# --------------------------------------------------------------------------
# 1. Happy path tests
# --------------------------------------------------------------------------


class TestInit:
    def test_init_stores_config(self):
        cfg = make_config()
        r = PacketRouter(cfg)
        assert r.config is cfg

    def test_init_logs_metadata_name_when_present(self, caplog):
        cfg = make_config(active_metadata=HeaderStruct)
        with caplog.at_level(logging.DEBUG):
            PacketRouter(cfg)
        assert "HeaderStruct" in caplog.text

    def test_init_logs_none_when_no_metadata(self, caplog):
        cfg = make_config(active_metadata=None)
        with caplog.at_level(logging.DEBUG):
            PacketRouter(cfg)
        # should not raise, and should not crash trying to read .__name__ on None


class TestGetPacketSize:
    @pytest.mark.parametrize(
        "struct, expected_size",
        [(HeaderStruct, 1), (SmallPacket, 2), (BigPacket, 4), (EmptyPacket, 0)],
    )
    def test_returns_correct_ctypes_size(self, router, struct, expected_size):
        assert router.get_packet_size(struct) == expected_size


class TestGetMaxPacketSize:
    def test_returns_largest_size_across_all_packet_ids(self, router):
        router.config.packet_info = {
            0: (SmallPacket,),
            1: (BigPacket, HeaderStruct),
        }
        assert router.get_max_packet_size() == 4

    def test_single_packet_struct(self, router):
        router.config.packet_info = {0: (HeaderStruct,)}
        assert router.get_max_packet_size() == 1


class TestConstructPacket:
    def test_matches_correct_struct_by_size(self, router):
        data = bytes([0x34, 0x12])  # 2 bytes -> matches SmallPacket
        packet = router.construct_packet(data, (SmallPacket, BigPacket))

        assert isinstance(packet, SmallPacket)
        assert packet.value == 0x1234  # little-endian

    def test_matches_second_struct_when_first_size_mismatches(self, router):
        data = bytes([0x01, 0x00, 0x00, 0x00])  # 4 bytes -> matches BigPacket
        packet = router.construct_packet(data, (SmallPacket, BigPacket))

        assert isinstance(packet, BigPacket)
        assert packet.value == 1

    def test_calls_dynamic_ingest_with_raw_packet_and_enum_mode(self, router, monkeypatch):
        sentinel = object()
        mock_ingest = MagicMock(return_value=sentinel)
        monkeypatch.setattr("RaceTelemetry.src.RaceTelemetry.router.dynamic_ingest", mock_ingest)
        router.config.enum_mode = 2

        data = bytes([0x01, 0x00])
        result = router.construct_packet(data, (SmallPacket,))

        assert result is sentinel
        args, kwargs = mock_ingest.call_args
        assert isinstance(args[0], SmallPacket)
        assert args[1] == 2


class TestRetrievePacket:
    def test_full_happy_path_with_header(self, router):
        """
        NOTE on a real quirk in retrieve_packet: it calls
        `self.construct_packet(data, possiblePacketStruct)` with the FULL
        `data` buffer -- it never slices off the header bytes first. That
        means packet-size matching (and decoding) happens against
        len(header + payload), not len(payload) alone, and the decoded
        struct's first byte(s) will actually be the header byte(s), not
        the start of the payload. This test documents that current
        (likely unintended) behaviour rather than the "payload only"
        behaviour you might expect from the method's docstring/intent.
        """
        router.config.packet_id_attr = "pid"
        router.config.header_packet = HeaderStruct  # 1 byte
        router.config.packet_info = {7: (CombinedPacket,)}  # 3 bytes = header + payload

        header_bytes = bytes([7])
        payload_bytes = bytes([0x0A, 0x0B])
        data = header_bytes + payload_bytes  # 3 bytes total

        packet, packet_id, header_packet = router.retrieve_packet(data)

        assert packet_id == 7
        assert isinstance(header_packet, HeaderStruct)
        assert header_packet.pid == 7

        # The "payload" struct actually decoded the WHOLE buffer, header
        # byte included -- this is the quirk being documented.
        assert isinstance(packet, CombinedPacket)
        assert bytes(packet.raw) == data

    def test_no_header_packet_defaults_id_to_zero(self, router):
        router.config.header_packet = None
        router.config.packet_info = {0: (SmallPacket,)}

        data = bytes([0x02, 0x00])
        packet, packet_id, header_packet = router.retrieve_packet(data)

        assert packet_id == 0
        assert header_packet is None
        assert isinstance(packet, SmallPacket)


# --------------------------------------------------------------------------
# 2. Edge case tests
# --------------------------------------------------------------------------


class TestConstructPacketEdgeCases:
    def test_no_struct_matches_data_length_returns_none(self, router, caplog):
        data = bytes([0x01, 0x02, 0x03])  # length 3, no struct is size 3
        with caplog.at_level(logging.WARNING):
            packet = router.construct_packet(data, (SmallPacket, BigPacket))

        assert packet is None
        assert "no matching packet size" in caplog.text.lower()

    def test_empty_possible_struct_tuple_returns_none(self, router, caplog):
        with caplog.at_level(logging.WARNING):
            packet = router.construct_packet(b"\x00\x00", ())
        assert packet is None

    def test_first_matching_size_wins_when_multiple_structs_share_a_size(self, router):
        data = bytes([0x01, 0x00])  # 2 bytes matches both same-size structs
        packet = router.construct_packet(data, (SameSizeAsSmallA, SameSizeAsSmallB))
        # Order in the tuple determines which one is tried (and succeeds) first.
        assert isinstance(packet, SameSizeAsSmallA)

    def test_empty_data_with_only_nonzero_size_structs_returns_none(self, router):
        packet = router.construct_packet(b"", (SmallPacket, BigPacket))
        assert packet is None

    def test_empty_data_matches_zero_size_struct(self, router):
        packet = router.construct_packet(b"", (EmptyPacket,))
        assert isinstance(packet, EmptyPacket)

    def test_size_match_but_unpack_raises_value_error_is_skipped(self, router, monkeypatch, caplog):
        """
        Documents a real quirk: if a struct's size matches the data length
        but `from_buffer_copy` still raises ValueError, that struct is
        silently skipped via `continue` -- but because the size *did*
        match, it was never added to `packetSizes`. That means the final
        `len(possiblePacketStruct) == len(packetSizes)` check can't be
        true here, so no "no matching packet size" warning is logged even
        though `packet` stays `None`.
        """

        def raising_from_buffer_copy(cls, data):
            raise ValueError("simulated corrupt buffer")

        monkeypatch.setattr(SmallPacket, "from_buffer_copy", classmethod(raising_from_buffer_copy))

        with caplog.at_level(logging.WARNING):
            packet = router.construct_packet(bytes([0x01, 0x00]), (SmallPacket,))

        assert packet is None
        assert "no matching packet size" not in caplog.text.lower()


class TestGetMaxPacketSizeEdgeCases:
    def test_all_zero_size_structs_returns_zero(self, router):
        router.config.packet_info = {0: (EmptyPacket,)}
        assert router.get_max_packet_size() == 0

    def test_packet_info_with_empty_tuple_for_an_id(self, router):
        router.config.packet_info = {0: (), 1: (SmallPacket,)}
        assert router.get_max_packet_size() == 2


class TestRetrievePacketEdgeCases:
    def test_header_packet_missing_id_attribute_defaults_to_zero(self, router, caplog):
        router.config.header_packet = HeaderStruct
        router.config.packet_id_attr = "doesNotExist"
        router.config.packet_info = {0: (SmallPacket,)}

        data = bytes([7]) + bytes([0x01, 0x00])
        with caplog.at_level(logging.WARNING):
            packet, packet_id, header_packet = router.retrieve_packet(data)

        assert packet_id == 0
        assert "doesn" in caplog.text.lower() or "id attribute" in caplog.text.lower()

    def test_packet_id_not_registered_returns_none_packet(self, router, caplog):
        router.config.header_packet = HeaderStruct
        router.config.packet_id_attr = "pid"
        router.config.packet_info = {1: (SmallPacket,)}  # only ID 1 registered

        data = bytes([99]) + bytes([0x01, 0x00])  # header says ID 99
        with caplog.at_level(logging.WARNING):
            packet, packet_id, header_packet = router.retrieve_packet(data)

        assert packet is None
        assert packet_id == 99
        assert "id not found" in caplog.text.lower()

    def test_packet_info_maps_id_to_empty_tuple(self, router):
        # `.get(packetID)` returns `()`, which is falsy -> treated like "not found"
        router.config.header_packet = None
        router.config.packet_info = {0: ()}

        packet, packet_id, header_packet = router.retrieve_packet(b"\x01\x00")
        assert packet is None
        assert packet_id == 0


# --------------------------------------------------------------------------
# 3. Error handling tests
# --------------------------------------------------------------------------


class TestErrorHandling:
    def test_get_max_packet_size_raises_on_empty_packet_info(self, router):
        router.config.packet_info = {}
        with pytest.raises(ValueError):
            router.get_max_packet_size()

    def test_get_max_packet_size_raises_on_none_packet_info(self, router):
        router.config.packet_info = None
        with pytest.raises(ValueError):
            router.get_max_packet_size()

    def test_retrieve_packet_raises_on_empty_packet_info(self, router):
        router.config.packet_info = {}
        with pytest.raises(ValueError):
            router.retrieve_packet(b"\x00")

    def test_retrieve_packet_raises_when_header_present_but_no_id_attr(self, router):
        router.config.header_packet = HeaderStruct
        router.config.packet_id_attr = None
        router.config.packet_info = {0: (SmallPacket,)}

        with pytest.raises(ValueError):
            router.retrieve_packet(bytes([0]) + b"\x00\x00")

    def test_retrieve_packet_propagates_error_when_data_too_short_for_header(self, router):
        """
        There's no guard rail here: `from_buffer_copy` on a header struct
        raises ValueError uncaught if `data` is shorter than the header
        itself. This documents that callers must ensure a minimum buffer
        length before calling `retrieve_packet`.
        """
        router.config.header_packet = BigPacket  # needs 4 bytes
        router.config.packet_id_attr = "value"
        router.config.packet_info = {0: (SmallPacket,)}

        with pytest.raises(ValueError):
            router.retrieve_packet(b"\x01")  # only 1 byte supplied

    def test_get_packet_size_raises_type_error_for_non_ctypes_class(self, router):
        with pytest.raises(TypeError):
            router.get_packet_size(NotACtypesStruct)


# --------------------------------------------------------------------------
# 4. Integration tests: PacketRouter driven by a real TelemetryConfig
# --------------------------------------------------------------------------


class TestIntegrationWithTelemetryConfig:
    def test_router_end_to_end_using_real_config(self, identity_ingest):
        from ..src.RaceTelemetry.config import TelemetryConfig

        # NOTE: as documented in TestRetrievePacket.test_full_happy_path_with_header,
        # retrieve_packet matches/decodes against the FULL buffer (header
        # included), so the registered struct must be sized for
        # header + payload, not payload alone.
        metadata_cls = type(
            "FakeMeta",
            (),
            {
                "headerInfo": HeaderStruct,  # 1 byte
                "packetIDAttribute": "pid",
                "packetInfo": {3: (CombinedPacket, BigPacket)},  # 3 bytes, 4 bytes
            },
        )

        cfg = TelemetryConfig()
        cfg.update_meta(metadata_cls)

        r = PacketRouter(cfg)
        data = bytes([3]) + bytes([0x2C, 0x01])  # header id=3, "payload" bytes

        packet, packet_id, header_packet = r.retrieve_packet(data)

        assert packet_id == 3
        assert isinstance(packet, CombinedPacket)
        assert bytes(packet.raw) == data
        assert r.get_max_packet_size() == 4  # BigPacket is the largest registered struct


# --------------------------------------------------------------------------
# 5. Lightweight performance smoke test
# --------------------------------------------------------------------------


class TestPerformance:
    def test_many_retrieve_packet_calls_complete_quickly(self, router):
        import time

        router.config.header_packet = HeaderStruct
        router.config.packet_id_attr = "pid"
        router.config.packet_info = {5: (SmallPacket,)}
        data = bytes([5]) + bytes([0x01, 0x00])

        start = time.perf_counter()
        for _ in range(5_000):
            router.retrieve_packet(data)
        elapsed = time.perf_counter() - start

        assert elapsed < 3.0
