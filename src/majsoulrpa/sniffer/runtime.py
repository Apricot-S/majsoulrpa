from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Protocol, cast

import zmq.asyncio

from majsoulrpa.config import AppConfig
from majsoulrpa.sniffer.correlator import CorrelatedMessage
from majsoulrpa.sniffer.playwright import (
    CaptureEvent,
    EventEmitterLike,
    PlaywrightFrameCapture,
)
from majsoulrpa.sniffer.worker import SnifferWorker
from majsoulrpa.sniffer.zmq import (
    AsyncZmqContextLike,
    ZmqSnifferPublisher,
)


class TerminableContext(Protocol):
    def term(self) -> None: ...


class CaptureBackend(Protocol):
    async def start(self, page: EventEmitterLike) -> None: ...
    async def receive(self) -> CaptureEvent: ...
    async def stop(self) -> None: ...


class PublisherBackend(Protocol):
    async def bind(self) -> None: ...
    async def publish(self, message: CorrelatedMessage) -> object: ...
    async def stop(self) -> None: ...


class WorkerBackend(Protocol):
    async def run(self) -> None: ...
    async def stop(self) -> None: ...


type ContextFactory = Callable[[], TerminableContext]
type CaptureFactory = Callable[[], CaptureBackend]
type PublisherFactory = Callable[
    [TerminableContext, AppConfig],
    PublisherBackend,
]
type WorkerFactory = Callable[
    [CaptureBackend, PublisherBackend],
    WorkerBackend,
]


class BrowserHostSnifferBackend:
    def __init__(
        self,
        config: AppConfig,
        *,
        context_factory: ContextFactory | None = None,
        capture_factory: CaptureFactory | None = None,
        publisher_factory: PublisherFactory | None = None,
        worker_factory: WorkerFactory | None = None,
    ) -> None:
        self._config = config
        self._context_factory = context_factory or _make_context
        self._capture_factory = capture_factory or PlaywrightFrameCapture
        self._publisher_factory = publisher_factory or _make_publisher
        self._worker_factory = worker_factory or _make_worker
        self._context: TerminableContext | None = None
        self._capture: CaptureBackend | None = None
        self._publisher: PublisherBackend | None = None
        self._worker: WorkerBackend | None = None

    async def start(self, page: object) -> None:
        if self._context is not None:
            msg = "Browser host Sniffer is already started."
            raise RuntimeError(msg)

        context = self._context_factory()
        capture: CaptureBackend | None = None
        publisher: PublisherBackend | None = None
        try:
            created_capture = self._capture_factory()
            capture = created_capture
            publisher = self._publisher_factory(context, self._config)
            worker = self._worker_factory(created_capture, publisher)
            await publisher.bind()
            await created_capture.start(cast("EventEmitterLike", page))
        except BaseException:
            await _cleanup_resources(
                context=context,
                capture=capture,
                publisher=publisher,
            )
            raise

        self._context = context
        self._capture = capture
        self._publisher = publisher
        self._worker = worker

    async def run(self) -> None:
        if self._worker is None:
            msg = "Browser host Sniffer is not started."
            raise RuntimeError(msg)
        await self._worker.run()

    async def stop(self) -> None:
        context = self._context
        capture = self._capture
        publisher = self._publisher
        worker = self._worker
        self._context = None
        self._capture = None
        self._publisher = None
        self._worker = None

        if context is None:
            return

        async with AsyncExitStack() as stack:
            stack.callback(context.term)
            if publisher is not None:
                stack.push_async_callback(publisher.stop)
            if capture is not None:
                stack.push_async_callback(capture.stop)
            if worker is not None:
                await worker.stop()


async def _cleanup_resources(
    *,
    context: TerminableContext,
    capture: CaptureBackend | None,
    publisher: PublisherBackend | None,
) -> None:
    async with AsyncExitStack() as stack:
        stack.callback(context.term)
        if publisher is not None:
            stack.push_async_callback(publisher.stop)
        if capture is not None:
            stack.push_async_callback(capture.stop)


def _make_context() -> TerminableContext:
    return zmq.asyncio.Context()


def _make_publisher(
    context: TerminableContext,
    config: AppConfig,
) -> PublisherBackend:
    return ZmqSnifferPublisher(
        context=cast("AsyncZmqContextLike", context),
        config=config,
    )


def _make_worker(
    capture: CaptureBackend,
    publisher: PublisherBackend,
) -> WorkerBackend:
    return SnifferWorker(capture=capture, publisher=publisher)
