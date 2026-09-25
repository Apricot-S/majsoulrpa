import asyncio
import datetime
import uuid
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from typing import Protocol

from majsoulrpa._clock import Clock, utc_now
from majsoulrpa.sniffer.correlator import Direction


class PlaywrightCaptureError(RuntimeError):
    """Base class for Playwright frame capture failures."""


class UnsupportedWebSocketFrameError(PlaywrightCaptureError):
    """Raised when Playwright observes a non-binary frame."""


class CaptureQueueOverflowError(PlaywrightCaptureError):
    """Raised when frame capture cannot enqueue an event."""


@dataclass(frozen=True, slots=True)
class CapturedFrame:
    connection_id: str
    frame_sequence: int
    direction: Direction
    observed_at: datetime.datetime
    payload: bytes


@dataclass(frozen=True, slots=True)
class CapturedConnectionClosed:
    connection_id: str
    observed_at: datetime.datetime


type CaptureEvent = CapturedFrame | CapturedConnectionClosed


class EventEmitterLike(Protocol):
    def on(self, event: str, callback: Callable[..., None]) -> None: ...
    def remove_listener(
        self,
        event: str,
        callback: Callable[..., None],
    ) -> None: ...


type ConnectionIDFactory = Callable[[], str]
type _QueueItem = CaptureEvent | PlaywrightCaptureError
type _WebSocketListeners = tuple[
    EventEmitterLike,
    Callable[..., None],
    Callable[..., None],
    Callable[..., None],
]


def _new_id() -> str:
    return str(uuid.uuid4())


class PlaywrightFrameCapture:
    def __init__(
        self,
        *,
        queue_size: int = 1024,
        clock: Clock = utc_now,
        connection_id_factory: ConnectionIDFactory = _new_id,
    ) -> None:
        if isinstance(queue_size, bool) or queue_size <= 0:
            msg = "queue_size must be a positive integer."
            raise ValueError(msg)
        self._queue: asyncio.Queue[_QueueItem] = asyncio.Queue(
            maxsize=queue_size,
        )
        self._clock = clock
        self._connection_id_factory = connection_id_factory
        self._next_frame_sequence = 1
        self._failure: PlaywrightCaptureError | None = None
        self._page: EventEmitterLike | None = None
        self._page_listener: Callable[..., None] | None = None
        self._websocket_listeners: list[_WebSocketListeners] = []

    async def start(self, page: EventEmitterLike) -> None:
        if self._page is not None:
            msg = "Playwright frame capture is already started."
            raise PlaywrightCaptureError(msg)

        def on_websocket(websocket: EventEmitterLike) -> None:
            self._observe_websocket(websocket)

        page.on("websocket", on_websocket)
        self._page = page
        self._page_listener = on_websocket

    async def receive(self) -> CaptureEvent:
        if self._failure is not None:
            raise self._failure

        item = await self._queue.get()
        if isinstance(item, PlaywrightCaptureError):
            raise item
        return item

    async def stop(self) -> None:
        page = self._page
        page_listener = self._page_listener
        self._page = None
        self._page_listener = None

        listeners = self._websocket_listeners
        self._websocket_listeners = []
        removals: list[tuple[EventEmitterLike, str, Callable[..., None]]] = []
        if page is not None and page_listener is not None:
            removals.append((page, "websocket", page_listener))
        for websocket, on_sent, on_received, on_close in listeners:
            removals.extend(
                (
                    (websocket, "framesent", on_sent),
                    (websocket, "framereceived", on_received),
                    (websocket, "close", on_close),
                ),
            )

        _remove_listeners(removals)

    def _observe_websocket(self, websocket: EventEmitterLike) -> None:
        if any(
            registered is websocket
            for registered, *_callbacks in self._websocket_listeners
        ):
            return

        connection_id = self._connection_id_factory()

        def on_sent(payload: bytes | str) -> None:
            self._observe_frame(
                connection_id=connection_id,
                direction=Direction.OUTBOUND,
                payload=payload,
            )

        def on_received(payload: bytes | str) -> None:
            self._observe_frame(
                connection_id=connection_id,
                direction=Direction.INBOUND,
                payload=payload,
            )

        def on_close() -> None:
            try:
                self._enqueue(
                    CapturedConnectionClosed(
                        connection_id=connection_id,
                        observed_at=self._clock(),
                    ),
                )
            finally:
                self._remove_websocket_listeners(websocket)

        registered: list[
            tuple[EventEmitterLike, str, Callable[..., None]]
        ] = []
        try:
            for event, callback in (
                ("framesent", on_sent),
                ("framereceived", on_received),
                ("close", on_close),
            ):
                websocket.on(event, callback)
                registered.append((websocket, event, callback))
        except BaseException:
            _remove_listeners(list(reversed(registered)))
            raise
        self._websocket_listeners.append(
            (websocket, on_sent, on_received, on_close),
        )

    def _remove_websocket_listeners(
        self,
        websocket: EventEmitterLike,
    ) -> None:
        for index, listeners in enumerate(self._websocket_listeners):
            registered, on_sent, on_received, on_close = listeners
            if registered is not websocket:
                continue

            del self._websocket_listeners[index]
            _remove_listeners(
                [
                    (websocket, "framesent", on_sent),
                    (websocket, "framereceived", on_received),
                    (websocket, "close", on_close),
                ],
            )
            return

    def _observe_frame(
        self,
        *,
        connection_id: str,
        direction: Direction,
        payload: bytes | str,
    ) -> None:
        if not isinstance(payload, bytes):
            msg = "Playwright WebSocket frame must be binary."
            self._record_failure(UnsupportedWebSocketFrameError(msg))
            return

        event = CapturedFrame(
            connection_id=connection_id,
            frame_sequence=self._next_frame_sequence,
            direction=direction,
            observed_at=self._clock(),
            payload=payload,
        )
        self._next_frame_sequence += 1
        self._enqueue(event)

    def _enqueue(self, event: CaptureEvent) -> None:
        if self._failure is not None:
            return
        try:
            self._queue.put_nowait(event)
        except asyncio.QueueFull:
            msg = "Playwright frame capture queue is full."
            self._record_failure(CaptureQueueOverflowError(msg))

    def _record_failure(self, error: PlaywrightCaptureError) -> None:
        if self._failure is not None:
            return
        self._failure = error
        with suppress(asyncio.QueueFull):
            self._queue.put_nowait(error)


def _remove_listeners(
    removals: list[tuple[EventEmitterLike, str, Callable[..., None]]],
) -> None:
    errors: list[BaseException] = []
    for emitter, event, callback in removals:
        try:
            emitter.remove_listener(event, callback)
        except BaseException as error:  # noqa: BLE001
            # Finish cleanup, then propagate every failure below.
            errors.append(error)

    if len(errors) == 1:
        raise errors[0]
    if errors:
        msg = "Playwright listener cleanup failed."
        raise BaseExceptionGroup(msg, errors)
