import asyncio
import base64
import datetime
import json
from abc import ABCMeta, abstractmethod
from asyncio.queues import Queue
from collections import deque
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, override

import google.protobuf.json_format
import zmq.asyncio
from google.protobuf.message_factory import GetMessageClass

from majsoulrpa._majsoul_internal.protocol import liqi_pb2

if TYPE_CHECKING:
    from google.protobuf.message import Message as ProtobufMessage

type Message = tuple[
    str,
    str,
    dict[str, Any],
    dict[str, Any] | None,
    datetime.datetime,
]


class MessageQueueBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, host: str, port: int) -> None:
        pass

    @abstractmethod
    async def run(self) -> None:
        pass

    @abstractmethod
    async def get(self) -> Message:
        pass

    @abstractmethod
    def get_nowait(self) -> Message | None:
        pass

    @abstractmethod
    def put_back(self, message: Message) -> None:
        pass

    @property
    @abstractmethod
    def account_id(self) -> int | None:
        pass


class MessageQueue(MessageQueueBase):
    _ACCOUNT_ID_MESSAGES: ClassVar[dict[str, list[str]]] = {
        ".lq.Lobby.oauth2Login": ["account_id"],
        ".lq.Lobby.createRoom": ["room", "owner_id"],
    }
    """List of WebSocket messages that can obtain the account id."""

    @override
    def __init__(self, host: str = "127.0.0.1", port: int = 37247) -> None:
        self._host = host
        self._port = port

        self._messages: Queue[Message] = Queue()
        self._put_back_messages: deque[Message] = deque()

        self._wrapper = liqi_pb2.Wrapper()
        self._message_type_map: dict[
            str,
            tuple[type[ProtobufMessage], type[ProtobufMessage] | None],
        ] = {}

        for sdesc in liqi_pb2.DESCRIPTOR.services_by_name.values():
            for mdesc in sdesc.methods:
                self._message_type_map["." + mdesc.full_name] = (
                    GetMessageClass(mdesc.input_type),
                    GetMessageClass(mdesc.output_type),
                )

        for tdesc in liqi_pb2.DESCRIPTOR.message_types_by_name.values():
            self._message_type_map["." + tdesc.full_name] = (
                GetMessageClass(tdesc),
                None,
            )

        self._account_id: int | None = None

    def _unwrap_message(self, message: bytes) -> tuple[str, bytes]:
        self._wrapper.ParseFromString(message)
        return (self._wrapper.name, self._wrapper.data)

    def _enqueue_message(self, message: dict[str, Any]) -> None:
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
            timestamp_float,
            datetime.UTC,
        )

        match request[0]:
            # A request message that does not require a response
            # is missing the two bytes of the message number.
            case 1:
                name, request_data = self._unwrap_message(request[1:])
            # A request message that has a corresponding
            # response message, there are 2 bytes to store
            # the message number, and the name must be extracted to
            # parse the response message.
            case 2:
                name, request_data = self._unwrap_message(request[3:])
            case _:
                msg = f"{request[0]}: unknown request type."
                raise RuntimeError(msg)

        if response is not None:
            if response[0] != 3:  # noqa: PLR2004
                msg = f"{response[0]}: unknown response type."
                raise RuntimeError(msg)
            response_name, response_data = self._unwrap_message(response[3:])
            if response_name != "":
                msg = f"{response_name}: unknown response name."
                raise RuntimeError(msg)
        else:
            response_data = b""

        # Convert Protocol Buffers messages to JSONizable object format
        def jsonize(
            name: str,
            data: bytes,
            *,
            is_response: bool,
        ) -> dict[str, Any]:
            if is_response:
                response = self._message_type_map[name][1]
                if response is None:
                    msg = "There is no response message."
                    raise RuntimeError(msg)

                try:
                    parser = response()
                except IndexError as ie:
                    now = datetime.datetime.now(datetime.UTC)
                    file_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{name}.bin")
                    with Path(file_name).open("wb") as fp:
                        fp.write(data)
                    msg = (
                        "A new API found:\n"
                        f"  name: {name}\n"
                        f"Raw data was saved to {file_name}.\n"
                        "Please cooperate by providing data. "
                        "Thank you for your cooperation."
                    )
                    raise RuntimeError(msg) from ie
            else:
                try:
                    parser = self._message_type_map[name][0]()
                except KeyError as ke:
                    now = datetime.datetime.now(datetime.UTC)
                    file_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{name}.bin")
                    with Path(file_name).open("wb") as fp:
                        fp.write(data)
                    msg = (
                        "A new API found:\n"
                        f"  name: {name}\n"
                        f"Raw data was saved to {file_name}.\n"
                        "Please cooperate by providing data. "
                        "Thank you for your cooperation."
                    )
                    raise RuntimeError(msg) from ke

            parser.ParseFromString(data)

            return google.protobuf.json_format.MessageToDict(
                parser,
                always_print_fields_with_no_presence=True,
                preserving_proto_field_name=True,
            )

        jsonized_request = jsonize(name, request_data, is_response=False)
        if response is not None:
            jsonized_response = jsonize(name, response_data, is_response=True)
        else:
            jsonized_response = None

        # If the message contains an account ID, extract the account ID.
        if name in self._ACCOUNT_ID_MESSAGES:
            if jsonized_response is None:
                msg = "Message without any response."
                raise RuntimeError(msg)
            account_id = jsonized_response
            keys = self._ACCOUNT_ID_MESSAGES[name]
            for key in keys:
                if key not in account_id:
                    msg = (
                        f"{name}: {key}: Could not find account id field:\n"
                        f"{jsonized_response}"
                    )
                    raise RuntimeError(msg)
                account_id = account_id[key]
            if self._account_id is None:
                self._account_id = account_id  # type: ignore[assignment]
            elif account_id != self._account_id:
                msg = "Inconsistent account IDs."
                raise RuntimeError(msg)

        self._messages.put_nowait(
            (
                request_direction,
                name,
                jsonized_request,
                jsonized_response,
                timestamp,
            ),
        )

    @override
    async def run(self) -> None:
        context = zmq.asyncio.Context()  # type: ignore[attr-defined]
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{self._host}:{self._port}")
        socket.subscribe(b"ws")

        while True:
            try:
                _, message_bytes = await socket.recv_multipart()
            except asyncio.CancelledError:
                socket.close()
                context.destroy()
                raise
            message_str = message_bytes.decode(encoding="utf-8")
            message: dict[str, Any] = json.loads(message_str)
            self._enqueue_message(message)

    @override
    async def get(self) -> Message:
        if len(self._put_back_messages) >= 1:
            return self._put_back_messages.popleft()
        return await self._messages.get()

    @override
    def get_nowait(self) -> Message | None:
        if len(self._put_back_messages) >= 1:
            return self._put_back_messages.popleft()
        if self._messages.empty():
            return None
        return self._messages.get_nowait()

    @override
    def put_back(self, message: Message) -> None:
        self._put_back_messages.append(message)

    @property
    @override
    def account_id(self) -> int | None:
        return self._account_id
