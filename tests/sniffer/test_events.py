import base64
import dataclasses
import datetime
import importlib
import sys
import uuid

import pytest

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.event_adapter import raw_event_from_publication
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    RawNotice,
    RawRequestResponse,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
)

STREAM_ID = uuid.UUID("12345678-1234-5678-1234-567812345678")
REQUEST_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)
RESPONSE_AT = datetime.datetime(2026, 1, 2, 3, 5, tzinfo=datetime.UTC)


def _encoded(payload: bytes) -> str:
    return base64.b64encode(payload).decode("ascii")


def test_notice_publication_becomes_public_raw_bytes_event() -> None:
    payload = b"synthetic-notice-payload"
    publication = NoticePublication(
        stream_id=STREAM_ID,
        publication_sequence=1,
        connection_id="connection-1",
        direction=Direction.INBOUND,
        frame_sequence=10,
        observed_at=REQUEST_AT,
        api_name=".lq.SyntheticNotice",
        payload_base64=_encoded(payload),
    )

    event = raw_event_from_publication(publication)

    assert event == RawNotice(
        direction=Direction.INBOUND,
        name=".lq.SyntheticNotice",
        payload=payload,
        observed_at=REQUEST_AT,
    )


def test_request_response_publication_becomes_public_raw_bytes_event() -> None:
    request = b"synthetic-request-payload"
    response = b"synthetic-response-payload"
    publication = RequestResponsePublication(
        stream_id=STREAM_ID,
        publication_sequence=1,
        connection_id="connection-1",
        request_direction=Direction.OUTBOUND,
        request_number=0x1234,
        request_frame_sequence=10,
        request_observed_at=REQUEST_AT,
        response_frame_sequence=11,
        response_observed_at=RESPONSE_AT,
        api_name=".lq.SyntheticService.call",
        request_payload_base64=_encoded(request),
        response_payload_base64=_encoded(response),
    )

    event = raw_event_from_publication(publication)

    assert event == RawRequestResponse(
        request_direction=Direction.OUTBOUND,
        name=".lq.SyntheticService.call",
        request=request,
        response=response,
        request_observed_at=REQUEST_AT,
        response_observed_at=RESPONSE_AT,
    )


def test_raw_and_decoded_events_are_immutable_value_objects() -> None:
    raw_notice = RawNotice(
        direction=Direction.INBOUND,
        name=".lq.SyntheticNotice",
        payload=b"synthetic-notice-payload",
        observed_at=REQUEST_AT,
    )
    raw_request_response = RawRequestResponse(
        request_direction=Direction.OUTBOUND,
        name=".lq.SyntheticService.call",
        request=b"synthetic-request-payload",
        response=b"synthetic-response-payload",
        request_observed_at=REQUEST_AT,
        response_observed_at=RESPONSE_AT,
    )
    decoded_notice = DecodedNotice(
        raw=raw_notice,
        message={"count": 1, "enabled": True},
    )
    decoded_request_response = DecodedRequestResponse(
        raw=raw_request_response,
        request={"account_id": 100001},
        response={"error": {"code": 0}},
    )

    _assert_is_frozen(raw_notice, "payload", b"replacement")
    _assert_is_frozen(raw_request_response, "response", b"replacement")
    _assert_is_frozen(decoded_notice, "message", {})
    _assert_is_frozen(decoded_request_response, "request", {})

    assert raw_notice.direction is Direction.INBOUND
    assert raw_notice.observed_at == REQUEST_AT
    assert raw_notice.payload == b"synthetic-notice-payload"
    assert decoded_notice.message == {"count": 1, "enabled": True}
    assert decoded_request_response.response == {"error": {"code": 0}}


def _assert_is_frozen(
    event: object,
    attribute: str,
    replacement: object,
) -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(event, attribute, replacement)


def test_sniffer_package_exports_only_user_event_types() -> None:
    sys.modules.pop("majsoulrpa.sniffer", None)
    sniffer = importlib.import_module("majsoulrpa.sniffer")

    assert sniffer.__all__ == [
        "DecodedNotice",
        "DecodedRequestResponse",
        "DecodedSnifferMessage",
        "Direction",
        "RawNotice",
        "RawRequestResponse",
        "RawSnifferMessage",
    ]
    assert not hasattr(sniffer, "ZmqSnifferPublisher")
    assert not hasattr(sniffer, "parse_liqi_envelope")
