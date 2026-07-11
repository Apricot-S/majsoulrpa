import datetime
from dataclasses import dataclass
from enum import StrEnum

from majsoulrpa.sniffer.envelope import (
    LiqiEnvelope,
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
)


class Direction(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def opposite(self) -> "Direction":
        if self is Direction.INBOUND:
            return Direction.OUTBOUND
        return Direction.INBOUND


@dataclass(frozen=True, slots=True)
class ObservedEnvelope:
    connection_id: str
    direction: Direction
    frame_sequence: int
    observed_at: datetime.datetime
    envelope: LiqiEnvelope


@dataclass(frozen=True, slots=True)
class CorrelatedNotice:
    observation: ObservedEnvelope


@dataclass(frozen=True, slots=True)
class CorrelatedRequestResponse:
    request: ObservedEnvelope
    response: ObservedEnvelope


type CorrelatedMessage = CorrelatedNotice | CorrelatedRequestResponse


class SnifferCorrelationError(RuntimeError):
    """Base class for request/response correlation failures."""


class DuplicateRequestError(SnifferCorrelationError):
    """Raised when a request reuses a key that is still pending."""


class UnmatchedResponseError(SnifferCorrelationError):
    """Raised when a response has no corresponding request."""


class ResponseDirectionMismatchError(SnifferCorrelationError):
    """Raised when a response travels in the request direction."""


class IncompleteExchangeError(SnifferCorrelationError):
    """Raised when stopping leaves pending requests."""


type _PendingKey = tuple[str, Direction, int]


class RequestResponseCorrelator:
    def __init__(self) -> None:
        self._pending: dict[_PendingKey, ObservedEnvelope] = {}

    def process(
        self,
        observation: ObservedEnvelope,
    ) -> CorrelatedMessage | None:
        match observation.envelope:
            case NoticeEnvelope():
                return CorrelatedNotice(observation=observation)
            case RequestEnvelope():
                self._store_request(observation)
                return None
            case ResponseEnvelope():
                return self._pair_response(observation)

    def connection_closed(self, connection_id: str) -> None:
        keys = [key for key in self._pending if key[0] == connection_id]
        if not keys:
            return

        for key in keys:
            del self._pending[key]
        msg = (
            f"WebSocket connection {connection_id!r} closed with "
            f"{len(keys)} pending request(s)."
        )
        raise IncompleteExchangeError(msg)

    def stop(self) -> None:
        pending_count = len(self._pending)
        if pending_count == 0:
            return

        self._pending.clear()
        msg = f"Sniffer stopped with {pending_count} pending request(s)."
        raise IncompleteExchangeError(msg)

    def _store_request(self, observation: ObservedEnvelope) -> None:
        envelope = observation.envelope
        if not isinstance(envelope, RequestEnvelope):
            msg = "Only Request envelopes can be stored as pending."
            raise TypeError(msg)

        key = (
            observation.connection_id,
            observation.direction,
            envelope.request_number,
        )
        if key in self._pending:
            msg = (
                "A request with the same connection, direction, and number "
                "is already pending."
            )
            raise DuplicateRequestError(msg)
        self._pending[key] = observation

    def _pair_response(
        self,
        observation: ObservedEnvelope,
    ) -> CorrelatedRequestResponse:
        envelope = observation.envelope
        if not isinstance(envelope, ResponseEnvelope):
            msg = "Only Response envelopes can be paired."
            raise TypeError(msg)

        expected_key = (
            observation.connection_id,
            observation.direction.opposite(),
            envelope.request_number,
        )
        request = self._pending.pop(expected_key, None)
        if request is not None:
            return CorrelatedRequestResponse(
                request=request,
                response=observation,
            )

        same_direction_key = (
            observation.connection_id,
            observation.direction,
            envelope.request_number,
        )
        if same_direction_key in self._pending:
            msg = "Request and Response have the same direction."
            raise ResponseDirectionMismatchError(msg)

        msg = (
            "Response has no pending request with the same connection and "
            "number."
        )
        raise UnmatchedResponseError(msg)
