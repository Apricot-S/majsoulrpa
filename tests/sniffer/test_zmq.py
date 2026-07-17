import asyncio
import datetime
import uuid

import pytest
import zmq

from majsoulrpa.config import AppConfig, EndpointConfig
from majsoulrpa.sniffer.correlator import (
    CorrelatedNotice,
    Direction,
    ObservedEnvelope,
)
from majsoulrpa.sniffer.envelope import NoticeEnvelope
from majsoulrpa.sniffer.publication import (
    SNIFFER_TOPIC,
    NoticePublication,
    dump_publication_json,
)
from majsoulrpa.sniffer.stream import PublicationSequenceGapError
from majsoulrpa.sniffer.zmq import (
    SnifferTransportError,
    ZmqSnifferPublisher,
    ZmqSnifferSubscriber,
)

STREAM_ID = uuid.UUID("12345678-1234-5678-1234-567812345678")
OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


class FakeSocket:
    def __init__(self) -> None:
        self.bound_endpoints: list[str] = []
        self.connected_endpoints: list[str] = []
        self.options: list[tuple[int, bytes | int]] = []
        self.sent: list[list[bytes]] = []
        self.to_receive: list[list[bytes]] = []
        self.closed_lingers: list[int] = []
        self.bind_error: Exception | None = None
        self.connect_error: Exception | None = None
        self.send_error: Exception | None = None

    def bind(self, endpoint: str) -> None:
        if self.bind_error is not None:
            raise self.bind_error
        self.bound_endpoints.append(endpoint)

    def connect(self, endpoint: str) -> None:
        if self.connect_error is not None:
            raise self.connect_error
        self.connected_endpoints.append(endpoint)

    def setsockopt(self, option: int, value: bytes | int) -> None:
        self.options.append((option, value))

    async def send_multipart(self, parts: list[bytes]) -> None:
        if self.send_error is not None:
            raise self.send_error
        self.sent.append(parts)

    async def recv_multipart(self) -> list[bytes]:
        return self.to_receive.pop(0)

    def close(self, *, linger: int) -> None:
        self.closed_lingers.append(linger)


class FakeContext:
    def __init__(self, socket: FakeSocket) -> None:
        self._socket = socket
        self.requested_socket_types: list[int] = []

    def socket(self, socket_type: int) -> FakeSocket:
        self.requested_socket_types.append(socket_type)
        return self._socket


def _notice() -> CorrelatedNotice:
    raw_payload = b"synthetic-notice"
    return CorrelatedNotice(
        observation=ObservedEnvelope(
            connection_id="connection-1",
            direction=Direction.INBOUND,
            frame_sequence=10,
            observed_at=OBSERVED_AT,
            envelope=NoticeEnvelope(
                api_name=".lq.SyntheticNotice",
                body=b"notice-body",
                raw_payload=raw_payload,
            ),
        ),
    )


def _config(
    *,
    browser_host: str = "192.0.2.10",
    client_host: str = "192.0.2.20",
) -> AppConfig:
    return AppConfig(
        endpoint=EndpointConfig(
            browser_host=browser_host,
            client_host=client_host,
            sniffer_port=12001,
        ),
    )


def test_publisher_binds_and_sends_topic_and_json_parts() -> None:
    async def run() -> None:
        socket = FakeSocket()
        context = FakeContext(socket)
        publisher = ZmqSnifferPublisher(
            context=context,
            config=_config(),
            stream_id=STREAM_ID,
        )

        await publisher.bind()
        first = await publisher.publish(_notice())
        second = await publisher.publish(_notice())
        await publisher.stop()

        assert context.requested_socket_types == [zmq.PUB]
        assert socket.bound_endpoints == ["tcp://192.0.2.20:12001"]
        assert [parts[0] for parts in socket.sent] == [
            SNIFFER_TOPIC,
            SNIFFER_TOPIC,
        ]
        assert first.publication_sequence == 1
        assert second.publication_sequence == 2
        assert socket.closed_lingers == [0]

    asyncio.run(run())


def test_publisher_enables_ipv6_for_ipv6_bind_address() -> None:
    async def run() -> None:
        socket = FakeSocket()
        publisher = ZmqSnifferPublisher(
            context=FakeContext(socket),
            config=_config(client_host="::1"),
            stream_id=STREAM_ID,
        )

        await publisher.bind()

        assert socket.options == [(zmq.IPV6, 1)]
        assert socket.bound_endpoints == ["tcp://[::1]:12001"]

    asyncio.run(run())


def test_subscriber_connects_subscribes_and_receives_publication() -> None:
    async def run() -> None:
        publisher_socket = FakeSocket()
        publisher = ZmqSnifferPublisher(
            context=FakeContext(publisher_socket),
            config=_config(),
            stream_id=STREAM_ID,
        )
        await publisher.bind()
        expected = await publisher.publish(_notice())

        subscriber_socket = FakeSocket()
        subscriber_socket.to_receive.append(publisher_socket.sent[0])
        context = FakeContext(subscriber_socket)
        subscriber = ZmqSnifferSubscriber(
            context=context,
            config=_config(),
        )
        await subscriber.connect()

        received = await subscriber.receive()
        await subscriber.stop()
        await publisher.stop()

        assert context.requested_socket_types == [zmq.SUB]
        assert subscriber_socket.options == [(zmq.SUBSCRIBE, SNIFFER_TOPIC)]
        assert subscriber_socket.connected_endpoints == [
            "tcp://192.0.2.10:12001",
        ]
        assert received == expected
        assert isinstance(received, NoticePublication)
        assert subscriber_socket.closed_lingers == [0]

    asyncio.run(run())


def test_subscriber_enables_ipv6_for_ipv6_connection_address() -> None:
    async def run() -> None:
        socket = FakeSocket()
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(browser_host="::1"),
        )

        await subscriber.connect()

        assert socket.options == [
            (zmq.IPV6, 1),
            (zmq.SUBSCRIBE, SNIFFER_TOPIC),
        ]
        assert socket.connected_endpoints == ["tcp://[::1]:12001"]

    asyncio.run(run())


def test_subscriber_records_when_first_publication_starts_midstream() -> None:
    async def run() -> None:
        publisher_socket = FakeSocket()
        publisher = ZmqSnifferPublisher(
            context=FakeContext(publisher_socket),
            config=_config(),
            stream_id=STREAM_ID,
        )
        await publisher.bind()
        publication = await publisher.publish(_notice())
        publication = publication.model_copy(
            update={"publication_sequence": 4},
        )

        socket = FakeSocket()
        socket.to_receive.append(
            [SNIFFER_TOPIC, dump_publication_json(publication)],
        )
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(),
        )
        await subscriber.connect()

        assert await subscriber.receive() == publication
        assert subscriber.started_midstream is True

    asyncio.run(run())


def test_subscriber_rejects_publication_sequence_gap() -> None:
    async def run() -> None:
        publisher_socket = FakeSocket()
        publisher = ZmqSnifferPublisher(
            context=FakeContext(publisher_socket),
            config=_config(),
            stream_id=STREAM_ID,
        )
        await publisher.bind()
        first = await publisher.publish(_notice())
        third = first.model_copy(update={"publication_sequence": 3})

        socket = FakeSocket()
        socket.to_receive.extend(
            [
                [SNIFFER_TOPIC, dump_publication_json(first)],
                [SNIFFER_TOPIC, dump_publication_json(third)],
            ],
        )
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(),
        )
        await subscriber.connect()

        assert await subscriber.receive() == first
        with pytest.raises(PublicationSequenceGapError):
            await subscriber.receive()

    asyncio.run(run())


@pytest.mark.parametrize(
    "parts",
    [
        [SNIFFER_TOPIC],
        [SNIFFER_TOPIC, b"{}", b"unexpected"],
        [b"unexpected.topic", b"{}"],
    ],
)
def test_subscriber_rejects_invalid_multipart_message(
    parts: list[bytes],
) -> None:
    async def run() -> None:
        socket = FakeSocket()
        socket.to_receive.append(parts)
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(),
        )
        await subscriber.connect()

        with pytest.raises(SnifferTransportError):
            await subscriber.receive()

    asyncio.run(run())


def test_publisher_closes_socket_when_bind_fails() -> None:
    async def run() -> None:
        socket = FakeSocket()
        socket.bind_error = RuntimeError("bind failed")
        publisher = ZmqSnifferPublisher(
            context=FakeContext(socket),
            config=_config(),
            stream_id=STREAM_ID,
        )

        with pytest.raises(RuntimeError, match="bind failed"):
            await publisher.bind()

        assert socket.closed_lingers == [0]

    asyncio.run(run())


def test_subscriber_closes_socket_when_connect_fails() -> None:
    async def run() -> None:
        socket = FakeSocket()
        socket.connect_error = RuntimeError("connect failed")
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(),
        )

        with pytest.raises(RuntimeError, match="connect failed"):
            await subscriber.connect()

        assert socket.closed_lingers == [0]

    asyncio.run(run())


def test_failed_publish_does_not_advance_sequence() -> None:
    async def run() -> None:
        socket = FakeSocket()
        publisher = ZmqSnifferPublisher(
            context=FakeContext(socket),
            config=_config(),
            stream_id=STREAM_ID,
        )
        await publisher.bind()
        socket.send_error = RuntimeError("send failed")

        with pytest.raises(RuntimeError, match="send failed"):
            await publisher.publish(_notice())

        socket.send_error = None
        publication = await publisher.publish(_notice())
        assert publication.publication_sequence == 1

    asyncio.run(run())
