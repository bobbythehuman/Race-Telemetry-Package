"""Integration-style tests for TelemetryManager orchestration."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ..src.RaceTelemetry.main import TelemetryManager


class Packet:
    pass


class Metadata:
    packetInfo = {1: (Packet,)}
    headerInfo = None
    packetIDAttribute = None
    allSharedMemoryNames = None


@pytest.fixture
def manager():
    telemetry = TelemetryManager()
    telemetry.updateMeta(Metadata)
    return telemetry


class TestTelemetryGenerator:
    def test_udp_generator_is_selected_by_default(self, manager, monkeypatch):
        raw_data = [b"raw-packet"]
        expected = [(SimpleNamespace(__name__="Packet"), 1, None)]
        manager._fetchTransport()
        manager._fetchDecoder()
        monkeypatch.setattr("RaceTelemetry.src.RaceTelemetry.main.dynamic_ingest", lambda value, *args: value)
        manager.transport_mode_class.retreive_packets = MagicMock(return_value=iter(raw_data))
        manager.decoder_mode_class.decode_packet = MagicMock(return_value=expected[0])

        assert list(manager._telemetry_generator()) == expected
        manager.transport_mode_class.retreive_packets.assert_called_once_with()
        manager.decoder_mode_class.decode_packet.assert_called_once_with(raw_data[0])

    def test_shared_memory_generator_is_selected_when_enabled(self, manager, monkeypatch):
        raw_data = [b"raw-packet"]
        expected = [(SimpleNamespace(__name__="Packet"), 1, None)]

        shared_memory_metadata = type(
            "SharedMemoryMetadata",
            (Metadata,),
            {"transportMode": "shared_memory"},
        )
        manager.updateMeta(shared_memory_metadata)
        manager._fetchTransport()
        manager._fetchDecoder()
        monkeypatch.setattr("RaceTelemetry.src.RaceTelemetry.main.dynamic_ingest", lambda value, *args: value)
        manager.transport_mode_class.retreive_packets = MagicMock(return_value=iter(raw_data))
        manager.decoder_mode_class.decode_packet = MagicMock(return_value=expected[0])

        assert list(manager._telemetry_generator()) == expected
        manager.transport_mode_class.retreive_packets.assert_called_once_with()
        manager.decoder_mode_class.decode_packet.assert_called_once_with(raw_data[0])

    def test_generator_is_empty_until_metadata_is_configured(self):
        manager = TelemetryManager()

        assert list(manager._telemetry_generator()) == []


class TestGetTelemetry:
    def test_single_threaded_mode_returns_transport_generator(self, manager):
        manager.supervisor.multi_threaded = False
        manager._telemetry_generator = MagicMock(return_value=iter([("packet", 1, None)]))

        result = manager.GetTelemetry()

        assert list(result) == [("packet", 1, None)]
        manager._telemetry_generator.assert_called_once_with()

    def test_multi_threaded_mode_starts_supervisor_and_returns_storage(self, manager):
        manager.supervisor.multi_threaded = True
        manager.supervisor._start_threads = MagicMock()

        result = manager.GetTelemetry()

        assert result is manager.readOnlyStorage
        manager.supervisor._start_threads.assert_called_once_with(network_target=manager._network_listener)


class TestNetworkAndLifecycle:
    def test_network_listener_writes_received_packets(self, manager):
        packet = SimpleNamespace(__name__="Packet", value=5)
        manager._telemetry_generator = lambda: iter([(packet, 1, None), (None, 0, None)])

        manager._network_listener()

        assert manager.activeStorage.latest_data["Packet"] is packet
        assert manager.activeStorage.all_data["Packet"] == [packet]

    def test_network_listener_requires_storage(self):
        manager = TelemetryManager()

        with pytest.raises(ValueError, match="Storage instance is not initialized"):
            manager._network_listener()

    def test_stop_telemetry_stops_supervisor(self, manager):
        manager.supervisor._trigger_stop = MagicMock()
        manager.supervisor._stop_threads = MagicMock()

        manager.StopTelemetry()

        manager.supervisor._trigger_stop.assert_called_once_with()
        manager.supervisor._stop_threads.assert_called_once_with()

    def test_start_telemetry_starts_and_waits_for_supervisor(self, manager):
        manager.supervisor._start_threads = MagicMock()
        manager.supervisor._wait_for_stop_signal = MagicMock()

        manager.StartTelemetry()

        manager.supervisor._start_threads.assert_called_once_with(network_target=manager._network_listener)
        manager.supervisor._wait_for_stop_signal.assert_called_once_with()

    def test_add_worker_thread_delegates_to_supervisor(self, manager):
        worker = MagicMock()
        manager.supervisor.add_worker_thread = MagicMock(return_value=True)

        assert manager.addWorkerThread(worker) is True
        manager.supervisor.add_worker_thread.assert_called_once_with(worker, manager.readOnlyStorage)

    def test_manual_stop_and_thread_mode_delegate_to_supervisor(self, manager):
        manager.supervisor.manual_stop = MagicMock(return_value=True)
        manager.supervisor.is_multi_threaded = MagicMock(return_value=True)

        assert manager.manualStop(True) is True
        assert manager.isMultiThreaded(False) is True
        manager.supervisor.manual_stop.assert_called_once_with(True)
        manager.supervisor.is_multi_threaded.assert_called_once_with(False)
