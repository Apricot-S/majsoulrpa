"""Addon for mitmproxy."""

# ruff: noqa: S101

import re
from enum import IntEnum

import wsproto.frame_protocol
import zmq.asyncio
from mitmproxy import ctx
from mitmproxy.addonmanager import Loader
from mitmproxy.http import HTTPFlow
from mitmproxy.websocket import WebSocketMessage

from majsoulrpa import netutils
from majsoulrpa.constants import DEFAULT_CLIENT_ADDRESS, DEFAULT_SNIFFER_PORT

NOTIFICATION_PATTERN = re.compile(b"^\x01..\n.(.*?)\x12", flags=re.DOTALL)
REQUEST_PATTERN = re.compile(b"^\x02..\n.(.*?)\x12", flags=re.DOTALL)
RESPONSE_PATTERN = re.compile(b"^\x03..\n\x00\x12", flags=re.DOTALL)
HEARTBEAT_PATTERN = re.compile(b"<= heartbeat -", flags=re.DOTALL)


class MessageType(IntEnum):
    NOTIFICATION = 1
    REQUEST = 2
    RESPONSE = 3


class Sniffer:
    def __init__(self) -> None:
        pass

    def load(self, loader: Loader) -> None:
        loader.add_option(
            name="address",
            typespec=str,
            default=DEFAULT_CLIENT_ADDRESS,
            help="IP address to send sniffed messages to",
        )
        loader.add_option(
            name="port",
            typespec=int,
            default=DEFAULT_SNIFFER_PORT,
            help="Port to send sniffed messages to",
        )

    def running(self) -> None:
        address_str: str = ctx.options.address
        port: int = ctx.options.port

        address = netutils.parse_ip_address(address_str)
        user_port = netutils.validate_user_port(port)
        endpoint = netutils.make_endpoint(address, user_port)

        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.PUB)

        if address.version == 6:  # noqa: PLR2004
            self._socket.setsockopt(zmq.IPV6, 1)

        self._socket.bind(f"tcp://{endpoint}")

    def done(self) -> None:
        self._socket.close()
        self._context.destroy()

    def websocket_message(self, flow: HTTPFlow) -> None:
        message = self._get_last_message(flow)

        if message.type != wsproto.frame_protocol.Opcode.BINARY:
            msg = f"{message.type}: An unsupported WebSocket message type."
            raise RuntimeError(msg)

        direction = "outbound" if message.from_client else "inbound"
        content = message.content

        if HEARTBEAT_PATTERN.search(content) is not None:
            # Ignore the heartbeats exchanged in the tournament room
            return

    def _get_last_message(self, flow: HTTPFlow) -> WebSocketMessage:
        websocket_data = flow.websocket
        assert websocket_data is not None
        assert websocket_data.messages
        return websocket_data.messages[-1]


addons = [Sniffer()]
