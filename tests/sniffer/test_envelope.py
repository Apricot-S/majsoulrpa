import pytest
from google.protobuf.message import DecodeError

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


@pytest.mark.parametrize("number", [0, 65535], ids=["zero", "uint16-max"])
@pytest.mark.parametrize(
    "kind", [b"\x02", b"\x03"], ids=["request", "response"]
)
def test_request_number_accepts_unsigned_16_bit_boundaries(
    kind: bytes,
    number: int,
) -> None:
    name = ".lq.SyntheticService.call" if kind == b"\x02" else ""
    payload = (
        kind
        + number.to_bytes(2, "little")
        + _wrapper(
            name=name,
            data=b"synthetic",
        )
    )

    envelope = parse_liqi_envelope(payload)

    assert isinstance(envelope, (RequestEnvelope, ResponseEnvelope))
    assert envelope.request_number == number
    assert envelope.body == b"synthetic"
    assert envelope.raw_payload == payload


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


@pytest.mark.parametrize(
    ("kind", "label"),
    [(b"\x02", "Request"), (b"\x03", "Response")],
    ids=["request", "response"],
)
@pytest.mark.parametrize(
    "number_bytes", [b"", b"\x00"], ids=["missing", "one-byte"]
)
def test_request_number_requires_two_bytes(
    kind: bytes, label: str, number_bytes: bytes
) -> None:
    with pytest.raises(SnifferDecodeError, match=f"{label} header"):
        parse_liqi_envelope(kind + number_bytes)


@pytest.mark.parametrize(
    "message_type",
    [b"\x01", b"\x02\x00\x00"],
    ids=["notice", "request"],
)
@pytest.mark.parametrize(
    "wrapper",
    [
        pytest.param(_wrapper(name="", data=b"synthetic"), id="omitted-name"),
        pytest.param(
            b"\x0a\x00" + _wrapper(name="", data=b"synthetic"),
            id="explicit-empty-name",
        ),
        pytest.param(b"", id="empty-wrapper"),
    ],
)
def test_notice_and_request_require_api_name(
    message_type: bytes, wrapper: bytes
) -> None:
    payload = message_type + wrapper

    with pytest.raises(SnifferDecodeError, match="API name"):
        parse_liqi_envelope(payload)


@pytest.mark.parametrize(
    "header",
    [b"\x01", b"\x02\x00\x00", b"\x03\x00\x00"],
    ids=["notice", "request", "response"],
)
@pytest.mark.parametrize(
    "wrapper",
    [
        pytest.param(b"\x0a\x01\xff", id="invalid-utf8-name"),
        pytest.param(b"\x12\x02\x00", id="truncated-body"),
    ],
)
def test_invalid_wrapper_bytes_preserve_decode_error_cause(
    header: bytes,
    wrapper: bytes,
) -> None:
    with pytest.raises(
        SnifferDecodeError, match="wrapper is malformed"
    ) as caught:
        parse_liqi_envelope(header + wrapper)
    assert isinstance(caught.value.__cause__, DecodeError)


@pytest.mark.parametrize(
    ("header", "name"),
    [
        pytest.param(b"\x01", ".lq.SyntheticNotice", id="notice"),
        pytest.param(
            b"\x02\x00\x00", ".lq.SyntheticService.call", id="request"
        ),
        pytest.param(b"\x03\x00\x00", "", id="empty-response-wrapper"),
    ],
)
def test_empty_protobuf_body_is_valid(header: bytes, name: str) -> None:
    payload = header + _wrapper(name=name, data=b"")

    envelope = parse_liqi_envelope(payload)

    assert envelope.body == b""
    assert envelope.raw_payload == payload


def test_response_rejects_nonempty_api_name() -> None:
    payload = b"\x03\x00\x00" + _wrapper(
        name=".lq.Unexpected",
        data=b"synthetic",
    )

    with pytest.raises(SnifferDecodeError, match="must be empty") as caught:
        parse_liqi_envelope(payload)
    assert str(caught.value) == "Response wrapper API name must be empty."
