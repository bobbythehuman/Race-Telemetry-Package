"""
Comprehensive pytest suite for RaceTelemetry.receiver
=======================================================

Covers ``UDPReceiver`` and ``SharedMemoryReceiver`` in receivers.py.

Design notes
------------
* All I/O (sockets, mmap) and collaborators (``PacketRouter``,
  ``ThreadSupervisor``, ``TelemetryConfig``) are mocked - these tests are
  pure unit tests with no real network or shared-memory access, so they
  are fast and hermetic.
* ``config`` objects are built with ``types.SimpleNamespace`` so tests only
  need to set the attributes that matter for that scenario; everything
  else defaults to a safe "off" value.
* ``supervisor._is_still_active`` is normally driven with a
  ``side_effect`` list so loops run a known, finite number of times
  instead of spinning forever.

* Heartbeat tests verify the current ``_packet_counter`` lifecycle and the
    configured heartbeat callback without requiring a real socket.
"""

# from __future__ import annotations

import socket
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, call, patch

import pytest

from ..src.RaceTelemetry.receivers import (
    SharedMemoryReceiver,
    UDPReceiver,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def make_config(**overrides) -> SimpleNamespace:
    """Build a minimal TelemetryConfig-like object with sane 'off' defaults."""
    defaults = dict(
        local_ip="127.0.0.1",
        main_port=20777,
        destination_ip=None,
        handshake_port=20778,
        handshake_func=None,
        heartbeat_func=None,
        heartbeat_destination=None,
        decryption_func=None,
        packet_info=None,
        all_shared_memory_names=None,
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


@pytest.fixture
def supervisor():
    s = MagicMock(name="ThreadSupervisor")
    s._is_still_active.return_value = False  # default: loops don't run
    return s


@pytest.fixture
def config():
    return make_config(
        get_max_packet_size=MagicMock(return_value=1500),
        get_packet_size=MagicMock(return_value=64),
    )


@pytest.fixture
def udp_receiver(config, supervisor):
    receiver = UDPReceiver(config=config, supervisor=supervisor)
    # In real usage, retreive_packets() sets FULLBUFFERSIZE before the loop
    # ever calls _process_loop(). Tests that exercise _process_loop()
    # directly must replicate that setup step themselves.
    receiver.FULLBUFFERSIZE = 1500
    return receiver


@pytest.fixture
def sm_receiver(config, supervisor):
    return SharedMemoryReceiver(config=config, supervisor=supervisor)


# ---------------------------------------------------------------------------
# UDPReceiver.__init__
# ---------------------------------------------------------------------------


class TestUDPReceiverInit:
    def test_stores_collaborators(self, config, supervisor):
        receiver = UDPReceiver(config=config, supervisor=supervisor)

        assert receiver.config is config
        assert receiver.supervisor is supervisor

    def test_initial_state(self, udp_receiver):
        assert udp_receiver.heartBeatDestination is None
        assert udp_receiver._packet_counter == 0
        assert udp_receiver._full_buffer_size == 0

    def test_heartbeat_interval_class_constant(self):
        assert UDPReceiver.HEARTBEAT_INTERVAL == 5


# ---------------------------------------------------------------------------
# UDPReceiver.call_handshake
# ---------------------------------------------------------------------------


class TestCallHandshake:
    def test_no_handshake_func_configured_is_a_noop(self, udp_receiver):
        sock = MagicMock()
        udp_receiver.config.handshake_func = None

        udp_receiver.call_handshake(sock, "start")  # must not raise

        sock.assert_not_called()

    def test_start_mode_calls_first_handshake_function(self, udp_receiver):
        sock = MagicMock()
        start_fn, stop_fn = MagicMock(), MagicMock()
        udp_receiver.config.handshake_func = (start_fn, stop_fn)
        udp_receiver.config.destination_ip = "10.0.0.5"
        udp_receiver.config.handshake_port = 9999

        udp_receiver.call_handshake(sock, "start")

        start_fn.assert_called_once_with(sock, ("10.0.0.5", 9999))
        stop_fn.assert_not_called()

    def test_stop_mode_calls_second_handshake_function(self, udp_receiver):
        sock = MagicMock()
        start_fn, stop_fn = MagicMock(), MagicMock()
        udp_receiver.config.handshake_func = (start_fn, stop_fn)
        udp_receiver.config.destination_ip = "10.0.0.5"
        udp_receiver.config.handshake_port = 9999

        udp_receiver.call_handshake(sock, "stop")

        stop_fn.assert_called_once_with(sock, ("10.0.0.5", 9999))
        start_fn.assert_not_called()

    def test_unknown_mode_calls_neither_function(self, udp_receiver):
        sock = MagicMock()
        start_fn, stop_fn = MagicMock(), MagicMock()
        udp_receiver.config.handshake_func = (start_fn, stop_fn)
        udp_receiver.config.destination_ip = "10.0.0.5"

        udp_receiver.call_handshake(sock, "pause")  # not "start" or "stop"

        start_fn.assert_not_called()
        stop_fn.assert_not_called()


# ---------------------------------------------------------------------------
# UDPReceiver.retreive_packets
# ---------------------------------------------------------------------------


class TestGetUdpPackets:
    def test_raises_when_handshake_configured_without_destination_ip(self, udp_receiver):
        udp_receiver.config.handshake_func = (MagicMock(), MagicMock())
        udp_receiver.config.destination_ip = None

        with pytest.raises(ValueError, match="Destination IP"):
            next(udp_receiver.retreive_packets())

    def test_raises_when_heartbeat_configured_without_destination_ip(self, udp_receiver):
        udp_receiver.config.heartbeat_func = MagicMock()
        udp_receiver.config.destination_ip = None

        with pytest.raises(ValueError, match="Destination IP"):
            next(udp_receiver.retreive_packets())

    @patch("RaceTelemetry.src.RaceTelemetry.receivers.socket.socket")
    def test_happy_path_binds_handshakes_and_yields_expected_number_of_packets(self, mock_socket_cls, udp_receiver, supervisor):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        # Run the loop body exactly 3 times, then stop.
        supervisor._is_still_active.side_effect = [True, True, True, False]

        start_fn, stop_fn = MagicMock(), MagicMock()
        udp_receiver.config.handshake_func = (start_fn, stop_fn)
        udp_receiver.config.destination_ip = "10.0.0.5"

        with patch.object(udp_receiver, "_process_loop", return_value=("pkt", 1, "hdr")) as mock_loop:
            results = list(udp_receiver.retreive_packets())

        mock_socket_cls.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
        mock_sock.settimeout.assert_called_once_with(1.0)
        mock_sock.bind.assert_called_once_with(("127.0.0.1", 20777))
        assert results == [("pkt", 1, "hdr")] * 3
        assert mock_loop.call_count == 3
        start_fn.assert_called_once_with(mock_sock, ("10.0.0.5", 20778))
        stop_fn.assert_called_once_with(mock_sock, ("10.0.0.5", 20778))
        mock_sock.close.assert_called_once()

    @patch("RaceTelemetry.src.RaceTelemetry.receivers.socket.socket")
    def test_bind_failure_triggers_supervisor_stop_and_skips_loop(self, mock_socket_cls, udp_receiver, supervisor):
        mock_sock = MagicMock()
        mock_sock.bind.side_effect = OSError("Only one usage of each socket address")
        mock_socket_cls.return_value = mock_sock

        results = list(udp_receiver.retreive_packets())

        assert results == []  # generator produced nothing
        supervisor._trigger_stop.assert_called_once()
        mock_sock.close.assert_called_once()  # finally block still runs

    @patch("RaceTelemetry.src.RaceTelemetry.receivers.socket.socket")
    def test_socket_closed_even_if_never_active(self, mock_socket_cls, udp_receiver, supervisor):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        supervisor._is_still_active.return_value = False  # loop body never runs

        list(udp_receiver.retreive_packets())

        mock_sock.close.assert_called_once()

    @patch("RaceTelemetry.src.RaceTelemetry.receivers.socket.socket")
    def test_process_loop_none_is_yielded_after_timeout(self, mock_socket_cls, udp_receiver, supervisor):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock
        supervisor._is_still_active.side_effect = [True, False]
        udp_receiver._process_loop = MagicMock(return_value=None)

        results = list(udp_receiver.retreive_packets())

        assert results == [None]
        udp_receiver._process_loop.assert_called_once_with(mock_sock)
        mock_sock.close.assert_called_once()


# ---------------------------------------------------------------------------
# UDPReceiver._process_loop
# ---------------------------------------------------------------------------


class TestProcessLoop:
    """
    Note: ``_process_loop`` reads ``self.FULLBUFFERSIZE``, which is only
    ever set inside ``retreive_packets`` (never in ``__init__``). The
    ``udp_receiver`` fixture sets it manually so these tests can call
    ``_process_loop`` in isolation, mirroring what ``retreive_packets``
    would have done before entering its loop.
    """

    def test_raises_if_heartbeat_func_not_callable(self, udp_receiver):
        udp_receiver.config.heartbeat_func = "not-a-function"
        sock = MagicMock()

        with pytest.raises(ValueError, match="Heart Beat Function"):
            udp_receiver._process_loop(sock)

    def test_raises_if_decryption_func_not_callable(self, udp_receiver):
        udp_receiver.config.decryption_func = "not-a-function"
        sock = MagicMock()
        sock.recvfrom.return_value = (b"data", ("1.2.3.4", 1000))

        with pytest.raises(ValueError, match="Decryption Function"):
            udp_receiver._process_loop(sock)

    def test_normal_packet_returns_raw_data(self, udp_receiver):
        sock = MagicMock()
        sock.recvfrom.return_value = (b"\x01\x02", ("1.2.3.4", 1000))

        result = udp_receiver._process_loop(sock)

        assert result == b"\x01\x02"

    def test_decryption_func_returns_decrypted_data(self, udp_receiver):
        sock = MagicMock()
        sock.recvfrom.return_value = (b"cipher", ("1.2.3.4", 1000))
        udp_receiver.config.decryption_func = MagicMock(return_value=b"plain")

        result = udp_receiver._process_loop(sock)

        udp_receiver.config.decryption_func.assert_called_once_with(b"cipher")
        assert result == b"plain"

    def test_timeout_without_heartbeat_returns_no_data(self, udp_receiver):
        sock = MagicMock()
        sock.recvfrom.side_effect = TimeoutError

        result = udp_receiver._process_loop(sock)

        assert result is None

    def test_keyboard_interrupt_triggers_stop_and_returns_no_data(self, udp_receiver, supervisor):
        sock = MagicMock()
        sock.recvfrom.side_effect = KeyboardInterrupt

        result = udp_receiver._process_loop(sock)

        supervisor._trigger_stop.assert_called_once()
        assert result is None

    def test_os_error_triggers_stop_and_returns_no_data(self, udp_receiver, supervisor):
        sock = MagicMock()
        sock.recvfrom.side_effect = OSError("boom")

        result = udp_receiver._process_loop(sock)

        supervisor._trigger_stop.assert_called_once()
        assert result is None


class TestProcessLoopHeartbeat:
    def test_heartbeat_configured_tracks_packets_without_attribute_error(self, udp_receiver):
        udp_receiver.config.heartbeat_func = MagicMock()
        sock = MagicMock()
        sock.recvfrom.return_value = (b"data", ("1.2.3.4", 1000))

        result = udp_receiver._process_loop(sock)

        assert result == b"data"
        assert udp_receiver._packet_counter == 1
        udp_receiver.config.heartbeat_func.assert_not_called()

    def test_heartbeat_on_timeout_resets_packet_counter(self, udp_receiver):
        udp_receiver._packet_counter = 4
        udp_receiver.config.heartbeat_func = MagicMock()
        sock = MagicMock()
        sock.recvfrom.side_effect = TimeoutError

        result = udp_receiver._process_loop(sock)

        udp_receiver.config.heartbeat_func.assert_called_with(sock, udp_receiver.heartBeatDestination)
        assert udp_receiver._packet_counter == 0
        assert result is None


# ---------------------------------------------------------------------------
# SharedMemoryReceiver.__init__
# ---------------------------------------------------------------------------


class TestSharedMemoryTransportInit:
    def test_stores_collaborators(self, config, supervisor):
        receiver = SharedMemoryReceiver(config=config, supervisor=supervisor)

        assert receiver.config is config
        assert receiver.supervisor is supervisor


# ---------------------------------------------------------------------------
# SharedMemoryReceiver.connect_map
# ---------------------------------------------------------------------------


class TestConnectMap:
    @patch("RaceTelemetry.src.RaceTelemetry.receivers.mmap.mmap")
    def test_without_struct_uses_max_packet_size(self, mock_mmap_cls, sm_receiver, config):
        mock_map = MagicMock()
        mock_mmap_cls.return_value = mock_map

        result = sm_receiver.connect_map("MyMap")

        config.get_max_packet_size.assert_called_once()
        config.get_packet_size.assert_not_called()
        mock_mmap_cls.assert_called_once_with(-1, 1500, tagname="MyMap", access=ANY)
        assert result == {mock_map: 1500}

    @patch("RaceTelemetry.src.RaceTelemetry.receivers.mmap.mmap")
    def test_with_struct_uses_packet_size_for_that_struct(self, mock_mmap_cls, sm_receiver, config):
        mock_map = MagicMock()
        mock_mmap_cls.return_value = mock_map

        class DummyPacket:
            pass

        result = sm_receiver.connect_map("MyMap", DummyPacket)

        config.get_packet_size.assert_called_once_with(DummyPacket)
        config.get_max_packet_size.assert_not_called()
        mock_mmap_cls.assert_called_once_with(-1, 64, tagname="MyMap", access=ANY)
        assert result == {mock_map: 64}


# ---------------------------------------------------------------------------
# SharedMemoryReceiver.setup_maps
# ---------------------------------------------------------------------------


class TestSetupMaps:
    def test_raises_if_packet_info_missing(self, sm_receiver):
        sm_receiver.config.packet_info = None

        with pytest.raises(ValueError, match="Packet Info"):
            sm_receiver.setup_maps("AnyName")

    def test_raises_if_packet_info_empty_dict(self, sm_receiver):
        sm_receiver.config.packet_info = {}

        with pytest.raises(ValueError, match="Packet Info"):
            sm_receiver.setup_maps("AnyName")

    def test_string_name_calls_connect_map_once(self, sm_receiver):
        sm_receiver.config.packet_info = {1: []}  # merely needs to be truthy

        with patch.object(sm_receiver, "connect_map", return_value={"MAP": 100}) as mock_connect:
            result = sm_receiver.setup_maps("SharedMapName")

        mock_connect.assert_called_once_with("SharedMapName")
        assert result == {"MAP": 100}

    def test_dict_name_connects_only_matching_struct_names(self, sm_receiver):
        class PacketA:
            pass

        class PacketB:
            pass

        sm_receiver.config.packet_info = {1: [PacketA, PacketB]}
        name_map = {"PacketA": "SharedA"}  # PacketB intentionally has no mapping

        fake_maps = {"SharedA": {"mapA": 10}}

        def fake_connect_map(name, struct=None):
            return fake_maps[name]

        with patch.object(sm_receiver, "connect_map", side_effect=fake_connect_map) as mock_connect:
            result = sm_receiver.setup_maps(name_map)

        mock_connect.assert_called_once_with("SharedA", PacketA)
        assert result == {"mapA": 10}

    def test_invalid_name_type_raises_value_error(self, sm_receiver):
        sm_receiver.config.packet_info = {1: []}

        with pytest.raises(ValueError, match="string or a dict"):
            sm_receiver.setup_maps(12345)  # not str or dict


# ---------------------------------------------------------------------------
# SharedMemoryReceiver.retreive_packets
# ---------------------------------------------------------------------------


class TestGetSharedPackets:
    def test_raises_if_shared_memory_names_not_set(self, sm_receiver):
        sm_receiver.config.all_shared_memory_names = None

        with pytest.raises(ValueError, match="Shared memory name is not set"):
            next(sm_receiver.retreive_packets())

    def test_yields_raw_data_for_nonzero_data_and_skips_all_zero_data(self, sm_receiver, supervisor):
        sm_receiver.config.all_shared_memory_names = "SomeMap"
        supervisor._is_still_active.side_effect = [True, False]

        zero_map = MagicMock()
        zero_map.read.return_value = b"\x00\x00\x00"
        live_map = MagicMock()
        live_map.read.return_value = b"\x01\x02\x03"

        setup_result = {zero_map: 3, live_map: 3}
        with patch.object(sm_receiver, "setup_maps", return_value=setup_result):
            results = list(sm_receiver.retreive_packets())

        # zero_map contributes nothing; live_map yields exactly one packet
        assert results == [b"\x01\x02\x03"]
        zero_map.close.assert_called_once()
        live_map.close.assert_called_once()

    def test_all_maps_seeked_to_start_before_each_read(self, sm_receiver, supervisor):
        sm_receiver.config.all_shared_memory_names = "SomeMap"
        supervisor._is_still_active.side_effect = [True, False]

        live_map = MagicMock()
        live_map.read.return_value = b"\x01"

        with patch.object(sm_receiver, "setup_maps", return_value={live_map: 1}):
            list(sm_receiver.retreive_packets())

        live_map.seek.assert_called_once_with(0)

    def test_keyboard_interrupt_triggers_stop(self, sm_receiver, supervisor):
        sm_receiver.config.all_shared_memory_names = "SomeMap"
        supervisor._is_still_active.side_effect = [True, False]

        broken_map = MagicMock()
        broken_map.seek.side_effect = KeyboardInterrupt

        with patch.object(sm_receiver, "setup_maps", return_value={broken_map: 1}):
            results = list(sm_receiver.retreive_packets())

        supervisor._trigger_stop.assert_called_once()
        assert results == []

    def test_os_error_triggers_stop(self, sm_receiver, supervisor):
        sm_receiver.config.all_shared_memory_names = "SomeMap"
        supervisor._is_still_active.side_effect = [True, False]

        broken_map = MagicMock()
        broken_map.read.side_effect = OSError("shared memory gone")

        with patch.object(sm_receiver, "setup_maps", return_value={broken_map: 1}):
            results = list(sm_receiver.retreive_packets())

        supervisor._trigger_stop.assert_called_once()
        assert results == []

    def test_maps_closed_after_loop_ends(self, sm_receiver, supervisor):
        sm_receiver.config.all_shared_memory_names = "SomeMap"
        supervisor._is_still_active.return_value = False  # loop body never runs

        m1, m2 = MagicMock(), MagicMock()
        with patch.object(sm_receiver, "setup_maps", return_value={m1: 10, m2: 10}):
            list(sm_receiver.retreive_packets())

        m1.close.assert_called_once()
        m2.close.assert_called_once()


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
