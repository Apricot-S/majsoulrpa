import base64
import datetime
import importlib
import sys
import uuid

from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.event_adapter import raw_event_from_publication
from majsoulrpa.sniffer.events import RawNotice, RawRequestResponse
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
