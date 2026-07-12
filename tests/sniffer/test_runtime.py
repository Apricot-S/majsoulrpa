import asyncio

import pytest

from majsoulrpa.config import AppConfig
from majsoulrpa.sniffer.correlator import CorrelatedMessage
from majsoulrpa.sniffer.playwright import CaptureEvent
from majsoulrpa.sniffer.runtime import BrowserHostSnifferBackend


class ContextSpy:
    def __init__(self, events: list[str]) -> None:
        self.events = events

    def socket(self, socket_type: int) -> object:
        _ = socket_type
        msg = "not used by injected publisher"
        raise AssertionError(msg)

    def term(self) -> None:
        self.events.append("context_term")


class CaptureSpy:
    def __init__(
        self,
        events: list[str],
        *,
        start_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.start_error = start_error
        self.started_pages: list[object] = []

    async def start(self, page: object) -> None:
        self.events.append("capture_start")
        self.started_pages.append(page)
        if self.start_error is not None:
            raise self.start_error

    async def receive(self) -> CaptureEvent:
        msg = "not used by injected worker"
        raise AssertionError(msg)

    async def stop(self) -> None:
        self.events.append("capture_stop")


class PublisherSpy:
    def __init__(
        self,
        events: list[str],
        *,
        bind_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.bind_error = bind_error

    async def bind(self) -> None:
        self.events.append("publisher_bind")
        if self.bind_error is not None:
            raise self.bind_error

    async def publish(self, message: CorrelatedMessage) -> object:
        _ = message
        msg = "not used by injected worker"
        raise AssertionError(msg)

    async def stop(self) -> None:
        self.events.append("publisher_stop")


class WorkerSpy:
    def __init__(
        self,
        events: list[str],
        *,
        stop_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.stop_error = stop_error

    async def run(self) -> None:
        self.events.append("worker_run")

    async def stop(self) -> None:
        self.events.append("worker_stop")
        if self.stop_error is not None:
            raise self.stop_error


def _backend(
    events: list[str],
    *,
    capture: CaptureSpy | None = None,
    publisher: PublisherSpy | None = None,
    worker: WorkerSpy | None = None,
) -> tuple[
    BrowserHostSnifferBackend,
    CaptureSpy,
    PublisherSpy,
    WorkerSpy,
]:
    capture = capture or CaptureSpy(events)
    publisher = publisher or PublisherSpy(events)
    worker = worker or WorkerSpy(events)

    def context_factory() -> ContextSpy:
        events.append("context_create")
        return ContextSpy(events)

    backend = BrowserHostSnifferBackend(
        AppConfig(),
        context_factory=context_factory,
        capture_factory=lambda: capture,
        publisher_factory=lambda _context, _config: publisher,
        worker_factory=lambda _capture, _publisher: worker,
    )
    return backend, capture, publisher, worker


def test_backend_lazily_starts_publisher_before_capture() -> None:
    async def run() -> None:
        events: list[str] = []
        backend, capture, _publisher, _worker = _backend(events)
        page = object()

        assert events == []
        await backend.start(page)
        await backend.run()

        assert events == [
            "context_create",
            "publisher_bind",
            "capture_start",
            "worker_run",
        ]
        assert capture.started_pages == [page]

    asyncio.run(run())


def test_backend_stop_cleans_resources_in_order_and_is_idempotent() -> None:
    async def run() -> None:
        events: list[str] = []
        backend, _capture, _publisher, _worker = _backend(events)
        await backend.start(object())
        events.clear()

        await backend.stop()
        await backend.stop()

        assert events == [
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


def test_backend_cleans_context_when_publisher_bind_fails() -> None:
    async def run() -> None:
        events: list[str] = []
        publisher = PublisherSpy(
            events,
            bind_error=RuntimeError("bind failed"),
        )
        backend, _capture, _publisher, _worker = _backend(
            events,
            publisher=publisher,
        )

        with pytest.raises(RuntimeError, match="bind failed"):
            await backend.start(object())

        assert events == [
            "context_create",
            "publisher_bind",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


def test_backend_cleans_resources_when_capture_start_fails() -> None:
    async def run() -> None:
        events: list[str] = []
        capture = CaptureSpy(
            events,
            start_error=RuntimeError("capture failed"),
        )
        backend, _capture, _publisher, _worker = _backend(
            events,
            capture=capture,
        )

        with pytest.raises(RuntimeError, match="capture failed"):
            await backend.start(object())

        assert events == [
            "context_create",
            "publisher_bind",
            "capture_start",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


def test_backend_keeps_cleaning_up_when_worker_stop_fails() -> None:
    async def run() -> None:
        events: list[str] = []
        worker = WorkerSpy(
            events,
            stop_error=RuntimeError("pending request"),
        )
        backend, _capture, _publisher, _worker = _backend(
            events,
            worker=worker,
        )
        await backend.start(object())
        events.clear()

        with pytest.raises(RuntimeError, match="pending request"):
            await backend.stop()

        assert events == [
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


def test_backend_rejects_run_before_start_and_duplicate_start() -> None:
    async def run() -> None:
        backend, _capture, _publisher, _worker = _backend([])

        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()

        await backend.start(object())
        with pytest.raises(RuntimeError, match="already started"):
            await backend.start(object())

    asyncio.run(run())
