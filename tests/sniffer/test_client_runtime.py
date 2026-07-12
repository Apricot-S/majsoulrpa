import asyncio
import base64
import datetime
import uuid
from collections.abc import Iterable

import pytest

from majsoulrpa.sniffer.client_runtime import SnifferClientRuntime
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    SnifferPublication,
)


class SubscriberStub:
    def __init__(self, publications: Iterable[SnifferPublication]) -> None:
        self._publications = iter(publications)
        self.connected = False
        self.stopped = False

    async def connect(self) -> None:
        self.connected = True

    async def receive(self) -> SnifferPublication:
        try:
            return next(self._publications)
        except StopIteration:
            future: asyncio.Future[SnifferPublication] = (
                asyncio.get_running_loop().create_future()
            )
            return await future

    async def stop(self) -> None:
        self.stopped = True


class DecoderStub:
    def __init__(
        self,
        decoded: dict[int, DecodedSnifferMessage],
        error: Exception | None = None,
    ) -> None:
        self._decoded = decoded
        self._error = error

    def decode(
        self,
        publication: SnifferPublication,
    ) -> DecodedSnifferMessage:
        if self._error is not None:
            raise self._error
        return self._decoded[id(publication)]


class QueueSpy:
    def __init__(self, *, stop_after: int | None = None) -> None:
        self.messages: list[DecodedSnifferMessage] = []
        self._stop_after = stop_after

    def enqueue(self, message: DecodedSnifferMessage) -> None:
        self.messages.append(message)
        if self._stop_after == len(self.messages):
            raise StopRuntimeError


class StopRuntimeError(RuntimeError):
    pass


def _publication(sequence: int) -> NoticePublication:
    return NoticePublication(
        stream_id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        publication_sequence=sequence,
        connection_id="connection-1",
        direction=Direction.INBOUND,
        frame_sequence=sequence,
        observed_at=datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
        api_name=f".lq.Synthetic{sequence}",
        payload_base64=base64.b64encode(b"synthetic").decode("ascii"),
    )


def _message(sequence: int) -> DecodedNotice:
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=f".lq.Synthetic{sequence}",
            payload=b"synthetic",
            observed_at=datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
        ),
        message={},
    )


def test_client_runtime_connects_decodes_and_enqueues_every_publication() -> (
    None
):
    publications = [_publication(1), _publication(2)]
    messages = [_message(1), _message(2)]
    subscriber = SubscriberStub(publications)
    decoder = DecoderStub(
        dict(zip(map(id, publications), messages, strict=True)),
    )
    queue = QueueSpy(stop_after=2)
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=decoder,
        queue=queue,
    )

    with pytest.raises(StopRuntimeError):
        asyncio.run(runtime.run())

    assert subscriber.connected
    assert queue.messages == messages
    assert subscriber.stopped


def test_client_runtime_propagates_decode_error_and_stops_subscriber() -> None:
    publication = _publication(1)
    subscriber = SubscriberStub([publication])
    error = RuntimeError("decode failed")
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub({}, error),
        queue=QueueSpy(),
    )

    with pytest.raises(RuntimeError, match="decode failed"):
        asyncio.run(runtime.run())

    assert subscriber.stopped


def test_client_runtime_stops_subscriber_when_cancelled() -> None:
    async def exercise() -> SubscriberStub:
        subscriber = SubscriberStub([])
        runtime = SnifferClientRuntime(
            subscriber=subscriber,
            decoder=DecoderStub({}),
            queue=QueueSpy(),
        )
        task = asyncio.create_task(runtime.run())
        await runtime.wait_until_ready()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        return subscriber

    subscriber = asyncio.run(exercise())

    assert subscriber.connected
    assert subscriber.stopped


def test_client_runtime_stops_subscriber_when_connect_fails() -> None:
    class FailingSubscriber(SubscriberStub):
        async def connect(self) -> None:
            msg = "connect failed"
            raise RuntimeError(msg)

    subscriber = FailingSubscriber([])
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub({}),
        queue=QueueSpy(),
    )

    with pytest.raises(RuntimeError, match="connect failed"):
        asyncio.run(runtime.run())

    assert subscriber.stopped
