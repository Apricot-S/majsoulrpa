import ipaddress
from collections.abc import Callable, Mapping
from contextlib import AsyncExitStack
from typing import Any, Protocol, cast

import zmq
import zmq.asyncio

from majsoulrpa.browser import (
    BrowserZmqClientTransport,
    RemoteBrowserController,
)
from majsoulrpa.client.runtime import RPARuntime, ScreenshotScreenDetector
from majsoulrpa.config import AppConfig
from majsoulrpa.screens import Screen, ScreenContext
from majsoulrpa.types import Callback


class ZmqSocketLike(Protocol):
    def connect(self, endpoint: str) -> None: ...
    def close(self, *, linger: int) -> None: ...
    async def send(self, payload: bytes) -> None: ...
    async def recv(self) -> bytes: ...


class ZmqContextLike(Protocol):
    def socket(self, socket_type: int) -> ZmqSocketLike: ...
    def term(self) -> None: ...


type ZmqContextFactory = Callable[[], ZmqContextLike]


def make_controller_zmq_endpoint(config: AppConfig) -> str:
    host = _format_zmq_host(config.endpoint.browser_host)
    return f"tcp://{host}:{config.endpoint.remote_port}"


class ControllerRuntimeFactory:
    def __init__(
        self,
        *,
        context_factory: ZmqContextFactory | None = None,
    ) -> None:
        self._context_factory = context_factory or _make_zmq_context

    def __call__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        context = self._context_factory()
        socket = context.socket(zmq.REQ)
        endpoint = make_controller_zmq_endpoint(config)
        socket.connect(endpoint)

        transport = BrowserZmqClientTransport(cast("Any", socket))
        controller = RemoteBrowserController(transport)
        screen_context = ScreenContext(
            browser=controller,
            viewport_width=_viewport_width(config),
            viewport_height=config.browser.viewport_height,
        )
        detector = ScreenshotScreenDetector(
            controller.screenshot,
            context=screen_context,
        )

        async def cleanup() -> None:
            async with AsyncExitStack() as stack:
                stack.callback(context.term)
                stack.callback(socket.close, linger=0)

        return RPARuntime(callbacks, detector, cleanup=cleanup)


def _format_zmq_host(host: str) -> str:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return host
    if isinstance(address, ipaddress.IPv6Address):
        return f"[{host}]"
    return host


def _viewport_width(config: AppConfig) -> int:
    return round(config.browser.viewport_height * 16 / 9)


def _make_zmq_context() -> ZmqContextLike:
    return cast("ZmqContextLike", zmq.asyncio.Context())
