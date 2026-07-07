import asyncio

import pytest
import zmq.asyncio

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse
from majsoulrpa.browser.runner import (
    _make_zmq_request_server_factory,
    run_browser_host,
)
from majsoulrpa.config import AppConfig


class BackendSpy:
    def __init__(self) -> None:
        self.page = object()
        self.started_configs: list[AppConfig] = []
        self.stopped = False

    async def start(self, config: AppConfig) -> None:
        self.started_configs.append(config)

    async def stop(self) -> None:
        self.stopped = True


class SnifferBackendSpy:
    def __init__(self) -> None:
        self.started_pages: list[object] = []
        self.stopped = False

    async def start(self, page: object) -> None:
        self.started_pages.append(page)

    async def stop(self) -> None:
        self.stopped = True


class FailingSnifferBackend(SnifferBackendSpy):
    async def start(self, page: object) -> None:
        await super().start(page)
        msg = "sniffer start failed"
        raise RuntimeError(msg)


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
        assert executor is executor_calls[0]
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
