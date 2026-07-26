"""
Comprehensive PyTest suite for main.py (TelemetryManager, CentralStorage,
ReadOnlyStorage).

Test types included:
    - Unit tests (happy path, edge case, error handling) for pure logic
      (validators, packet construction, storage).
    - Integration-style tests for generator/thread orchestration methods,
      with external dependencies (sockets, mmap, real threads/timing)
      mocked or monkeypatched out.

External dependencies that are ALWAYS mocked in these tests:
    - socket.socket (via unittest.mock.MagicMock) - no real network I/O.
    - mmap.mmap is not exercised directly (get_shared_packets is only
      tested up to its input-validation branches, before any mmap use,
      to avoid platform-specific shared-memory behaviour).
    - threading.Thread targets are monkeypatched to short, deterministic
      functions so tests never block or depend on real wall-clock timing
      beyond small sleeps used to keep a background loop alive briefly.

Because TelemetryManager uses Python's double-underscore name mangling for
its "private" helper methods, they are accessed in tests via their mangled
name, e.g. ``instance._TelemetryManager__construct_packet(...)``. This is
intentional and mirrors how the class's own methods call each other.
"""

import ctypes
import socket
import threading
import time
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from ..src.RaceTelemetry.main import CentralStorage, ReadOnlyStorage, TelemetryManager


# ===========================================================================
# Shared fixtures / helper ctypes structures & fake metadata
# ===========================================================================


class Header(ctypes.Structure):
    """A minimal header packet: just a packet-ID field."""

    _fields_ = [("packetID", ctypes.c_int)]


class PacketA(ctypes.Structure):
    """A 'full' packet whose first field overlaps the header's field,
    mirroring a real protocol where the header is a view onto the front
    of a larger, self-contained packet struct."""

    _fields_ = [("packetID", ctypes.c_int), ("value", ctypes.c_float)]


class PacketB(ctypes.Structure):
    _fields_ = [("packetID", ctypes.c_int), ("flag", ctypes.c_bool)]


class FakeMetaDataFull:
    """A metadata class exposing every attribute __unpack_meta_data looks for."""

    port = 5005
    heartBeatPort = 6000
    heartBeatFunc = None
    handShakePort = 7000
    handShakeFunc = None
    decryptionFunc = None
    headerInfo = Header
    packetIDAttribute = "packetID"
    allSharedMemoryNames = None
    packetInfo = {1: (PacketA,), 2: (PacketB,)}


class FakeMetaDataMinimal:
    """A metadata class with none of the OPTIONAL attributes set - exercises
    the __meta_data_check default-value fallback path. `packetInfo` is still
    required here because CentralStorage's constructor reads it directly
    from the raw metadata class (before any defaulting logic runs)."""

    packetInfo = {}


class FakeMetaDataNoPacketInfo:
    """A metadata class missing `packetInfo` entirely - used to document
    that updateMeta() has no guard for this and lets the AttributeError
    from CentralStorage propagate."""

    pass


@pytest.fixture
def manager():
    """A fresh, unconfigured TelemetryManager for each test."""
    return TelemetryManager()


@pytest.fixture
def configured_manager():
    """A TelemetryManager that has already had updateMeta() called with a
    fully-populated fake metadata class."""
    tm = TelemetryManager()
    tm.updateMeta(FakeMetaDataFull)
    return tm


# ===========================================================================
# CentralStorage / ReadOnlyStorage
# ===========================================================================


class TestCentralStorage:
    def test_init_creates_empty_slots_for_every_packet_name(self):
        class MetaData:
            packetInfo = {1: (PacketA,), 2: (PacketB,)}

        storage = CentralStorage(MetaData)

        assert storage.allData == {"PacketA": [], "PacketB": []}
        assert storage.latestData == {"PacketA": None, "PacketB": None}

    def test_duplicate_packet_names_across_ids_are_not_duplicated(self):
        # Two different packetIDs mapping to the SAME struct type should
        # only produce one storage slot for that struct's name.
        class MetaData:
            packetInfo = {1: (PacketA,), 2: (PacketA,)}

        storage = CentralStorage(MetaData)
        assert list(storage.allData.keys()) == ["PacketA"]

    def test_empty_packet_info_produces_empty_storage(self):
        class MetaData:
            packetInfo = {}

        storage = CentralStorage(MetaData)
        assert storage.allData == {}
        assert storage.latestData == {}

    def test_write_appends_to_all_data_and_updates_latest(self):
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        p1 = SimpleNamespace(__name__="PacketA", value=1)
        p2 = SimpleNamespace(__name__="PacketA", value=2)

        storage._write(p1)
        storage._write(p2)

        assert storage.allData["PacketA"] == [p1, p2]
        assert storage.latestData["PacketA"] is p2

    def test_write_with_none_is_a_no_op(self):
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        storage._write(None)

        assert storage.allData["PacketA"] == []
        assert storage.latestData["PacketA"] is None

    def test_snapshot_returns_both_keys_with_current_data(self):
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        p1 = SimpleNamespace(__name__="PacketA", value=1)
        storage._write(p1)

        snap = storage.snapshot()

        assert snap["allData"]["PacketA"] == [p1]
        assert snap["latestData"]["PacketA"] is p1

    def test_snapshot_dict_itself_is_a_separate_copy(self):
        # Mutating the returned dict's top level (e.g. adding a new key)
        # must not affect the live storage.
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        snap = storage.snapshot()
        snap["allData"]["NewKey"] = ["intruder"]

        assert "NewKey" not in storage.allData

    def test_snapshot_list_values_are_shallow_shared_not_deep_copied(self):
        # NOTE: `.copy()` on a dict is a SHALLOW copy, so the list objects
        # inside "allData" are the same list instances as the live storage.
        # A write() *after* taking the snapshot therefore still shows up in
        # the earlier snapshot's "allData" list, even though the class
        # docstring describes the snapshot as "immutable". This test
        # documents the current (shared-list) behaviour rather than
        # asserting the ideal one - worth knowing if code relies on the
        # snapshot being a true point-in-time copy.
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        p1 = SimpleNamespace(__name__="PacketA", value=1)
        storage._write(p1)

        snap = storage.snapshot()
        p2 = SimpleNamespace(__name__="PacketA", value=2)
        storage._write(p2)

        assert snap["allData"]["PacketA"] == [p1, p2]

    def test_snapshot_latest_data_entry_is_not_affected_by_later_writes(self):
        # Unlike the list case above, latestData re-assigns the dict VALUE
        # (not mutating in place), and dict.copy() takes a fresh top-level
        # dict, so an old snapshot's latestData entry is unaffected by
        # writes that happen after the snapshot was taken.
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        p1 = SimpleNamespace(__name__="PacketA", value=1)
        storage._write(p1)
        snap = storage.snapshot()

        p2 = SimpleNamespace(__name__="PacketA", value=2)
        storage._write(p2)

        assert snap["latestData"]["PacketA"] is p1


class TestReadOnlyStorage:
    def test_snapshot_delegates_to_underlying_storage(self):
        class MetaData:
            packetInfo = {1: (PacketA,)}

        storage = CentralStorage(MetaData)
        p1 = SimpleNamespace(__name__="PacketA", value=1)
        storage._write(p1)

        ro = ReadOnlyStorage(storage)
        snap = ro.snapshot()

        assert snap["latestData"]["PacketA"] is p1

    def test_read_only_storage_has_no_write_method(self):
        # This is the whole point of the wrapper: worker threads must not
        # be able to mutate the storage.
        storage = CentralStorage(type("M", (), {"packetInfo": {}}))
        ro = ReadOnlyStorage(storage)

        assert not hasattr(ro, "_write")
        assert not hasattr(ro, "write")


# ===========================================================================
# TelemetryManager - initial state
# ===========================================================================


class TestTelemetryManagerInitialState:
    def test_defaults(self, manager):
        assert manager.IP == "0.0.0.0"
        assert manager.destinationIP is None
        assert manager.multiThreaded is True
        assert manager.sharedMemory is False
        assert manager.enumMode == 0
        assert manager.HEARTBEAT_INTERVAL == 5
        assert manager.PACKET_COUNTER == 0
        assert manager.workersAreWorking is False
        assert isinstance(manager.stop_event, threading.Event)
        assert manager.stop_event.is_set() is False


# ===========================================================================
# updateMeta / __unpack_meta_data / __meta_data_check
# ===========================================================================


class TestUpdateMeta:
    def test_unpacks_all_attributes_from_full_metadata(self, manager):
        manager.updateMeta(FakeMetaDataFull)

        assert manager.mainPort == 5005
        assert manager.heartBeatPort == 6000
        assert manager.handShakePort == 7000
        assert manager.headerPacket is Header
        assert manager.packetIDAttr == "packetID"
        assert manager.packetInfo == FakeMetaDataFull.packetInfo

    def test_missing_attributes_fall_back_to_defaults(self, manager):
        manager.updateMeta(FakeMetaDataMinimal)

        assert manager.mainPort is None
        assert manager.heartBeatPort is None
        assert manager.headerPacket is None
        assert manager.packetIDAttr is None
        assert manager.packetInfo == {}

    def test_creates_active_and_read_only_storage(self, manager):
        manager.updateMeta(FakeMetaDataFull)

        assert isinstance(manager.activeStorage, CentralStorage)
        assert isinstance(manager.readOnlyStorage, ReadOnlyStorage)

    def test_calling_again_with_same_metadata_keeps_same_storage_instance(self, manager):
        manager.updateMeta(FakeMetaDataFull)
        storage_before = manager.activeStorage

        manager.updateMeta(FakeMetaDataFull)

        assert manager.activeStorage is storage_before

    def test_calling_with_different_metadata_creates_new_storage(self, manager):
        manager.updateMeta(FakeMetaDataFull)
        storage_before = manager.activeStorage

        manager.updateMeta(FakeMetaDataMinimal)

        assert manager.activeStorage is not storage_before

    def test_refuses_to_update_once_workers_are_running(self, manager, caplog):
        manager.workersAreWorking = True

        manager.updateMeta(FakeMetaDataFull)

        assert manager.ACTIVE_METADATA is None
        assert "Tried to update meta after telemetry has started" in caplog.text

    def test_metadata_missing_packet_info_entirely_raises_attribute_error(self, manager):
        # NOTE: this documents a real gap rather than an intended feature -
        # CentralStorage.__init__ reads `MetaData.packetInfo` directly, with
        # no fallback, so a metadata class that omits `packetInfo` blows up
        # with an AttributeError rather than a friendly validation message.
        with pytest.raises(AttributeError, match="packetInfo"):
            manager.updateMeta(FakeMetaDataNoPacketInfo)


# ===========================================================================
# IP validation (updateLocalIP / updateSendIP / __is_valid_ip)
# ===========================================================================


class TestIPValidation:
    @pytest.mark.parametrize("ip", ["0.0.0.0", "192.168.1.1", "10.0.0.1", "255.255.255.255"])
    def test_valid_ips_accepted(self, manager, ip):
        assert manager.updateLocalIP(ip) is True
        assert manager.IP == ip

    @pytest.mark.parametrize("ip", ["256.1.1.1", "999.1.1.1", "300.300.300.300", "not.an.ip.addr"])
    def test_invalid_ips_rejected_and_ip_unchanged(self, manager, ip):
        original = manager.IP
        assert manager.updateLocalIP(ip) is False
        assert manager.IP == original

    def test_non_string_ip_rejected(self, manager):
        assert manager.updateLocalIP(12345) is False

    def test_update_send_ip_valid(self, manager):
        assert manager.updateSendIP("10.0.0.5") is True
        assert manager.destinationIP == "10.0.0.5"

    def test_update_send_ip_invalid_leaves_destination_none(self, manager):
        assert manager.updateSendIP("999.0.0.5") is False
        assert manager.destinationIP is None


# ===========================================================================
# addWorkerThread
# ===========================================================================


class TestAddWorkerThread:
    def test_valid_function_is_registered(self, manager):
        def worker(worker_id, ro_storage, stop_event):
            pass

        assert manager.addWorkerThread(worker) is True
        assert manager.threadCount == 1
        assert 1 in manager.workerThreads
        assert isinstance(manager.workerThreads[1], threading.Thread)
        assert manager.workerThreads[1].daemon is True

    def test_non_callable_is_rejected(self, manager):
        assert manager.addWorkerThread(123) is False
        assert manager.threadCount == 0
        assert manager.workerThreads == {}

    def test_class_is_rejected(self, manager):
        class NotAFunction:
            pass

        assert manager.addWorkerThread(NotAFunction) is False
        assert manager.threadCount == 0

    def test_multiple_workers_increment_thread_count(self, manager):
        def worker(worker_id, ro_storage, stop_event):
            pass

        manager.addWorkerThread(worker)
        manager.addWorkerThread(worker)
        manager.addWorkerThread(worker)

        assert manager.threadCount == 3
        assert set(manager.workerThreads.keys()) == {1, 2, 3}

    def test_failed_registration_does_not_increment_count(self, manager):
        def worker(worker_id, ro_storage, stop_event):
            pass

        manager.addWorkerThread(worker)
        manager.addWorkerThread(123)  # rejected

        assert manager.threadCount == 1


# ===========================================================================
# Simple boolean/int setters
# ===========================================================================


class TestSimpleSetters:
    def test_manual_stop_accepts_bool(self, manager):
        assert manager.manualStop(True) is True
        assert manager.manuallyStopped is True

    def test_manual_stop_rejects_non_bool(self, manager):
        assert manager.manualStop("yes") is False
        assert manager.manuallyStopped is False

    def test_is_multi_threaded_accepts_bool_and_defaults_true(self, manager):
        assert manager.isMultiThreaded() is True
        assert manager.multiThreaded is True
        assert manager.isMultiThreaded(False) is True
        assert manager.multiThreaded is False

    def test_is_multi_threaded_rejects_non_bool(self, manager):
        assert manager.isMultiThreaded("nope") is False

    def test_is_shared_memory_accepts_bool(self, manager):
        assert manager.isSharedMemory(True) is True
        assert manager.sharedMemory is True

    def test_is_shared_memory_rejects_non_bool(self, manager):
        assert manager.isSharedMemory(1) is False

    @pytest.mark.parametrize("mode", [0, 1, 2])
    def test_set_enum_mode_accepts_valid_modes(self, manager, mode):
        assert manager.setEnumMode(mode) is True
        assert manager.enumMode == mode

    def test_set_enum_mode_rejects_out_of_range_int(self, manager):
        assert manager.setEnumMode(9) is False
        assert manager.enumMode == 0

    def test_set_enum_mode_rejects_non_int(self, manager):
        assert manager.setEnumMode("2") is False
        assert manager.enumMode == 0


# ===========================================================================
# Packet size helpers (__get_packet_size / __get_max_packet_size)
# ===========================================================================


class TestPacketSizeHelpers:
    def test_get_packet_size_matches_ctypes_sizeof(self, manager):
        assert manager._TelemetryManager__get_packet_size(PacketA) == ctypes.sizeof(PacketA)

    def test_get_max_packet_size_returns_largest_struct(self, configured_manager):
        # PacketA has an extra float field so should be the larger of the two.
        expected = max(ctypes.sizeof(PacketA), ctypes.sizeof(PacketB))
        assert configured_manager._TelemetryManager__get_max_packet_size() == expected

    def test_get_max_packet_size_raises_if_packet_info_empty(self, manager):
        manager.packetInfo = {}
        with pytest.raises(ValueError, match="Packet Info is empty"):
            manager._TelemetryManager__get_max_packet_size()

    def test_get_max_packet_size_raises_if_packet_info_none(self, manager):
        manager.packetInfo = None
        with pytest.raises(ValueError, match="Packet Info is empty"):
            manager._TelemetryManager__get_max_packet_size()


# ===========================================================================
# __construct_packet
# ===========================================================================


class TestConstructPacket:
    def test_matches_correct_struct_by_size_and_decodes(self, configured_manager):
        raw = bytes(PacketA(packetID=1, value=3.5))

        packet = configured_manager._TelemetryManager__construct_packet(raw, (PacketA, PacketB))

        assert packet is not None
        assert packet.packetID == 1
        assert packet.value == pytest.approx(3.5)

    def test_no_matching_size_returns_none(self, configured_manager, caplog):
        raw = b"\x00" * 3  # doesn't match any known struct size

        packet = configured_manager._TelemetryManager__construct_packet(raw, (PacketA, PacketB))

        assert packet is None
        assert "No matching packet size" in caplog.text

    def test_uses_configured_enum_mode_when_decoding(self, configured_manager):
        # enumMode is passed straight through to dynamic_ingest; this proves
        # the argument flows through correctly even without any enum fields
        # present (dynamic_ingest just ignores enumMode if there's nothing
        # to convert).
        configured_manager.enumMode = 2
        raw = bytes(PacketA(packetID=1, value=1.0))

        packet = configured_manager._TelemetryManager__construct_packet(raw, (PacketA,))

        assert packet.packetID == 1

    def test_from_buffer_copy_value_error_is_skipped(self, configured_manager, monkeypatch):
        # Simulate a struct whose from_buffer_copy raises ValueError (e.g.
        # buffer too small at the ctypes level) - construct_packet should
        # log and continue rather than propagating the exception.
        class Bad(ctypes.Structure):
            _fields_ = [("packetID", ctypes.c_int), ("value", ctypes.c_float)]

        def boom(data):
            raise ValueError("buffer too small")

        monkeypatch.setattr(Bad, "from_buffer_copy", staticmethod(boom))

        raw = bytes(PacketA(packetID=1, value=1.0))
        packet = configured_manager._TelemetryManager__construct_packet(raw, (Bad,))

        assert packet is None


# ===========================================================================
# __retrieve_packet
# ===========================================================================


class TestRetrievePacket:
    def test_returns_packet_id_and_header_when_id_recognised(self, configured_manager):
        raw = bytes(PacketA(packetID=1, value=2.5))

        packet, packet_id, header = configured_manager._TelemetryManager__retrieve_packet(raw)

        assert packet.packetID == 1
        assert packet.value == pytest.approx(2.5)
        assert packet_id == 1
        assert header.packetID == 1

    def test_unrecognised_packet_id_returns_none_packet(self, configured_manager, caplog):
        raw = bytes(PacketA(packetID=999, value=1.0))

        packet, packet_id, header = configured_manager._TelemetryManager__retrieve_packet(raw)

        assert packet is None
        assert packet_id == 999
        assert header.packetID == 999
        assert "ID not found" in caplog.text

    def test_no_header_packet_configured_defaults_id_to_zero(self, manager):
        manager.packetInfo = {0: (PacketA,)}
        manager.headerPacket = None

        raw = bytes(PacketA(packetID=1, value=1.0))
        packet, packet_id, header = manager._TelemetryManager__retrieve_packet(raw)

        assert packet_id == 0
        assert header is None
        # PacketA IS matched under ID 0 since no header narrows the search.
        assert packet.packetID == 1

    def test_raises_if_packet_info_missing(self, manager):
        manager.packetInfo = {}
        with pytest.raises(ValueError, match="Packet Info is empty"):
            manager._TelemetryManager__retrieve_packet(b"\x00" * 8)

    def test_raises_if_header_configured_but_no_id_attr(self, configured_manager):
        configured_manager.packetIDAttr = None
        raw = bytes(PacketA(packetID=1, value=1.0))
        with pytest.raises(ValueError, match="Packet ID Attribute is empty"):
            configured_manager._TelemetryManager__retrieve_packet(raw)


# ===========================================================================
# __process_loop
# ===========================================================================


class TestProcessLoop:
    def test_raises_if_heartbeat_func_not_callable(self, configured_manager):
        configured_manager.heartBeatFunc = "not callable"
        with pytest.raises(ValueError, match="Heart Beat Function is not a function"):
            configured_manager._TelemetryManager__process_loop(MagicMock())

    def test_raises_if_decryption_func_not_callable(self, configured_manager):
        configured_manager.decryptionFunc = "not callable"
        with pytest.raises(ValueError, match="Decryption Function is not a function"):
            configured_manager._TelemetryManager__process_loop(MagicMock())

    def test_heartbeat_fires_every_nth_call_and_resets_counter(self, configured_manager):
        hb_calls = []
        configured_manager.heartBeatFunc = lambda sock, dest: hb_calls.append(dest)
        configured_manager.HEARTBEAT_INTERVAL = 3
        configured_manager.destinationIP = "127.0.0.1"
        configured_manager.FULLBUFFERSIZE = ctypes.sizeof(PacketA)

        mock_sock = MagicMock()
        mock_sock.recvfrom.return_value = (bytes(PacketA(packetID=1, value=1.0)), ("x", 1))

        for i in range(1, 4):
            configured_manager._TelemetryManager__process_loop(mock_sock)

        # Heartbeat should have fired exactly once (on the 3rd call) and the
        # counter should have reset back to 0 afterwards.
        assert len(hb_calls) == 1
        assert configured_manager.PACKET_COUNTER == 0

    def test_decodes_received_packet_via_retrieve_packet(self, configured_manager):
        mock_sock = MagicMock()
        mock_sock.recvfrom.return_value = (bytes(PacketA(packetID=1, value=4.0)), ("x", 1))

        packet, packet_id, header = configured_manager._TelemetryManager__process_loop(mock_sock)

        assert packet.value == pytest.approx(4.0)
        assert packet_id == 1

    def test_decryption_func_is_applied_before_decoding(self, configured_manager):
        real_bytes = bytes(PacketA(packetID=1, value=9.0))
        seen = {}

        def decrypt(data):
            seen["data"] = data
            return data  # identity "decryption" for the test

        configured_manager.decryptionFunc = decrypt
        mock_sock = MagicMock()
        mock_sock.recvfrom.return_value = (real_bytes, ("x", 1))

        configured_manager._TelemetryManager__process_loop(mock_sock)

        assert seen["data"] == real_bytes

    def test_timeout_error_triggers_heartbeat_and_returns_none_packet(self, configured_manager):
        hb_calls = []
        configured_manager.heartBeatFunc = lambda sock, dest: hb_calls.append(dest)
        configured_manager.destinationIP = "127.0.0.1"

        mock_sock = MagicMock()
        mock_sock.recvfrom.side_effect = TimeoutError()

        packet, packet_id, header = configured_manager._TelemetryManager__process_loop(mock_sock)

        assert (packet, packet_id, header) == (None, 0, None)
        assert len(hb_calls) == 1  # heartbeat fired on timeout regardless of interval

    def test_os_error_triggers_stop_and_returns_none_packet(self, configured_manager, caplog):
        mock_sock = MagicMock()
        mock_sock.recvfrom.side_effect = OSError("socket broke")

        result = configured_manager._TelemetryManager__process_loop(mock_sock)

        assert result == (None, 0, None)
        assert configured_manager.stop_event.is_set() is True
        assert "Socket error" in caplog.text

    def test_keyboard_interrupt_triggers_stop_and_returns_none_packet(self, configured_manager):
        mock_sock = MagicMock()
        mock_sock.recvfrom.side_effect = KeyboardInterrupt()

        result = configured_manager._TelemetryManager__process_loop(mock_sock)

        assert result == (None, 0, None)
        assert configured_manager.stop_event.is_set() is True


# ===========================================================================
# get_udp_packets / get_shared_packets - validation branches
# ===========================================================================


class TestGetUdpPacketsValidation:
    def test_raises_if_handshake_or_heartbeat_set_without_destination_ip(self, manager):
        manager.packetInfo = {1: (PacketA,)}
        manager.heartBeatFunc = lambda *a: None
        manager.destinationIP = None

        gen = manager.get_udp_packets()
        with pytest.raises(ValueError, match="Destination IP must be set"):
            next(gen)

    def test_no_error_raised_when_no_handshake_or_heartbeat_configured(self, manager, monkeypatch):
        # Avoid actually binding a real socket: patch socket.socket to a
        # stub whose bind()/recvfrom() are inert, and stop the loop
        # immediately via stop_event.
        manager.packetInfo = {1: (PacketA,)}
        manager.mainPort = 0
        manager.stop_event.set()  # ensures the while loop body never runs

        fake_sock = MagicMock()
        monkeypatch.setattr(socket, "socket", lambda *a, **k: fake_sock)

        gen = manager.get_udp_packets()
        with pytest.raises(StopIteration):
            next(gen)

        fake_sock.bind.assert_called_once()
        fake_sock.close.assert_called_once()


class TestGetSharedPacketsValidation:
    def test_raises_if_shared_memory_name_not_set(self, manager):
        manager.allSharedMemoryNames = None
        manager.packetInfo = {1: (PacketA,)}

        with pytest.raises(ValueError, match="Shared memory name is not set"):
            next(manager.get_shared_packets())

    def test_raises_if_packet_info_empty(self, manager):
        manager.allSharedMemoryNames = "shm_test"
        manager.packetInfo = None

        with pytest.raises(ValueError, match="Packet Info is empty"):
            next(manager.get_shared_packets())

    def test_raises_if_shared_memory_names_wrong_type(self, manager):
        manager.allSharedMemoryNames = 12345  # neither str nor dict
        manager.packetInfo = {1: (PacketA,)}

        with pytest.raises(ValueError, match="must be a string or a dict"):
            next(manager.get_shared_packets())


# ===========================================================================
# GetTelemetry dispatch
# ===========================================================================


class TestGetTelemetryDispatch:
    def test_dispatches_to_shared_packets_when_shared_memory_enabled(self, manager, monkeypatch):
        calls = []

        def fake_shared(self):
            calls.append("shared")
            yield (None, 0, None)

        monkeypatch.setattr(TelemetryManager, "get_shared_packets", fake_shared)
        manager.sharedMemory = True

        list(manager.GetTelemetry())

        assert calls == ["shared"]

    def test_dispatches_to_udp_packets_when_shared_memory_disabled(self, manager, monkeypatch):
        calls = []

        def fake_udp(self):
            calls.append("udp")
            yield (None, 0, None)

        monkeypatch.setattr(TelemetryManager, "get_udp_packets", fake_udp)
        manager.sharedMemory = False

        list(manager.GetTelemetry())

        assert calls == ["udp"]


# ===========================================================================
# __network_listener
# ===========================================================================


class TestNetworkListener:
    def test_raises_if_storage_not_initialised(self, manager):
        manager.activeStorage = None
        with pytest.raises(ValueError, match="Storage instance is not initialized"):
            manager._TelemetryManager__network_listener()

    def test_writes_each_yielded_packet_into_active_storage(self, manager, monkeypatch):
        class MetaData:
            packetInfo = {1: (PacketA,)}

        manager.activeStorage = CentralStorage(MetaData)

        p1 = SimpleNamespace(__name__="PacketA", value=1)
        p2 = SimpleNamespace(__name__="PacketA", value=2)

        def fake_telemetry(self):
            yield (p1, 1, None)
            yield (None, 0, None)  # a "no packet this round" tick
            yield (p2, 1, None)

        monkeypatch.setattr(TelemetryManager, "GetTelemetry", fake_telemetry)

        manager._TelemetryManager__network_listener()

        assert manager.activeStorage.allData["PacketA"] == [p1, p2]
        assert manager.activeStorage.latestData["PacketA"] is p2


# ===========================================================================
# Thread lifecycle: __start_threads / __stop_threads / __trigger_stop /
# __is_still_active / __wait_for_stop_signal
# ===========================================================================


class TestThreadLifecycle:
    def test_start_threads_no_op_without_metadata(self, manager):
        manager.ACTIVE_METADATA = None
        manager.IP = "0.0.0.0"

        manager._TelemetryManager__start_threads()

        assert manager.networkThread is None
        assert manager.workersAreWorking is False

    def test_start_threads_no_op_without_ip(self, manager):
        manager.ACTIVE_METADATA = object()
        manager.IP = None

        manager._TelemetryManager__start_threads()

        assert manager.networkThread is None
        assert manager.workersAreWorking is False

    def test_start_threads_starts_network_and_worker_threads(self, manager, monkeypatch):
        # Replace the real network listener with a short-lived loop so the
        # background thread exits quickly once stop_event is set.
        def fake_listener(self):
            while not self.stop_event.is_set():
                time.sleep(0.01)

        monkeypatch.setattr(TelemetryManager, "_TelemetryManager__network_listener", fake_listener)

        worker_ran = threading.Event()

        def worker(worker_id, ro_storage, stop_event):
            worker_ran.set()

        manager.ACTIVE_METADATA = object()
        manager.IP = "0.0.0.0"
        manager.addWorkerThread(worker)

        manager._TelemetryManager__start_threads()
        try:
            assert manager.workersAreWorking is True
            assert manager.networkThread.is_alive()
            assert worker_ran.wait(timeout=1.0) is True
        finally:
            manager._TelemetryManager__trigger_stop()
            manager.networkThread.join(timeout=1.0)

    def test_stop_threads_no_op_if_workers_not_running(self, manager):
        manager.workersAreWorking = False
        manager._TelemetryManager__stop_threads()  # should not raise
        assert manager.workersAreWorking is False

    def test_stop_threads_no_op_if_no_network_thread(self, manager):
        manager.workersAreWorking = True
        manager.networkThread = None
        manager._TelemetryManager__stop_threads()  # should not raise / not crash
        # workersAreWorking is left as-is because the function returns early.
        assert manager.workersAreWorking is True

    def test_stop_threads_joins_and_resets_flag(self, manager, monkeypatch):
        def fake_listener(self):
            while not self.stop_event.is_set():
                time.sleep(0.01)

        monkeypatch.setattr(TelemetryManager, "_TelemetryManager__network_listener", fake_listener)
        manager.ACTIVE_METADATA = object()
        manager.IP = "0.0.0.0"
        manager._TelemetryManager__start_threads()

        manager._TelemetryManager__stop_threads()

        assert manager.workersAreWorking is False
        assert manager.stop_event.is_set() is True

    def test_trigger_stop_default_sets_event(self, manager):
        manager._TelemetryManager__trigger_stop()
        assert manager.stop_event.is_set() is True

    def test_trigger_stop_false_clears_event(self, manager):
        manager.stop_event.set()
        manager._TelemetryManager__trigger_stop(False)
        assert manager.stop_event.is_set() is False

    def test_is_still_active_true_by_default(self, manager):
        assert manager._TelemetryManager__is_still_active() is True

    def test_is_still_active_false_once_stop_event_set(self, manager):
        manager.stop_event.set()
        assert manager._TelemetryManager__is_still_active() is False

    def test_is_still_active_false_once_manually_stopped(self, manager):
        manager.manuallyStopped = True
        assert manager._TelemetryManager__is_still_active() is False

    def test_wait_for_stop_signal_exits_immediately_if_already_stopped(self, manager):
        manager.stop_event.set()
        # Should return promptly without blocking or prompting for input.
        manager._TelemetryManager__wait_for_stop_signal()

    def test_wait_for_stop_signal_manual_quit_sets_stop_event(self, manager):
        # Simulate manuallyStopped flipping true mid-wait (as another thread
        # might do), then the user typing "q" at the prompt.
        def fake_wait(seconds):
            manager.manuallyStopped = True

        manager._TelemetryManager__wait = fake_wait

        with patch("builtins.input", return_value="q") as mock_input:
            manager._TelemetryManager__wait_for_stop_signal()

        assert mock_input.called
        assert manager.stop_event.is_set() is True

    def test_wait_for_stop_signal_manual_prompt_declined_does_not_set_stop_event(self, manager):
        # NOTE: __is_still_active() treats manuallyStopped==True as "not
        # active" too, so as soon as manuallyStopped flips true the outer
        # while loop exits on its NEXT check regardless of what the user
        # types at the prompt. Answering anything other than "q" therefore
        # still ends the wait loop - it just does so WITHOUT setting
        # stop_event (only __trigger_stop(), triggered by "q", does that).
        def fake_wait(seconds):
            manager.manuallyStopped = True

        manager._TelemetryManager__wait = fake_wait

        with patch("builtins.input", return_value="n") as mock_input:
            manager._TelemetryManager__wait_for_stop_signal()

        assert mock_input.called
        assert manager.stop_event.is_set() is False

    def test_wait_for_stop_signal_always_stops_threads_in_finally(self, manager, monkeypatch):
        stopped = []
        monkeypatch.setattr(
            TelemetryManager, "_TelemetryManager__stop_threads", lambda self: stopped.append(True)
        )
        manager.stop_event.set()

        manager._TelemetryManager__wait_for_stop_signal()

        assert stopped == [True]


# ===========================================================================
# StartTelemetry
# ===========================================================================


class TestStartTelemetry:
    def test_raises_if_read_only_storage_not_initialised(self, manager):
        manager.readOnlyStorage = None
        with pytest.raises(RuntimeError, match="Read-only storage is not initialized"):
            manager.StartTelemetry()

    def test_calls_start_threads_then_waits_for_stop_signal(self, manager, monkeypatch):
        calls = []
        monkeypatch.setattr(
            TelemetryManager, "_TelemetryManager__start_threads", lambda self: calls.append("start")
        )
        monkeypatch.setattr(
            TelemetryManager,
            "_TelemetryManager__wait_for_stop_signal",
            lambda self: calls.append("wait"),
        )
        manager.readOnlyStorage = object()

        manager.StartTelemetry()

        assert calls == ["start", "wait"]