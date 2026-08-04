import asyncio
from collections.abc import Awaitable, Callable

import pytest
import zmq.asyncio

from majsoulrpa.browser import runner as browser_runner
from majsoulrpa.browser.history import LoggingBrowserCommandExecutor
from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse
from majsoulrpa.browser.runner import (
    _make_zmq_request_server_factory,
    run_browser_host,
)
from majsoulrpa.config import AppConfig


class BackendSpy:
    def __init__(self, events: list[str] | None = None) -> None:
        self.page = object()
        self.started_configs: list[AppConfig] = []
        self.stopped = False
        self.events = events

    async def start(
        self,
        config: AppConfig,
        *,
        page_ready: Callable[[object], Awaitable[None]] | None = None,
    ) -> None:
        self.started_configs.append(config)
        if self.events is not None:
            self.events.append("page_created")
        if page_ready is not None:
            await page_ready(self.page)
        if self.events is not None:
            self.events.append("navigated")

    async def stop(self) -> None:
        self.stopped = True


class SnifferBackendSpy:
    def __init__(self, events: list[str] | None = None) -> None:
        self.started_pages: list[object] = []
        self.stopped = False
        self.run_started = False
        self.run_cancelled = False
        self.run_started_event = asyncio.Event()
        self.events = events

    async def start(self, page: object) -> None:
        self.started_pages.append(page)
        if self.events is not None:
            self.events.append("sniffer_started")

    async def run(self) -> None:
        self.run_started = True
        self.run_started_event.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.run_cancelled = True
            raise

    async def stop(self) -> None:
        self.stopped = True


class FailingSnifferBackend(SnifferBackendSpy):
    async def start(self, page: object) -> None:
        await super().start(page)
        msg = "sniffer start failed"
        raise RuntimeError(msg)


class FailingRunningSnifferBackend(SnifferBackendSpy):
    async def run(self) -> None:
        self.run_started = True
        msg = "sniffer worker failed"
        raise RuntimeError(msg)


class CancellationFailingSnifferBackend(SnifferBackendSpy):
    async def run(self) -> None:
        self.run_started = True
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            msg = "sniffer cancellation failed"
            raise CleanupError(msg) from None


class RequestServerSpy:
    def __init__(self) -> None:
        self.bound = False
        self.served = False
        self.stopped = False

    async def bind(self) -> None:
        self.bound = True

    async def serve_forever(self) -> None:
        self.served = True

    async def stop(self) -> None:
        self.stopped = True


class BlockingRequestServer(RequestServerSpy):
    def __init__(self) -> None:
        super().__init__()
        self.serve_cancelled = False
        self.serve_started_event = asyncio.Event()

    async def serve_forever(self) -> None:
        self.served = True
        self.serve_started_event.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.serve_cancelled = True
            raise


class CancellationFailingRequestServer(BlockingRequestServer):
    async def serve_forever(self) -> None:
        self.served = True
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            msg = "server cancellation failed"
            raise CleanupError(msg) from None


class NavigationFailingBackend(BackendSpy):
    async def start(
        self,
        config: AppConfig,
        *,
        page_ready: Callable[[object], Awaitable[None]] | None = None,
    ) -> None:
        await super().start(config, page_ready=page_ready)
        msg = "navigation failed"
        raise RuntimeError(msg)


class StartFailingBackend(BackendSpy):
    async def start(
        self,
        config: AppConfig,
        *,
        page_ready: Callable[[object], Awaitable[None]] | None = None,
    ) -> None:
        _ = (config, page_ready)
        msg = "backend start failed"
        raise RuntimeError(msg)


class ZmqContextSpy:
    def __init__(self) -> None:
        self.terminated = 0

    def term(self) -> None:
        self.terminated += 1


class FailingRequestServer(RequestServerSpy):
    async def serve_forever(self) -> None:
        msg = "serve failed"
        raise RuntimeError(msg)


class StopFailingRequestServer(RequestServerSpy):
    async def stop(self) -> None:
        self.stopped = True
        msg = "request server stop failed"
        raise CleanupError(msg)


class InterruptingRequestServer(RequestServerSpy):
    async def serve_forever(self) -> None:
        raise KeyboardInterrupt


class CleanupError(Exception):
    pass


class PlaywrightCloseFailingBackend(BackendSpy):
    async def stop(self) -> None:
        self.stopped = True
        msg = "Browser.close: Connection closed while reading from the driver"
        raise CleanupError(msg)


class UnexpectedCloseFailingBackend(BackendSpy):
    async def stop(self) -> None:
        self.stopped = True
        msg = "unexpected close failure"
        raise CleanupError(msg)


class ExecutorSpy:
    def __init__(self, page: object) -> None:
        self.page = page

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        _ = command
        msg = "not used"
        raise AssertionError(msg)


def test_run_browser_host_binds_and_serves_request_server() -> None:
    backend = BackendSpy()
    server = RequestServerSpy()
    config = AppConfig()
    executor_calls: list[ExecutorSpy] = []

    def command_executor_factory(page: object) -> ExecutorSpy:
        executor = ExecutorSpy(page)
        executor_calls.append(executor)
        return executor

    def request_server_factory(executor: object) -> RequestServerSpy:
        assert isinstance(executor, LoggingBrowserCommandExecutor)
        assert executor._executor is executor_calls[0]
        return server

    asyncio.run(
        run_browser_host(
            config,
            backend=backend,
            command_executor_factory=command_executor_factory,
            request_server_factory=request_server_factory,
        ),
    )

    assert backend.started_configs == [config]
    assert executor_calls[0].page is backend.page
    assert server.bound
    assert server.served
    assert server.stopped
    assert backend.stopped


def test_run_browser_host_terminates_zmq_context_when_backend_start_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = ZmqContextSpy()
    monkeypatch.setattr(
        browser_runner.zmq.asyncio,
        "Context",
        lambda: context,
    )

    with pytest.raises(RuntimeError, match="backend start failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=StartFailingBackend(),
                command_executor_factory=ExecutorSpy,
            ),
        )

    assert context.terminated == 1


@pytest.mark.parametrize(
    ("backend", "sniffer", "error_message"),
    [
        (
            BackendSpy(),
            FailingSnifferBackend(),
            "sniffer start failed",
        ),
        (
            NavigationFailingBackend(),
            SnifferBackendSpy(),
            "navigation failed",
        ),
    ],
)
def test_run_browser_host_terminates_zmq_context_during_page_startup_failure(
    monkeypatch: pytest.MonkeyPatch,
    backend: BackendSpy,
    sniffer: SnifferBackendSpy,
    error_message: str,
) -> None:
    context = ZmqContextSpy()
    monkeypatch.setattr(
        browser_runner.zmq.asyncio,
        "Context",
        lambda: context,
    )

    with pytest.raises(RuntimeError, match=error_message):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
            ),
        )

    assert context.terminated == 1


def test_run_browser_host_uses_sniffer_with_default_browser_backend(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    backend = BackendSpy()
    sniffer = SnifferBackendSpy()
    server = RequestServerSpy()

    class PlaywrightModule:
        @staticmethod
        def PlaywrightBrowserBackend() -> BackendSpy:  # noqa: N802
            return backend

    monkeypatch.setattr(
        browser_runner.importlib,
        "import_module",
        lambda _name: PlaywrightModule,
    )
    monkeypatch.setattr(
        browser_runner,
        "_make_default_sniffer_backend",
        lambda _config: sniffer,
    )

    asyncio.run(
        run_browser_host(
            AppConfig(),
            command_executor_factory=ExecutorSpy,
            request_server_factory=lambda _executor: server,
        ),
    )

    assert sniffer.started_pages == [backend.page]
    assert sniffer.run_started
    assert sniffer.stopped


def test_run_browser_host_starts_and_stops_sniffer_backend() -> None:
    backend = BackendSpy()
    sniffer = SnifferBackendSpy()
    server = RequestServerSpy()

    asyncio.run(
        run_browser_host(
            AppConfig(),
            backend=backend,
            sniffer_backend=sniffer,
            command_executor_factory=ExecutorSpy,
            request_server_factory=lambda _executor: server,
        ),
    )

    assert sniffer.started_pages == [backend.page]
    assert server.bound
    assert server.served
    assert server.stopped
    assert sniffer.stopped
    assert backend.stopped


def test_run_browser_host_starts_sniffer_before_navigation() -> None:
    events: list[str] = []
    backend = BackendSpy(events)
    sniffer = SnifferBackendSpy(events)
    server = RequestServerSpy()

    asyncio.run(
        run_browser_host(
            AppConfig(),
            backend=backend,
            sniffer_backend=sniffer,
            command_executor_factory=ExecutorSpy,
            request_server_factory=lambda _executor: server,
        ),
    )

    assert events == ["page_created", "sniffer_started", "navigated"]
    assert sniffer.run_started
    assert sniffer.run_cancelled


def test_run_browser_host_propagates_sniffer_worker_failure() -> None:
    backend = BackendSpy()
    sniffer = FailingRunningSnifferBackend()
    server = BlockingRequestServer()

    with pytest.raises(RuntimeError, match="sniffer worker failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.serve_cancelled
    assert server.stopped
    assert sniffer.stopped
    assert backend.stopped


@pytest.mark.parametrize(
    ("server", "sniffer", "primary_message", "cleanup_message"),
    [
        (
            FailingRequestServer(),
            CancellationFailingSnifferBackend(),
            "serve failed",
            "sniffer cancellation failed",
        ),
        (
            CancellationFailingRequestServer(),
            FailingRunningSnifferBackend(),
            "sniffer worker failed",
            "server cancellation failed",
        ),
    ],
)
def test_run_browser_host_preserves_task_and_sibling_cleanup_failures(
    server: RequestServerSpy,
    sniffer: SnifferBackendSpy,
    primary_message: str,
    cleanup_message: str,
) -> None:
    with pytest.raises(ExceptionGroup) as exc_info:
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=BackendSpy(),
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert exc_info.group_contains(RuntimeError, match=primary_message)
    assert exc_info.group_contains(CleanupError, match=cleanup_message)


def test_run_browser_host_stops_sniffer_when_request_server_fails() -> None:
    backend = BackendSpy()
    sniffer = SnifferBackendSpy()
    server = FailingRequestServer()

    with pytest.raises(RuntimeError, match="serve failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert sniffer.run_cancelled
    assert server.stopped
    assert sniffer.stopped
    assert backend.stopped


def test_run_browser_host_cleans_up_sniffer_when_navigation_fails() -> None:
    backend = NavigationFailingBackend()
    sniffer = SnifferBackendSpy()
    server = RequestServerSpy()

    with pytest.raises(RuntimeError, match="navigation failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert sniffer.stopped
    assert server.bound is False
    assert backend.stopped


def test_run_browser_host_cancellation_stops_server_and_sniffer() -> None:
    async def run() -> None:
        backend = BackendSpy()
        sniffer = SnifferBackendSpy()
        server = BlockingRequestServer()
        task = asyncio.create_task(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )
        await asyncio.gather(
            server.serve_started_event.wait(),
            sniffer.run_started_event.wait(),
        )

        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        assert server.serve_cancelled
        assert sniffer.run_cancelled
        assert server.stopped
        assert sniffer.stopped
        assert backend.stopped

    asyncio.run(run())


def test_run_browser_host_stops_backend_when_sniffer_start_fails() -> None:
    backend = BackendSpy()
    sniffer = FailingSnifferBackend()
    server = RequestServerSpy()

    with pytest.raises(RuntimeError, match="sniffer start failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                sniffer_backend=sniffer,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert sniffer.started_pages == [backend.page]
    assert sniffer.stopped is False
    assert server.bound is False
    assert server.stopped is False
    assert backend.stopped


def test_zmq_request_server_factory_does_not_wrap_context_cleanup() -> None:
    context = zmq.asyncio.Context()
    try:
        factory = _make_zmq_request_server_factory(AppConfig(), context)

        server = factory(ExecutorSpy(object()))

        assert server.__class__.__name__ == "BrowserZmqRequestServer"
    finally:
        context.term()


def test_run_browser_host_cleans_up_when_serve_fails() -> None:
    backend = BackendSpy()
    server = FailingRequestServer()

    with pytest.raises(RuntimeError, match="serve failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped
    assert backend.stopped


def test_run_browser_host_reports_disconnect_on_interrupt_cleanup() -> None:
    backend = PlaywrightCloseFailingBackend()
    server = InterruptingRequestServer()

    with pytest.raises(CleanupError, match="Connection closed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped
    assert backend.stopped


def test_run_browser_host_reports_cleanup_failure_during_interrupt() -> None:
    backend = UnexpectedCloseFailingBackend()
    server = InterruptingRequestServer()

    with pytest.raises(CleanupError, match="unexpected close failure"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped
    assert backend.stopped


def test_run_browser_host_keeps_disconnect_without_interrupt() -> None:
    backend = PlaywrightCloseFailingBackend()
    server = RequestServerSpy()

    with pytest.raises(CleanupError, match="Connection closed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped
    assert backend.stopped


def test_run_browser_host_stops_backend_after_server_stop_failure() -> None:
    backend = BackendSpy()
    server = StopFailingRequestServer()

    with pytest.raises(CleanupError, match="request server stop failed"):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped
    assert backend.stopped


def test_run_browser_host_rejects_backend_without_page() -> None:
    backend = BackendSpy()
    backend.page = None
    server = RequestServerSpy()

    with pytest.raises(
        RuntimeError,
        match=r"browser backend did not create a page\.",
    ):
        asyncio.run(
            run_browser_host(
                AppConfig(),
                backend=backend,
                command_executor_factory=ExecutorSpy,
                request_server_factory=lambda _executor: server,
            ),
        )

    assert server.stopped is False
    assert backend.stopped
