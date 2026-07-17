import datetime

import pytest

from majsoulrpa.sniffer.correlator import (
    CorrelatedNotice,
    CorrelatedRequestResponse,
    Direction,
    DuplicateRequestError,
    IncompleteExchangeError,
    ObservedEnvelope,
    RequestResponseCorrelator,
    ResponseDirectionMismatchError,
    UnmatchedResponseError,
)
from majsoulrpa.sniffer.envelope import (
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
)

OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


def _notice(
    *,
    connection_id: str = "connection-1",
    direction: Direction = Direction.INBOUND,
    frame_sequence: int = 1,
) -> ObservedEnvelope:
    payload = b"synthetic-notice"
    return ObservedEnvelope(
        connection_id=connection_id,
        direction=direction,
        frame_sequence=frame_sequence,
        observed_at=OBSERVED_AT,
        envelope=NoticeEnvelope(
            api_name=".lq.SyntheticNotice",
            body=b"notice-body",
            raw_payload=payload,
        ),
    )


def _request(
    *,
    connection_id: str = "connection-1",
    direction: Direction = Direction.OUTBOUND,
    request_number: int = 0x1234,
    api_name: str = ".lq.SyntheticService.call",
    frame_sequence: int = 1,
) -> ObservedEnvelope:
    payload = f"synthetic-request-{connection_id}-{direction}".encode()
    return ObservedEnvelope(
        connection_id=connection_id,
        direction=direction,
        frame_sequence=frame_sequence,
        observed_at=OBSERVED_AT,
        envelope=RequestEnvelope(
            request_number=request_number,
            api_name=api_name,
            body=b"request-body",
            raw_payload=payload,
        ),
    )


def _response(
    *,
    connection_id: str = "connection-1",
    direction: Direction = Direction.INBOUND,
    request_number: int = 0x1234,
    frame_sequence: int = 2,
) -> ObservedEnvelope:
    payload = f"synthetic-response-{connection_id}-{direction}".encode()
    return ObservedEnvelope(
        connection_id=connection_id,
        direction=direction,
        frame_sequence=frame_sequence,
        observed_at=OBSERVED_AT,
        envelope=ResponseEnvelope(
            request_number=request_number,
            body=b"response-body",
            raw_payload=payload,
        ),
    )


def test_notice_is_emitted_immediately() -> None:
    correlator = RequestResponseCorrelator()
    notice = _notice()

    correlated = correlator.process(notice)

    assert correlated == CorrelatedNotice(observation=notice)


def test_request_is_held_until_opposite_direction_response_arrives() -> None:
    correlator = RequestResponseCorrelator()
    request = _request()
    response = _response()

    assert correlator.process(request) is None

    correlated = correlator.process(response)

    assert correlated == CorrelatedRequestResponse(
        request=request,
        response=response,
    )
    correlator.stop()


def test_same_request_number_on_different_connections_is_independent() -> None:
    correlator = RequestResponseCorrelator()
    request_1 = _request(connection_id="connection-1", api_name=".lq.One")
    request_2 = _request(connection_id="connection-2", api_name=".lq.Two")
    response_1 = _response(connection_id="connection-1")
    response_2 = _response(connection_id="connection-2")

    correlator.process(request_1)
    correlator.process(request_2)

    assert correlator.process(response_2) == CorrelatedRequestResponse(
        request=request_2,
        response=response_2,
    )
    assert correlator.process(response_1) == CorrelatedRequestResponse(
        request=request_1,
        response=response_1,
    )


def test_same_request_number_in_both_directions_is_independent() -> None:
    correlator = RequestResponseCorrelator()
    outbound_request = _request(direction=Direction.OUTBOUND)
    inbound_request = _request(direction=Direction.INBOUND)
    inbound_response = _response(direction=Direction.INBOUND)
    outbound_response = _response(direction=Direction.OUTBOUND)

    correlator.process(outbound_request)
    correlator.process(inbound_request)

    assert correlator.process(inbound_response) == CorrelatedRequestResponse(
        request=outbound_request,
        response=inbound_response,
    )
    assert correlator.process(outbound_response) == CorrelatedRequestResponse(
        request=inbound_request,
        response=outbound_response,
    )


def test_duplicate_request_does_not_replace_original() -> None:
    correlator = RequestResponseCorrelator()
    original = _request(api_name=".lq.Original")
    duplicate = _request(api_name=".lq.Duplicate", frame_sequence=2)
    response = _response(frame_sequence=3)
    correlator.process(original)

    with pytest.raises(DuplicateRequestError, match="already pending"):
        correlator.process(duplicate)

    assert correlator.process(response) == CorrelatedRequestResponse(
        request=original,
        response=response,
    )


def test_response_without_request_is_rejected() -> None:
    correlator = RequestResponseCorrelator()

    with pytest.raises(UnmatchedResponseError, match="no pending request"):
        correlator.process(_response())


def test_response_in_same_direction_as_request_is_rejected() -> None:
    correlator = RequestResponseCorrelator()
    correlator.process(_request(direction=Direction.INBOUND))

    with pytest.raises(ResponseDirectionMismatchError, match="same direction"):
        correlator.process(_response(direction=Direction.INBOUND))


def test_connection_close_rejects_and_removes_incomplete_exchange() -> None:
    correlator = RequestResponseCorrelator()
    correlator.process(_request(connection_id="connection-1"))
    correlator.process(_request(connection_id="connection-2"))

    with pytest.raises(IncompleteExchangeError, match="connection-1"):
        correlator.connection_closed("connection-1")

    correlator.connection_closed("connection-1")
    with pytest.raises(IncompleteExchangeError, match="connection-2"):
        correlator.connection_closed("connection-2")
    correlator.stop()


def test_stop_rejects_and_removes_all_incomplete_exchanges() -> None:
    correlator = RequestResponseCorrelator()
    correlator.process(_request(connection_id="connection-1"))
    correlator.process(_request(connection_id="connection-2"))

    with pytest.raises(IncompleteExchangeError, match="2 pending"):
        correlator.stop()

    correlator.stop()
