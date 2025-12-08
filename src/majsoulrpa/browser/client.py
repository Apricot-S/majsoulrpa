from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from typing import Self, override

import zmq.asyncio

from majsoulrpa.browser import schemas
from majsoulrpa.netutils import UserPort, make_endpoint


class ClientBase(ABC):
    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        pass

    @abstractmethod
    async def send(self, request: schemas.Request) -> schemas.Response:
        pass


class Client(ClientBase):
    def __init__(
        self,
        address: IPv4Address | IPv6Address,
        port: UserPort,
    ) -> None:
        endpoint = make_endpoint(address, port)

        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        if address.version == 6:  # noqa: PLR2004
            self._socket.setsockopt(zmq.IPV6, 1)

        self._socket.connect(f"tcp://{endpoint}")

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self._close()

    @override
    async def send(self, request: schemas.Request) -> schemas.Response:
        await self._socket.send_string(request.model_dump_json())
        res = await self._socket.recv_string()
        return schemas.RESPONSE_ADAPTER.validate_json(res)

    def _close(self) -> None:
        self._socket.close()
        self._ctx.destroy()
