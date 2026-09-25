import asyncio
import datetime
from collections.abc import Callable

import pytest

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.playwright import (
    CapturedConnectionClosed,
    CapturedFrame,
    CaptureQueueOverflowError,
    PlaywrightCaptureError,
    PlaywrightFrameCapture,
    UnsupportedWebSocketFrameError,
)

OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


class FakeEventEmitter:
    def __init__(self) -> None:
        self.listeners: dict[str, list[Callable[..., None]]] = {}

    def on(self, event: str, callback: Callable[..., None]) -> None:
        self.listeners.setdefault(event, []).append(callback)

    def remove_listener(
        self,
        event: str,
        callback: Callable[..., None],
    ) -> None:
        self.listeners[event].remove(callback)

    def emit(self, event: str, *args: object) -> None:
        for callback in list(self.listeners.get(event, [])):
            callback(*args)

    def listener_count(self, event: str) -> int:
        return len(self.listeners.get(event, []))


def _connection_ids(*values: str) -> Callable[[], str]:
    iterator = iter(values)
    return lambda: next(iterator)


class FalseyCallable[T]:
    def __init__(self, value: T) -> None:
        self._value = value

    def __bool__(self) -> bool:
        return False

    def __call__(self) -> T:
        return self._value


class FailingRemoveEmitter(FakeEventEmitter):
    def __init__(self, event: str, error: RuntimeError) -> None:
        super().__init__()
        self._event = event
        self._error = error

    def remove_listener(
        self,
        event: str,
        callback: Callable[..., None],
    ) -> None:
        if event == self._event:
            raise self._error
        super().remove_listener(event, callback)


class FailingRegistrationEmitter(FakeEventEmitter):
    def __init__(self, failed_event: str) -> None:
        super().__init__()
        self.failed_event = failed_event
        self.error = RuntimeError("synthetic registration failure")

    def on(self, event: str, callback: Callable[..., None]) -> None:
        if event == self.failed_event:
            raise self.error
        super().on(event, callback)


class FailingRegistrationAndRemovalEmitter(FailingRegistrationEmitter):
    def __init__(self) -> None:
        super().__init__("close")
        self.cleanup_error = RuntimeError("synthetic rollback failure")

    def remove_listener(
        self,
        event: str,
        callback: Callable[..., None],
    ) -> None:
        if event == "framereceived":
            raise self.cleanup_error
        super().remove_listener(event, callback)


def test_page_registration_failure_does_not_mark_capture_started() -> None:
    async def run() -> None:
        failed_page = FailingRegistrationEmitter("websocket")
        page = FakeEventEmitter()
        capture = PlaywrightFrameCapture()

        with pytest.raises(RuntimeError) as caught:
            await capture.start(failed_page)

        assert caught.value is failed_page.error
        assert failed_page.listener_count("websocket") == 0
        await capture.start(page)
        assert page.listener_count("websocket") == 1
        await capture.stop()
        assert page.listener_count("websocket") == 0

    asyncio.run(run())


@pytest.mark.parametrize(
    "same_page", [True, False], ids=["same-page", "other-page"]
)
def test_repeated_start_preserves_original_page(*, same_page: bool) -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        other_page = page if same_page else FakeEventEmitter()
        capture = PlaywrightFrameCapture()
        await capture.start(page)

        with pytest.raises(PlaywrightCaptureError, match="already started"):
            await capture.start(other_page)

        assert page.listener_count("websocket") == 1
        assert other_page.listener_count("websocket") == int(same_page)
        await capture.stop()
        assert page.listener_count("websocket") == 0
        assert other_page.listener_count("websocket") == 0

    asyncio.run(run())


def test_registration_and_rollback_failures_are_both_reported() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FailingRegistrationAndRemovalEmitter()
        capture = PlaywrightFrameCapture()
        await capture.start(page)

        with pytest.raises(RuntimeError) as caught:
            page.emit("websocket", websocket)

        assert caught.value is websocket.cleanup_error
        assert caught.value.__context__ is websocket.error
        assert websocket.listener_count("framesent") == 0
        assert websocket.listener_count("framereceived") == 1
        await capture.stop()

    asyncio.run(run())


@pytest.mark.parametrize(
    "failed_event", ["framesent", "framereceived", "close"]
)
def test_websocket_registration_failure_removes_registered_listeners(
    failed_event: str,
) -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FailingRegistrationEmitter(failed_event)
        capture = PlaywrightFrameCapture()
        await capture.start(page)
        with pytest.raises(RuntimeError) as caught:
            page.emit("websocket", websocket)
        assert caught.value is websocket.error
        for event in ("framesent", "framereceived", "close"):
            assert websocket.listener_count(event) == 0
        await capture.stop()

    asyncio.run(run())


@pytest.mark.parametrize(
    "failed_event",
    ["websocket", "framesent", "framereceived", "close"],
)
def test_stop_attempts_remaining_removals_after_failure(
    failed_event: str,
) -> None:
    async def run() -> None:
        error = RuntimeError("synthetic removal failure")
        page = FailingRemoveEmitter(failed_event, error)
        websocket = FailingRemoveEmitter(failed_event, error)
        other_websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture()
        await capture.start(page)
        page.emit("websocket", websocket)
        page.emit("websocket", other_websocket)

        with pytest.raises(RuntimeError) as caught:
            await capture.stop()

        assert caught.value is error
        assert page.listener_count("websocket") == int(
            failed_event == "websocket"
        )
        for event in ("framesent", "framereceived", "close"):
            assert websocket.listener_count(event) == int(
                event == failed_event
            )
            assert other_websocket.listener_count(event) == 0

    asyncio.run(run())


@pytest.mark.parametrize(
    "failed_event", ["framesent", "framereceived", "close"]
)
def test_connection_close_finishes_cleanup_after_removal_failure(
    failed_event: str,
) -> None:
    async def run() -> None:
        error = RuntimeError("synthetic removal failure")
        page = FakeEventEmitter()
        websocket = FailingRemoveEmitter(failed_event, error)
        other_websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            clock=lambda: OBSERVED_AT,
            connection_id_factory=_connection_ids(
                "connection-1", "connection-2"
            ),
        )
        await capture.start(page)
        page.emit("websocket", websocket)
        page.emit("websocket", other_websocket)

        with pytest.raises(RuntimeError) as caught:
            websocket.emit("close")

        assert caught.value is error
        for event in ("framesent", "framereceived", "close"):
            assert websocket.listener_count(event) == int(
                event == failed_event
            )
            assert other_websocket.listener_count(event) == 1
        assert await capture.receive() == CapturedConnectionClosed(
            connection_id="connection-1",
            observed_at=OBSERVED_AT,
        )
        await capture.stop()
        for event in ("framesent", "framereceived", "close"):
            assert other_websocket.listener_count(event) == 0

    asyncio.run(run())


def test_stop_reports_multiple_removal_failures_together() -> None:
    async def run() -> None:
        page_error = RuntimeError("synthetic page removal failure")
        websocket_error = RuntimeError("synthetic WebSocket removal failure")
        page = FailingRemoveEmitter("websocket", page_error)
        websocket = FailingRemoveEmitter("framesent", websocket_error)
        capture = PlaywrightFrameCapture()
        await capture.start(page)
        page.emit("websocket", websocket)

        with pytest.raises(ExceptionGroup) as caught:
            await capture.stop()

        assert caught.value.exceptions == (page_error, websocket_error)
        assert websocket.listener_count("framereceived") == 0
        assert websocket.listener_count("close") == 0

    asyncio.run(run())


def test_capture_uses_falsey_clock_and_connection_id_factory() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            clock=FalseyCallable(OBSERVED_AT),
            connection_id_factory=FalseyCallable("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)
        websocket.emit("framesent", b"synthetic")
        websocket.emit("close")

        assert await capture.receive() == CapturedFrame(
            connection_id="connection-1",
            frame_sequence=1,
            direction=Direction.OUTBOUND,
            observed_at=OBSERVED_AT,
            payload=b"synthetic",
        )
        assert await capture.receive() == CapturedConnectionClosed(
            connection_id="connection-1",
            observed_at=OBSERVED_AT,
        )
        await capture.stop()

    asyncio.run(run())


def test_capture_observes_sent_and_received_binary_frames() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            clock=lambda: OBSERVED_AT,
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)

        websocket.emit("framesent", b"synthetic-outbound")
        websocket.emit("framereceived", b"synthetic-inbound")

        assert await capture.receive() == CapturedFrame(
            connection_id="connection-1",
            frame_sequence=1,
            direction=Direction.OUTBOUND,
            observed_at=OBSERVED_AT,
            payload=b"synthetic-outbound",
        )
        assert await capture.receive() == CapturedFrame(
            connection_id="connection-1",
            frame_sequence=2,
            direction=Direction.INBOUND,
            observed_at=OBSERVED_AT,
            payload=b"synthetic-inbound",
        )

    asyncio.run(run())


def test_capture_assigns_connection_ids_and_global_frame_sequence() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        first_websocket = FakeEventEmitter()
        second_websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            clock=lambda: OBSERVED_AT,
            connection_id_factory=_connection_ids(
                "connection-1",
                "connection-2",
            ),
        )
        await capture.start(page)
        page.emit("websocket", first_websocket)
        page.emit("websocket", second_websocket)

        second_websocket.emit("framesent", b"second")
        first_websocket.emit("framereceived", b"first")

        second = await capture.receive()
        first = await capture.receive()
        assert isinstance(second, CapturedFrame)
        assert isinstance(first, CapturedFrame)
        assert (second.connection_id, second.frame_sequence) == (
            "connection-2",
            1,
        )
        assert (first.connection_id, first.frame_sequence) == (
            "connection-1",
            2,
        )

    asyncio.run(run())


def test_capture_emits_connection_close_event() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            clock=lambda: OBSERVED_AT,
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)

        websocket.emit("close")

        assert await capture.receive() == CapturedConnectionClosed(
            connection_id="connection-1",
            observed_at=OBSERVED_AT,
        )
        assert websocket.listener_count("framesent") == 0
        assert websocket.listener_count("framereceived") == 0
        assert websocket.listener_count("close") == 0
        await capture.stop()

    asyncio.run(run())


def test_capture_does_not_register_same_websocket_twice() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)

        page.emit("websocket", websocket)
        page.emit("websocket", websocket)

        assert websocket.listener_count("framesent") == 1
        assert websocket.listener_count("framereceived") == 1
        assert websocket.listener_count("close") == 1

    asyncio.run(run())


def test_connection_close_cleans_up_listeners_when_queue_overflows() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            queue_size=1,
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)
        websocket.emit("framesent", b"fill-queue")

        websocket.emit("close")

        with pytest.raises(CaptureQueueOverflowError):
            await capture.receive()
        assert websocket.listener_count("framesent") == 0
        assert websocket.listener_count("framereceived") == 0
        assert websocket.listener_count("close") == 0
        await capture.stop()

    asyncio.run(run())


@pytest.mark.parametrize("event", ["framesent", "framereceived"])
def test_capture_rejects_text_frames(event: str) -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)

        websocket.emit(event, "synthetic-text")

        with pytest.raises(
            UnsupportedWebSocketFrameError,
            match="binary",
        ):
            await capture.receive()

    asyncio.run(run())


def test_capture_queue_overflow_is_fatal() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            queue_size=1,
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)

        websocket.emit("framesent", b"first")
        websocket.emit("framesent", b"second")

        with pytest.raises(CaptureQueueOverflowError, match="queue is full"):
            await capture.receive()

    asyncio.run(run())


@pytest.mark.parametrize(
    ("payload", "error_type"),
    [
        pytest.param(b"overflow", CaptureQueueOverflowError, id="overflow"),
        pytest.param(
            "synthetic-text", UnsupportedWebSocketFrameError, id="text"
        ),
    ],
)
def test_waiting_receive_prioritizes_failure_over_queued_frame(
    payload: bytes | str,
    error_type: type[RuntimeError],
) -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(queue_size=1)
        await capture.start(page)
        page.emit("websocket", websocket)
        receiver = asyncio.create_task(capture.receive())
        await asyncio.sleep(0)
        assert not receiver.done()

        websocket.emit("framesent", b"first")
        websocket.emit("framesent", payload)

        with pytest.raises(error_type):
            await receiver
        with pytest.raises(error_type):
            await capture.receive()
        await capture.stop()

    asyncio.run(run())


def test_capture_reuses_queue_capacity_after_receive() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(queue_size=1)
        await capture.start(page)
        page.emit("websocket", websocket)

        websocket.emit("framesent", b"first")
        first = await capture.receive()
        websocket.emit("framereceived", b"second")
        second = await capture.receive()

        assert isinstance(first, CapturedFrame)
        assert isinstance(second, CapturedFrame)
        assert (first.payload, second.payload) == (b"first", b"second")
        assert (first.frame_sequence, second.frame_sequence) == (1, 2)
        await capture.stop()

    asyncio.run(run())


def test_stop_removes_page_and_websocket_listeners() -> None:
    async def run() -> None:
        page = FakeEventEmitter()
        websocket = FakeEventEmitter()
        capture = PlaywrightFrameCapture(
            connection_id_factory=_connection_ids("connection-1"),
        )
        await capture.start(page)
        page.emit("websocket", websocket)

        await capture.stop()
        await capture.stop()

        assert page.listener_count("websocket") == 0
        assert websocket.listener_count("framesent") == 0
        assert websocket.listener_count("framereceived") == 0
        assert websocket.listener_count("close") == 0

    asyncio.run(run())


@pytest.mark.parametrize(
    "queue_size",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(True, id="boolean-true"),
        pytest.param(False, id="boolean-false"),
    ],
)
def test_capture_rejects_invalid_queue_size(queue_size: int) -> None:
    with pytest.raises(ValueError, match="queue_size"):
        PlaywrightFrameCapture(queue_size=queue_size)
