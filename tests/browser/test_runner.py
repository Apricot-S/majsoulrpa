import asyncio

import pytest
import zmq.asyncio

from majsoulrpa.browser import BrowserCommand, BrowserResponse
from majsoulrpa.browser.runner import (
    _make_zmq_request_server_factory,
    make_zmq_endpoint,
    run_browser_host,
)
from majsoulrpa.config import AppConfig, EndpointConfig


class BackendSpy:
    def __init__(self) -> None:
        self.page = object()
        self.started_configs: list[AppConfig] = []
        self.stopped = False

    async def start(self, config: AppConfig) -> None:
        self.started_configs.append(config)

    async def stop(self) -> None:
        self.stopped = True


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


class ExecutorSpy:
    def __init__(self, page: object) -> None:
        self.page = page

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        _ = command
        msg = "not used"
        raise AssertionError(msg)


def test_make_zmq_endpoint_uses_browser_host_and_remote_port() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            browser_host="192.0.2.10",
            remote_port=12000,
        ),
    )

    assert make_zmq_endpoint(config) == "tcp://192.0.2.10:12000"


def test_make_zmq_endpoint_brackets_ipv6_literal() -> None:
    config = AppConfig(
        endpoint=EndpointConfig(
            browser_host="::1",
            remote_port=12000,
        ),
    )

    assert make_zmq_endpoint(config) == "tcp://[::1]:12000"


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
