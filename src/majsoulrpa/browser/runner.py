import asyncio
import importlib
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack, suppress
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
PageReadyHook = Callable[[object], Awaitable[None]]


class BrowserBackend(Protocol):
    async def start(
        self,
        config: AppConfig,
        *,
        page_ready: PageReadyHook | None = None,
    ) -> None: ...
    async def stop(self) -> None: ...


class SnifferBackend(Protocol):
    async def start(self, page: object) -> None: ...
    async def run(self) -> None: ...
    async def stop(self) -> None: ...


async def run_browser_host(
    config: AppConfig,
    *,
    backend: BrowserBackend | None = None,
    sniffer_backend: SnifferBackend | None = None,
    command_executor_factory: CommandExecutorFactory | None = None,
    request_server_factory: RequestServerFactory | None = None,
) -> None:
    use_default_sniffer = backend is None and sniffer_backend is None
    if backend is None:
        playwright = importlib.import_module("majsoulrpa.browser.playwright")
        backend = playwright.PlaywrightBrowserBackend()
    if use_default_sniffer:
        sniffer_backend = _make_default_sniffer_backend(config)

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
        stack.push_async_callback(backend.stop)

        async def page_ready(page: object) -> None:
            if sniffer_backend is None:
                return
            await sniffer_backend.start(page)
            stack.push_async_callback(sniffer_backend.stop)

        await backend.start(
            config,
            page_ready=page_ready if sniffer_backend is not None else None,
        )

        if zmq_context is not None:
            stack.callback(zmq_context.term)

        page = getattr(backend, "page", None)
        if page is None:
            msg = "browser backend did not create a page."
            raise RuntimeError(msg)

        command_executor = LoggingBrowserCommandExecutor(
            executor_factory(page),
        )
        request_server = server_factory(command_executor)
        await request_server.bind()
        stack.push_async_callback(request_server.stop)
        if sniffer_backend is None:
            await request_server.serve_forever()
        else:
            await _serve_with_sniffer(request_server, sniffer_backend)


async def _serve_with_sniffer(
    request_server: BrowserRequestServer,
    sniffer_backend: SnifferBackend,
) -> None:
    server_task = asyncio.create_task(request_server.serve_forever())
    sniffer_task = asyncio.create_task(sniffer_backend.run())
    tasks = (server_task, sniffer_task)
    done: set[asyncio.Task[None]] = set()
    try:
        done, _pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
        )
    finally:
        unfinished = [task for task in tasks if not task.done()]
        for task in unfinished:
            task.cancel()
        for task in unfinished:
            with suppress(asyncio.CancelledError):
                await task

    for task in tasks:
        if task in done:
            task.result()

    if sniffer_task in done and server_task not in done:
        msg = "Sniffer worker stopped unexpectedly."
        raise RuntimeError(msg)


def _make_playwright_command_executor(page: object) -> BrowserCommandExecutor:
    playwright = importlib.import_module("majsoulrpa.browser.playwright")
    return playwright.PlaywrightCommandExecutor(cast("Any", page))


def _make_default_sniffer_backend(config: AppConfig) -> SnifferBackend:
    runtime = importlib.import_module("majsoulrpa.sniffer.runtime")
    return runtime.BrowserHostSnifferBackend(config)


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
