"""
Pytest suite for threads.py: ThreadSupervisor.

Run with:  pytest test_threads.py -v
"""

# from __future__ import annotations

import logging
import threading
import time
from unittest.mock import MagicMock, patch

import pytest

from ..src.RaceTelemetry.threads import (
    ThreadSupervisor,
)

# --------------------------------------------------------------------------
# Helpers / fixtures
# --------------------------------------------------------------------------


def dummy_worker(worker_id, ro_storage, stop_event):
    """A minimal, well-behaved worker function matching the expected signature."""
    while not stop_event.is_set():
        time.sleep(0.01)


class NotAFunction:
    """A callable *class* -- used to test the `isinstance(mainFunc, type)` guard."""

    def __call__(self, worker_id, ro_storage, stop_event):
        pass


@pytest.fixture
def supervisor():
    return ThreadSupervisor()


@pytest.fixture
def fake_ro_storage():
    return MagicMock(name="ReadOnlyStorage")


# --------------------------------------------------------------------------
# 1. Happy path tests
# --------------------------------------------------------------------------


class TestInitialState:
    def test_initial_state(self, supervisor):
        assert isinstance(supervisor.stop_event, threading.Event)
        assert supervisor.manually_stopped is False
        assert supervisor.network_thread is None
        assert supervisor.worker_threads == {}
        assert supervisor.workers_are_working is False
        assert supervisor.thread_count == 0
        assert supervisor.multi_threaded is True


class TestAddWorkerThread:
    def test_add_valid_worker_returns_true(self, supervisor, fake_ro_storage):
        result = supervisor.add_worker_thread(dummy_worker, fake_ro_storage)

        assert result is True
        assert supervisor.thread_count == 1
        assert 1 in supervisor.worker_threads
        assert isinstance(supervisor.worker_threads[1], threading.Thread)

    def test_added_thread_is_not_started_yet(self, supervisor, fake_ro_storage):
        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        assert not supervisor.worker_threads[1].is_alive()

    def test_add_multiple_workers_increments_ids_sequentially(self, supervisor, fake_ro_storage):
        for _ in range(3):
            supervisor.add_worker_thread(dummy_worker, fake_ro_storage)

        assert supervisor.thread_count == 3
        assert set(supervisor.worker_threads.keys()) == {1, 2, 3}

    # def test_worker_thread_receives_expected_kwargs(self, supervisor, fake_ro_storage):
    #     # Introspect via mock rather than Thread's private _kwargs attribute,
    #     # so this test doesn't depend on undocumented internals.
    #     with patch("threads.threading.Thread") as mock_thread_cls:
    #         supervisor.add_worker_thread(dummy_worker, fake_ro_storage)

    #     _, call_kwargs = mock_thread_cls.call_args
    #     assert call_kwargs["target"] is dummy_worker
    #     assert call_kwargs["kwargs"] == {
    #         "worker_id": 1,
    #         "ro_storage": fake_ro_storage,
    #         "stop_event": supervisor.stop_event,
    #     }
    #     assert call_kwargs["daemon"] is True


class TestManualStop:
    @pytest.mark.parametrize("value", [True, False])
    def test_valid_bool_sets_flag_and_returns_true(self, supervisor, value):
        # seed with the opposite value first so the change is observable
        supervisor.manually_stopped = not value
        assert supervisor.manual_stop(value) is True
        assert supervisor.manually_stopped is value


class TestIsMultiThreaded:
    def test_default_argument_sets_true(self, supervisor):
        supervisor.multi_threaded = False
        assert supervisor.is_multi_threaded() is True
        assert supervisor.multi_threaded is True

    @pytest.mark.parametrize("value", [True, False])
    def test_valid_bool_sets_flag(self, supervisor, value):
        assert supervisor.is_multi_threaded(value) is True
        assert supervisor.multi_threaded is value


class TestTriggerStopAndIsStillActive:
    def test_is_still_active_true_by_default(self, supervisor):
        assert supervisor._is_still_active() is True

    def test_trigger_stop_default_sets_event(self, supervisor):
        supervisor._trigger_stop()
        assert supervisor.stop_event.is_set() is True
        assert supervisor._is_still_active() is False

    def test_trigger_stop_false_clears_event(self, supervisor):
        supervisor.stop_event.set()
        supervisor._trigger_stop(False)
        assert supervisor.stop_event.is_set() is False
        assert supervisor._is_still_active() is True

    def test_wait_blocks_on_stop_event_and_returns_promptly_once_set(self, supervisor):
        start = time.perf_counter()
        supervisor.stop_event.set()
        supervisor._wait(2.0)  # should return almost immediately, event already set
        elapsed = time.perf_counter() - start
        assert elapsed < 0.5


# --------------------------------------------------------------------------
# 2. Edge case tests
# --------------------------------------------------------------------------


class TestAddWorkerThreadEdgeCases:
    def test_non_callable_main_func_returns_false(self, supervisor, fake_ro_storage, caplog):
        with caplog.at_level(logging.WARNING):
            result = supervisor.add_worker_thread("not a function", fake_ro_storage)

        assert result is False
        assert supervisor.thread_count == 0
        assert supervisor.worker_threads == {}
        assert "callable" in caplog.text.lower()

    def test_class_passed_as_main_func_returns_false(self, supervisor, fake_ro_storage, caplog):
        with caplog.at_level(logging.WARNING):
            result = supervisor.add_worker_thread(NotAFunction, fake_ro_storage)

        assert result is False
        assert supervisor.thread_count == 0

    def test_none_ro_storage_returns_false(self, supervisor, caplog):
        with caplog.at_level(logging.WARNING):
            result = supervisor.add_worker_thread(dummy_worker, None)

        assert result is False
        assert supervisor.thread_count == 0

    def test_falsy_but_not_none_ro_storage_returns_false(self, supervisor, caplog):
        # `if not ro_storage` treats any falsy object (e.g. an empty MagicMock
        # configured with __bool__ False, or 0 / "" / []) the same as None.
        with caplog.at_level(logging.WARNING):
            result = supervisor.add_worker_thread(dummy_worker, 0)
        assert result is False

    def test_add_worker_thread_count_not_incremented_on_failure(self, supervisor, fake_ro_storage):
        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)  # succeeds -> count 1
        supervisor.add_worker_thread("bad", fake_ro_storage)  # fails
        assert supervisor.thread_count == 1


class TestManualStopEdgeCases:
    @pytest.mark.parametrize("bad_value", [1, 0, "true", None, [], {}])
    def test_non_bool_returns_false_and_logs_error(self, supervisor, bad_value, caplog):
        original = supervisor.manually_stopped
        with caplog.at_level(logging.ERROR):
            result = supervisor.manual_stop(bad_value)

        assert result is False
        assert supervisor.manually_stopped == original  # unchanged
        assert "invalid type" in caplog.text.lower()


class TestIsMultiThreadedEdgeCases:
    @pytest.mark.parametrize("bad_value", [1, 0, "true", None, [], {}])
    def test_non_bool_returns_false_and_logs_error(self, supervisor, bad_value, caplog):
        original = supervisor.multi_threaded
        with caplog.at_level(logging.ERROR):
            result = supervisor.is_multi_threaded(bad_value)

        assert result is False
        assert supervisor.multi_threaded == original


# --------------------------------------------------------------------------
# 3. Error handling / lifecycle tests
# --------------------------------------------------------------------------


class TestStartThreads:
    def test_start_threads_starts_network_and_workers(self, supervisor, fake_ro_storage):
        started = threading.Event()

        def network_target():
            started.set()
            supervisor.stop_event.wait(1)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)

        assert started.wait(timeout=1) is True
        assert supervisor.network_thread.is_alive()
        assert supervisor.worker_threads[1].is_alive()
        assert supervisor.workers_are_working is True

        # cleanup
        supervisor._trigger_stop()
        supervisor.network_thread.join(timeout=1)
        supervisor.worker_threads[1].join(timeout=1)

    def test_start_threads_can_restart_after_stop(self, supervisor, fake_ro_storage):
        started = threading.Event()

        def network_target():
            started.set()
            supervisor.stop_event.wait(1)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)
        first_worker = supervisor.worker_threads[1]
        assert started.wait(timeout=1) is True
        supervisor._stop_threads()

        started.clear()
        supervisor._start_threads(network_target)

        assert supervisor.stop_event.is_set() is False
        assert supervisor.worker_threads[1] is not first_worker
        assert started.wait(timeout=1) is True
        assert supervisor.worker_threads[1].is_alive()

        supervisor._stop_threads()

    def test_start_threads_with_no_workers_still_starts_network(self, supervisor):
        started = threading.Event()

        def network_target():
            started.set()
            supervisor.stop_event.wait(1)

        supervisor._start_threads(network_target)
        assert started.wait(timeout=1) is True

        supervisor._trigger_stop()
        supervisor.network_thread.join(timeout=1)


class TestStopThreads:
    def test_stop_threads_noop_if_workers_not_working(self, supervisor):
        # workers_are_working is False by default -- nothing should blow up
        supervisor._stop_threads()
        assert supervisor.workers_are_working is False

    def test_stop_threads_noop_if_no_network_thread(self, supervisor):
        supervisor.workers_are_working = True
        supervisor.network_thread = None
        supervisor._stop_threads()  # should return early, not raise
        assert supervisor.workers_are_working is True  # untouched by early return

    def test_stop_threads_sets_stop_event_and_joins(self, supervisor, fake_ro_storage):
        def network_target():
            supervisor.stop_event.wait(2)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)

        supervisor._stop_threads()

        assert supervisor.stop_event.is_set() is True
        assert supervisor.workers_are_working is False
        assert not supervisor.network_thread.is_alive()
        assert not supervisor.worker_threads[1].is_alive()

    def test_stop_threads_warns_when_worker_does_not_stop_in_time(self, supervisor, caplog):
        def stubborn_worker(worker_id, ro_storage, stop_event):
            # ignores stop_event entirely, sleeps well past the join timeout
            time.sleep(5)

        def network_target():
            supervisor.stop_event.wait(2)

        supervisor.add_worker_thread(stubborn_worker, MagicMock())
        supervisor._start_threads(network_target)

        with caplog.at_level(logging.WARNING):
            supervisor._stop_threads()

        assert "did not stop in time" in caplog.text.lower()
        # the (still-running) stubborn thread is daemonic, so the process
        # can still exit cleanly; nothing further to assert/clean up here.


class TestWaitForStopSignal:
    def test_returns_and_stops_threads_when_stop_event_set_externally(self, supervisor, fake_ro_storage):
        def network_target():
            supervisor.stop_event.wait(5)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)

        def flip_stop_soon():
            time.sleep(0.2)
            supervisor.stop_event.set()

        threading.Thread(target=flip_stop_soon, daemon=True).start()

        start = time.perf_counter()
        supervisor._wait_for_stop_signal()
        elapsed = time.perf_counter() - start

        assert elapsed < 2.0
        assert supervisor.workers_are_working is False

    def test_keyboard_interrupt_triggers_cleanup(self, supervisor, fake_ro_storage):
        def network_target():
            supervisor.stop_event.wait(5)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)

        with patch.object(supervisor, "_wait", side_effect=KeyboardInterrupt):
            supervisor._wait_for_stop_signal()

        # `finally` block must still run `_stop_threads`
        assert supervisor.workers_are_working is False
        assert supervisor.stop_event.is_set() is True

    def test_manual_stop_prompts_for_quit_and_stops_on_q(self, supervisor, fake_ro_storage, monkeypatch):
        def network_target():
            supervisor.stop_event.wait(5)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)
        supervisor.manually_stopped = True

        monkeypatch.setattr("builtins.input", lambda *_: "q")

        supervisor._wait_for_stop_signal()

        assert supervisor.stop_event.is_set() is True
        assert supervisor.workers_are_working is False

    def test_manual_stop_prompt_declined_keeps_running_until_event_set(self, supervisor, fake_ro_storage, monkeypatch):
        """
        If the user answers anything other than 'q', the loop should keep
        polling rather than stopping immediately. We simulate a couple of
        declines before finally flipping the stop_event directly.
        """

        def network_target():
            supervisor.stop_event.wait(5)

        supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        supervisor._start_threads(network_target)
        supervisor.manually_stopped = True

        answers = iter(["n", "no", "q"])
        monkeypatch.setattr("builtins.input", lambda *_: next(answers, "q"))

        supervisor._wait_for_stop_signal()

        assert supervisor.stop_event.is_set() is True
        assert supervisor.workers_are_working is False


# --------------------------------------------------------------------------
# 4. Integration test: full add -> start -> stop lifecycle
# --------------------------------------------------------------------------


class TestFullLifecycleIntegration:
    def test_full_lifecycle_with_multiple_workers(self, supervisor, fake_ro_storage):
        seen_ids = []
        lock = threading.Lock()

        def recording_worker(worker_id, ro_storage, stop_event):
            with lock:
                seen_ids.append(worker_id)
            while not stop_event.is_set():
                time.sleep(0.01)

        for _ in range(4):
            assert supervisor.add_worker_thread(recording_worker, fake_ro_storage) is True

        def network_target():
            supervisor.stop_event.wait(2)

        supervisor._start_threads(network_target)
        time.sleep(0.2)  # let workers register themselves
        supervisor._stop_threads()

        assert sorted(seen_ids) == [1, 2, 3, 4]
        assert supervisor.workers_are_working is False
        assert all(not t.is_alive() for t in supervisor.worker_threads.values())


# --------------------------------------------------------------------------
# 5. Lightweight performance / stress test
# --------------------------------------------------------------------------


class TestPerformance:
    def test_adding_many_worker_threads_is_fast(self, supervisor, fake_ro_storage):
        start = time.perf_counter()
        for _ in range(500):
            supervisor.add_worker_thread(dummy_worker, fake_ro_storage)
        elapsed = time.perf_counter() - start

        assert supervisor.thread_count == 500
        assert elapsed < 2.0  # thread *object* creation only, none started
