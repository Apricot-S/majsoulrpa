import base64
import datetime
import uuid

import pytest

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
    response_number = raw_response_number or request_number
    response_raw = (
        b"\x03"
        + response_number.to_bytes(2, byteorder="little")
        + Wrapper(data=response_body).SerializeToString()
    )
    return RequestResponsePublication(
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


def test_decoder_rejects_malformed_known_message_body() -> None:
    publication = _notice_publication(body=b"\x80")

    with pytest.raises(LiqiBodyDecodeError, match="protobuf body"):
        SnifferMessageDecoder().decode(publication)


def test_decoder_rejects_publication_and_wrapper_api_name_mismatch() -> None:
    publication = _notice_publication(wrapper_name=".lq.NotifyAccountLogout")

    with pytest.raises(PublicationEnvelopeMismatchError, match="API name"):
        SnifferMessageDecoder().decode(publication)


def test_decoder_rejects_request_and_response_number_mismatch() -> None:
    publication = _request_response_publication(raw_response_number=0x4321)

    with pytest.raises(
        PublicationEnvelopeMismatchError,
        match="request number",
    ):
        SnifferMessageDecoder().decode(publication)


def test_request_response_rejects_api_without_response_type() -> None:
    api_name = ".lq.NotifyAccountLogout"
    publication = _request_response_publication(
        api_name=api_name,
        wrapper_name=api_name,
        request_body=b"",
    )

    with pytest.raises(MissingResponseTypeError, match="response type"):
        SnifferMessageDecoder().decode(publication)
