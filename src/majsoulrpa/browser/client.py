from abc import ABC, abstractmethod
from typing import Self, override

import zmq.asyncio

from majsoulrpa import netutils
from majsoulrpa.browser import schemas


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
    def __init__(self, address: str, port: int) -> None:
        ip_address = netutils.parse_ip_address(address)
        user_port = netutils.validate_user_port(port)
        endpoint = netutils.make_endpoint(ip_address, user_port)

        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        if ip_address.version == 6:  # noqa: PLR2004
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
