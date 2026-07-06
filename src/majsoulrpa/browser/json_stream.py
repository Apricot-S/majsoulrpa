import json
from typing import Protocol

from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserResponse,
    dump_browser_command_json,
    dump_browser_response_json,
    parse_browser_command_json,
    parse_browser_response_json,
)


class StreamReaderLike(Protocol):
    async def readline(self) -> bytes: ...


class StreamWriterLike(Protocol):
    def write(self, data: bytes) -> None: ...
    async def drain(self) -> None: ...


class BrowserJsonStreamTransport:
    def __init__(
        self,
        reader: StreamReaderLike,
        writer: StreamWriterLike,
    ) -> None:
        self._reader = reader
        self._writer = writer

    async def send_command(self, command: BrowserCommand) -> None:
        await self._write_json(dump_browser_command_json(command))

    async def recv_response(self) -> BrowserResponse:
        line = await self._read_line()
        return parse_browser_response_json(line)

    async def recv_command(self) -> BrowserCommand:
        line = await self._read_line()
        return parse_browser_command_json(line)

    async def send_response(self, response: BrowserResponse) -> None:
        await self._write_json(dump_browser_response_json(response))

    async def _read_line(self) -> bytes:
        line = await self._reader.readline()
        if not line:
            msg = "browser JSON stream closed."
            raise EOFError(msg)
        try:
            json.loads(line)
        except json.JSONDecodeError as error:
            msg = "browser JSON stream received invalid JSON."
            raise ValueError(msg) from error
        return line

    async def _write_json(self, payload: bytes) -> None:
        self._writer.write(payload + b"\n")
        await self._writer.drain()
