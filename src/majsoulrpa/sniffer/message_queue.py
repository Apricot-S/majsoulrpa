from abc import ABC, abstractmethod
from asyncio.queues import Queue
from collections import deque
from ipaddress import IPv4Address, IPv6Address
from typing import Self, override

from google.protobuf.descriptor import FileDescriptor
from google.protobuf.message import Message as ProtobufMessage
from google.protobuf.message_factory import GetMessageClass

from majsoulrpa._majsoul_internal.protocol import liqi_pb2
from majsoulrpa.netutils import UserPort, make_endpoint
from majsoulrpa.sniffer.message import Message


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

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        raise NotImplementedError

    @override
    async def run(self) -> None:
        raise NotImplementedError

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

    def _unwrap_message(self, message: bytes) -> tuple[str, bytes]:
        self._wrapper.ParseFromString(message)
        return (self._wrapper.name, self._wrapper.data)
