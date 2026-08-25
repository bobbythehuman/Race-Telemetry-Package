"""Tests for TelemetryManager configuration and storage integration."""

from types import SimpleNamespace

import pytest

from ..src.RaceTelemetry.main import CentralStorage, ReadOnlyStorage, TelemetryManager
from ..src.RaceTelemetry.decoders import IracingDynamicDecoder, StaticDecoding
from ..src.RaceTelemetry.receivers import SharedMemoryReceiver, UDPReceiver


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


class SharedMemoryMetadata(Metadata):
    receiverMode = "shared_memory"


class IracingMetadata(Metadata):
    receiverMode = "shared_memory"
    decoderMode = "iracing_dynamic"


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
        assert manager.receiver_mode_class is None
        assert manager.decoder_mode_class is None
        assert manager.config.receiver_mode == "udp"
        assert manager.config.decoder_mode == "static"
        assert manager.readOnlyStorage is None
        assert manager.use_shared_memory is False

    def test_update_meta_builds_storage(self, configured_manager):
        assert configured_manager.config.active_metadata is Metadata
        assert isinstance(configured_manager.activeStorage, CentralStorage)
        assert isinstance(configured_manager.readOnlyStorage, ReadOnlyStorage)

    def test_fetch_receiver_selects_udp_by_default(self, configured_manager):
        configured_manager._fetchReceiver()

        assert isinstance(configured_manager.receiver_mode_class, UDPReceiver)

    def test_fetch_transport_selects_shared_memory_when_enabled(self, configured_manager):
        configured_manager.config.all_shared_memory_names = "$testLocation"
        configured_manager.useSharedMemory(True)

        configured_manager._fetchReceiver()

        assert isinstance(configured_manager.receiver_mode_class, SharedMemoryReceiver)

    def test_fetch_decoder_selects_static_decoder_by_default(self, configured_manager):
        configured_manager._fetchDecoder()

        assert isinstance(configured_manager.decoder_mode_class, StaticDecoding)

    @pytest.mark.parametrize(
        ("metadata", "receiver_type", "decoder_type"),
        [
            (SharedMemoryMetadata, SharedMemoryReceiver, StaticDecoding),
            (IracingMetadata, SharedMemoryReceiver, IracingDynamicDecoder),
        ],
    )
    def test_fetches_modes_declared_by_metadata(self, manager, metadata, receiver_type, decoder_type):
        manager.updateMeta(metadata)

        manager._fetchDecoder()
        manager._fetchReceiver()

        assert isinstance(manager.receiver_mode_class, receiver_type)
        assert isinstance(manager.decoder_mode_class, decoder_type)

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
    def test_use_shared_memory_rejects_non_boolean_values(self, manager, value):
        assert manager.useSharedMemory(value) is False
        assert manager.use_shared_memory is False

    def test_use_shared_memory_accepts_boolean_values(self, manager):
        manager.config.all_shared_memory_names = "$testLocation"
        assert manager.useSharedMemory(True) is True
        assert manager.use_shared_memory is True


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
