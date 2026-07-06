import importlib
import ipaddress
from collections.abc import Callable
from typing import Any, cast

import zmq.asyncio

from majsoulrpa.browser.host import BrowserBackend
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestServer,
)
from majsoulrpa.browser.zmq import BrowserZmqRequestServer
from majsoulrpa.config import AppConfig

CommandExecutorFactory = Callable[[object], BrowserCommandExecutor]
RequestServerFactory = Callable[[BrowserCommandExecutor], BrowserRequestServer]


def make_zmq_endpoint(config: AppConfig) -> str:
    host = _format_zmq_host(config.endpoint.browser_host)
    return f"tcp://{host}:{config.endpoint.remote_port}"


def _format_zmq_host(host: str) -> str:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return host
    if isinstance(address, ipaddress.IPv6Address):
        return f"[{host}]"
    return host


async def run_browser_host(
    config: AppConfig,
    *,
    backend: BrowserBackend | None = None,
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

    request_server: BrowserRequestServer | None = None
    try:
        await backend.start(config)
        page = getattr(backend, "page", None)
        if page is None:
            msg = "browser backend did not create a page."
            raise RuntimeError(msg)
        command_executor = executor_factory(page)
        request_server = server_factory(command_executor)
        await request_server.bind()
        await request_server.serve_forever()
    finally:
        if request_server is not None:
            await request_server.stop()
        if zmq_context is not None:
            zmq_context.term()
        await backend.stop()


def _make_playwright_command_executor(page: object) -> BrowserCommandExecutor:
    playwright = importlib.import_module("majsoulrpa.browser.playwright")
    return playwright.PlaywrightCommandExecutor(cast("Any", page))


def _make_zmq_request_server_factory(
    config: AppConfig,
    context: zmq.asyncio.Context,
) -> RequestServerFactory:
    endpoint = make_zmq_endpoint(config)

    def request_server_factory(
        executor: BrowserCommandExecutor,
    ) -> BrowserRequestServer:
        return BrowserZmqRequestServer(
            context=context,
            endpoint=endpoint,
            executor=executor,
        )

    return request_server_factory
