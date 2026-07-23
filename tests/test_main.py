"""
Test suite for main.py

Run with:
    pip install pytest --break-system-packages   # if not already installed
    pytest test_main.py -v
"""

import ctypes
import enum
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
# CentralStorage
# ---------------------------------------------------------------------------

storage = CentralStorage(metaData)

class TestCentralStorage:

    def test_central_storage_initialization(self):
        assert isinstance(storage, CentralStorage)
        assert storage.allData == {'testPacket1':[], 'testPacket2':[], 'HeaderPacket':[]}
        assert storage.latestData == {'testPacket1':None,'testPacket2':None, 'HeaderPacket':None}

    def test_snapshot_output(self):
        output = {"allData": {'testPacket1': [], 'testPacket2': [], 'HeaderPacket': []}, "latestData": {'testPacket1': None, 'testPacket2': None, 'HeaderPacket': None}}
        assert storage.snapshot() == output

# ---------------------------------------------------------------------------
# ReadOnlyStorage
# ---------------------------------------------------------------------------

RO_storage = ReadOnlyStorage(storage)

class TestReadOnlyStorage:

    def test_readonly_storage_initialization(self):
        assert isinstance(RO_storage, ReadOnlyStorage)

    def test_snapshot_output(self):
        output = {"allData": {'testPacket1': [], 'testPacket2': [], 'HeaderPacket': []}, "latestData": {'testPacket1': None, 'testPacket2': None, 'HeaderPacket': None}}
        assert RO_storage.snapshot() == output


# ---------------------------------------------------------------------------
# TelemetryManager - Base functionality
# ---------------------------------------------------------------------------


class TestTelemetryManager:

    def test_telemetry_manager_initialization(self):
        telemetry = telemetryManager()
        assert isinstance(telemetry, telemetryManager)

    def test_meta_data_check(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)
        assert telemetry._telemetryManager__metaDataCheck("port") == 1234
        assert telemetry._telemetryManager__metaDataCheck("packetIDAttribute") == "header_id"
        assert telemetry._telemetryManager__metaDataCheck("headerInfo") == SubHeaderPacket
        assert telemetry._telemetryManager__metaDataCheck("heartBeatPort") == None
        assert telemetry._telemetryManager__metaDataCheck("heartBeatPort", 1234) == 1234

    def test_packet_size(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)
        assert telemetry._telemetryManager__getPacketSize(testPacket1) == 4
        assert telemetry._telemetryManager__getPacketSize(testPacket2) == 8

    def test_max_packet_size(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)
        assert telemetry._telemetryManager__getMaxPacketSize() == 59

    def test_trigger_stop(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)

        assert telemetry.stop_event.is_set() == False

        telemetry._telemetryManager__triggerStop()
        assert telemetry.stop_event.is_set() == True

    def test_manual_stop(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)

        assert telemetry.stop_event.is_set() == False

        telemetry.manualStop(True)
        assert telemetry.stop_event.is_set() == True

    def test_is_still_active(self):
        telemetry = telemetryManager()
        telemetry.updateMeta(metaData)

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

    def test_construct_packet_wrong_type(self):
        telemetry = telemetryManager()
        # telemetry.updateMeta(metaData)

        constructed_packet1 = telemetry._telemetryManager__construct_packet(full_packet_byte, [testPacket1, testPacket2])
        assert constructed_packet1 == None

        constructed_packet2 = telemetry._telemetryManager__construct_packet(full_packet_byte, [])
        assert constructed_packet2 == None


# ---------------------------------------------------------------------------
# TelemetryManager - Packets
# ---------------------------------------------------------------------------

telemetry = telemetryManager()
telemetry.updateMeta(metaData)

constructed_packet, packetID, headerPacker = telemetry._telemetryManager__retrieve_packet(header_packet_byte)
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

telemetry = telemetryManager()
telemetry.updateMeta(metaData)
warnings.filterwarnings("ignore")

class TestUserInputs:

    def test_update_local_ip_valid(self):
        # Test invalid IP addresses
        assert False == telemetry.updateLocalIP(5)
        assert False == telemetry.updateLocalIP(-8)
        assert False == telemetry.updateLocalIP(2.7)
        assert False == telemetry.updateLocalIP("invalid_ip")
        assert False == telemetry.updateLocalIP("256.100.50.25")
        assert False == telemetry.updateLocalIP("256.256.256.256")
        assert False == telemetry.updateLocalIP("192.168.1")
        assert False == telemetry.updateLocalIP("1.2.3.4.5")
        assert False == telemetry.updateLocalIP("192.1")
        assert False == telemetry.updateLocalIP(False)
        assert False == telemetry.updateLocalIP(testPacket1)

        # test valid IP address
        assert True == telemetry.updateLocalIP("1.1.1.1")
        assert True == telemetry.updateLocalIP("192.168.1.1")
        assert True == telemetry.updateLocalIP("192.168.68.1")
        assert True == telemetry.updateLocalIP("255.255.255.255")

    def test_update_send_ip_valid(self):
        # Test invalid IP addresses
        assert False == telemetry.updateSendIP(5)
        assert False == telemetry.updateSendIP(-8)
        assert False == telemetry.updateSendIP(2.7)
        assert False == telemetry.updateSendIP("invalid_ip")
        assert False == telemetry.updateSendIP("256.100.50.25")
        assert False == telemetry.updateSendIP("256.256.256.256")
        assert False == telemetry.updateSendIP("192.168.1")
        assert False == telemetry.updateSendIP("1.2.3.4.5")
        assert False == telemetry.updateSendIP("192.1")
        assert False == telemetry.updateSendIP(False)
        assert False == telemetry.updateSendIP(testPacket1)

        # test valid IP address
        assert True == telemetry.updateSendIP("1.1.1.1")
        assert True == telemetry.updateSendIP("192.168.1.1")
        assert True == telemetry.updateSendIP("192.168.68.1")
        assert True == telemetry.updateSendIP("255.255.255.255")

    def test_add_worker_thread(self):
        assert False == telemetry.addWorkerThread(False)
        assert False == telemetry.addWorkerThread(15)
        assert False == telemetry.addWorkerThread(-45)
        assert False == telemetry.addWorkerThread(3.6)
        assert False == telemetry.addWorkerThread("1.1.1.1")
        assert False == telemetry.addWorkerThread("hello")
        assert False == telemetry.addWorkerThread(testPacket1)

        assert True == telemetry.addWorkerThread(func1)
        assert True == telemetry.addWorkerThread(func2)
        assert True == telemetry.addWorkerThread(func3)
        assert True == telemetry.addWorkerThread(func4)
        assert True == telemetry.addWorkerThread(workerClass.workerFunc)

    def test_manual_stop(self):
        assert False == telemetry.manualStop(1)
        assert False == telemetry.manualStop(0)
        assert False == telemetry.manualStop(5)
        assert False == telemetry.manualStop(-8)
        assert False == telemetry.manualStop(2.7)
        assert False == telemetry.manualStop("test")
        assert False == telemetry.manualStop("1.1.1.1")
        assert False == telemetry.manualStop(testPacket1)
        assert False == telemetry.manualStop(func1)

        assert True == telemetry.manualStop(False)
        assert True == telemetry.manualStop(True)

    def test_is_multi_thread(self):
        assert False == telemetry.isMultiThreaded(1)
        assert False == telemetry.isMultiThreaded(0)
        assert False == telemetry.isMultiThreaded(5)
        assert False == telemetry.isMultiThreaded(-8)
        assert False == telemetry.isMultiThreaded(2.7)
        assert False == telemetry.isMultiThreaded("test")
        assert False == telemetry.isMultiThreaded("1.1.1.1")
        assert False == telemetry.isMultiThreaded(testPacket1)
        assert False == telemetry.isMultiThreaded(func1)

        assert True == telemetry.isMultiThreaded(False)
        assert True == telemetry.isMultiThreaded(True)

    def test_is_shared_memory(self):
        assert False == telemetry.isSharedMemory(1)
        assert False == telemetry.isSharedMemory(0)
        assert False == telemetry.isSharedMemory(5)
        assert False == telemetry.isSharedMemory(-8)
        assert False == telemetry.isSharedMemory(2.7)
        assert False == telemetry.isSharedMemory("test")
        assert False == telemetry.isSharedMemory("1.1.1.1")
        assert False == telemetry.isSharedMemory(testPacket1)
        assert False == telemetry.isSharedMemory(func1)

        assert True == telemetry.isSharedMemory(False)
        assert True == telemetry.isSharedMemory(True)

    def test_enum_mode(self):
        assert False == telemetry.setEnumMode(-8)
        assert False == telemetry.setEnumMode(3)
        assert False == telemetry.setEnumMode(-1)
        assert False == telemetry.setEnumMode(2.7)
        assert False == telemetry.setEnumMode("test")
        assert False == telemetry.setEnumMode("1.1.1.1")
        assert False == telemetry.setEnumMode(testPacket1)
        assert False == telemetry.setEnumMode(func1)
        
        # False is considered 0, True is considered 1
        assert True == telemetry.setEnumMode(False)
        assert True == telemetry.setEnumMode(True)
        
        assert True == telemetry.setEnumMode(0)
        assert True == telemetry.setEnumMode(1)
        assert True == telemetry.setEnumMode(2)


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
