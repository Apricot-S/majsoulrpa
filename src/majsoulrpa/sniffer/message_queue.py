import base64
from abc import ABC, abstractmethod
from asyncio.queues import Queue
from collections import deque
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Self, override

import zmq.asyncio
from google.protobuf.descriptor import FileDescriptor
from google.protobuf.message import Message as ProtobufMessage
from google.protobuf.message_factory import GetMessageClass

from majsoulrpa._majsoul_internal.protocol import liqi_pb2
from majsoulrpa.netutils import UserPort, make_endpoint
from majsoulrpa.sniffer.exceptions import UnknownAPIError
from majsoulrpa.sniffer.message import Message, MessageType


def _build_message_type_map(
    descriptor: FileDescriptor,
) -> dict[str, tuple[type[ProtobufMessage], type[ProtobufMessage] | None]]:
    mapping: dict[
        str,
        tuple[type[ProtobufMessage], type[ProtobufMessage] | None],
    ] = {}

    for sdesc in descriptor.services_by_name.values():
        for mdesc in sdesc.methods:
            MESSAGE_TYPE_MAP["." + mdesc.full_name] = (
                GetMessageClass(mdesc.input_type),
                GetMessageClass(mdesc.output_type),
            )

    for tdesc in descriptor.message_types_by_name.values():
        MESSAGE_TYPE_MAP["." + tdesc.full_name] = (
            GetMessageClass(tdesc),
            None,
        )

    return mapping


MESSAGE_TYPE_MAP: dict = _build_message_type_map(liqi_pb2.DESCRIPTOR)


class MessageQueueBase(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
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
    def __init__(
        self,
        address: IPv4Address | IPv6Address,
        port: UserPort,
    ) -> None:
        self._endpoint = make_endpoint(address, port)
        self._messages: Queue[Message] = Queue()
        self._put_back_messages: deque[Message] = deque()
        self._wrapper = liqi_pb2.Wrapper()
        self._account_id: int | None = None

        self._ctx: zmq.asyncio.Context | None = None
        self._socket: zmq.asyncio.Socket | None = None

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self._close()

    @override
    async def run(self) -> None:
        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.SUB)
        self._socket.setsockopt(zmq.SUBSCRIBE, "")
        self._socket.connect(f"tcp://{self._endpoint}")

        while True:
            message_str = await self._socket.recv_string()
            message = Message.model_validate_json(message_str)
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

    def _close(self) -> None:
        if self._socket is not None:
            self._socket.close()
        if self._ctx is not None:
            self._ctx.destroy()

    def _enqueue_message(self, message: Message) -> None:
        request_direction = message.request_direction
        encoded_request = message.request
        encoded_response = message.response
        timestamp = message.timestamp

        request = base64.b64decode(encoded_request)
        response = (
            base64.b64decode(encoded_response)
            if encoded_response is not None
            else None
        )

        name, request_data = self._parse_request(request)
        jsonized_request = self._jsonize_request(name, request_data)

        if response is not None:
            response_data = self._parse_response(response)
            jsonized_response = self._jsonize_response(name, response_data)
        else:
            jsonized_response = None

    def _unwrap_message(self, message: bytes) -> tuple[str, bytes]:
        self._wrapper.ParseFromString(message)
        return (self._wrapper.name, self._wrapper.data)

    def _parse_request(self, request: bytes) -> tuple[str, bytes]:
        match request[0]:
            case MessageType.NOTIFICATION.value:
                # A request message that does not require a response
                # is missing the two bytes of the message number.
                return self._unwrap_message(request[1:])
            case MessageType.REQUEST.value:
                # A request message that has a corresponding
                # response message, there are 2 bytes to store
                # the message number, and the name must be extracted to
                # parse the response message.
                return self._unwrap_message(request[3:])
            case _:
                msg = f"{request[0]}: unknown request type."
                raise RuntimeError(msg)

    def _parse_response(self, response: bytes) -> bytes:
        if response[0] != MessageType.RESPONSE.value:
            msg = f"{response[0]}: unknown response type."
            raise RuntimeError(msg)

        name, data = self._unwrap_message(response[3:])
        if name != "":
            msg = f"{name}: unknown response name."
            raise RuntimeError(msg)

        return data

    def _jsonize_request(self, name: str, data: bytes) -> dict[str, Any]:
        raise NotImplementedError

    def _jsonize_response(self, name: str, data: bytes) -> dict[str, Any]:
        response = MESSAGE_TYPE_MAP[name][1]
        if response is None:
            msg = f"message type `{name}` does not define a response."
            raise RuntimeError(msg)

        try:
            parser = response()
        except IndexError as e:
            raise UnknownAPIError(name, data) from e

        raise NotImplementedError
