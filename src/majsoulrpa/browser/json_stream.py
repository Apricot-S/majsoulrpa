import json
from typing import Protocol

from pydantic import TypeAdapter

from majsoulrpa.browser.messages import BrowserCommand, BrowserResponse

_COMMAND_ADAPTER = TypeAdapter(BrowserCommand)
_RESPONSE_ADAPTER = TypeAdapter(BrowserResponse)


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

    async def send(self, command: BrowserCommand) -> None:
        await self._write_json(_COMMAND_ADAPTER.dump_json(command))

    async def recv(self) -> BrowserResponse:
        line = await self._read_line()
        return _RESPONSE_ADAPTER.validate_json(line)

    async def recv_command(self) -> BrowserCommand:
        line = await self._read_line()
        return _COMMAND_ADAPTER.validate_json(line)

    async def send_response(self, response: BrowserResponse) -> None:
        await self._write_json(_RESPONSE_ADAPTER.dump_json(response))

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


def parse_browser_command_json(payload: str | bytes) -> BrowserCommand:
    return _COMMAND_ADAPTER.validate_json(payload)


def parse_browser_response_json(payload: str | bytes) -> BrowserResponse:
    return _RESPONSE_ADAPTER.validate_json(payload)
