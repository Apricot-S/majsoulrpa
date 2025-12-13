from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from logging import getLogger
from typing import Self, override

import zmq.asyncio

from majsoulrpa.browser import schemas
from majsoulrpa.netutils import UserPort, make_endpoint

logger = getLogger(__name__)


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
        logger.debug("Initializing browser client")

        self._ctx = zmq.asyncio.Context()
        self._socket = self._ctx.socket(zmq.REQ)
        if address.version == 6:  # noqa: PLR2004
            self._socket.setsockopt(zmq.IPV6, 1)

        self._endpoint = make_endpoint(address, port)
        self._socket.connect(f"tcp://{self._endpoint}")
        logger.info("Connected to browser endpoint %s", self._endpoint)

    @override
    async def __aenter__(self) -> Self:
        return self

    @override
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # noqa: ANN001
        self._close()

    @override
    async def send(self, request: schemas.Request) -> schemas.Response:
        req = request.model_dump_json()
        logger.debug("Sending request: %s", req)
        await self._socket.send_string(req)

        res = await self._socket.recv_string()
        logger.debug(
            "Received response (%d bytes) for %s",
            len(res.encode(encoding="utf-8")),
            req,
        )
        return schemas.RESPONSE_ADAPTER.validate_json(res)

    def _close(self) -> None:
        self._socket.close()
        logger.debug("Closing socket for %s", self._endpoint)

        self._ctx.destroy()
        logger.info("Socket and context destroyed for %s", self._endpoint)
