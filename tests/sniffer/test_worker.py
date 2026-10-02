import asyncio
import datetime
from collections.abc import Sequence

import pytest

from majsoulrpa.assets.protocol.liqi_pb2 import Wrapper
from majsoulrpa.sniffer.correlator import (
    CorrelatedMessage,
    CorrelatedNotice,
    CorrelatedRequestResponse,
    Direction,
    IncompleteExchangeError,
    RequestResponseCorrelator,
    UnmatchedResponseError,
)
from majsoulrpa.sniffer.envelope import SnifferDecodeError
from majsoulrpa.sniffer.playwright import (
    CapturedConnectionClosed,
    CapturedFrame,
    CaptureEvent,
)
from majsoulrpa.sniffer.worker import SnifferWorker

OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


class FakeCapture:
    def __init__(
        self,
        events: Sequence[CaptureEvent] = (),
        *,
        error: Exception | None = None,
    ) -> None:
        self.events = list(events)
        self.error = error

    async def receive(self) -> CaptureEvent:
        if self.events:
            return self.events.pop(0)
        if self.error is not None:
            raise self.error
        msg = "No synthetic capture event is available."
        raise AssertionError(msg)


class FakePublisher:
    def __init__(self, *, error: Exception | None = None) -> None:
        self.messages: list[CorrelatedMessage] = []
        self.attempts: list[CorrelatedMessage] = []
        self.error = error

    async def publish(self, message: CorrelatedMessage) -> object:
        self.attempts.append(message)
        if self.error is not None:
            raise self.error
        self.messages.append(message)
        return object()


def _frame(
    payload: bytes,
    *,
    direction: Direction,
    frame_sequence: int,
    connection_id: str = "connection-1",
) -> CapturedFrame:
    return CapturedFrame(
        connection_id=connection_id,
        frame_sequence=frame_sequence,
        direction=direction,
        observed_at=OBSERVED_AT,
        payload=payload,
    )


def _notice_payload() -> bytes:
    return (
        b"\x01"
        + Wrapper(
            name=".lq.SyntheticNotice",
            data=b"notice-body",
        ).SerializeToString()
    )


def _request_payload() -> bytes:
    return (
        b"\x02\x34\x12"
        + Wrapper(
            name=".lq.SyntheticService.call",
            data=b"request-body",
        ).SerializeToString()
    )


def _response_payload() -> bytes:
    return (
        b"\x03\x34\x12"
        + Wrapper(
            data=b"response-body",
        ).SerializeToString()
    )


def test_worker_preserves_falsey_injected_correlator() -> None:
    class FalseyCorrelator(RequestResponseCorrelator):
        def __bool__(self) -> bool:
            return False

    async def run() -> None:
        correlator = FalseyCorrelator()
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture(
                [
                    _frame(
                        _request_payload(),
                        direction=Direction.OUTBOUND,
                        frame_sequence=1,
                    ),
                ]
            ),
            publisher=publisher,
            correlator=correlator,
        )

        assert await worker.process_once() is None
        assert publisher.messages == []
        with pytest.raises(IncompleteExchangeError, match="1 pending"):
            correlator.stop()
        await worker.stop()

    asyncio.run(run())


def test_worker_publishes_notice_immediately() -> None:
    async def run() -> None:
        frame = _frame(
            _notice_payload(),
            direction=Direction.INBOUND,
            frame_sequence=1,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture([frame]),
            publisher=publisher,
        )

        correlated = await worker.process_once()

        assert isinstance(correlated, CorrelatedNotice)
        assert correlated.observation.connection_id == "connection-1"
        assert correlated.observation.frame_sequence == 1
        assert correlated.observation.direction is Direction.INBOUND
        assert correlated.observation.observed_at == OBSERVED_AT
        assert publisher.messages == [correlated]

    asyncio.run(run())


def test_pending_request_survives_heartbeat_and_notice() -> None:
    async def run() -> None:
        request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=1,
        )
        heartbeat = _frame(
            b"<= heartbeat - synthetic payload",
            direction=Direction.INBOUND,
            frame_sequence=2,
        )
        notice = _frame(
            _notice_payload(),
            direction=Direction.INBOUND,
            frame_sequence=3,
        )
        response = _frame(
            _response_payload(),
            direction=Direction.INBOUND,
            frame_sequence=4,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture([request, heartbeat, notice, response]),
            publisher=publisher,
        )

        assert await worker.process_once() is None
        assert publisher.messages == []
        assert await worker.process_once() is None
        assert publisher.attempts == []

        correlated_notice = await worker.process_once()
        assert isinstance(correlated_notice, CorrelatedNotice)
        assert correlated_notice.observation.frame_sequence == 3
        assert publisher.messages == [correlated_notice]
        correlated = await worker.process_once()

        assert isinstance(correlated, CorrelatedRequestResponse)
        assert correlated.request.frame_sequence == 1
        assert correlated.response.frame_sequence == 4
        assert publisher.messages == [correlated_notice, correlated]
        assert publisher.attempts == publisher.messages
        await worker.stop()

    asyncio.run(run())


def test_worker_close_preserves_other_connection_pending_request() -> None:
    async def run() -> None:
        request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=1,
        )
        close = CapturedConnectionClosed(
            connection_id="connection-1",
            observed_at=OBSERVED_AT,
        )
        other_request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=2,
            connection_id="connection-2",
        )
        other_response = _frame(
            _response_payload(),
            direction=Direction.INBOUND,
            frame_sequence=3,
            connection_id="connection-2",
        )
        late_response = _frame(
            _response_payload(),
            direction=Direction.INBOUND,
            frame_sequence=4,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture(
                [
                    request,
                    other_request,
                    close,
                    close,
                    other_response,
                    late_response,
                ]
            ),
            publisher=publisher,
        )
        await worker.process_once()
        await worker.process_once()

        with pytest.raises(IncompleteExchangeError, match="connection-1"):
            await worker.process_once()
        assert await worker.process_once() is None
        assert publisher.attempts == []

        correlated = await worker.process_once()
        assert isinstance(correlated, CorrelatedRequestResponse)
        assert correlated.request.connection_id == "connection-2"
        assert correlated.response.connection_id == "connection-2"
        assert correlated.request.frame_sequence == 2
        assert correlated.response.frame_sequence == 3

        with pytest.raises(UnmatchedResponseError):
            await worker.process_once()
        assert publisher.messages == [correlated]
        assert publisher.attempts == [correlated]
        await worker.stop()

    asyncio.run(run())


@pytest.mark.parametrize(
    ("payload", "error_type"),
    [
        pytest.param(b"malformed", SnifferDecodeError, id="decode"),
        pytest.param(
            _response_payload(), UnmatchedResponseError, id="correlation"
        ),
    ],
)
def test_worker_run_stops_before_publish_on_invalid_frame(
    payload: bytes,
    error_type: type[Exception],
) -> None:
    async def run() -> None:
        frame = _frame(
            payload,
            direction=Direction.INBOUND,
            frame_sequence=1,
        )
        later = _frame(
            _notice_payload(),
            direction=Direction.INBOUND,
            frame_sequence=2,
        )
        capture = FakeCapture([frame, later])
        publisher = FakePublisher()
        worker = SnifferWorker(capture=capture, publisher=publisher)

        with pytest.raises(error_type):
            await worker.run()
        assert publisher.attempts == []
        assert capture.events == [later]

    asyncio.run(run())


@pytest.mark.parametrize(
    "direction",
    [Direction.INBOUND, Direction.OUTBOUND],
)
def test_worker_ignores_tournament_heartbeat(direction: Direction) -> None:
    async def run() -> None:
        heartbeat = _frame(
            b"<= heartbeat - synthetic payload",
            direction=direction,
            frame_sequence=1,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture([heartbeat]),
            publisher=publisher,
        )

        assert await worker.process_once() is None
        assert publisher.messages == []

    asyncio.run(run())


@pytest.mark.parametrize(
    "payload",
    [
        b"<= heartbeat",
        b"<= HEARTBEAT -",
        b"< heartbeat -",
        b"synthetic <= heartbeat - payload",
        b"malformed",
    ],
)
def test_worker_does_not_treat_other_malformed_frames_as_heartbeat(
    payload: bytes,
) -> None:
    async def run() -> None:
        worker = SnifferWorker(
            capture=FakeCapture(
                [
                    _frame(
                        payload,
                        direction=Direction.INBOUND,
                        frame_sequence=1,
                    ),
                ],
            ),
            publisher=FakePublisher(),
        )

        with pytest.raises(SnifferDecodeError):
            await worker.process_once()

    asyncio.run(run())


@pytest.mark.parametrize("kind", ["notice", "exchange"])
def test_worker_run_stops_on_publisher_failure(kind: str) -> None:
    async def run() -> None:
        notice = _frame(
            _notice_payload(),
            direction=Direction.INBOUND,
            frame_sequence=1,
        )
        frames = (
            [notice]
            if kind == "notice"
            else [
                _frame(
                    _request_payload(),
                    direction=Direction.OUTBOUND,
                    frame_sequence=1,
                ),
                _frame(
                    _response_payload(),
                    direction=Direction.INBOUND,
                    frame_sequence=2,
                ),
            ]
        )
        later = _frame(
            _notice_payload(), direction=Direction.INBOUND, frame_sequence=3
        )
        capture = FakeCapture([*frames, later])
        error = PublisherFailureError("publish failed")
        publisher = FakePublisher(error=error)
        worker = SnifferWorker(capture=capture, publisher=publisher)

        with pytest.raises(PublisherFailureError) as caught:
            await worker.run()
        assert caught.value is error
        assert capture.events == [later]
        assert publisher.messages == []
        assert len(publisher.attempts) == 1
        expected_type = (
            CorrelatedNotice if kind == "notice" else CorrelatedRequestResponse
        )
        assert isinstance(publisher.attempts[0], expected_type)

    asyncio.run(run())


def test_worker_cancels_pending_publish_without_consuming_next_frame() -> None:
    async def run() -> None:
        entered = asyncio.Event()
        cancelled = asyncio.Event()
        release = asyncio.Event()

        class BlockingPublisher(FakePublisher):
            async def publish(self, message: CorrelatedMessage) -> object:
                self.attempts.append(message)
                entered.set()
                try:
                    await release.wait()
                except asyncio.CancelledError:
                    cancelled.set()
                    raise
                self.messages.append(message)
                return object()

        first = _frame(
            _notice_payload(), direction=Direction.INBOUND, frame_sequence=1
        )
        later = _frame(
            _notice_payload(), direction=Direction.INBOUND, frame_sequence=2
        )
        capture = FakeCapture([first, later])
        publisher = BlockingPublisher()
        worker = SnifferWorker(capture=capture, publisher=publisher)
        task = asyncio.create_task(worker.run())
        try:
            async with asyncio.timeout(1):
                await entered.wait()
            assert capture.events == [later]
            assert not task.done()
        finally:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

        assert cancelled.is_set()
        assert len(publisher.attempts) == 1
        assert publisher.messages == []
        assert capture.events == [later]
        await worker.stop()

    asyncio.run(run())


def test_worker_run_propagates_capture_failure() -> None:
    async def run() -> None:
        worker = SnifferWorker(
            capture=FakeCapture(error=CaptureFailureError("capture failed")),
            publisher=FakePublisher(),
        )

        with pytest.raises(CaptureFailureError, match="capture failed"):
            await worker.run()

    asyncio.run(run())


def test_stop_reports_pending_request_after_capture_cancellation() -> None:
    async def run() -> None:
        waiting = asyncio.Event()
        cancelled = asyncio.Event()
        release = asyncio.Event()

        class BlockingCapture(FakeCapture):
            async def receive(self) -> CaptureEvent:
                if self.events:
                    return await super().receive()
                waiting.set()
                try:
                    await release.wait()
                except asyncio.CancelledError:
                    cancelled.set()
                    raise
                return await super().receive()

        request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=1,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=BlockingCapture([request]), publisher=publisher
        )
        task = asyncio.create_task(worker.run())
        try:
            async with asyncio.timeout(1):
                await waiting.wait()
            assert not task.done()
        finally:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task

        assert cancelled.is_set()
        with pytest.raises(IncompleteExchangeError, match="1 pending"):
            await worker.stop()
        await worker.stop()
        assert publisher.attempts == []

    asyncio.run(run())


class CaptureFailureError(RuntimeError):
    pass


class PublisherFailureError(RuntimeError):
    pass
