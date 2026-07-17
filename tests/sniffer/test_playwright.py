import asyncio
import datetime
from collections.abc import Callable

import pytest

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.playwright import (
    CapturedConnectionClosed,
    CapturedFrame,
    CaptureQueueOverflowError,
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


def test_capture_rejects_nonpositive_queue_size() -> None:
    with pytest.raises(ValueError, match="queue_size"):
        PlaywrightFrameCapture(queue_size=0)
