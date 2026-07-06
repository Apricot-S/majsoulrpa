import asyncio
from contextlib import suppress
from uuid import uuid4

import zmq
import zmq.asyncio

from majsoulrpa.browser import (
    BrowserCommand,
    BrowserResponse,
    BrowserZmqClientTransport,
    BrowserZmqRequestServer,
    BrowserZmqServerTransport,
    ClickCommand,
    ClickResponse,
    TextInputCommand,
    TextInputResponse,
)


async def _roundtrip_command_and_response() -> None:
    context = zmq.asyncio.Context()
    server_socket = context.socket(zmq.REP)
    client_socket = context.socket(zmq.REQ)
    endpoint = f"inproc://browser-{uuid4()}"
    try:
        server_socket.bind(endpoint)
        client_socket.connect(endpoint)

        client = BrowserZmqClientTransport(client_socket)
        server = BrowserZmqServerTransport(server_socket)

        await client.send_command(
            ClickCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
            ),
        )
        command = await server.recv_command()
        await server.send_response(ClickResponse(x=25, y=40))
        response = await client.recv_response()
    finally:
        client_socket.close(linger=0)
        server_socket.close(linger=0)
        context.term()

    assert command == ClickCommand(
        x=25,
        y=40,
        mouse_down_up_delay_seconds=0.1,
    )
    assert response == ClickResponse(x=25, y=40)


def test_browser_zmq_transport_roundtrips_command_and_response() -> None:
    asyncio.run(_roundtrip_command_and_response())


async def _server_transport_receives_command_and_sends_response() -> None:
    context = zmq.asyncio.Context()
    server_socket = context.socket(zmq.REP)
    client_socket = context.socket(zmq.REQ)
    endpoint = f"inproc://browser-{uuid4()}"
    try:
        server_socket.bind(endpoint)
        client_socket.connect(endpoint)
        server = BrowserZmqServerTransport(server_socket)

        await client_socket.send_json(
            {
                "type": "text_input",
                "text": "abc",
                "character_delay_seconds": 0.05,
            },
        )
        command = await server.recv_command()
        await server.send_response(TextInputResponse(text="abc"))
        response = await client_socket.recv_json()
    finally:
        client_socket.close(linger=0)
        server_socket.close(linger=0)
        context.term()

    assert command == TextInputCommand(
        text="abc",
        character_delay_seconds=0.05,
    )
    assert response == {"type": "text_input", "text": "abc"}


def test_browser_zmq_server_transport_receives_command() -> None:
    asyncio.run(_server_transport_receives_command_and_sends_response())


class RecordingExecutor:
    def __init__(self) -> None:
        self.commands: list[BrowserCommand] = []

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        self.commands.append(command)
        match command:
            case ClickCommand(x=x, y=y):
                return ClickResponse(x=x, y=y)
            case TextInputCommand(text=text):
                return TextInputResponse(text=text)
            case _:
                msg = "unexpected command"
                raise AssertionError(msg)


async def _zmq_request_server_handles_client_requests() -> None:
    context = zmq.asyncio.Context()
    endpoint = f"inproc://browser-{uuid4()}"
    executor = RecordingExecutor()
    server = BrowserZmqRequestServer(
        context=context,
        endpoint=endpoint,
        executor=executor,
    )
    client_socket = context.socket(zmq.REQ)
    task: asyncio.Task[None] | None = None
    try:
        await server.bind()
        task = asyncio.create_task(server.serve_forever())
        client_socket.connect(endpoint)
        client = BrowserZmqClientTransport(client_socket)

        await client.send_command(
            ClickCommand(
                x=25,
                y=40,
                mouse_down_up_delay_seconds=0.1,
            ),
        )
        click_response = await client.recv_response()

        await client.send_command(
            TextInputCommand(
                text="abc",
                character_delay_seconds=0.05,
            ),
        )
        text_response = await client.recv_response()
    finally:
        if task is not None:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        client_socket.close(linger=0)
        await server.stop()
        context.term()

    assert executor.commands == [
        ClickCommand(
            x=25,
            y=40,
            mouse_down_up_delay_seconds=0.1,
        ),
        TextInputCommand(
            text="abc",
            character_delay_seconds=0.05,
        ),
    ]
    assert click_response == ClickResponse(x=25, y=40)
    assert text_response == TextInputResponse(text="abc")


def test_browser_zmq_request_server_handles_client_requests() -> None:
    asyncio.run(_zmq_request_server_handles_client_requests())
