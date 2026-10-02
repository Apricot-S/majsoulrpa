import asyncio
import base64
import datetime
import uuid
from collections.abc import Iterable

import pytest

from majsoulrpa.assets.protocol.liqi_pb2 import (
    Error,
    NotifyAccountLevelChange,
    ReqHeatBeat,
    ResCommon,
    Wrapper,
)
from majsoulrpa.sniffer.client_runtime import SnifferClientRuntime
from majsoulrpa.sniffer.decoder import SnifferMessageDecoder
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
    RawRequestResponse,
)
from majsoulrpa.sniffer.message_queue import (
    SnifferMessageQueue,
    SnifferMessageQueueOverflowError,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
    SnifferPublication,
)
from majsoulrpa.sniffer.stream import PublicationSequenceGapError


class SubscriberStub:
    def __init__(self, publications: Iterable[SnifferPublication]) -> None:
        self._publications = iter(publications)
        self.connected = False
        self.stopped = False
        self.received: list[SnifferPublication] = []

    async def connect(self) -> None:
        self.connected = True

    async def receive(self) -> SnifferPublication:
        try:
            publication = next(self._publications)
        except StopIteration:
            future: asyncio.Future[SnifferPublication] = (
                asyncio.get_running_loop().create_future()
            )
            return await future
        self.received.append(publication)
        return publication

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
        self.publications: list[SnifferPublication] = []

    def decode(
        self,
        publication: SnifferPublication,
    ) -> DecodedSnifferMessage:
        self.publications.append(publication)
        if self._error is not None:
            raise self._error
        return self._decoded[id(publication)]


class QueueSpy:
    def __init__(
        self,
        *,
        stop_after: int | None = None,
        events: list[str] | None = None,
    ) -> None:
        self.messages: list[DecodedSnifferMessage] = []
        self._stop_after = stop_after
        self._events = events

    def enqueue(self, message: DecodedSnifferMessage) -> None:
        if self._events is not None:
            self._events.append("enqueue")
        self.messages.append(message)
        if self._stop_after == len(self.messages):
            raise StopRuntimeError


class StopRuntimeError(RuntimeError):
    pass


class ObserverSpy:
    def __init__(
        self,
        events: list[str] | None = None,
        *,
        error: Exception | None = None,
    ) -> None:
        self.messages: list[DecodedSnifferMessage] = []
        self._events = events
        self._error = error

    def observe(self, message: DecodedSnifferMessage) -> None:
        if self._events is not None:
            self._events.append("observe")
        self.messages.append(message)
        if self._error is not None:
            raise self._error


def _publication(sequence: int) -> NoticePublication:
    return NoticePublication(
        schema_version=1,
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
    events: list[str] = []
    observer = ObserverSpy(events)
    queue = QueueSpy(stop_after=2, events=events)
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=decoder,
        observer=observer,
        queue=queue,
    )

    with pytest.raises(StopRuntimeError):
        asyncio.run(runtime.run())

    assert subscriber.connected
    assert observer.messages == messages
    assert queue.messages == messages
    assert events == ["observe", "enqueue", "observe", "enqueue"]
    assert subscriber.stopped


def _deliver_with_real_decoder(
    publication: SnifferPublication,
    payload_bytes: int,
) -> DecodedSnifferMessage:
    queue = SnifferMessageQueue(capacity=1, max_payload_bytes=payload_bytes)

    class InspectingObserver(ObserverSpy):
        def observe(self, message: DecodedSnifferMessage) -> None:
            assert queue.get_nowait() is None
            super().observe(message)

    class OnePublicationSubscriber(SubscriberStub):
        async def receive(self) -> SnifferPublication:
            if self.received:
                raise StopRuntimeError
            return await super().receive()

    subscriber = OnePublicationSubscriber([publication])
    observer = InspectingObserver()
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=SnifferMessageDecoder(),
        observer=observer,
        queue=queue,
    )
    with pytest.raises(StopRuntimeError):
        asyncio.run(runtime.run())

    assert len(observer.messages) == 1
    message = queue.get_nowait()
    assert message is observer.messages[0]
    assert message is not None
    assert queue.get_nowait() is None
    assert subscriber.stopped
    return message


def test_runtime_delivers_real_decoded_notice_to_observer_and_queue() -> None:
    name = ".lq.NotifyAccountLevelChange"
    payload = (
        b"\x01"
        + Wrapper(
            name=name,
            data=NotifyAccountLevelChange(type=2).SerializeToString(),
        ).SerializeToString()
    )
    data = _publication(1).model_dump()
    data.update(
        api_name=name, payload_base64=base64.b64encode(payload).decode("ascii")
    )
    publication = NoticePublication.model_validate(data)
    message = _deliver_with_real_decoder(publication, len(payload))
    assert isinstance(message, DecodedNotice)
    assert message.message["type"] == 2
    assert message.raw == RawNotice(
        direction=publication.direction,
        name=name,
        payload=payload,
        observed_at=publication.observed_at,
    )


def test_runtime_delivers_real_decoded_exchange_without_swapping_sides() -> (
    None
):
    name = ".lq.Lobby.heatbeat"
    request = (
        b"\x02\x34\x12"
        + Wrapper(
            name=name,
            data=ReqHeatBeat(no_operation_counter=9).SerializeToString(),
        ).SerializeToString()
    )
    response = (
        b"\x03\x34\x12"
        + Wrapper(
            data=ResCommon(error=Error(code=7)).SerializeToString()
        ).SerializeToString()
    )
    request_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    response_at = request_at + datetime.timedelta(seconds=1)
    publication = RequestResponsePublication(
        schema_version=1,
        stream_id=_publication(1).stream_id,
        publication_sequence=1,
        connection_id="connection-1",
        request_direction=Direction.OUTBOUND,
        request_number=0x1234,
        request_frame_sequence=1,
        response_frame_sequence=2,
        request_observed_at=request_at,
        response_observed_at=response_at,
        api_name=name,
        request_payload_base64=base64.b64encode(request).decode("ascii"),
        response_payload_base64=base64.b64encode(response).decode("ascii"),
    )
    message = _deliver_with_real_decoder(
        publication, len(request) + len(response)
    )

    assert isinstance(message, DecodedRequestResponse)
    assert message.request["no_operation_counter"] == 9
    error = message.response["error"]
    assert isinstance(error, dict)
    assert error["code"] == 7
    assert message.raw == RawRequestResponse(
        request_direction=Direction.OUTBOUND,
        name=name,
        request=request,
        response=response,
        request_observed_at=request_at,
        response_observed_at=response_at,
    )


def test_client_runtime_propagates_decode_error_and_stops_subscriber() -> None:
    publication = _publication(1)
    subscriber = SubscriberStub([publication, _publication(2)])
    error = RuntimeError("decode failed")
    events: list[str] = []
    observer = ObserverSpy(events)
    queue = QueueSpy(events=events)
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub({}, error),
        observer=observer,
        queue=queue,
    )

    with pytest.raises(RuntimeError) as caught:
        asyncio.run(runtime.run())

    assert caught.value is error
    assert events == []
    assert observer.messages == []
    assert queue.messages == []
    assert subscriber.received == [publication]
    assert subscriber.stopped


def test_observer_failure_stops_before_enqueue_and_next_receive() -> None:
    publications = [_publication(1), _publication(2)]
    message = _message(1)
    subscriber = SubscriberStub(publications)
    error = RuntimeError("observer failed")
    observer = ObserverSpy(error=error)
    queue = QueueSpy()
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub({id(publications[0]): message}),
        observer=observer,
        queue=queue,
    )

    with pytest.raises(RuntimeError) as caught:
        asyncio.run(runtime.run())

    assert caught.value is error
    assert observer.messages == [message]
    assert observer.messages[0] is message
    assert queue.messages == []
    assert subscriber.received == [publications[0]]
    assert subscriber.stopped


@pytest.mark.parametrize(
    ("capacity", "max_payload_bytes"),
    [(1, 1024), (3, len(b"synthetic"))],
    ids=["count-limit", "byte-limit"],
)
def test_queue_overflow_stops_receiving_and_preserves_retained_message(
    capacity: int,
    max_payload_bytes: int,
) -> None:
    publications = [_publication(1), _publication(2), _publication(3)]
    messages = [_message(1), _message(2)]
    subscriber = SubscriberStub(publications)
    observer = ObserverSpy()
    queue = SnifferMessageQueue(
        capacity=capacity, max_payload_bytes=max_payload_bytes
    )
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub(
            dict(zip(map(id, publications[:2]), messages, strict=True))
        ),
        observer=observer,
        queue=queue,
    )

    with pytest.raises(SnifferMessageQueueOverflowError):
        asyncio.run(runtime.run())

    assert subscriber.received == publications[:2]
    assert subscriber.stopped
    assert observer.messages == messages
    assert queue.get_nowait() is messages[0]
    assert queue.get_nowait() is None


@pytest.mark.parametrize(
    "error_type",
    [RuntimeError, PublicationSequenceGapError],
    ids=["receive-error", "stream-gap"],
)
def test_receive_failure_stops_after_previously_processed_message(
    error_type: type[Exception],
) -> None:
    error = error_type("receive failed")

    class FailingSubscriber(SubscriberStub):
        receive_calls = 0

        async def receive(self) -> SnifferPublication:
            self.receive_calls += 1
            if self.receive_calls == 2:
                raise error
            return await super().receive()

    first = _publication(1)
    message = _message(1)
    subscriber = FailingSubscriber([first, _publication(2)])
    decoder = DecoderStub({id(first): message})
    observer = ObserverSpy()
    queue = QueueSpy()
    runtime = SnifferClientRuntime(
        subscriber=subscriber, decoder=decoder, observer=observer, queue=queue
    )

    with pytest.raises(error_type) as caught:
        asyncio.run(runtime.run())

    assert caught.value is error
    assert subscriber.receive_calls == 2
    assert subscriber.received == [first]
    assert decoder.publications == [first]
    assert observer.messages == [message]
    assert queue.messages == [message]
    assert subscriber.stopped


def test_client_runtime_stops_subscriber_when_cancelled() -> None:
    async def exercise() -> SubscriberStub:
        subscriber = SubscriberStub([])
        runtime = SnifferClientRuntime(
            subscriber=subscriber,
            decoder=DecoderStub({}),
            observer=ObserverSpy(),
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


@pytest.mark.parametrize("outcome", ["connected", "cancelled"])
def test_ready_waits_for_connect_completion(outcome: str) -> None:
    async def exercise() -> None:
        connecting = asyncio.Event()
        allow_connect = asyncio.Event()

        class BlockingSubscriber(SubscriberStub):
            receive_calls = 0

            async def connect(self) -> None:
                connecting.set()
                await allow_connect.wait()
                await super().connect()

            async def receive(self) -> SnifferPublication:
                self.receive_calls += 1
                return await super().receive()

        subscriber = BlockingSubscriber([])
        runtime = SnifferClientRuntime(
            subscriber=subscriber,
            decoder=DecoderStub({}),
            observer=ObserverSpy(),
            queue=QueueSpy(),
        )
        ready = asyncio.create_task(runtime.wait_until_ready())
        task = asyncio.create_task(runtime.run())
        try:
            async with asyncio.timeout(1):
                await connecting.wait()
            assert not ready.done()
            assert subscriber.receive_calls == 0
            if outcome == "connected":
                allow_connect.set()
                async with asyncio.timeout(1):
                    await asyncio.shield(ready)
                assert subscriber.connected
                assert subscriber.receive_calls == 1

            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert subscriber.stopped
            if outcome == "cancelled":
                assert not ready.done()
                assert not subscriber.connected
                assert subscriber.receive_calls == 0
        finally:
            task.cancel()
            ready.cancel()
            await asyncio.gather(task, ready, return_exceptions=True)

    asyncio.run(exercise())


@pytest.mark.parametrize("stage", ["decode", "cancelled-receive"])
def test_stop_failure_preserves_original_failure(stage: str) -> None:
    decode_error = RuntimeError("decode failed")
    cancellation = asyncio.CancelledError("receive cancelled")
    stop_error = RuntimeError("stop failed")

    class FailingStopSubscriber(SubscriberStub):
        stop_calls = 0

        async def receive(self) -> SnifferPublication:
            if stage == "cancelled-receive":
                raise cancellation
            return await super().receive()

        async def stop(self) -> None:
            self.stop_calls += 1
            raise stop_error

    publication = _publication(1)
    subscriber = FailingStopSubscriber([publication, _publication(2)])
    decoder = DecoderStub({}, error=decode_error)
    observer = ObserverSpy()
    queue = QueueSpy()
    runtime = SnifferClientRuntime(
        subscriber=subscriber, decoder=decoder, observer=observer, queue=queue
    )

    with pytest.raises(RuntimeError) as caught:
        asyncio.run(runtime.run())

    assert caught.value is stop_error
    original_error = decode_error if stage == "decode" else cancellation
    assert stop_error.__context__ is original_error
    assert subscriber.stop_calls == 1
    expected = [publication] if stage == "decode" else []
    assert subscriber.received == expected
    assert decoder.publications == expected
    assert observer.messages == []
    assert queue.messages == []


def test_client_runtime_stops_subscriber_when_connect_fails() -> None:
    class FailingSubscriber(SubscriberStub):
        async def connect(self) -> None:
            msg = "connect failed"
            raise RuntimeError(msg)

    subscriber = FailingSubscriber([])
    runtime = SnifferClientRuntime(
        subscriber=subscriber,
        decoder=DecoderStub({}),
        observer=ObserverSpy(),
        queue=QueueSpy(),
    )

    with pytest.raises(RuntimeError, match="connect failed"):
        asyncio.run(runtime.run())

    assert subscriber.stopped
