import importlib
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any, Protocol, cast

import zmq.asyncio

from majsoulrpa.browser.history import LoggingBrowserCommandExecutor
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestServer,
)
from majsoulrpa.browser.zmq import BrowserZmqRequestServer
from majsoulrpa.config import AppConfig
from majsoulrpa.endpoint import make_client_tcp_endpoint

CommandExecutorFactory = Callable[[object], BrowserCommandExecutor]
RequestServerFactory = Callable[[BrowserCommandExecutor], BrowserRequestServer]


class BrowserBackend(Protocol):
    async def start(self, config: AppConfig) -> None: ...
    async def stop(self) -> None: ...


class SnifferBackend(Protocol):
    async def start(self, page: object) -> None: ...
    async def stop(self) -> None: ...


async def run_browser_host(
    config: AppConfig,
    *,
    backend: BrowserBackend | None = None,
    sniffer_backend: SnifferBackend | None = None,
    command_executor_factory: CommandExecutorFactory | None = None,
    request_server_factory: RequestServerFactory | None = None,
) -> None:
    if backend is None:
        playwright = importlib.import_module("majsoulrpa.browser.playwright")
        backend = playwright.PlaywrightBrowserBackend()

    executor_factory = (
        _make_playwright_command_executor
        if command_executor_factory is None
        else command_executor_factory
    )
    zmq_context: zmq.asyncio.Context | None = None
    if request_server_factory is None:
        zmq_context = zmq.asyncio.Context()
        server_factory = _make_zmq_request_server_factory(config, zmq_context)
    else:
        server_factory = request_server_factory

    async with AsyncExitStack() as stack:
        await backend.start(config)
        stack.push_async_callback(backend.stop)

        if zmq_context is not None:
            stack.callback(zmq_context.term)

        page = getattr(backend, "page", None)
        if page is None:
            msg = "browser backend did not create a page."
            raise RuntimeError(msg)

        if sniffer_backend is not None:
            await sniffer_backend.start(page)
            stack.push_async_callback(sniffer_backend.stop)

        command_executor = LoggingBrowserCommandExecutor(
            executor_factory(page),
        )
        request_server = server_factory(command_executor)
        await request_server.bind()
        stack.push_async_callback(request_server.stop)
        await request_server.serve_forever()


def _make_playwright_command_executor(page: object) -> BrowserCommandExecutor:
    playwright = importlib.import_module("majsoulrpa.browser.playwright")
    return playwright.PlaywrightCommandExecutor(cast("Any", page))


def _make_zmq_request_server_factory(
    config: AppConfig,
    context: zmq.asyncio.Context,
) -> RequestServerFactory:
    endpoint = make_client_tcp_endpoint(config)

    def request_server_factory(
        executor: BrowserCommandExecutor,
    ) -> BrowserRequestServer:
        return BrowserZmqRequestServer(
            context=context,
            endpoint=endpoint,
            executor=executor,
        )

    return request_server_factory
