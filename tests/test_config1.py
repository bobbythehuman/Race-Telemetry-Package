"""
Pytest suite for config.py: TelemetryConfig.

Run with:  pytest test_config.py -v
"""

# from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest

from ..src.RaceTelemetry.config import TelemetryConfig

# --------------------------------------------------------------------------
# Helpers / fixtures
# --------------------------------------------------------------------------


def make_metadata_cls(**overrides) -> type:
    """
    Build a throwaway metadata class. Only the attributes passed in
    `overrides` are set, so tests can check that missing attributes fall
    back to `TelemetryConfig`'s defaults.
    """
    return type("FakeMeta", (), overrides)


class HeaderPacket:
    """Stand-in for a ctypes-style header struct class."""


@pytest.fixture
def cfg():
    return TelemetryConfig()


@pytest.fixture
def full_metadata_cls():
    return make_metadata_cls(
        port=1234,
        heartBeatPort=5678,
        heartBeatFunc=lambda: "heartbeat",
        handShakePort=9999,
        handShakeFunc=(lambda: "req", lambda: "resp"),
        decryptionFunc=lambda data: data,
        headerInfo=HeaderPacket,
        packetIDAttribute="pid",
        allSharedMemoryNames={"telemetry": "Local\\Telemetry"},
        packetInfo={0: (HeaderPacket,)},
    )


# --------------------------------------------------------------------------
# 1. Happy path tests
# --------------------------------------------------------------------------


class TestInitialDefaults:
    def test_defaults(self, cfg):
        assert cfg.active_metadata is None
        assert cfg.local_ip == "0.0.0.0"
        assert cfg.destination_ip is None
        assert cfg.main_port is None
        assert cfg.heartbeat_port is None
        assert cfg.heartbeat_func is None
        assert cfg.handshake_port is None
        assert cfg.handshake_func is None
        assert cfg.decryption_func is None
        assert cfg.header_packet is None
        assert cfg.packet_id_attr is None
        assert cfg.all_shared_memory_names is None
        assert cfg.packet_info is None
        assert cfg.enum_mode == 0


class TestUpdateMeta:
    def test_update_meta_returns_true_and_sets_active_metadata(self, cfg, full_metadata_cls):
        assert cfg.update_meta(full_metadata_cls) is True
        assert cfg.active_metadata is full_metadata_cls

    def test_update_meta_unpacks_all_known_attributes(self, cfg, full_metadata_cls):
        cfg.update_meta(full_metadata_cls)

        assert cfg.main_port == 1234
        assert cfg.heartbeat_port == 5678
        assert cfg.heartbeat_func() == "heartbeat"
        assert cfg.handshake_port == 9999
        assert cfg.handshake_func[0]() == "req"
        assert cfg.handshake_func[1]() == "resp"
        assert cfg.decryption_func("x") == "x"
        assert cfg.header_packet is HeaderPacket
        assert cfg.packet_id_attr == "pid"
        assert cfg.all_shared_memory_names == {"telemetry": "Local\\Telemetry"}
        assert cfg.packet_info == {0: (HeaderPacket,)}

    def test_update_meta_with_same_class_is_a_no_op(self, cfg, full_metadata_cls, monkeypatch):
        cfg.update_meta(full_metadata_cls)

        spy = MagicMock()
        monkeypatch.setattr(cfg, "_unpack_meta_data", spy)

        result = cfg.update_meta(full_metadata_cls)

        assert result is True
        spy.assert_not_called()  # short-circuited before re-unpacking

    def test_update_meta_with_new_class_re_unpacks(self, cfg, full_metadata_cls, monkeypatch):
        cfg.update_meta(full_metadata_cls)

        spy = MagicMock()
        monkeypatch.setattr(cfg, "_unpack_meta_data", spy)

        other_cls = make_metadata_cls(port=1)
        cfg.update_meta(other_cls)

        spy.assert_called_once()
        assert cfg.active_metadata is other_cls


class TestUpdateIpAddresses:
    @pytest.mark.parametrize("ip", ["192.168.1.1", "0.0.0.0", "255.255.255.255", "10.0.0.1"])
    def test_update_local_ip_accepts_valid_ips(self, cfg, ip):
        assert cfg.update_local_ip(ip) is True
        assert cfg.local_ip == ip

    @pytest.mark.parametrize("ip", ["192.168.1.1", "8.8.8.8"])
    def test_update_send_ip_accepts_valid_ips(self, cfg, ip):
        assert cfg.update_send_ip(ip) is True
        assert cfg.destination_ip == ip


class TestSetEnumMode:
    @pytest.mark.parametrize("mode", [0, 1, 2])
    def test_valid_modes_are_accepted(self, cfg, mode):
        assert cfg.set_enum_mode(mode) is True
        assert cfg.enum_mode == mode

    def test_default_argument_sets_zero(self, cfg):
        cfg.enum_mode = 2
        assert cfg.set_enum_mode() is True
        assert cfg.enum_mode == 0


# --------------------------------------------------------------------------
# 2. Edge case tests
# --------------------------------------------------------------------------


class TestUpdateMetaEdgeCases:
    def test_missing_attributes_fall_back_to_defaults(self, cfg):
        sparse_cls = make_metadata_cls(port=42)  # everything else absent
        cfg.update_meta(sparse_cls)

        assert cfg.main_port == 42
        assert cfg.heartbeat_port is None
        assert cfg.heartbeat_func is None
        assert cfg.handshake_port is None
        assert cfg.handshake_func is None
        assert cfg.decryption_func is None
        assert cfg.header_packet is None
        assert cfg.packet_id_attr is None
        assert cfg.all_shared_memory_names is None
        assert cfg.packet_info == {}  # explicit {} default, unlike the others

    def test_completely_empty_metadata_class(self, cfg):
        empty_cls = make_metadata_cls()
        assert cfg.update_meta(empty_cls) is True
        assert cfg.packet_info == {}
        assert cfg.main_port is None

    def test_update_meta_with_none_is_treated_as_new_metadata_once(self, cfg, monkeypatch):
        # active_metadata starts as None, so calling update_meta(None) hits
        # the "== active_metadata" branch immediately (None == None).
        spy = MagicMock()
        monkeypatch.setattr(cfg, "_unpack_meta_data", spy)
        result = cfg.update_meta(None)

        assert result is True
        spy.assert_not_called()
        assert cfg.active_metadata is None


class TestIpEdgeCases:
    @pytest.mark.parametrize(
        "ip",
        [
            "256.1.1.1",  # octet out of range
            "999.999.999.999",
            "1.1.1.",  # trailing dot, missing last octet
            "1.1.1.1.1",  # too many octets
            "192.168.1",  # too few octets
            "abc.def.ghi.jkl",
            "",
            "01.02.03.04",  # leading zeros rejected by the regex
            " 1.2.3.4",  # leading whitespace
            "1.2.3.4 ",  # trailing whitespace
        ],
    )
    def test_invalid_ip_formats_are_rejected(self, cfg, ip):
        assert cfg.update_local_ip(ip) is False
        assert cfg.local_ip == "0.0.0.0"  # unchanged from default

    def test_boundary_ip_255_is_valid(self, cfg):
        assert cfg._is_valid_ip("255.255.255.255") is True

    def test_boundary_ip_256_is_invalid(self, cfg):
        assert cfg._is_valid_ip("256.255.255.255") is False

    def test_update_local_ip_does_not_overwrite_on_failure(self, cfg):
        cfg.update_local_ip("10.0.0.5")
        assert cfg.update_local_ip("not-an-ip") is False
        assert cfg.local_ip == "10.0.0.5"

    def test_update_send_ip_stays_none_on_failure(self, cfg):
        assert cfg.update_send_ip("garbage") is False
        assert cfg.destination_ip is None


class TestSetEnumModeEdgeCases:
    @pytest.mark.parametrize("bad_mode", [-1, 3, 100])
    def test_out_of_range_int_rejected(self, cfg, bad_mode):
        assert cfg.set_enum_mode(bad_mode) is False
        assert cfg.enum_mode == 0  # unchanged

    def test_failed_update_does_not_change_existing_mode(self, cfg):
        cfg.set_enum_mode(1)
        assert cfg.set_enum_mode(99) is False
        assert cfg.enum_mode == 1


# --------------------------------------------------------------------------
# 3. Error handling tests
# --------------------------------------------------------------------------


class TestTypeValidationErrors:
    @pytest.mark.parametrize("bad_ip", [123, None, 1.5, [], {}, ("1", "2", "3", "4")])
    def test_update_local_ip_rejects_non_string_types(self, cfg, bad_ip, caplog):
        with caplog.at_level(logging.WARNING):
            result = cfg.update_local_ip(bad_ip)
        assert result is False
        assert "must be a" in caplog.text.lower()

    @pytest.mark.parametrize("bad_ip", [123, None, 1.5, []])
    def test_update_send_ip_rejects_non_string_types(self, cfg, bad_ip):
        assert cfg.update_send_ip(bad_ip) is False

    @pytest.mark.parametrize("bad_mode", ["0", None, 1.0, [0], True])
    def test_set_enum_mode_rejects_non_int_types(self, cfg, bad_mode):
        # NOTE: bool is a subclass of int in Python, so `True`/`False` will
        # actually pass isinstance(value, int) -- this test documents that
        # `True` is accepted as `1`, which is a real gotcha in the API.
        result = cfg.set_enum_mode(bad_mode)
        if isinstance(bad_mode, bool):
            assert result is True
            assert cfg.enum_mode == int(bad_mode)
        else:
            assert result is False

    def test_meta_data_check_returns_default_when_active_metadata_is_none(self, cfg):
        assert cfg._meta_data_check("port", "fallback") == "fallback"

    def test_meta_data_check_returns_default_when_attribute_missing(self, cfg, full_metadata_cls):
        cfg.active_metadata = full_metadata_cls
        assert cfg._meta_data_check("doesNotExist", "fallback") == "fallback"

    def test_meta_data_check_returns_actual_value_when_present(self, cfg, full_metadata_cls):
        cfg.active_metadata = full_metadata_cls
        assert cfg._meta_data_check("port") == 1234


# --------------------------------------------------------------------------
# Logging behaviour
# --------------------------------------------------------------------------


class TestLogging:
    def test_invalid_ip_logs_warning_with_offending_value(self, cfg, caplog):
        with caplog.at_level(logging.WARNING):
            cfg.update_local_ip("999.999.999.999")
        assert "invalid ip address" in caplog.text.lower()
        assert "999.999.999.999" in caplog.text

    def test_invalid_enum_mode_logs_warning(self, cfg, caplog):
        with caplog.at_level(logging.WARNING):
            cfg.set_enum_mode(7)
        assert "enum mode" in caplog.text.lower()


# --------------------------------------------------------------------------
# 4. Integration test: a realistic end-to-end config setup
# --------------------------------------------------------------------------


class TestIntegrationRealisticSetup:
    def test_typical_startup_sequence(self, cfg, full_metadata_cls):
        assert cfg.update_meta(full_metadata_cls) is True
        assert cfg.update_local_ip("192.168.0.10") is True
        assert cfg.update_send_ip("192.168.0.20") is True
        assert cfg.set_enum_mode(1) is True

        assert cfg.active_metadata is full_metadata_cls
        assert cfg.local_ip == "192.168.0.10"
        assert cfg.destination_ip == "192.168.0.20"
        assert cfg.enum_mode == 1
        assert cfg.packet_info == {0: (HeaderPacket,)}


# --------------------------------------------------------------------------
# 5. Lightweight performance smoke test
# --------------------------------------------------------------------------


class TestPerformance:
    def test_many_ip_validations_complete_quickly(self, cfg):
        import time

        start = time.perf_counter()
        for i in range(10_000):
            cfg._is_valid_ip(f"192.168.{i % 256}.{(i * 3) % 256}")
        elapsed = time.perf_counter() - start

        assert elapsed < 2.0
