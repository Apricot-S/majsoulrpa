import datetime
from abc import ABCMeta, abstractmethod
from collections import deque
from typing import TYPE_CHECKING, Any, ClassVar

from google.protobuf.message_factory import GetMessageClass

from majsoulrpa._majsoul_internal.protocol import liqi_pb2
from majsoulrpa.timeout import TimeoutType

if TYPE_CHECKING:
    from google.protobuf.message import Message as ProtobufMessage

type Message = tuple[
    str,
    str,
    dict[str, Any],
    dict[str, Any] | None,
    datetime.datetime,
]


class MessageQueueClientBase(metaclass=ABCMeta):
    def __init__(self, host: str, port: int | None) -> None:  # noqa: ARG002
        self._put_back_messages: deque[Message] = deque()
        self._account_id: int | None = None
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

    # List of WebSocket messages that can obtain account id
    _ACCOUNT_ID_MESSAGES: ClassVar[dict[str, list[str]]] = {
        ".lq.Lobby.oauth2Login": ["account_id"],
        ".lq.Lobby.createRoom": ["room", "owner_id"],
    }

    @abstractmethod
    def dequeue_message(self, timeout: TimeoutType) -> Message | None:
        pass

    def put_back(self, message: Message) -> None:
        self._put_back_messages.appendleft(message)

    @property
    def account_id(self) -> int | None:
        return self._account_id
