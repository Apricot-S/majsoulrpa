"""Addon for mitmproxy."""

# ruff: noqa: S101

import re
from enum import Enum, StrEnum
from typing import Annotated, Literal, TypedDict

import wsproto.frame_protocol
import zmq.asyncio
from mitmproxy import ctx
from mitmproxy.addonmanager import Loader
from mitmproxy.http import HTTPFlow
from mitmproxy.websocket import WebSocketMessage
from pydantic import BaseModel, Field

from majsoulrpa import netutils
from majsoulrpa.constants import DEFAULT_CLIENT_ADDRESS, DEFAULT_SNIFFER_PORT

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


class PendingRequest(TypedDict):
    direction: Direction
    name: str
    request: bytes


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
                msg = "Invalid request format"
                raise ValueError(msg)
            return RequestHeader(
                sequence_number=get_message_number(content),
                api_name=m.group(1).decode("utf-8"),
            )
        case MessageType.RESPONSE:
            m = RESPONSE_PATTERN.match(content)
            if not m:
                msg = "Invalid response format"
                raise ValueError(msg)
            return ResponseHeader(sequence_number=get_message_number(content))
        case _:
            msg = f"unsupported message type: {message_type}"
            raise ValueError(msg)


class Sniffer:
    def __init__(self) -> None:
        self._message_queue: dict[int, PendingRequest] = {}

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
        message = Sniffer._get_last_message(flow)

        if message.type != wsproto.frame_protocol.Opcode.BINARY:
            msg = f"{message.type}: An unsupported WebSocket message type."
            raise RuntimeError(msg)

        if message.from_client:
            direction = Direction.OUTBOUND
        else:
            direction = Direction.INBOUND

        content = message.content

        if HEARTBEAT_PATTERN.search(content) is not None:
            # Ignore the heartbeats exchanged in the tournament room
            return

        header = parse_message_header(content)
        match header:
            case NotificationHeader():
                # Process a request message that do not require
                # a response.
                request_direction = direction

                match request_direction:
                    case Direction.OUTBOUND:
                        direction = Direction.INBOUND
                    case Direction.INBOUND:
                        direction = Direction.OUTBOUND

                request = content
                response = None
            case RequestHeader():
                # Process a request message that expect a response
                # message. Queue the message until a corresponding
                # response message is found.
                if header.sequence_number in self._message_queue:
                    # TODO: リクエストメッセージに対する応答がないまま
                    # 同じリクエストメッセージが来たときの
                    # ログの対応をする
                    pass

                self._message_queue[header.sequence_number] = PendingRequest(
                    direction=direction,
                    name=header.api_name,
                    request=content,
                )

                return
            case ResponseHeader():
                # Response message.
                # Find the corresponding request message from the queue.
                if header.sequence_number not in self._message_queue:
                    # TODO: レスポンスメッセージに対応する
                    # リクエストメッセージがないときの
                    # ログの対応をする
                    pass

                entry = self._message_queue.pop(header.sequence_number)
                request_direction = entry["direction"]
                name = entry["name"]
                request = entry["request"]
                response = content

    @staticmethod
    def _get_last_message(flow: HTTPFlow) -> WebSocketMessage:
        websocket_data = flow.websocket
        assert websocket_data is not None
        assert websocket_data.messages
        return websocket_data.messages[-1]


addons = [Sniffer()]
