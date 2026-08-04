import asyncio
import importlib
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack
from typing import Any, Protocol, cast

import zmq.asyncio

from majsoulrpa._tasks import cancel_tasks, raise_task_errors
from majsoulrpa.browser.history import LoggingBrowserCommandExecutor
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestServer,
)
from majsoulrpa.browser.zmq import BrowserZmqRequestServer
from majsoulrpa.config import AppConfig
from majsoulrpa.endpoint import is_ipv6_literal, make_client_tcp_endpoint

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
            ipv6=is_ipv6_literal(config.endpoint.client_host),
        )

    return request_server_factory


async def run_browser_host(
    config: AppConfig,
    *,
    backend: BrowserBackend | None = None,
    sniffer_backend: SnifferBackend | None = None,
    command_executor_factory: CommandExecutorFactory = (
        _make_playwright_command_executor
    ),
    request_server_factory: RequestServerFactory | None = None,
) -> None:
    use_default_sniffer = backend is None and sniffer_backend is None
    if backend is None:
        playwright = importlib.import_module("majsoulrpa.browser.playwright")
        backend = playwright.PlaywrightBrowserBackend()
    if use_default_sniffer:
        sniffer_backend = _make_default_sniffer_backend(config)

    server_factory = request_server_factory

    async with AsyncExitStack() as stack:
        stack.push_async_callback(backend.stop)

        if server_factory is None:
            zmq_context = zmq.asyncio.Context()
            stack.callback(zmq_context.term)
            server_factory = _make_zmq_request_server_factory(
                config,
                zmq_context,
            )

        async def page_ready(page: object) -> None:
            if sniffer_backend is None:
                return
            await sniffer_backend.start(page)
            stack.push_async_callback(sniffer_backend.stop)

        await backend.start(
            config,
            page_ready=page_ready if sniffer_backend is not None else None,
        )

        page = getattr(backend, "page", None)
        if page is None:
            msg = "browser backend did not create a page."
            raise RuntimeError(msg)

        command_executor = LoggingBrowserCommandExecutor(
            command_executor_factory(page),
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
    try:
        done, pending = await asyncio.wait(
            tasks,
            return_when=asyncio.FIRST_COMPLETED,
        )
    except BaseException as error:
        cleanup_errors = await cancel_tasks(tasks)
        if cleanup_errors:
            msg = "Browser host task cancellation failed."
            raise BaseExceptionGroup(msg, [error, *cleanup_errors]) from None
        raise

    cleanup_errors = await cancel_tasks(pending)
    task_errors: list[BaseException] = []
    sniffer_stopped_normally = False
    for task in tasks:
        if task not in done:
            continue
        try:
            task.result()
        except BaseException as error:  # noqa: BLE001
            task_errors.append(error)
        else:
            if task is sniffer_task and server_task not in done:
                sniffer_stopped_normally = True

    if sniffer_stopped_normally:
        msg = "Sniffer worker stopped unexpectedly."
        task_errors.append(RuntimeError(msg))

    raise_task_errors(
        [*task_errors, *cleanup_errors],
        group_message="Browser host tasks failed.",
    )
