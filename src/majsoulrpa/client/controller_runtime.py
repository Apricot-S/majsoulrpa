import warnings
from collections.abc import Callable, Mapping
from contextlib import AsyncExitStack
from typing import Any, Protocol, cast

import zmq
import zmq.asyncio

from majsoulrpa.browser.controller import RemoteBrowserController
from majsoulrpa.browser.history import LoggingBrowserClientTransport
from majsoulrpa.browser.zmq import BrowserZmqClientTransport
from majsoulrpa.client.runtime import RPARuntime, ScreenshotScreenDetector
from majsoulrpa.client.session import SessionState
from majsoulrpa.config import AppConfig
from majsoulrpa.endpoint import make_browser_host_tcp_endpoint
from majsoulrpa.screens import Screen, ScreenContext
from majsoulrpa.screens.room.cache import RoomStateCache
from majsoulrpa.sniffer.client_runtime import SnifferClientRuntime
from majsoulrpa.sniffer.decoder import SnifferMessageDecoder
from majsoulrpa.sniffer.message_queue import SnifferMessageQueue
from majsoulrpa.sniffer.zmq import (
    AsyncZmqContextLike,
    ZmqSnifferSubscriber,
)
from majsoulrpa.types import Callback
from majsoulrpa.viewport import viewport_width_for_height


class ZmqSocketLike(Protocol):
    def connect(self, endpoint: str) -> None: ...
    def close(self, *, linger: int) -> None: ...
    async def send(self, payload: bytes) -> None: ...
    async def recv(self) -> bytes: ...


class ZmqContextLike(Protocol):
    def socket(self, socket_type: int) -> ZmqSocketLike: ...
    def term(self) -> None: ...


type ZmqContextFactory = Callable[[], ZmqContextLike]

SNIFFER_QUEUE_CAPACITY = 1024
SNIFFER_QUEUE_MAX_PAYLOAD_BYTES = 64 * 1024 * 1024


class StopFlag:
    def __init__(self) -> None:
        self._requested = False

    async def request_stop(self) -> None:
        self._requested = True

    def is_requested(self) -> bool:
        return self._requested


class ControllerRuntimeFactory:
    def __init__(
        self,
        *,
        context_factory: ZmqContextFactory | None = None,
    ) -> None:
        self._context_factory = context_factory or zmq.asyncio.Context

    def __call__(
        self,
        callbacks: Mapping[type[Screen], Callback[Any]],
        config: AppConfig,
    ) -> RPARuntime:
        # On Windows, the `ProactorEventLoop` does not implement
        # the add_reader family of methods.
        # When using `zmq.asyncio`, Tornado automatically registers
        # a selector thread to provide add_reader support.
        # This behavior always triggers a `RuntimeWarning`,
        # even though it is harmless.
        # Since Tornado is functioning correctly and the warning only
        # causes confusion, we suppress it here to keep the output
        # clean.
        warnings.filterwarnings(
            "ignore",
            message="Proactor event loop does not implement add_reader",
            category=RuntimeWarning,
            module="zmq",
        )

        context = self._context_factory()
        socket = context.socket(zmq.REQ)
        endpoint = make_browser_host_tcp_endpoint(config)
        socket.connect(endpoint)

        transport = LoggingBrowserClientTransport(
            BrowserZmqClientTransport(socket),
        )
        controller = RemoteBrowserController(transport)
        stop_flag = StopFlag()
        sniffer_queue = SnifferMessageQueue(
            capacity=SNIFFER_QUEUE_CAPACITY,
            max_payload_bytes=SNIFFER_QUEUE_MAX_PAYLOAD_BYTES,
        )
        session_state = SessionState()
        room_state_cache = RoomStateCache()
        screen_context = ScreenContext(
            browser=controller,
            sniffer_messages=sniffer_queue,
            room_state_cache=room_state_cache,
            account_state=session_state,
            request_stop=stop_flag.request_stop,
            viewport_width=viewport_width_for_height(
                config.browser.viewport_height,
            ),
            viewport_height=config.browser.viewport_height,
        )
        detector = ScreenshotScreenDetector(
            controller.screenshot,
            context=screen_context,
        )
        sniffer_subscriber = ZmqSnifferSubscriber(
            context=cast("AsyncZmqContextLike", context),
            config=config,
        )
        sniffer_runtime = SnifferClientRuntime(
            subscriber=sniffer_subscriber,
            decoder=SnifferMessageDecoder(),
            observer=session_state,
            queue=sniffer_queue,
        )

        async def cleanup() -> None:
            async with AsyncExitStack() as stack:
                stack.callback(context.term)
                stack.callback(socket.close, linger=0)

        return RPARuntime(
            callbacks,
            detector,
            cleanup=cleanup,
            should_stop=stop_flag.is_requested,
            background_service=sniffer_runtime.run,
            background_ready=sniffer_runtime.wait_until_ready,
        )
