"""Tests for TelemetryManager configuration and storage integration."""

from types import SimpleNamespace

import pytest

from ..src.RaceTelemetry.main import CentralStorage, ReadOnlyStorage, TelemetryManager
from ..src.RaceTelemetry.transport import SharedMemoryTransport, UDPTransport


class Packet:
    pass


class OtherPacket:
    pass


class Metadata:
    port = 20777
    heartBeatPort = 20778
    heartBeatFunc = None
    handShakePort = 20779
    handShakeFunc = None
    decryptionFunc = None
    headerInfo = None
    packetIDAttribute = None
    allSharedMemoryNames = None
    packetInfo = {1: (Packet,), 2: (OtherPacket,)}


@pytest.fixture
def manager():
    return TelemetryManager()


@pytest.fixture
def configured_manager(manager):
    manager.updateMeta(Metadata)
    return manager


class TestStorage:
    def test_central_storage_initializes_packet_slots(self):
        storage = CentralStorage(Metadata)

        assert storage.all_data == {"Packet": [], "OtherPacket": []}
        assert storage.latest_data == {"Packet": None, "OtherPacket": None}

    def test_write_updates_history_and_latest(self):
        storage = CentralStorage(Metadata)
        packet = SimpleNamespace(__name__="Packet", value=3)

        storage._write(packet)

        assert storage.all_data["Packet"] == [packet]
        assert storage.latest_data["Packet"] is packet

    def test_write_none_is_ignored(self):
        storage = CentralStorage(Metadata)
        storage._write(None)

        assert storage.all_data["Packet"] == []

    def test_read_only_storage_exposes_snapshot_without_write(self):
        storage = CentralStorage(Metadata)
        read_only = ReadOnlyStorage(storage)

        assert read_only.snapshot() == storage.snapshot()
        assert not hasattr(read_only, "_write")


class TestTelemetryManager:
    def test_initializes_unconfigured(self, manager):
        assert manager.config.active_metadata is None
        assert manager.router is None
        assert manager.transport_mode_class is None
        assert manager.shared_memory is False

    def test_update_meta_builds_storage_and_router(self, configured_manager):
        assert configured_manager.config.active_metadata is Metadata
        assert isinstance(configured_manager.activeStorage, CentralStorage)
        assert isinstance(configured_manager.readOnlyStorage, ReadOnlyStorage)
        assert configured_manager.router is not None

    def test_fetch_transport_selects_udp_by_default(self, configured_manager):
        configured_manager._fetchTransport()

        assert isinstance(configured_manager.transport_mode_class, UDPTransport)

    def test_fetch_transport_selects_shared_memory_when_enabled(self, configured_manager):
        configured_manager.isSharedMemory(True)

        configured_manager._fetchTransport()

        assert isinstance(configured_manager.transport_mode_class, SharedMemoryTransport)

    def test_update_meta_same_metadata_keeps_existing_storage(self, configured_manager):
        storage = configured_manager.activeStorage

        configured_manager.updateMeta(Metadata)

        assert configured_manager.activeStorage is storage

    def test_update_meta_is_blocked_while_workers_run(self, configured_manager, caplog):
        storage = configured_manager.activeStorage
        configured_manager.supervisor.workers_are_working = True

        configured_manager.updateMeta(type("NewMetadata", (), {"packetInfo": {}}))

        assert configured_manager.activeStorage is storage
        assert "Tried to update meta after telemetry has started" in caplog.text

    @pytest.mark.parametrize("value", ["bad", 1, None])
    def test_is_shared_memory_rejects_non_boolean_values(self, manager, value):
        assert manager.isSharedMemory(value) is False
        assert manager.shared_memory is False

    def test_is_shared_memory_accepts_boolean_values(self, manager):
        assert manager.isSharedMemory(True) is True
        assert manager.shared_memory is True

    def test_configuration_methods_delegate_to_config(self, manager):
        assert manager.updateLocalIP("192.168.1.10") is True
        assert manager.config.local_ip == "192.168.1.10"
        assert manager.updateSendIP("10.0.0.5") is True
        assert manager.config.destination_ip == "10.0.0.5"
        assert manager.setEnumMode(2) is True
        assert manager.config.enum_mode == 2

    def test_start_telemetry_requires_metadata(self, manager):
        with pytest.raises(RuntimeError, match="Read-only storage is not initialized"):
            manager.StartTelemetry()
