"""
Pytest suite for storage.py: CentralStorage and ReadOnlyStorage.

Run with:  pytest test_storage.py -v
"""

# from __future__ import annotations

import threading
import time
from types import SimpleNamespace

import pytest

from src.RaceTelemetry.storage import (
    CentralStorage,
    ReadOnlyStorage,
)

# --------------------------------------------------------------------------
# Helpers / fixtures
# --------------------------------------------------------------------------


class PacketA:
    """Stand-in for a real packet struct class."""


class PacketB:
    """Stand-in for a real packet struct class."""


def make_metadata_cls(packet_info: dict, common_field_map: dict | None = None) -> type:
    """
    Build a throwaway class exposing a `packetInfo` attribute, mimicking
    the `metadata_cls` argument CentralStorage expects.
    """
    return type(
        "FakeMeta",
        (),
        {
            "packetInfo": packet_info,
            "commonFieldMap": common_field_map or {},
        },
    )


def make_packet(name: str, **extra) -> SimpleNamespace:
    """
    Build a SimpleNamespace that behaves like the objects `_write` expects:
    it needs a `.__name__` attribute equal to a registered packet name.
    """
    ns = SimpleNamespace(**extra)
    ns.__name__ = name  # instance attribute, not the type's dunder
    return ns


def expected_common_data(storage, values: dict[str, object] | None = None) -> SimpleNamespace:
    """Build common-data expectations from the storage's configured fields."""
    values = values or {}
    return SimpleNamespace(
        **{
            attribute: values.get(attribute, [])
            for attribute in storage.common_attributes
        }
    )


def expected_latest_common_data(storage, values: dict[str, object] | None = None) -> SimpleNamespace:
    """Build latest common-data expectations from the storage's configured fields."""
    values = values or {}
    return SimpleNamespace(
        **{
            attribute: values.get(attribute)
            for attribute in storage.common_attributes
        }
    )


@pytest.fixture
def metadata_cls():
    """Two packet ids, three packet classes, one name duplicated across ids."""
    return make_metadata_cls(
        {
            1: [PacketA],
            2: [PacketB, PacketA],  # PacketA duplicated on purpose
        },
        {"speed": "speed", "engineRPM": "rpm", "gear": "gear"},
    )


@pytest.fixture
def storage(metadata_cls):
    return CentralStorage(metadata_cls)


# --------------------------------------------------------------------------
# 1. Happy path tests
# --------------------------------------------------------------------------


class TestCentralStorageHappyPath:
    def test_init_registers_all_packet_names(self, storage):
        assert set(storage.all_data.keys()) == {"PacketA", "PacketB"}
        assert set(storage.latest_data.keys()) == {"PacketA", "PacketB"}

    def test_init_starts_empty(self, storage):
        assert storage.all_data["PacketA"] == []
        assert storage.latest_data["PacketA"] is None

    def test_init_starts_common_data_empty(self, storage):
        assert storage.all_common_data == expected_common_data(storage)
        assert storage.latest_common_data == expected_latest_common_data(storage)

    def test_write_appends_and_updates_latest(self, storage):
        pkt = make_packet("PacketA", speed=100, rpm=8_000, gear=3)
        storage._write(pkt)

        assert storage.all_data["PacketA"] == [pkt]
        assert storage.latest_data["PacketA"] is pkt
        expected_values = {
            common_key: getattr(pkt, mapped_key)
            for common_key, mapped_key in storage.mapped_data.items()
            if common_key in storage.common_attributes and hasattr(pkt, mapped_key)
        }
        assert storage.all_common_data == expected_common_data(
            storage,
            {common_key: [value] for common_key, value in expected_values.items()},
        )
        assert storage.latest_common_data == expected_latest_common_data(storage, expected_values)

    def test_write_multiple_appends_in_order(self, storage):
        pkt1 = make_packet("PacketA", lap=1)
        pkt2 = make_packet("PacketA", lap=2)
        storage._write(pkt1)
        storage._write(pkt2)

        assert storage.all_data["PacketA"] == [pkt1, pkt2]
        assert storage.latest_data["PacketA"] is pkt2  # most recent wins

    def test_snapshot_shape_and_keys(self, storage):
        snap = storage.snapshot()
        assert set(snap.keys()) == {"allData", "latestData", "allCommonData", "latestCommonData"}
        assert snap["allData"] == storage.all_data
        assert snap["latestData"] == storage.latest_data
        assert snap["allCommonData"] == storage.all_common_data
        assert snap["latestCommonData"] == storage.latest_common_data

    def test_snapshot_reflects_writes(self, storage):
        pkt = make_packet("PacketB", rpm=8000, speed=120, gear=4)
        storage._write(pkt)
        snap = storage.snapshot()

        assert snap["latestData"]["PacketB"] is pkt
        assert snap["allData"]["PacketB"] == [pkt]
        expected_values = {
            common_key: getattr(pkt, mapped_key)
            for common_key, mapped_key in storage.mapped_data.items()
            if common_key in storage.common_attributes and hasattr(pkt, mapped_key)
        }
        assert snap["allCommonData"] == expected_common_data(
            storage,
            {common_key: [value] for common_key, value in expected_values.items()},
        )
        assert snap["latestCommonData"] == expected_latest_common_data(storage, expected_values)


# --------------------------------------------------------------------------
# 2. Edge case tests
# --------------------------------------------------------------------------


class TestCentralStorageEdgeCases:
    def test_empty_packet_info_produces_empty_storage(self):
        empty_meta = make_metadata_cls({})
        s = CentralStorage(empty_meta)
        assert s.all_data == {}
        assert s.latest_data == {}

    def test_duplicate_packet_name_not_duplicated_in_dicts(self, storage):
        # PacketA appears under both packet id 1 and 2 in the fixture;
        # it must only occupy a single slot in each dict.
        assert list(storage.all_data.keys()).count("PacketA") == 1

    def test_write_none_is_a_no_op(self, storage):
        storage._write(None)
        assert storage.all_data == {"PacketA": [], "PacketB": []}
        assert storage.latest_data == {"PacketA": None, "PacketB": None}

    def test_snapshot_returns_shallow_copy_not_same_object(self, storage):
        snap = storage.snapshot()
        snap["allData"]["PacketA"].append("mutated")

        # The top-level dict was copied, so this key in the *original*
        # dict now shares the same list object (shallow copy) -- verifying
        # that behaviour explicitly avoids false assumptions about depth.
        assert storage.all_data["PacketA"] == ["mutated"]

        # But replacing/removing a top-level key on the snapshot must NOT
        # affect the original, proving the outer dict itself was copied.
        del snap["allData"]["PacketA"]
        assert "PacketA" in storage.all_data

    def test_snapshot_copies_common_data_lists(self, storage):
        common_key = next(iter(storage.common_attributes))
        mapped_key = storage.mapped_data[common_key]
        storage._write(make_packet("PacketA", **{mapped_key: 100}))
        snap = storage.snapshot()

        getattr(snap["allCommonData"], common_key).append("mutated")

        assert getattr(snap["allCommonData"], common_key) == [100, "mutated"]
        assert getattr(storage.all_common_data, common_key) == [100]

    def test_write_unknown_packet_name_raises_keyerror(self, storage):
        rogue = make_packet("NotRegisteredPacket")
        with pytest.raises(KeyError):
            storage._write(rogue)


# --------------------------------------------------------------------------
# 3. Error handling tests
# --------------------------------------------------------------------------


class TestCentralStorageErrorHandling:
    def test_metadata_cls_missing_packet_info_raises(self):
        bad_cls = type("BadMeta", (), {})
        with pytest.raises(AttributeError):
            CentralStorage(bad_cls)

    def test_write_object_without_dunder_name_raises(self, storage):
        # A plain SimpleNamespace has no usable `.__name__` attribute set,
        # so accessing it inside `_write` should fail predictably.
        with pytest.raises(AttributeError):
            storage._write(SimpleNamespace(foo="bar"))


# --------------------------------------------------------------------------
# 4. Integration / concurrency tests
# --------------------------------------------------------------------------


class TestCentralStorageConcurrency:
    def test_concurrent_writes_are_thread_safe(self, storage):
        """
        Spin up several writer threads hammering `_write` simultaneously and
        confirm no updates are lost -- this is the whole point of the
        internal RLock.
        """
        writes_per_thread = 200
        thread_count = 8

        def writer():
            for i in range(writes_per_thread):
                storage._write(make_packet("PacketA", i=i))

        threads = [threading.Thread(target=writer) for _ in range(thread_count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        assert len(storage.all_data["PacketA"]) == writes_per_thread * thread_count
        assert storage.latest_data["PacketA"] is not None

    def test_readonly_storage_sees_live_updates(self, storage):
        ro = ReadOnlyStorage(storage)
        assert ro.snapshot()["latestData"]["PacketA"] is None

        pkt = make_packet("PacketA", value=42)
        storage._write(pkt)

        assert ro.snapshot()["latestData"]["PacketA"] is pkt


# --------------------------------------------------------------------------
# ReadOnlyStorage-specific tests
# --------------------------------------------------------------------------


class TestReadOnlyStorage:
    def test_snapshot_delegates_to_central_storage(self, storage):
        ro = ReadOnlyStorage(storage)
        assert ro.snapshot() == storage.snapshot()

    def test_no_write_method_exposed(self, storage):
        ro = ReadOnlyStorage(storage)
        assert not hasattr(ro, "_write")
        assert not hasattr(ro, "all_data")
        assert not hasattr(ro, "latest_data")

    def test_iter_returns_self(self, storage):
        ro = ReadOnlyStorage(storage)
        assert iter(ro) is ro

    def test_next_returns_latest_data_dict(self, storage):
        ro = ReadOnlyStorage(storage)
        
        first = next(ro)
        expected1 = {
            "allData": {"PacketA": [], "PacketB": []},
            "latestData": {"PacketA": None, "PacketB": None},
            "allCommonData": expected_common_data(storage),
            "latestCommonData": expected_latest_common_data(storage),
        }
        assert first == expected1

        pkt = make_packet("PacketB", n=1)
        storage._write(pkt)
        
        second = next(ro)
        expected2 = {
            "allData": {"PacketA": [], "PacketB": [pkt]},
            "latestData": {"PacketA": None, "PacketB": pkt},
            "allCommonData": expected_common_data(storage),
            "latestCommonData": expected_latest_common_data(storage),
        }
        assert second == expected2

    def test_repeated_iteration_never_raises_stopiteration(self, storage):
        ro = ReadOnlyStorage(storage)
        # A "live" iterator like this should be usable indefinitely rather
        # than exhausting after a fixed number of items.
        for _ in range(5):
            next(ro)  # should not raise


# --------------------------------------------------------------------------
# 5. Lightweight performance smoke test
# --------------------------------------------------------------------------


class TestPerformance:
    def test_bulk_write_and_snapshot_completes_quickly(self, storage):
        start = time.perf_counter()
        for i in range(5_000):
            storage._write(make_packet("PacketA", i=i))
        for _ in range(1_000):
            storage.snapshot()
        elapsed = time.perf_counter() - start

        # Generous ceiling -- this is a smoke test for gross regressions,
        # not a strict performance benchmark.
        assert elapsed < 5.0
        assert len(storage.all_data["PacketA"]) == 5_000
