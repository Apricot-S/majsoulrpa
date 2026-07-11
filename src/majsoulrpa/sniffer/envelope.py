from dataclasses import dataclass
from enum import IntEnum

from google.protobuf.message import DecodeError

from majsoulrpa.assets.protocol.liqi_pb2 import Wrapper


class SnifferDecodeError(ValueError):
    """Raised when a WebSocket payload is not a valid liqi envelope."""


class _MessageKind(IntEnum):
    NOTICE = 0x01
    REQUEST = 0x02
    RESPONSE = 0x03


@dataclass(frozen=True, slots=True)
class NoticeEnvelope:
    api_name: str
    body: bytes
    raw_payload: bytes


@dataclass(frozen=True, slots=True)
class RequestEnvelope:
    request_number: int
    api_name: str
    body: bytes
    raw_payload: bytes


@dataclass(frozen=True, slots=True)
class ResponseEnvelope:
    request_number: int
    body: bytes
    raw_payload: bytes


type LiqiEnvelope = NoticeEnvelope | RequestEnvelope | ResponseEnvelope


def parse_liqi_envelope(payload: bytes) -> LiqiEnvelope:
    if not payload:
        msg = "Cannot decode an empty WebSocket payload."
        raise SnifferDecodeError(msg)

    try:
        kind = _MessageKind(payload[0])
    except ValueError as error:
        msg = f"Unknown liqi message kind: {payload[0]:#04x}."
        raise SnifferDecodeError(msg) from error

    match kind:
        case _MessageKind.NOTICE:
            return _parse_notice(payload)
        case _MessageKind.REQUEST:
            return _parse_request(payload)
        case _MessageKind.RESPONSE:
            return _parse_response(payload)


def _parse_notice(payload: bytes) -> NoticeEnvelope:
    wrapper = _parse_wrapper(payload[1:], label="Notice")
    _require_api_name(wrapper.name, label="Notice")
    return NoticeEnvelope(
        api_name=wrapper.name,
        body=wrapper.data,
        raw_payload=payload,
    )


def _parse_request(payload: bytes) -> RequestEnvelope:
    _require_request_number(payload, label="Request")
    wrapper = _parse_wrapper(payload[3:], label="Request")
    _require_api_name(wrapper.name, label="Request")
    return RequestEnvelope(
        request_number=int.from_bytes(payload[1:3], byteorder="little"),
        api_name=wrapper.name,
        body=wrapper.data,
        raw_payload=payload,
    )


def _parse_response(payload: bytes) -> ResponseEnvelope:
    _require_request_number(payload, label="Response")
    wrapper = _parse_wrapper(payload[3:], label="Response")
    if wrapper.name:
        msg = "Response wrapper API name must be empty."
        raise SnifferDecodeError(msg)
    return ResponseEnvelope(
        request_number=int.from_bytes(payload[1:3], byteorder="little"),
        body=wrapper.data,
        raw_payload=payload,
    )


def _require_request_number(payload: bytes, *, label: str) -> None:
    if len(payload) < 3:  # noqa: PLR2004
        msg = f"{label} header does not contain a 2-byte request number."
        raise SnifferDecodeError(msg)


def _parse_wrapper(payload: bytes, *, label: str) -> Wrapper:
    wrapper = Wrapper()
    try:
        wrapper.ParseFromString(payload)
    except DecodeError as error:
        msg = f"{label} wrapper is malformed."
        raise SnifferDecodeError(msg) from error
    return wrapper


def _require_api_name(api_name: str, *, label: str) -> None:
    if not api_name:
        msg = f"{label} wrapper does not contain an API name."
        raise SnifferDecodeError(msg)
