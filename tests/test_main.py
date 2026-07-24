"""
Test suite for main.py

Run with:
    pip install pytest --break-system-packages   # if not already installed
    pytest test_main.py -v
"""

import ctypes
import enum
from typing import Any
import warnings

import pytest

from ..src.RaceTelemetry.main import CentralStorage, ReadOnlyStorage, telemetryManager
from .test_resources import (
    testPacket1,
    testPacket2,
    metaData,
    SubPacket,
    FullPacket,
    full_packet_byte,
    full_unpacked_packet,
    SubHeaderPacket,
    HeaderPacket,
    header_packet_byte,
    header_unpacked_packet,
    subheader_unpacked_packet,
    func1,
    func2,
    func3,
    func4,
    workerClass,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def storage() -> CentralStorage:
    return CentralStorage(metaData)


@pytest.fixture
def RO_storage(storage: CentralStorage) -> ReadOnlyStorage:
    return ReadOnlyStorage(storage)


@pytest.fixture
def telemetry() -> telemetryManager:
    telemetry = telemetryManager()
    telemetry.updateMeta(metaData)
    return telemetry


# ---------------------------------------------------------------------------
# CentralStorage
# ---------------------------------------------------------------------------


class TestCentralStorage:

    def test_central_storage_initialization(self, storage: CentralStorage):
        assert isinstance(storage, CentralStorage)
        assert storage.allData == {"testPacket1": [], "testPacket2": [], "HeaderPacket": []}
        assert storage.latestData == {"testPacket1": None, "testPacket2": None, "HeaderPacket": None}

    def test_snapshot_output(self, storage: CentralStorage):
        output = {
            "allData": {"testPacket1": [], "testPacket2": [], "HeaderPacket": []},
            "latestData": {"testPacket1": None, "testPacket2": None, "HeaderPacket": None},
        }
        assert storage.snapshot() == output


# ---------------------------------------------------------------------------
# ReadOnlyStorage
# ---------------------------------------------------------------------------


class TestReadOnlyStorage:

    def test_readonly_storage_initialization(self, RO_storage: ReadOnlyStorage):
        assert isinstance(RO_storage, ReadOnlyStorage)

    def test_snapshot_output(self, RO_storage: ReadOnlyStorage):
        output = {
            "allData": {"testPacket1": [], "testPacket2": [], "HeaderPacket": []},
            "latestData": {"testPacket1": None, "testPacket2": None, "HeaderPacket": None},
        }
        assert RO_storage.snapshot() == output


# ---------------------------------------------------------------------------
# TelemetryManager - Base functionality
# ---------------------------------------------------------------------------


class TestTelemetryManager:

    def test_telemetry_manager_initialization(self, telemetry: telemetryManager):
        assert isinstance(telemetry, telemetryManager)

    def test_meta_data_check(self, telemetry: telemetryManager):
        assert telemetry._telemetryManager__metaDataCheck("port") == 1234
        assert telemetry._telemetryManager__metaDataCheck("packetIDAttribute") == "header_id"
        assert telemetry._telemetryManager__metaDataCheck("headerInfo") == SubHeaderPacket
        assert telemetry._telemetryManager__metaDataCheck("heartBeatPort") == None
        assert telemetry._telemetryManager__metaDataCheck("heartBeatPort", 1234) == 1234

    def test_packet_size(self, telemetry: telemetryManager):
        assert telemetry._telemetryManager__getPacketSize(testPacket1) == 4
        assert telemetry._telemetryManager__getPacketSize(testPacket2) == 8

    def test_max_packet_size(self, telemetry: telemetryManager):
        assert telemetry._telemetryManager__getMaxPacketSize() == 59

    def test_trigger_stop(self, telemetry: telemetryManager):
        assert telemetry.stop_event.is_set() == False

        telemetry._telemetryManager__triggerStop()
        assert telemetry.stop_event.is_set() == True

    def test_manual_stop(self, telemetry: telemetryManager):
        assert telemetry.stop_event.is_set() == False

        telemetry.manualStop(True)
        assert telemetry.stop_event.is_set() == True

    def test_is_still_active(self, telemetry: telemetryManager):
        # check it is active
        assert telemetry._telemetryManager__isStillActive() == True

        # check it is not active after manual stop
        telemetry.manualStop(True)
        assert telemetry._telemetryManager__isStillActive() == False

        # reset manuallyStopped to False and check it is active again
        telemetry.manualStop(False)
        assert telemetry._telemetryManager__isStillActive() == True

        telemetry._telemetryManager__triggerStop()
        assert telemetry._telemetryManager__isStillActive() == False

    def test_construct_packet_wrong_type(self, telemetry: telemetryManager):
        constructed_packet1 = telemetry._telemetryManager__construct_packet(full_packet_byte, [testPacket1, testPacket2])
        assert constructed_packet1 == None

        constructed_packet2 = telemetry._telemetryManager__construct_packet(full_packet_byte, [])
        assert constructed_packet2 == None


# ---------------------------------------------------------------------------
# TelemetryManager - Packets
# ---------------------------------------------------------------------------

packetTelemetry = telemetryManager()
packetTelemetry.updateMeta(metaData)
constructed_packet, packetID, headerPacker = packetTelemetry._telemetryManager__retrieve_packet(header_packet_byte)


class TestRetrievePacket:
    def test_packetID(self):
        assert packetID == 1

    def test_header_packet(self):
        assert headerPacker.header_id == 1
        assert headerPacker.packetNum == 28

    def test_retrieve_packet(self):
        assert constructed_packet.flag is True
        assert constructed_packet.byte_val == -12
        assert constructed_packet.short_val == -1000
        assert constructed_packet.int_val == -100000
        assert constructed_packet.long_val == -123456
        assert constructed_packet.longlong_val == -1234567890123
        assert constructed_packet.ssize_val == -42
        assert constructed_packet.ubyte_val == 200
        assert constructed_packet.ushort_val == 40000
        assert constructed_packet.uint_val == 3000000000
        assert constructed_packet.ulong_val == 123456
        assert constructed_packet.ulonglong_val == 12345678901234
        assert constructed_packet.size_val == 999


# ---------------------------------------------------------------------------
# TelemetryManager - User Inputs
# ---------------------------------------------------------------------------


class TestUserInputs:

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (5, False),
            (-8, False),
            (2.7, False),
            ("invalid_ip", False),
            ("256.100.50.25", False),
            ("256.256.256.256", False),
            ("192.168.1", False),
            ("1.2.3.4.5", False),
            ("192.1", False),
            (False, False),
            (testPacket1, False),
            ("1.1.1.1", True),
            ("192.168.1.1", True),
            ("192.168.68.1", True),
            ("255.255.255.255", True),
        ],
    )
    def test_update_local_ip_valid(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.updateLocalIP(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (5, False),
            (-8, False),
            (2.7, False),
            ("invalid_ip", False),
            ("256.100.50.25", False),
            ("256.256.256.256", False),
            ("192.168.1", False),
            ("1.2.3.4.5", False),
            ("192.1", False),
            (False, False),
            (testPacket1, False),
            ("1.1.1.1", True),
            ("192.168.1.1", True),
            ("192.168.68.1", True),
            ("255.255.255.255", True),
        ],
    )
    def test_update_send_ip_valid(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.updateLocalIP(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (False, False),
            (True, False),
            (15, False),
            (-45, False),
            (3.6, False),
            ("test", False),
            ("1.1.1.1", False),
            (testPacket1, False),
            (func1, True),
            (func2, True),
            (func3, True),
            (func4, True),
            (workerClass.workerFunc, True),
        ],
    )
    def test_add_worker_thread(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.addWorkerThread(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (1, False),
            (0, False),
            (5, False),
            (-8, False),
            (2.7, False),
            ("test", False),
            ("1.1.1.1", False),
            (testPacket1, False),
            (func1, False),
            (False, True),
            (True, True),
        ],
    )
    def test_manual_stop(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.manualStop(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (1, False),
            (0, False),
            (5, False),
            (-8, False),
            (2.7, False),
            ("test", False),
            ("1.1.1.1", False),
            (testPacket1, False),
            (func1, False),
            (False, True),
            (True, True),
        ],
    )
    def test_is_multi_thread(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.isMultiThreaded(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (1, False),
            (0, False),
            (5, False),
            (-8, False),
            (2.7, False),
            ("test", False),
            ("1.1.1.1", False),
            (testPacket1, False),
            (func1, False),
            (False, True),
            (True, True),
        ],
    )
    def test_is_shared_memory(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.isSharedMemory(operand) == expected

    @pytest.mark.parametrize(
        "operand, expected",
        [
            (5, False),
            (-8, False),
            (2.7, False),
            ("test", False),
            ("1.1.1.1", False),
            (testPacket1, False),
            (func1, False),
            (0, True),
            (1, True),
            (2, True),
            (False, True),
            (True, True),
        ],
    )
    def test_enum_mode(self, telemetry: telemetryManager, operand: Any, expected: bool) -> None:
        assert telemetry.setEnumMode(operand) == expected


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
    # --disable-warnings
