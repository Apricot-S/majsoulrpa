import base64
import dataclasses
import datetime
import json
import uuid

import pytest
from pydantic import ValidationError

from majsoulrpa.sniffer.correlator import (
    CorrelatedNotice,
    CorrelatedRequestResponse,
    Direction,
    ObservedEnvelope,
)
from majsoulrpa.sniffer.envelope import (
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
    dump_publication_json,
    make_publication,
    parse_publication_json,
)

STREAM_ID = uuid.UUID("12345678-1234-5678-1234-567812345678")
REQUEST_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)
RESPONSE_AT = datetime.datetime(2026, 1, 2, 3, 5, tzinfo=datetime.UTC)


def _encoded(payload: bytes) -> str:
    return base64.b64encode(payload).decode("ascii")


def _notice() -> CorrelatedNotice:
    raw_payload = b"synthetic-notice"
    return CorrelatedNotice(
        observation=ObservedEnvelope(
            connection_id="connection-1",
            direction=Direction.INBOUND,
            frame_sequence=10,
            observed_at=REQUEST_AT,
            envelope=NoticeEnvelope(
                api_name=".lq.SyntheticNotice",
                body=b"notice-body",
                raw_payload=raw_payload,
            ),
        ),
    )


def _request_response() -> CorrelatedRequestResponse:
    request_raw = b"synthetic-request"
    response_raw = b"synthetic-response"
    return CorrelatedRequestResponse(
        request=ObservedEnvelope(
            connection_id="connection-1",
            direction=Direction.OUTBOUND,
            frame_sequence=20,
            observed_at=REQUEST_AT,
            envelope=RequestEnvelope(
                request_number=0x1234,
                api_name=".lq.SyntheticService.call",
                body=b"request-body",
                raw_payload=request_raw,
            ),
        ),
        response=ObservedEnvelope(
            connection_id="connection-1",
            direction=Direction.INBOUND,
            frame_sequence=21,
            observed_at=RESPONSE_AT,
            envelope=ResponseEnvelope(
                request_number=0x1234,
                body=b"response-body",
                raw_payload=response_raw,
            ),
        ),
    )


def test_make_notice_publication() -> None:
    publication = make_publication(
        _notice(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )

    assert publication == NoticePublication(
        schema_version=1,
        stream_id=STREAM_ID,
        publication_sequence=1,
        connection_id="connection-1",
        kind="notice",
        direction=Direction.INBOUND,
        frame_sequence=10,
        observed_at=REQUEST_AT,
        api_name=".lq.SyntheticNotice",
        payload_base64=_encoded(b"synthetic-notice"),
    )


def test_make_request_response_publication() -> None:
    publication = make_publication(
        _request_response(),
        stream_id=STREAM_ID,
        publication_sequence=2,
    )

    assert publication == RequestResponsePublication(
        schema_version=1,
        stream_id=STREAM_ID,
        publication_sequence=2,
        connection_id="connection-1",
        kind="request_response",
        request_direction=Direction.OUTBOUND,
        request_number=0x1234,
        request_frame_sequence=20,
        request_observed_at=REQUEST_AT,
        response_frame_sequence=21,
        response_observed_at=RESPONSE_AT,
        api_name=".lq.SyntheticService.call",
        request_payload_base64=_encoded(b"synthetic-request"),
        response_payload_base64=_encoded(b"synthetic-response"),
    )


@pytest.mark.parametrize(
    ("response", "message"),
    [
        (
            dataclasses.replace(
                _request_response().response,
                connection_id="connection-2",
            ),
            "different connections",
        ),
        (
            dataclasses.replace(
                _request_response().response,
                envelope=ResponseEnvelope(
                    request_number=0x4321,
                    body=b"response-body",
                    raw_payload=b"synthetic-response",
                ),
            ),
            "different request numbers",
        ),
        (
            dataclasses.replace(
                _request_response().response,
                direction=Direction.OUTBOUND,
            ),
            "opposite directions",
        ),
    ],
)
def test_make_request_response_revalidates_correlation(
    response: ObservedEnvelope,
    message: str,
) -> None:
    correlated = dataclasses.replace(
        _request_response(),
        response=response,
    )

    with pytest.raises(ValueError, match=message):
        make_publication(
            correlated,
            stream_id=STREAM_ID,
            publication_sequence=1,
        )


@pytest.mark.parametrize("message", [_notice(), _request_response()])
def test_publication_json_round_trip(
    message: CorrelatedNotice | CorrelatedRequestResponse,
) -> None:
    publication = make_publication(
        message,
        stream_id=STREAM_ID,
        publication_sequence=3,
    )

    encoded = dump_publication_json(publication)

    assert parse_publication_json(encoded) == publication


def test_parse_publication_rejects_unknown_field() -> None:
    publication = make_publication(
        _notice(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["unexpected"] = True

    with pytest.raises(ValidationError, match="extra_forbidden"):
        parse_publication_json(json.dumps(data))


def test_parse_publication_rejects_unsupported_schema_version() -> None:
    publication = make_publication(
        _notice(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["schema_version"] = 2

    with pytest.raises(ValidationError, match="literal_error"):
        parse_publication_json(json.dumps(data))


def test_parse_publication_rejects_invalid_base64() -> None:
    publication = make_publication(
        _notice(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["payload_base64"] = "not base64!"

    with pytest.raises(ValidationError, match="valid base64"):
        parse_publication_json(json.dumps(data))
