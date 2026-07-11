import ipaddress
import uuid
from typing import Protocol

import zmq

from majsoulrpa.config import AppConfig
from majsoulrpa.endpoint import (
    make_sniffer_publisher_tcp_endpoint,
    make_sniffer_subscriber_tcp_endpoint,
)
from majsoulrpa.sniffer.correlator import CorrelatedMessage
from majsoulrpa.sniffer.publication import (
    SNIFFER_TOPIC,
    SnifferPublication,
    dump_publication_json,
    make_publication,
    parse_publication_json,
)
from majsoulrpa.sniffer.stream import PublicationStreamTracker


class SnifferTransportError(RuntimeError):
    """Raised when a transport message is structurally invalid."""


class AsyncZmqSocketLike(Protocol):
    def bind(self, endpoint: str) -> None: ...
    def connect(self, endpoint: str) -> None: ...
    def setsockopt(self, option: int, value: bytes | int) -> None: ...
    async def send_multipart(self, parts: list[bytes]) -> object: ...
    async def recv_multipart(self) -> list[bytes]: ...
    def close(self, *, linger: int) -> None: ...


class AsyncZmqContextLike(Protocol):
    def socket(self, socket_type: int) -> AsyncZmqSocketLike: ...


class ZmqSnifferPublisher:
    def __init__(
        self,
        *,
        context: AsyncZmqContextLike,
        config: AppConfig,
        stream_id: uuid.UUID | None = None,
    ) -> None:
        self._context = context
        self._endpoint = make_sniffer_publisher_tcp_endpoint(config)
        self._is_ipv6 = _is_ipv6_literal(config.endpoint.client_host)
        self._stream_id = stream_id or uuid.uuid4()
        self._next_sequence = 1
        self._socket: AsyncZmqSocketLike | None = None

    async def bind(self) -> None:
        if self._socket is not None:
            msg = "Sniffer publisher is already bound."
            raise SnifferTransportError(msg)

        socket = self._context.socket(zmq.PUB)
        try:
            if self._is_ipv6:
                socket.setsockopt(zmq.IPV6, 1)
            socket.bind(self._endpoint)
        except Exception:
            socket.close(linger=0)
            raise
        self._socket = socket

    async def publish(
        self,
        message: CorrelatedMessage,
    ) -> SnifferPublication:
        if self._socket is None:
            msg = "Sniffer publisher is not bound."
            raise SnifferTransportError(msg)

        publication = make_publication(
            message,
            stream_id=self._stream_id,
            publication_sequence=self._next_sequence,
        )
        await self._socket.send_multipart(
            [SNIFFER_TOPIC, dump_publication_json(publication)],
        )
        self._next_sequence += 1
        return publication

    async def stop(self) -> None:
        if self._socket is None:
            return
        socket = self._socket
        self._socket = None
        socket.close(linger=0)


class ZmqSnifferSubscriber:
    def __init__(
        self,
        *,
        context: AsyncZmqContextLike,
        config: AppConfig,
    ) -> None:
        self._context = context
        self._endpoint = make_sniffer_subscriber_tcp_endpoint(config)
        self._is_ipv6 = _is_ipv6_literal(config.endpoint.browser_host)
        self._stream_tracker = PublicationStreamTracker()
        self._socket: AsyncZmqSocketLike | None = None

    @property
    def started_midstream(self) -> bool | None:
        return self._stream_tracker.started_midstream

    async def connect(self) -> None:
        if self._socket is not None:
            msg = "Sniffer subscriber is already connected."
            raise SnifferTransportError(msg)

        socket = self._context.socket(zmq.SUB)
        try:
            if self._is_ipv6:
                socket.setsockopt(zmq.IPV6, 1)
            socket.setsockopt(zmq.SUBSCRIBE, SNIFFER_TOPIC)
            socket.connect(self._endpoint)
        except Exception:
            socket.close(linger=0)
            raise
        self._socket = socket

    async def receive(self) -> SnifferPublication:
        if self._socket is None:
            msg = "Sniffer subscriber is not connected."
            raise SnifferTransportError(msg)

        parts = await self._socket.recv_multipart()
        if len(parts) != 2:  # noqa: PLR2004
            msg = "Sniffer publication must contain exactly two parts."
            raise SnifferTransportError(msg)
        topic, payload = parts
        if topic != SNIFFER_TOPIC:
            msg = "Sniffer publication has an unexpected topic."
            raise SnifferTransportError(msg)
        publication = parse_publication_json(payload)
        self._stream_tracker.observe(publication)
        return publication

    async def stop(self) -> None:
        if self._socket is None:
            return
        socket = self._socket
        self._socket = None
        socket.close(linger=0)


def _is_ipv6_literal(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return isinstance(address, ipaddress.IPv6Address)
