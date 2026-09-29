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
    make_publication,
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
        self.option_errors: dict[int, Exception] = {}

    def bind(self, endpoint: str) -> None:
        if self.bind_error is not None:
            raise self.bind_error
        self.bound_endpoints.append(endpoint)

    def connect(self, endpoint: str) -> None:
        if self.connect_error is not None:
            raise self.connect_error
        self.connected_endpoints.append(endpoint)

    def setsockopt(self, option: int, value: bytes | int) -> None:
        if option in self.option_errors:
            raise self.option_errors[option]
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
    ("topic", "part_count", "error_message"),
    [
        pytest.param(SNIFFER_TOPIC, 0, "exactly two parts", id="empty"),
        pytest.param(
            SNIFFER_TOPIC, 1, "exactly two parts", id="missing-payload"
        ),
        pytest.param(SNIFFER_TOPIC, 3, "exactly two parts", id="extra-part"),
        pytest.param(
            b"unexpected.topic", 2, "unexpected topic", id="wrong-topic"
        ),
        pytest.param(
            SNIFFER_TOPIC + b".extra", 2, "unexpected topic", id="topic-suffix"
        ),
    ],
)
def test_subscriber_rejects_invalid_multipart_message(
    topic: bytes,
    part_count: int,
    error_message: str,
) -> None:
    async def run() -> None:
        publication = make_publication(
            _notice(), stream_id=STREAM_ID, publication_sequence=4
        )
        parts = [topic, dump_publication_json(publication), b"unexpected"][
            :part_count
        ]
        first = make_publication(
            _notice(), stream_id=STREAM_ID, publication_sequence=1
        )
        socket = FakeSocket()
        socket.to_receive.extend(
            [parts, [SNIFFER_TOPIC, dump_publication_json(first)]]
        )
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(),
        )
        await subscriber.connect()

        with pytest.raises(SnifferTransportError, match=error_message):
            await subscriber.receive()
        assert subscriber.started_midstream is None
        assert await subscriber.receive() == first
        assert subscriber.started_midstream is False
        await subscriber.stop()

    asyncio.run(run())


@pytest.mark.parametrize("option", [None, zmq.IPV6], ids=["bind", "ipv6"])
def test_publisher_closes_socket_when_setup_fails(option: int | None) -> None:
    async def run() -> None:
        socket = FakeSocket()
        error = RuntimeError("setup failed")
        if option is None:
            socket.bind_error = error
        else:
            socket.option_errors[option] = error
        publisher = ZmqSnifferPublisher(
            context=FakeContext(socket),
            config=_config(client_host="::1"),
            stream_id=STREAM_ID,
        )

        with pytest.raises(RuntimeError) as caught:
            await publisher.bind()
        assert caught.value is error
        with pytest.raises(SnifferTransportError, match="not bound"):
            await publisher.publish(_notice())
        await publisher.stop()
        assert socket.bound_endpoints == []
        assert socket.closed_lingers == [0]

    asyncio.run(run())


@pytest.mark.parametrize(
    "option",
    [None, zmq.IPV6, zmq.SUBSCRIBE],
    ids=["connect", "ipv6", "subscribe"],
)
def test_subscriber_closes_socket_when_setup_fails(option: int | None) -> None:
    async def run() -> None:
        socket = FakeSocket()
        error = RuntimeError("setup failed")
        if option is None:
            socket.connect_error = error
        else:
            socket.option_errors[option] = error
        subscriber = ZmqSnifferSubscriber(
            context=FakeContext(socket),
            config=_config(browser_host="::1"),
        )

        with pytest.raises(RuntimeError) as caught:
            await subscriber.connect()
        assert caught.value is error
        with pytest.raises(SnifferTransportError, match="not connected"):
            await subscriber.receive()
        await subscriber.stop()
        assert socket.connected_endpoints == []
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
