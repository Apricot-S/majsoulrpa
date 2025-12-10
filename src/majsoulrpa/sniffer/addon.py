"""Addon for mitmproxy."""

# ruff: noqa: S101

import datetime
import re
from base64 import b64encode
from dataclasses import dataclass
from enum import Enum, StrEnum
from logging import getLogger
from typing import Annotated, Literal

import wsproto.frame_protocol
import zmq
from mitmproxy import ctx
from mitmproxy.addonmanager import Loader
from mitmproxy.http import HTTPFlow
from mitmproxy.websocket import WebSocketMessage
from pydantic import BaseModel, Field

from majsoulrpa import netutils
from majsoulrpa.constants import DEFAULT_CLIENT_ADDRESS, DEFAULT_SNIFFER_PORT
from majsoulrpa.sniffer.message import Message

logger = getLogger(__name__)

NOTIFICATION_PATTERN = re.compile(b"^\x01\n.(.*?)\x12", flags=re.DOTALL)
REQUEST_PATTERN = re.compile(b"^\x02..\n.(.*?)\x12", flags=re.DOTALL)
RESPONSE_PATTERN = re.compile(b"^\x03..\n\x00\x12", flags=re.DOTALL)
HEARTBEAT_PATTERN = re.compile(b"<= heartbeat -", flags=re.DOTALL)


class MessageType(Enum):
    NOTIFICATION = 0x01
    REQUEST = 0x02
    RESPONSE = 0x03


class NotificationHeader(BaseModel):
    message_type: Literal[MessageType.NOTIFICATION] = MessageType.NOTIFICATION
    api_name: str


class RequestHeader(BaseModel):
    message_type: Literal[MessageType.REQUEST] = MessageType.REQUEST
    sequence_number: int
    api_name: str


class ResponseHeader(BaseModel):
    message_type: Literal[MessageType.RESPONSE] = MessageType.RESPONSE
    sequence_number: int


type MessageHeader = Annotated[
    NotificationHeader | RequestHeader | ResponseHeader,
    Field(discriminator="message_type"),
]


class Direction(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


@dataclass(frozen=True)
class PendingRequest:
    direction: Direction
    name: str
    content: bytes


@dataclass(frozen=True)
class SniffedMessage:
    request_direction: Direction
    name: str
    request: bytes
    response: bytes | None


def detect_message_type(content: bytes) -> MessageType:
    if not content:
        msg = "empty message"
        raise ValueError(msg)

    first_byte = content[0]
    match first_byte:
        case MessageType.NOTIFICATION.value:
            return MessageType.NOTIFICATION
        case MessageType.REQUEST.value:
            return MessageType.REQUEST
        case MessageType.RESPONSE.value:
            return MessageType.RESPONSE
        case _:
            msg = f"unknown message type: {first_byte:#x}"
            raise ValueError(msg)


def get_message_number(content: bytes) -> int:
    return int.from_bytes(content[1:2], byteorder="little")


def parse_message_header(content: bytes) -> MessageHeader:
    message_type = detect_message_type(content)
    match message_type:
        case MessageType.NOTIFICATION:
            m = NOTIFICATION_PATTERN.match(content)
            if not m:
                msg = "invalid notification format"
                raise ValueError(msg)
            return NotificationHeader(api_name=m.group(1).decode("utf-8"))
        case MessageType.REQUEST:
            m = REQUEST_PATTERN.match(content)
            if not m:
                msg = "invalid request format"
                raise ValueError(msg)
            return RequestHeader(
                sequence_number=get_message_number(content),
                api_name=m.group(1).decode("utf-8"),
            )
        case MessageType.RESPONSE:
            m = RESPONSE_PATTERN.match(content)
            if not m:
                msg = "invalid response format"
                raise ValueError(msg)
            return ResponseHeader(sequence_number=get_message_number(content))
        case _:
            msg = f"unsupported message type: {message_type}"
            raise ValueError(msg)


class Sniffer:
    def __init__(self) -> None:
        self._pending_requests: dict[int, PendingRequest] = {}

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

        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)

        if address.version == 6:  # noqa: PLR2004
            self._socket.setsockopt(zmq.IPV6, 1)

        self._socket.bind(f"tcp://{endpoint}")

    def done(self) -> None:
        self._socket.close()
        self._context.destroy()

    def websocket_message(self, flow: HTTPFlow) -> None:
        message = Sniffer._get_last_message(flow)

        # Validate supported message type
        if message.type != wsproto.frame_protocol.Opcode.BINARY:
            msg = f"{message.type}: An unsupported WebSocket message type."
            raise RuntimeError(msg)

        direction = Sniffer._direction_from_ws_message(message)
        content = message.content

        if HEARTBEAT_PATTERN.search(content) is not None:
            # Ignore the heartbeats exchanged in the tournament room
            return

        header = parse_message_header(content)

        match header:
            case NotificationHeader():
                sniffed = self._handle_notification(header, direction, content)
            case RequestHeader():
                # Request expects a response; queue it and return early.
                self._handle_request(header, direction, content)
                return
            case ResponseHeader():
                sniffed = self._handle_response(header, direction, content)
            case _:
                msg = f"unsupported message type: {type(header)}"
                raise ValueError(msg)

        self._send_sniffed_message(sniffed)

    @staticmethod
    def _get_last_message(flow: HTTPFlow) -> WebSocketMessage:
        websocket_data = flow.websocket
        assert websocket_data is not None
        assert websocket_data.messages
        return websocket_data.messages[-1]

    @staticmethod
    def _direction_from_ws_message(message: WebSocketMessage) -> Direction:
        return Direction.OUTBOUND if message.from_client else Direction.INBOUND

    def _handle_notification(
        self,
        header: NotificationHeader,
        direction: Direction,
        content: bytes,
    ) -> SniffedMessage:
        return SniffedMessage(
            request_direction=direction,
            name=header.api_name,
            request=content,
            response=None,
        )

    def _handle_request(
        self,
        header: RequestHeader,
        direction: Direction,
        content: bytes,
    ) -> None:
        if header.sequence_number in self._pending_requests:
            prev_request = self._pending_requests[header.sequence_number]
            msg = (
                "There is not any response message"
                " for the following WebSocket request message:\n"
                f"direction: {prev_request.direction}\n"
                f"content: {prev_request.content!r}"
            )
            logger.warning(msg)

        self._pending_requests[header.sequence_number] = PendingRequest(
            direction=direction,
            name=header.api_name,
            content=content,
        )

    def _handle_response(
        self,
        header: ResponseHeader,
        direction: Direction,
        content: bytes,
    ) -> SniffedMessage:
        if header.sequence_number not in self._pending_requests:
            msg = (
                "An WebSocket response message"
                " that does not match to any request message:\n"
                f"direction: {direction}\n"
                f"content: {content!r}"
            )
            logger.warning(msg)

        p = self._pending_requests.pop(header.sequence_number)
        request_direction = p.direction
        name = p.name
        request = p.content
        response = content

        # Validate direction consistency for response messages.
        if request_direction == direction:
            msg = (
                f"Both request and response WebSocket messages are {direction}"
            )
            raise RuntimeError(msg)

        return SniffedMessage(
            request_direction=request_direction,
            name=name,
            request=request,
            response=response,
        )

    def _send_sniffed_message(self, sniffed: SniffedMessage) -> None:
        encoded_request = b64encode(sniffed.request).decode(encoding="utf-8")
        encoded_response = (
            b64encode(sniffed.response).decode(encoding="utf-8")
            if sniffed.response is not None
            else None
        )

        data = Message(
            request_direction=sniffed.request_direction.value,
            name=sniffed.name,
            request=encoded_request,
            response=encoded_response,
            timestamp=datetime.datetime.now(tz=datetime.UTC),
        )
        self._socket.send_string(data.model_dump_json())


addons = [Sniffer()]
