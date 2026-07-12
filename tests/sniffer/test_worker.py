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
        self.error = error

    async def publish(self, message: CorrelatedMessage) -> object:
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


def test_worker_holds_request_until_response_then_publishes_pair() -> None:
    async def run() -> None:
        request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=1,
        )
        response = _frame(
            _response_payload(),
            direction=Direction.INBOUND,
            frame_sequence=2,
        )
        publisher = FakePublisher()
        worker = SnifferWorker(
            capture=FakeCapture([request, response]),
            publisher=publisher,
        )

        assert await worker.process_once() is None
        assert publisher.messages == []
        correlated = await worker.process_once()

        assert isinstance(correlated, CorrelatedRequestResponse)
        assert correlated.request.frame_sequence == 1
        assert correlated.response.frame_sequence == 2
        assert publisher.messages == [correlated]

    asyncio.run(run())


def test_worker_passes_connection_close_to_correlator() -> None:
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
        worker = SnifferWorker(
            capture=FakeCapture([request, close]),
            publisher=FakePublisher(),
        )
        await worker.process_once()

        with pytest.raises(IncompleteExchangeError, match="connection-1"):
            await worker.process_once()

    asyncio.run(run())


def test_worker_propagates_decode_failure() -> None:
    async def run() -> None:
        frame = _frame(
            b"malformed",
            direction=Direction.INBOUND,
            frame_sequence=1,
        )
        worker = SnifferWorker(
            capture=FakeCapture([frame]),
            publisher=FakePublisher(),
        )

        with pytest.raises(SnifferDecodeError):
            await worker.process_once()

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


def test_worker_propagates_publisher_failure() -> None:
    async def run() -> None:
        frame = _frame(
            _notice_payload(),
            direction=Direction.INBOUND,
            frame_sequence=1,
        )
        worker = SnifferWorker(
            capture=FakeCapture([frame]),
            publisher=FakePublisher(
                error=PublisherFailureError("publish failed"),
            ),
        )

        with pytest.raises(PublisherFailureError, match="publish failed"):
            await worker.process_once()

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


def test_worker_stop_rejects_pending_request_then_becomes_idempotent() -> None:
    async def run() -> None:
        request = _frame(
            _request_payload(),
            direction=Direction.OUTBOUND,
            frame_sequence=1,
        )
        worker = SnifferWorker(
            capture=FakeCapture([request]),
            publisher=FakePublisher(),
        )
        await worker.process_once()

        with pytest.raises(IncompleteExchangeError, match="1 pending"):
            await worker.stop()
        await worker.stop()

    asyncio.run(run())


class CaptureFailureError(RuntimeError):
    pass


class PublisherFailureError(RuntimeError):
    pass
