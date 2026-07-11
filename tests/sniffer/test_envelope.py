import pytest

from majsoulrpa.assets.protocol.liqi_pb2 import Wrapper
from majsoulrpa.sniffer.envelope import (
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
    SnifferDecodeError,
    parse_liqi_envelope,
)


def _wrapper(*, name: str, data: bytes) -> bytes:
    return Wrapper(name=name, data=data).SerializeToString()


def test_parse_notice_envelope() -> None:
    body = b"synthetic-notice"
    payload = b"\x01" + _wrapper(name=".lq.SyntheticNotice", data=body)

    envelope = parse_liqi_envelope(payload)

    assert envelope == NoticeEnvelope(
        api_name=".lq.SyntheticNotice",
        body=body,
        raw_payload=payload,
    )


def test_parse_request_envelope_uses_two_byte_little_endian_number() -> None:
    body = b"synthetic-request"
    payload = b"\x02\x34\x12" + _wrapper(
        name=".lq.SyntheticService.call", data=body
    )

    envelope = parse_liqi_envelope(payload)

    assert envelope == RequestEnvelope(
        request_number=0x1234,
        api_name=".lq.SyntheticService.call",
        body=body,
        raw_payload=payload,
    )


def test_parse_response_envelope() -> None:
    body = b"synthetic-response"
    payload = b"\x03\x34\x12" + _wrapper(name="", data=body)

    envelope = parse_liqi_envelope(payload)

    assert envelope == ResponseEnvelope(
        request_number=0x1234,
        body=body,
        raw_payload=payload,
    )


def test_parse_response_envelope_accepts_explicit_empty_api_name() -> None:
    body = b"synthetic-response"
    wrapper = b"\x0a\x00" + Wrapper(data=body).SerializeToString()
    payload = b"\x03\x34\x12" + wrapper

    envelope = parse_liqi_envelope(payload)

    assert envelope == ResponseEnvelope(
        request_number=0x1234,
        body=body,
        raw_payload=payload,
    )


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (b"", "empty"),
        (b"\x04", "Unknown"),
        (b"\x02\x00", "Request header"),
        (b"\x03\x00", "Response header"),
        (b"\x01not-a-wrapper", "Notice wrapper"),
        (b"\x02\x00\x00not-a-wrapper", "Request wrapper"),
        (b"\x03\x00\x00not-a-wrapper", "Response wrapper"),
    ],
)
def test_parse_liqi_envelope_rejects_malformed_payload(
    payload: bytes,
    message: str,
) -> None:
    with pytest.raises(SnifferDecodeError, match=message):
        parse_liqi_envelope(payload)


@pytest.mark.parametrize("message_type", [b"\x01", b"\x02\x00\x00"])
def test_notice_and_request_require_api_name(message_type: bytes) -> None:
    payload = message_type + _wrapper(name="", data=b"synthetic")

    with pytest.raises(SnifferDecodeError, match="API name"):
        parse_liqi_envelope(payload)


def test_response_rejects_nonempty_api_name() -> None:
    payload = b"\x03\x00\x00" + _wrapper(
        name=".lq.Unexpected",
        data=b"synthetic",
    )

    with pytest.raises(SnifferDecodeError, match="must be empty"):
        parse_liqi_envelope(payload)
