import asyncio
import importlib
from collections.abc import Callable

import pytest

from majsoulrpa.config import AppConfig
from majsoulrpa.sniffer.correlator import CorrelatedMessage
from majsoulrpa.sniffer.playwright import CaptureEvent
from majsoulrpa.sniffer.runtime import (
    BrowserHostSnifferBackend,
    CaptureBackend,
    PublisherBackend,
    TerminableContext,
)


class ContextSpy:
    def __init__(
        self,
        events: list[str],
        *,
        stop_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.stop_error = stop_error

    def socket(self, socket_type: int) -> object:
        _ = socket_type
        msg = "not used by injected publisher"
        raise AssertionError(msg)

    def term(self) -> None:
        self.events.append("context_term")
        if self.stop_error is not None:
            raise self.stop_error


class CaptureSpy:
    def __init__(
        self,
        events: list[str],
        *,
        start_error: BaseException | None = None,
        stop_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.start_error = start_error
        self.stop_error = stop_error
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
        if self.stop_error is not None:
            raise self.stop_error


class PublisherSpy:
    def __init__(
        self,
        events: list[str],
        *,
        bind_error: BaseException | None = None,
        stop_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.bind_error = bind_error
        self.stop_error = stop_error

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
        if self.stop_error is not None:
            raise self.stop_error


class WorkerSpy:
    def __init__(
        self,
        events: list[str],
        *,
        stop_error: Exception | None = None,
        run_error: Exception | None = None,
    ) -> None:
        self.events = events
        self.stop_error = stop_error
        self.run_error = run_error

    async def run(self) -> None:
        self.events.append("worker_run")
        if self.run_error is not None:
            raise self.run_error

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


@pytest.mark.parametrize(
    ("stage", "expected"),
    [
        ("context", ["context_create"]),
        ("capture", ["context_create", "capture_create", "context_term"]),
        (
            "publisher",
            [
                "context_create",
                "capture_create",
                "publisher_create",
                "capture_stop",
                "context_term",
            ],
        ),
        (
            "worker",
            [
                "context_create",
                "capture_create",
                "publisher_create",
                "worker_create",
                "capture_stop",
                "publisher_stop",
                "context_term",
            ],
        ),
    ],
)
def test_factory_failure_cleans_only_created_resources(
    stage: str,
    expected: list[str],
) -> None:
    async def run() -> None:
        events: list[str] = []
        error = RuntimeError("factory failed")

        def creating(name: str) -> None:
            events.append(f"{name}_create")
            if name == stage:
                raise error

        def context_factory() -> ContextSpy:
            creating("context")
            return ContextSpy(events)

        def capture_factory() -> CaptureSpy:
            creating("capture")
            return CaptureSpy(events)

        def publisher_factory(
            _context: TerminableContext,
            _config: AppConfig,
        ) -> PublisherSpy:
            creating("publisher")
            return PublisherSpy(events)

        def worker_factory(
            _capture: CaptureBackend,
            _publisher: PublisherBackend,
        ) -> WorkerSpy:
            creating("worker")
            return WorkerSpy(events)

        backend = BrowserHostSnifferBackend(
            AppConfig(),
            context_factory=context_factory,
            capture_factory=capture_factory,
            publisher_factory=publisher_factory,
            worker_factory=worker_factory,
        )
        with pytest.raises(RuntimeError) as caught:
            await backend.start(object())
        assert caught.value is error
        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()
        await backend.stop()
        assert events == expected

    asyncio.run(run())


def test_backend_preserves_falsey_factories(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FalseyFactory[**P, T]:
        def __init__(self, factory: Callable[P, T]) -> None:
            self.factory = factory

        def __bool__(self) -> bool:
            return False

        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
            return self.factory(*args, **kwargs)

    def unexpected_default(*_args: object) -> None:
        msg = "Injected factory was replaced."
        raise AssertionError(msg)

    for name in (
        "_make_context",
        "PlaywrightFrameCapture",
        "_make_publisher",
        "_make_worker",
    ):
        monkeypatch.setattr(
            importlib.import_module("majsoulrpa.sniffer.runtime"),
            name,
            unexpected_default,
        )

    async def run() -> None:
        events: list[str] = []
        context = ContextSpy(events)
        capture = CaptureSpy(events)
        publisher = PublisherSpy(events)
        worker = WorkerSpy(events)
        config = AppConfig()

        def make_publisher(
            actual_context: TerminableContext, actual_config: AppConfig
        ) -> PublisherSpy:
            assert actual_context is context
            assert actual_config is config
            return publisher

        def make_worker(
            actual_capture: CaptureBackend, actual_publisher: PublisherBackend
        ) -> WorkerSpy:
            assert actual_capture is capture
            assert actual_publisher is publisher
            return worker

        backend = BrowserHostSnifferBackend(
            config,
            context_factory=FalseyFactory(lambda: context),
            capture_factory=FalseyFactory(lambda: capture),
            publisher_factory=FalseyFactory(make_publisher),
            worker_factory=FalseyFactory(make_worker),
        )
        page = object()
        await backend.start(page)
        await backend.run()
        await backend.stop()
        assert capture.started_pages == [page]
        assert events == [
            "publisher_bind",
            "capture_start",
            "worker_run",
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


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


def test_run_failure_propagates_and_all_resources_remain_stoppable() -> None:
    async def run() -> None:
        events: list[str] = []
        error = RuntimeError("worker run failed")
        backend, _capture, _publisher, _worker = _backend(
            events, worker=WorkerSpy(events, run_error=error)
        )
        await backend.start(object())
        events.clear()

        with pytest.raises(RuntimeError) as caught:
            await backend.run()
        assert caught.value is error
        assert events == ["worker_run"]

        await backend.stop()
        await backend.stop()
        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()
        assert events == [
            "worker_run",
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

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


@pytest.mark.parametrize("stage", ["bind", "capture-start"])
@pytest.mark.parametrize("error_type", [RuntimeError, asyncio.CancelledError])
def test_start_and_cleanup_failures_preserve_all_causes(
    stage: str,
    error_type: type[BaseException],
) -> None:
    async def run() -> None:
        events: list[str] = []
        start_error = error_type("start failed")
        capture_error = RuntimeError("capture stop failed")
        publisher_error = RuntimeError("publisher stop failed")
        backend, _capture, _publisher, _worker = _backend(
            events,
            capture=CaptureSpy(
                events,
                start_error=start_error if stage == "capture-start" else None,
                stop_error=capture_error,
            ),
            publisher=PublisherSpy(
                events,
                bind_error=start_error if stage == "bind" else None,
                stop_error=publisher_error,
            ),
        )

        with pytest.raises(BaseExceptionGroup) as caught:
            await backend.start(object())
        assert caught.value.exceptions == (start_error, publisher_error)
        assert publisher_error.__context__ is capture_error
        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()
        await backend.stop()

        expected = ["context_create", "publisher_bind"]
        if stage == "capture-start":
            expected.append("capture_start")
        expected.extend(["capture_stop", "publisher_stop", "context_term"])
        assert events == expected

    asyncio.run(run())


@pytest.mark.parametrize("stage", ["bind", "capture-start"])
def test_backend_retries_start_with_fresh_resources(stage: str) -> None:
    async def run() -> None:
        old_events: list[str] = []
        new_events: list[str] = []
        failure = RuntimeError("start failed")
        contexts = [ContextSpy(old_events), ContextSpy(new_events)]
        captures = [
            CaptureSpy(
                old_events,
                start_error=failure if stage == "capture-start" else None,
            ),
            CaptureSpy(new_events),
        ]
        publishers = [
            PublisherSpy(
                old_events, bind_error=failure if stage == "bind" else None
            ),
            PublisherSpy(new_events),
        ]
        workers = [WorkerSpy(old_events), WorkerSpy(new_events)]
        context_iter = iter(contexts)
        capture_iter = iter(captures)
        publisher_iter = iter(publishers)
        worker_iter = iter(workers)

        def make_publisher(
            context: TerminableContext, _config: AppConfig
        ) -> PublisherSpy:
            publisher = next(publisher_iter)
            assert context is contexts[publishers.index(publisher)]
            return publisher

        def make_worker(
            capture: CaptureBackend, publisher: PublisherBackend
        ) -> WorkerSpy:
            worker = next(worker_iter)
            index = workers.index(worker)
            assert capture is captures[index]
            assert publisher is publishers[index]
            return worker

        backend = BrowserHostSnifferBackend(
            AppConfig(),
            context_factory=lambda: next(context_iter),
            capture_factory=lambda: next(capture_iter),
            publisher_factory=make_publisher,
            worker_factory=make_worker,
        )
        with pytest.raises(RuntimeError) as caught:
            await backend.start(object())
        assert caught.value is failure
        old_snapshot = old_events.copy()

        page = object()
        await backend.start(page)
        await backend.run()
        await backend.stop()

        assert captures[1].started_pages == [page]
        assert old_events == old_snapshot
        assert "worker_run" not in old_events
        assert "worker_stop" not in old_events
        assert new_events == [
            "publisher_bind",
            "capture_start",
            "worker_run",
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


@pytest.mark.parametrize("stage", ["bind", "capture-start"])
def test_start_cancellation_cleans_resources(stage: str) -> None:
    async def run() -> None:
        events: list[str] = []
        waiting = asyncio.Event()
        release = asyncio.Event()

        class BlockingPublisher(PublisherSpy):
            async def bind(self) -> None:
                await super().bind()
                if stage == "bind":
                    waiting.set()
                    await release.wait()

        class BlockingCapture(CaptureSpy):
            async def start(self, page: object) -> None:
                await super().start(page)
                if stage == "capture-start":
                    waiting.set()
                    await release.wait()

        backend, _capture, _publisher, _worker = _backend(
            events,
            capture=BlockingCapture(events),
            publisher=BlockingPublisher(events),
        )
        task = asyncio.create_task(backend.start(object()))
        try:
            async with asyncio.timeout(1):
                await waiting.wait()
            assert not task.done()
        finally:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()
        await backend.stop()
        expected = ["context_create", "publisher_bind"]
        if stage == "capture-start":
            expected.append("capture_start")
        expected.extend(["capture_stop", "publisher_stop", "context_term"])
        assert events == expected

    asyncio.run(run())


@pytest.mark.parametrize("stage", ["worker", "capture", "publisher"])
def test_backend_keeps_cleaning_up_when_stop_fails(stage: str) -> None:
    async def run() -> None:
        events: list[str] = []
        error = RuntimeError("stop failed")
        worker = WorkerSpy(
            events,
            stop_error=error if stage == "worker" else None,
        )
        capture = CaptureSpy(
            events, stop_error=error if stage == "capture" else None
        )
        publisher = PublisherSpy(
            events, stop_error=error if stage == "publisher" else None
        )
        backend, _capture, _publisher, _worker = _backend(
            events,
            worker=worker,
            capture=capture,
            publisher=publisher,
        )
        await backend.start(object())
        events.clear()

        with pytest.raises(RuntimeError) as caught:
            await backend.stop()
        assert caught.value is error
        await backend.stop()

        assert events == [
            "worker_stop",
            "capture_stop",
            "publisher_stop",
            "context_term",
        ]

    asyncio.run(run())


def test_stop_preserves_all_failures_and_does_not_repeat_cleanup() -> None:
    async def run() -> None:
        events: list[str] = []
        worker_error = RuntimeError("worker stop failed")
        capture_error = RuntimeError("capture stop failed")
        publisher_error = RuntimeError("publisher stop failed")
        context_error = RuntimeError("context term failed")
        context = ContextSpy(events, stop_error=context_error)
        capture = CaptureSpy(events, stop_error=capture_error)
        publisher = PublisherSpy(events, stop_error=publisher_error)
        worker = WorkerSpy(events, stop_error=worker_error)
        backend = BrowserHostSnifferBackend(
            AppConfig(),
            context_factory=lambda: context,
            capture_factory=lambda: capture,
            publisher_factory=lambda _context, _config: publisher,
            worker_factory=lambda _capture, _publisher: worker,
        )
        await backend.start(object())
        events.clear()

        with pytest.raises(RuntimeError) as caught:
            await backend.stop()
        assert caught.value is context_error
        assert context_error.__context__ is publisher_error
        assert publisher_error.__context__ is capture_error
        assert capture_error.__context__ is worker_error

        await backend.stop()
        with pytest.raises(RuntimeError, match="not started"):
            await backend.run()
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
