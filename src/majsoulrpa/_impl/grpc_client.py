import base64
import datetime
import json
import subprocess
from typing import Any

import google.protobuf.json_format
import grpc  # type:ignore[import-untyped]

from majsoulrpa._impl.protobuf_grpc import grpcserver_pb2
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2_grpc import GRPCServerStub
from majsoulrpa.common import TimeoutType, to_timedelta

from .db_client import DBClientBase, Message
from .proto import liqi_pb2


class GRPCClient(DBClientBase):

    def __init__(self, host: str = "gRPC", port: int = 37247) -> None:
        super().__init__(host, port)
        self._channel = grpc.insecure_channel(f"localhost:{port}")
        self._client = GRPCServerStub(self._channel)

    def dequeue_message(self, timeout: TimeoutType) -> Message | None:  # noqa: C901, PLR0912, PLR0915
        timeout = to_timedelta(timeout)

        if timeout.total_seconds() <= 0.0:  # noqa: PLR2004
            return None

        if len(self._put_back_messages) > 0:
            return self._put_back_messages.popleft()

        message_bytes: bytes = self._client.PopMessage(
                grpcserver_pb2.Timeout(seconds=timeout.total_seconds()),
            ).content
        if message_bytes == b"":
            return None

        message_str = message_bytes.decode(encoding="utf-8")
        message = json.loads(message_str)
        request_direction: str = message["request_direction"]
        encoded_request: str = message["request"]
        encoded_response: str | None = message["response"]
        timestamp_float: float = message["timestamp"]

        # Decode the data that was encoded for JSON.
        request = base64.b64decode(encoded_request)
        if encoded_response is not None:
            response = base64.b64decode(encoded_response)
        else:
            response = None
        timestamp = datetime.datetime.fromtimestamp(
            timestamp_float, datetime.UTC,
        )

        def unwrap_message(message: bytes) -> tuple[str, bytes]:
            wrapper = liqi_pb2.Wrapper() # type: ignore[attr-defined]
            wrapper.ParseFromString(message)
            return (wrapper.name, wrapper.data)

        match request[0]:
            # A request message that does not require a response
            # is missing the two bytes of the message number.
            case 1:
                name, request_data = unwrap_message(request[1:])
            # A request message that has a corresponding
            # response message, there are 2 bytes to store
            # the message number, and the name must be extracted to
            # parse the response message.
            case 2:
                name, request_data = unwrap_message(request[3:])
            case _:
                msg = f"{request[0]}: unknown request type."
                raise RuntimeError(msg)

        if response is not None:
            if response[0] != 3:  # noqa: PLR2004
                msg = f"{response[0]}: unknown response type."
                raise RuntimeError(msg)
            response_name, response_data = unwrap_message(response[3:])
            if response_name != "":
                msg = f"{response_name}: unknown response name."
                raise RuntimeError(msg)
        else:
            response_data = b""

        # Convert Protocol Buffers messages to JSONizable object format
        def jsonize(name: str, data: bytes, *, is_response: bool) \
                -> dict[str, Any]:
            if is_response:
                try:
                    parser = self._message_type_map[name][1]()
                except IndexError as ie:
                    proc = subprocess.run(
                        ["protoc", "--decode_raw"],  # noqa: S603, S607
                        input=data, capture_output=True, check=True,
                    )
                    stdout = proc.stdout.decode("utf-8")
                    msg = (
                        "A new API found:\n"
                        f"  name: {name}\n"
                        f"  data: {data!r}\n"
                        "\n"
                        "===============================\n"
                        "Output of 'protoc --decode_raw'\n"
                        "===============================\n"
                        f"{stdout}"
                    )
                    raise RuntimeError(msg) from ie
            else:
                try:
                    parser = self._message_type_map[name][0]()
                except KeyError as ke:
                    proc = subprocess.run(
                        ["protoc", "--decode_raw"],  # noqa: S603, S607
                        input=data, capture_output=True, check=True,
                    )
                    stdout = proc.stdout.decode("utf-8")
                    msg = (
                        "A new API found:\n"
                        f"  name: {name}\n"
                        f"  data: {data!r}\n"
                        "\n"
                        "===============================\n"
                        "Output of 'protoc --decode_raw'\n"
                        "===============================\n"
                        f"{stdout}"
                    )
                    raise RuntimeError(msg) from ke

            parser.ParseFromString(data)

            return google.protobuf.json_format.MessageToDict(
                parser,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
            )

        jsonized_request = jsonize(name, request_data, is_response=False)
        if response is not None:
            jsonized_response = jsonize(name, response_data, is_response=True)
        else:
            jsonized_response = None

        # If the message contains an account ID,
        # extract the account ID.
        if name in DBClientBase._ACCOUNT_ID_MESSAGES:  # noqa: SLF001
            if jsonized_response is None:
                msg = "Message without any response."
                raise RuntimeError(msg)
            account_id = jsonized_response
            keys = DBClientBase._ACCOUNT_ID_MESSAGES[name]  # noqa: SLF001
            for key in keys:
                if key not in account_id:
                    msg = (
                        f"{name}: {key}: Could not find account id field:\n"
                        f"{jsonized_response}"
                    )
                    raise RuntimeError(msg)
                account_id = account_id[key]
            if self._account_id is None:
                self._account_id = account_id # type: ignore[assignment]
            elif account_id != self._account_id:
                msg = "Inconsistent account IDs."
                raise RuntimeError(msg)

        return (
            request_direction, name, jsonized_request, jsonized_response,
            timestamp,
        )