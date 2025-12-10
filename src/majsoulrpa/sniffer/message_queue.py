from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from typing import Self, override

from majsoulrpa.netutils import UserPort, make_endpoint
from majsoulrpa.sniffer.message import Message


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
        self._account_id: int | None = None

    @override
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        raise NotImplementedError

    @override
    async def run(self) -> None:
        raise NotImplementedError

    @override
    async def get(self) -> Message:
        raise NotImplementedError

    @override
    def get_nowait(self) -> Message | None:
        raise NotImplementedError

    @override
    def put_back(self, message: Message) -> None:
        raise NotImplementedError

    @property
    @override
    def account_id(self) -> int | None:
        return self._account_id
