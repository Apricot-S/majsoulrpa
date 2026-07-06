import asyncio
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from socket import socket
from typing import Protocol

from majsoulrpa.browser.json_stream import (
    BrowserJsonStreamTransport,
    StreamReaderLike,
)
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestHandler,
)


class StreamWriterLike(Protocol):
    def write(self, data: bytes) -> None: ...
    async def drain(self) -> None: ...
    def close(self) -> None: ...
    async def wait_closed(self) -> None: ...


class AsyncioServerLike(Protocol):
    @property
    def sockets(self) -> Sequence[socket] | None: ...

    def close(self) -> None: ...
    async def wait_closed(self) -> None: ...


ClientConnectedCallback = Callable[
    [StreamReaderLike, StreamWriterLike],
    Awaitable[None],
]
StartServer = Callable[
    [ClientConnectedCallback, str, int],
    Awaitable[AsyncioServerLike],
]


@dataclass(frozen=True)
class BrowserTcpAddress:
    host: str
    port: int


class BrowserTcpServer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        executor: BrowserCommandExecutor,
        start_server: StartServer = asyncio.start_server,
    ) -> None:
        self._host = host
        self._port = port
        self._executor = executor
        self._start_server = start_server
        self._server: AsyncioServerLike | None = None

    @property
    def address(self) -> BrowserTcpAddress:
        if self._server is None:
            msg = "browser TCP server is not running."
            raise RuntimeError(msg)
        return BrowserTcpAddress(self._host, self._bound_port())

    async def start(self) -> None:
        self._server = await self._start_server(
            self._handle_client,
            self._host,
            self._port,
        )

    async def stop(self) -> None:
        if self._server is None:
            return
        server = self._server
        self._server = None
        server.close()
        await server.wait_closed()

    async def _handle_client(
        self,
        reader: StreamReaderLike,
        writer: StreamWriterLike,
    ) -> None:
        transport = BrowserJsonStreamTransport(reader, writer)
        handler = BrowserRequestHandler(transport, self._executor)
        try:
            await handler.serve_forever()
        except EOFError:
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    def _bound_port(self) -> int:
        if self._server is None:
            msg = "browser TCP server is not running."
            raise RuntimeError(msg)
        sockets = self._server.sockets
        if sockets is None:
            return self._port
        if not sockets:
            return self._port
        sockname = sockets[0].getsockname()
        return int(sockname[1])
