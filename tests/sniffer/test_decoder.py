import base64
import datetime
import uuid

import pytest
from google.protobuf.message import DecodeError

from majsoulrpa.assets.protocol.liqi_pb2 import (
    AccountLevel,
    Error,
    NotifyAccountLevelChange,
    ReqHeatBeat,
    ResCommon,
    Wrapper,
)
from majsoulrpa.sniffer.correlator import Direction
from majsoulrpa.sniffer.decoder import (
    DecodedNotice,
    DecodedRequestResponse,
    LiqiBodyDecodeError,
    MissingResponseTypeError,
    PublicationEnvelopeMismatchError,
    SnifferMessageDecoder,
    UnknownAPIError,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
)

STREAM_ID = uuid.UUID("12345678-1234-5678-1234-567812345678")
OBSERVED_AT = datetime.datetime(2026, 1, 2, 3, 4, tzinfo=datetime.UTC)


def _encoded(payload: bytes) -> str:
    return base64.b64encode(payload).decode("ascii")


def _notice_publication(
    *,
    api_name: str = ".lq.NotifyAccountLevelChange",
    wrapper_name: str | None = None,
    body: bytes | None = None,
) -> NoticePublication:
    if body is None:
        body = NotifyAccountLevelChange(
            origin=AccountLevel(id=10101, score=1200),
            final=AccountLevel(id=10102, score=1300),
            type=2,
        ).SerializeToString()
    raw_payload = (
        b"\x01"
        + Wrapper(
            name=wrapper_name or api_name,
            data=body,
        ).SerializeToString()
    )
    return NoticePublication(
        schema_version=1,
        stream_id=STREAM_ID,
        publication_sequence=1,
        connection_id="connection-1",
        direction=Direction.INBOUND,
        frame_sequence=1,
        observed_at=OBSERVED_AT,
        api_name=api_name,
        payload_base64=_encoded(raw_payload),
    )


def _request_response_publication(
    *,
    api_name: str = ".lq.Lobby.heatbeat",
    wrapper_name: str | None = None,
    request_number: int = 0x1234,
    raw_response_number: int | None = None,
    request_body: bytes | None = None,
    response_body: bytes | None = None,
) -> RequestResponsePublication:
    if request_body is None:
        request_body = ReqHeatBeat(no_operation_counter=9).SerializeToString()
    if response_body is None:
        response_body = ResCommon(
            error=Error(code=7, message="synthetic-error"),
        ).SerializeToString()
    request_raw = (
        b"\x02"
        + request_number.to_bytes(2, byteorder="little")
        + Wrapper(
            name=wrapper_name or api_name,
            data=request_body,
        ).SerializeToString()
    )
    response_number = (
        request_number if raw_response_number is None else raw_response_number
    )
    response_raw = (
        b"\x03"
        + response_number.to_bytes(2, byteorder="little")
        + Wrapper(data=response_body).SerializeToString()
    )
    return RequestResponsePublication(
        schema_version=1,
        stream_id=STREAM_ID,
        publication_sequence=1,
        connection_id="connection-1",
        request_direction=Direction.OUTBOUND,
        request_number=request_number,
        request_frame_sequence=1,
        request_observed_at=OBSERVED_AT,
        response_frame_sequence=2,
        response_observed_at=OBSERVED_AT,
        api_name=api_name,
        request_payload_base64=_encoded(request_raw),
        response_payload_base64=_encoded(response_raw),
    )


def test_decoder_decodes_notice_with_descriptor_message_type() -> None:
    publication = _notice_publication()

    decoded = SnifferMessageDecoder().decode(publication)

    assert isinstance(decoded, DecodedNotice)
    assert decoded.raw.payload == base64.b64decode(publication.payload_base64)
    assert decoded.raw.name == publication.api_name
    assert decoded.message["type"] == 2
    assert decoded.message["origin"] == {"id": 10101, "score": 1200}
    assert decoded.message["final"] == {"id": 10102, "score": 1300}


def test_decoder_decodes_request_and_response_from_service_method() -> None:
    publication = _request_response_publication()

    decoded = SnifferMessageDecoder().decode(publication)

    assert isinstance(decoded, DecodedRequestResponse)
    assert decoded.raw.request == base64.b64decode(
        publication.request_payload_base64,
    )
    assert decoded.raw.response == base64.b64decode(
        publication.response_payload_base64,
    )
    assert decoded.request["no_operation_counter"] == 9
    error = decoded.response["error"]
    assert isinstance(error, dict)
    assert error["code"] == 7
    assert error["message"] == "synthetic-error"


@pytest.mark.parametrize(
    "publication",
    [
        _notice_publication(
            api_name=".lq.UnknownNotice",
            wrapper_name=".lq.UnknownNotice",
        ),
        _request_response_publication(
            api_name=".lq.UnknownService.call",
            wrapper_name=".lq.UnknownService.call",
        ),
    ],
)
def test_decoder_rejects_unknown_api(
    publication: NoticePublication | RequestResponsePublication,
) -> None:
    with pytest.raises(UnknownAPIError, match="Unknown API"):
        SnifferMessageDecoder().decode(publication)


@pytest.mark.parametrize(
    "publication",
    [
        pytest.param(_notice_publication(body=b"\x80"), id="notice"),
        pytest.param(
            _request_response_publication(request_body=b"\x80"), id="request"
        ),
        pytest.param(
            _request_response_publication(response_body=b"\x80"), id="response"
        ),
    ],
)
def test_decoder_rejects_malformed_known_message_body(
    publication: NoticePublication | RequestResponsePublication,
) -> None:
    with pytest.raises(LiqiBodyDecodeError, match="protobuf body") as caught:
        SnifferMessageDecoder().decode(publication)
    assert isinstance(caught.value.__cause__, DecodeError)


def test_decoder_accepts_empty_notice_body() -> None:
    decoded = SnifferMessageDecoder().decode(_notice_publication(body=b""))

    assert isinstance(decoded, DecodedNotice)
    assert decoded.message["type"] == 0
    assert "origin" not in decoded.message
    assert "final" not in decoded.message


def test_decoder_accepts_empty_request_and_response_bodies() -> None:
    decoded = SnifferMessageDecoder().decode(
        _request_response_publication(request_body=b"", response_body=b"")
    )

    assert isinstance(decoded, DecodedRequestResponse)
    assert decoded.request["no_operation_counter"] == 0
    assert "error" not in decoded.response


@pytest.mark.parametrize(
    "publication",
    [
        pytest.param(
            _notice_publication(wrapper_name=".lq.NotifyAccountLogout"),
            id="notice",
        ),
        pytest.param(
            _request_response_publication(wrapper_name=".lq.Lobby.login"),
            id="request",
        ),
    ],
)
def test_decoder_rejects_publication_and_wrapper_api_name_mismatch(
    publication: NoticePublication | RequestResponsePublication,
) -> None:
    with pytest.raises(PublicationEnvelopeMismatchError, match="API name"):
        SnifferMessageDecoder().decode(publication)


@pytest.mark.parametrize(
    ("publication", "field", "payload", "expected_kind"),
    [
        pytest.param(
            _notice_publication(),
            "payload_base64",
            _request_response_publication().request_payload_base64,
            "Notice",
            id="request-in-notice",
        ),
        pytest.param(
            _request_response_publication(),
            "request_payload_base64",
            _notice_publication().payload_base64,
            "Request",
            id="notice-in-request",
        ),
        pytest.param(
            _request_response_publication(),
            "response_payload_base64",
            _request_response_publication().request_payload_base64,
            "Response",
            id="request-in-response",
        ),
    ],
)
def test_decoder_rejects_wrong_envelope_kind(
    publication: NoticePublication | RequestResponsePublication,
    field: str,
    payload: str,
    expected_kind: str,
) -> None:
    data = publication.model_dump()
    data[field] = payload
    publication = type(publication).model_validate(data)

    with pytest.raises(
        PublicationEnvelopeMismatchError,
        match=f"does not contain a {expected_kind} envelope",
    ):
        SnifferMessageDecoder().decode(publication)


@pytest.mark.parametrize(
    ("publication_number", "request_number", "response_number"),
    [
        pytest.param(0x1234, 0x1234, 0, id="response-zero"),
        pytest.param(0x1234, 0, 0x1234, id="request-zero"),
        pytest.param(0, 0x1234, 0x1234, id="metadata-only"),
    ],
)
def test_decoder_rejects_request_and_response_number_mismatch(
    publication_number: int,
    request_number: int,
    response_number: int,
) -> None:
    publication = _request_response_publication(
        request_number=request_number, raw_response_number=response_number
    )
    data = publication.model_dump()
    data["request_number"] = publication_number
    publication = RequestResponsePublication.model_validate(data)

    with pytest.raises(
        PublicationEnvelopeMismatchError,
        match="request number",
    ):
        SnifferMessageDecoder().decode(publication)


def test_decoder_accepts_request_number_zero() -> None:
    publication = _request_response_publication(
        request_number=0, raw_response_number=0
    )

    decoded = SnifferMessageDecoder().decode(publication)

    assert isinstance(decoded, DecodedRequestResponse)
    assert decoded.request["no_operation_counter"] == 9
    error = decoded.response["error"]
    assert isinstance(error, dict)
    assert error["code"] == 7


def test_request_response_rejects_api_without_response_type() -> None:
    api_name = ".lq.NotifyAccountLogout"
    publication = _request_response_publication(
        api_name=api_name,
        wrapper_name=api_name,
        request_body=b"",
    )

    with pytest.raises(MissingResponseTypeError, match="response type"):
        SnifferMessageDecoder().decode(publication)
