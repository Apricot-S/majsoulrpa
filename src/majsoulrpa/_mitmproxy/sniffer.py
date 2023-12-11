# ruff: noqa: S101, INP001
import base64
import datetime
import json
import re
from logging import getLogger
from typing import Final

import grpc  # type:ignore[import-untyped]
import mitmproxy.http
import wsproto.frame_protocol
from majsoulrpa._impl.grpcserver.grpcserver_pb2 import Message
from majsoulrpa._impl.grpcserver.grpcserver_pb2_grpc import GRPCServerStub

logger = getLogger(__name__)

_NUM_SERVER_PORT: Final[int] = 37247

_message_queue: dict[int, dict] = {}
_message_pattern = re.compile(b"^(?:\x01|\x02..)\n.(.*?)\x12", flags=re.DOTALL)
_response_pattern = re.compile(b"^\x03..\n\x00\x12", flags=re.DOTALL)
_channel = grpc.insecure_channel(f"localhost:{_NUM_SERVER_PORT}")
_client = GRPCServerStub(_channel)


def websocket_message(flow: mitmproxy.http.HTTPFlow) -> None:  # noqa: C901, PLR0912, PLR0915
    global _message_queue  # noqa: PLW0602

    websocket_data = flow.websocket
    if websocket_data is None:
        msg = "'websocket_data is None'"
        raise RuntimeError(msg)

    # Get the last message of WebSocket.
    if len(websocket_data.messages) == 0:
        msg = "'len(websocket_data.messages) == 0'"
        raise RuntimeError(msg)
    message = websocket_data.messages[-1]

    if message.type != wsproto.frame_protocol.Opcode.BINARY:
        msg = f"{message.type}: An unsupported WebSocket message type."
        raise RuntimeError(msg)

    direction = "outbound" if message.from_client else "inbound"

    content = message.content

    m = _message_pattern.search(content)
    if m is not None:
        type_ = content[0]
        assert type_ in [1, 2]

        number = None
        name = m.group(1).decode(encoding="utf-8")

        if type_ == 2:  # noqa: PLR2004
            # Processing request messages
            # that expect response messages.
            # Store messages in a queue until
            # a corresponding response message is found.
            number = int.from_bytes(content[1:2], byteorder="little")
            if number in _message_queue:
                prev_request = _message_queue[number]
                msg = (
                    "There is not any response message"
                    " for the following WebSocket request message:\n"
                    f"direction: {prev_request['direction']}\n"
                    f"content: {prev_request['request']}"
                )
                logger.warning(msg)

            _message_queue[number] = {
                "direction": direction,
                "name": name,
                "request": content,
            }

            return

        # Processing request messages that do not require a response
        assert type_ == 1
        assert number is None

        request_direction = direction
        request = content

        if request_direction == "outbound":
            direction = "inbound"
        else:
            assert request_direction == "inbound"
            direction = "outbound"
        response = None

    else:
        # Response message.
        # Find the corresponding request message from the queue.
        m = _response_pattern.search(content)
        if m is None:
            msg = (
                "An unknown WebSocket message:\n"
                f"direction: {direction}\n"
                f"content: {content!r}"
            )
            raise RuntimeError(msg)

        number = int.from_bytes(content[1:2], byteorder="little")
        if number not in _message_queue:
            msg = (
                "An WebSocket response message"
                " that does not match to any request message:\n"
                f"direction: {direction}\n"
                f"content: {content!r}"
            )
            raise RuntimeError(msg)

        request_direction = _message_queue[number]["direction"]
        name = _message_queue[number]["name"]
        request = _message_queue[number]["request"]
        response = content
        del _message_queue[number]

    # Check that the directions of
    # the request and response are consistent.
    if request_direction == "inbound":
        if direction == "inbound":
            msg = "Both request and response WebSocket messages are inbound."
            raise RuntimeError(msg)
        assert direction == "outbound"
    else:
        assert request_direction == "outbound"
        if direction == "outbound":
            msg = "Both request and response WebSocket messages are outbound."
            raise RuntimeError(msg)
        assert direction == "inbound"

    # Encode to JSON format so that it can be enqueueed to DB.
    encoded_request = base64.b64encode(request).decode(encoding="utf-8")
    if response is not None:
        encoded_response = \
            base64.b64encode(response).decode(encoding="utf-8")
    else:
        encoded_response = None
    now = datetime.datetime.now(tz=datetime.UTC)
    data = {
        "request_direction": request_direction,
        "request": encoded_request,
        "response": encoded_response,
        "timestamp": now.timestamp(),
    }

    data_str = json.dumps(data, allow_nan=False, separators=(",", ":"))
    data_bytes = data_str.encode(encoding="utf-8")

    _client.PushMessage(Message(content=data_bytes))
