from typing import Protocol

from majsoulrpa.sniffer.correlator import (
    CorrelatedMessage,
    ObservedEnvelope,
    RequestResponseCorrelator,
)
from majsoulrpa.sniffer.envelope import parse_liqi_envelope
from majsoulrpa.sniffer.playwright import (
    CapturedConnectionClosed,
    CapturedFrame,
    CaptureEvent,
)


class CaptureSource(Protocol):
    async def receive(self) -> CaptureEvent: ...


class CorrelatedMessagePublisher(Protocol):
    async def publish(self, message: CorrelatedMessage) -> object: ...


class SnifferWorker:
    def __init__(
        self,
        *,
        capture: CaptureSource,
        publisher: CorrelatedMessagePublisher,
        correlator: RequestResponseCorrelator | None = None,
    ) -> None:
        self._capture = capture
        self._publisher = publisher
        self._correlator = correlator or RequestResponseCorrelator()

    async def run(self) -> None:
        while True:
            await self.process_once()

    async def process_once(self) -> CorrelatedMessage | None:
        event = await self._capture.receive()
        match event:
            case CapturedFrame():
                observation = ObservedEnvelope(
                    connection_id=event.connection_id,
                    direction=event.direction,
                    frame_sequence=event.frame_sequence,
                    observed_at=event.observed_at,
                    envelope=parse_liqi_envelope(event.payload),
                )
                correlated = self._correlator.process(observation)
                if correlated is not None:
                    await self._publisher.publish(correlated)
                return correlated
            case CapturedConnectionClosed():
                self._correlator.connection_closed(event.connection_id)
                return None

    async def stop(self) -> None:
        self._correlator.stop()
