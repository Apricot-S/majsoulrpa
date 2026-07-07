import warnings
from typing import Protocol, overload

import zmq
import zmq.asyncio
from zmq.asyncio import Socket

from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserResponse,
    dump_browser_command_json,
    dump_browser_response_json,
    parse_browser_command_json,
    parse_browser_response_json,
)
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestHandler,
)


class BrowserZmqSocket(Protocol):
    async def send(self, payload: bytes) -> object: ...
    async def recv(self) -> bytes: ...


class BrowserZmqClientTransport:
    @overload
    def __init__(self, socket: Socket) -> None: ...

    @overload
    def __init__(self, socket: BrowserZmqSocket) -> None: ...

    def __init__(self, socket: Socket | BrowserZmqSocket) -> None:
        self._socket = socket

    async def send_command(self, command: BrowserCommand) -> None:
        await self._socket.send(dump_browser_command_json(command))

    async def recv_response(self) -> BrowserResponse:
        payload = await self._socket.recv()
        return parse_browser_response_json(payload)


class BrowserZmqServerTransport:
    @overload
    def __init__(self, socket: Socket) -> None: ...

    @overload
    def __init__(self, socket: BrowserZmqSocket) -> None: ...

    def __init__(self, socket: Socket | BrowserZmqSocket) -> None:
        self._socket = socket

    async def recv_command(self) -> BrowserCommand:
        payload = await self._socket.recv()
        return parse_browser_command_json(payload)

    async def send_response(self, response: BrowserResponse) -> None:
        await self._socket.send(dump_browser_response_json(response))


class BrowserZmqRequestServer:
    def __init__(
        self,
        *,
        context: zmq.asyncio.Context,
        endpoint: str,
        executor: BrowserCommandExecutor,
    ) -> None:
        self._context = context
        self._endpoint = endpoint
        self._executor = executor
        self._socket: Socket | None = None

    async def bind(self) -> None:
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

        socket = self._context.socket(zmq.REP)
        try:
            socket.bind(self._endpoint)
        except Exception:
            socket.close(linger=0)
            raise
        self._socket = socket

    async def serve_forever(self) -> None:
        if self._socket is None:
            msg = "browser ZeroMQ request server is not running."
            raise RuntimeError(msg)
        transport = BrowserZmqServerTransport(self._socket)
        handler = BrowserRequestHandler(transport, self._executor)
        await handler.serve_forever()

    async def stop(self) -> None:
        if self._socket is None:
            return
        socket = self._socket
        self._socket = None
        socket.close(linger=0)
