import asyncio
from uuid import uuid4

import zmq
import zmq.asyncio

from majsoulrpa.browser import (
    BrowserZmqClientTransport,
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
