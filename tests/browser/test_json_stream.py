import asyncio
import json

import pytest
from pydantic import ValidationError

from majsoulrpa.browser import (
    BrowserJsonStreamTransport,
    ClickCommand,
    ClickResponse,
    TextInputCommand,
    TextInputResponse,
    parse_browser_command_json,
    parse_browser_response_json,
)


class StreamReaderStub:
    def __init__(self, *lines: bytes) -> None:
        self._lines = list(lines)

    async def readline(self) -> bytes:
        if not self._lines:
            return b""
        return self._lines.pop(0)


class StreamWriterSpy:
    def __init__(self) -> None:
        self.written: list[bytes] = []
        self.drained = 0

    def write(self, data: bytes) -> None:
        self.written.append(data)

    async def drain(self) -> None:
        self.drained += 1


def test_browser_json_stream_transport_sends_command_json_line() -> None:
    writer = StreamWriterSpy()
    transport = BrowserJsonStreamTransport(StreamReaderStub(), writer)

    asyncio.run(
        transport.send_command(
            ClickCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
            ),
        ),
    )

    assert writer.drained == 1
    assert writer.written == [
        b'{"type":"click","x":25.0,"y":40.0,'
        b'"mouse_down_up_delay_seconds":0.1}\n',
    ]


def test_browser_json_stream_transport_receives_response() -> None:
    transport = BrowserJsonStreamTransport(
        StreamReaderStub(b'{"type":"click","x":25,"y":40}\n'),
        StreamWriterSpy(),
    )

    response = asyncio.run(transport.recv_response())

    assert response == ClickResponse(x=25, y=40)


def test_json_stream_transport_receives_command_and_sends_response() -> None:
    writer = StreamWriterSpy()
    transport = BrowserJsonStreamTransport(
        StreamReaderStub(
            b'{"type":"text_input","text":"abc",'
            b'"character_delay_seconds":0.05}\n',
        ),
        writer,
    )

    command = asyncio.run(transport.recv_command())
    asyncio.run(transport.send_response(TextInputResponse(text="abc")))

    assert command == TextInputCommand(
        text="abc",
        character_delay_seconds=0.05,
    )
    assert writer.written == [b'{"type":"text_input","text":"abc"}\n']


def test_browser_json_stream_transport_rejects_invalid_json() -> None:
    transport = BrowserJsonStreamTransport(
        StreamReaderStub(b"{invalid json}\n"),
        StreamWriterSpy(),
    )

    with pytest.raises(ValueError, match="invalid JSON"):
        asyncio.run(transport.recv_response())


def test_browser_json_stream_transport_reports_eof() -> None:
    transport = BrowserJsonStreamTransport(
        StreamReaderStub(), StreamWriterSpy()
    )

    with pytest.raises(EOFError, match="closed"):
        asyncio.run(transport.recv_command())


def test_browser_json_parse_helpers_use_discriminated_schema() -> None:
    command = parse_browser_command_json(
        json.dumps(
            {
                "type": "click",
                "x": 25,
                "y": 40,
                "mouse_down_up_delay_seconds": 0.1,
            },
        ),
    )
    response = parse_browser_response_json(
        json.dumps({"type": "click", "x": 25, "y": 40}),
    )

    assert command == ClickCommand(
        x=25,
        y=40,
        mouse_down_up_delay_seconds=0.1,
    )
    assert response == ClickResponse(x=25, y=40)

    with pytest.raises(ValidationError):
        parse_browser_command_json(json.dumps({"type": "unknown"}))
