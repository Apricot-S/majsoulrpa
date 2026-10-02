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


def _notice(raw_payload: bytes = b"synthetic-notice") -> CorrelatedNotice:
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


def _request_response(
    *,
    request_raw: bytes = b"synthetic-request",
    response_raw: bytes = b"synthetic-response",
) -> CorrelatedRequestResponse:
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


@pytest.mark.parametrize(
    ("message", "field"),
    [
        pytest.param(
            _notice(), "publication_sequence", id="notice-publication-sequence"
        ),
        pytest.param(_notice(), "frame_sequence", id="notice-frame-sequence"),
        pytest.param(
            _request_response(),
            "publication_sequence",
            id="exchange-publication-sequence",
        ),
        pytest.param(
            _request_response(), "request_number", id="request-number"
        ),
        pytest.param(
            _request_response(),
            "request_frame_sequence",
            id="request-frame-sequence",
        ),
        pytest.param(
            _request_response(),
            "response_frame_sequence",
            id="response-frame-sequence",
        ),
    ],
)
@pytest.mark.parametrize(
    "value", ["1", True, 1.0], ids=["string", "boolean", "float"]
)
def test_wire_integer_fields_reject_coercion(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    field: str,
    *,
    value: str | bool | float,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    data[field] = value

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(
        error["loc"][-1] == field and error["type"] == "int_type"
        for error in caught.value.errors()
    )


@pytest.mark.parametrize(
    ("message", "field"),
    [
        pytest.param(
            _notice(), "publication_sequence", id="notice-publication"
        ),
        pytest.param(_notice(), "frame_sequence", id="notice-frame"),
        pytest.param(
            _request_response(),
            "publication_sequence",
            id="exchange-publication",
        ),
        pytest.param(
            _request_response(), "request_frame_sequence", id="request-frame"
        ),
        pytest.param(
            _request_response(), "response_frame_sequence", id="response-frame"
        ),
    ],
)
def test_wire_sequence_rejects_zero(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    field: str,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    data[field] = 0

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(
        error["loc"][-1] == field and error["type"] == "greater_than_equal"
        for error in caught.value.errors()
    )


@pytest.mark.parametrize(
    "message", [_notice(), _request_response()], ids=["notice", "exchange"]
)
def test_wire_publication_accepts_minimum_sequences(
    message: CorrelatedNotice | CorrelatedRequestResponse,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    if isinstance(publication, NoticePublication):
        data["frame_sequence"] = 1
    else:
        data["request_frame_sequence"] = 1
        data["response_frame_sequence"] = 2

    parsed = parse_publication_json(json.dumps(data))
    assert parsed.model_dump(mode="json") == data


@pytest.mark.parametrize("number", [0, 0xFFFF], ids=["minimum", "maximum"])
def test_wire_request_number_accepts_boundaries(number: int) -> None:
    publication = make_publication(
        _request_response(), stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    data["request_number"] = number

    parsed = parse_publication_json(json.dumps(data))
    assert isinstance(parsed, RequestResponsePublication)
    assert parsed.request_number == number


@pytest.mark.parametrize(
    ("number", "error_type"),
    [(-1, "greater_than_equal"), (0x10000, "less_than_equal")],
    ids=["below-minimum", "above-maximum"],
)
def test_wire_request_number_rejects_out_of_range(
    number: int, error_type: str
) -> None:
    publication = make_publication(
        _request_response(), stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    data["request_number"] = number

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(
        error["loc"][-1] == "request_number" and error["type"] == error_type
        for error in caught.value.errors()
    )


@pytest.mark.parametrize(
    "response_sequence", [20, 19], ids=["same", "earlier"]
)
def test_wire_exchange_rejects_invalid_frame_order(
    response_sequence: int,
) -> None:
    publication = make_publication(
        _request_response(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["response_frame_sequence"] = response_sequence

    with pytest.raises(
        ValidationError, match="Response frame sequence must follow Request"
    ):
        parse_publication_json(json.dumps(data))


@pytest.mark.parametrize(
    "response_sequence", [20, 19], ids=["same", "earlier"]
)
def test_make_exchange_rejects_invalid_frame_order(
    response_sequence: int,
) -> None:
    message = _request_response()
    message = dataclasses.replace(
        message,
        response=dataclasses.replace(
            message.response, frame_sequence=response_sequence
        ),
    )
    with pytest.raises(
        ValidationError, match="Response frame sequence must follow Request"
    ):
        make_publication(message, stream_id=STREAM_ID, publication_sequence=1)


def test_exchange_accepts_frame_gap_and_clock_rollback() -> None:
    message = _request_response()
    message = dataclasses.replace(
        message,
        response=dataclasses.replace(
            message.response,
            frame_sequence=25,
            observed_at=REQUEST_AT - datetime.timedelta(seconds=1),
        ),
    )
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    assert isinstance(publication, RequestResponsePublication)
    assert publication.response_frame_sequence == 25
    assert publication.response_observed_at == message.response.observed_at
    assert (
        parse_publication_json(dump_publication_json(publication))
        == publication
    )


@pytest.mark.parametrize(
    "message",
    [_notice(), _request_response()],
    ids=["notice", "exchange"],
)
def test_wire_publication_requires_schema_version(
    message: CorrelatedNotice | CorrelatedRequestResponse,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    del data["schema_version"]

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(
        error["loc"][-1] == "schema_version" and error["type"] == "missing"
        for error in caught.value.errors()
    )


@pytest.mark.parametrize(
    "message", [_notice(), _request_response()], ids=["notice", "exchange"]
)
def test_parse_publication_rejects_unknown_field(
    message: CorrelatedNotice | CorrelatedRequestResponse,
) -> None:
    publication = make_publication(
        message,
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["unexpected"] = True

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(
        error["loc"][-1] == "unexpected" and error["type"] == "extra_forbidden"
        for error in caught.value.errors()
    )


@pytest.mark.parametrize(
    "message", [_notice(), _request_response()], ids=["notice", "exchange"]
)
@pytest.mark.parametrize(
    ("kind", "error_type"),
    [
        pytest.param(None, "union_tag_not_found", id="missing"),
        pytest.param("unknown", "union_tag_invalid", id="unknown"),
    ],
)
def test_wire_publication_requires_known_kind(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    kind: str | None,
    error_type: str,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    if kind is None:
        del data["kind"]
    else:
        data["kind"] = kind

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert [error["type"] for error in caught.value.errors()] == [error_type]


def test_frame_order_error_hides_publication_input() -> None:
    publication = make_publication(
        _request_response(),
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["response_frame_sequence"] = data["request_frame_sequence"]

    with pytest.raises(
        ValidationError, match="Response frame sequence"
    ) as caught:
        parse_publication_json(json.dumps(data))
    assert "input_value=" not in str(caught.value)
    assert data["request_payload_base64"] not in str(caught.value)
    assert data["response_payload_base64"] not in str(caught.value)


@pytest.mark.parametrize(
    "message", [_notice(), _request_response()], ids=["notice", "exchange"]
)
@pytest.mark.parametrize(
    "version",
    [True, 1.0, "1", 2],
    ids=["boolean", "float", "string", "unsupported"],
)
def test_parse_publication_rejects_invalid_schema_version(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    *,
    version: bool | float | str,
) -> None:
    publication = make_publication(
        message,
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    data["schema_version"] = version

    with pytest.raises(ValidationError, match="schema_version"):
        parse_publication_json(json.dumps(data))


@pytest.mark.parametrize(
    ("message", "field"),
    [
        pytest.param(_notice(), "payload_base64", id="notice"),
        pytest.param(
            _request_response(), "request_payload_base64", id="request"
        ),
        pytest.param(
            _request_response(), "response_payload_base64", id="response"
        ),
    ],
)
def test_invalid_base64_error_hides_input(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    field: str,
) -> None:
    publication = make_publication(
        message,
        stream_id=STREAM_ID,
        publication_sequence=1,
    )
    data = json.loads(dump_publication_json(publication))
    marker = "synthetic-payload-not-for-error-output!"
    data[field] = marker

    with pytest.raises(ValidationError, match="valid base64") as caught:
        parse_publication_json(json.dumps(data))
    assert marker not in str(caught.value)
    assert "input_value=" not in str(caught.value)


@pytest.mark.parametrize(
    ("message", "field"),
    [
        pytest.param(_notice(), "payload_base64", id="notice"),
        pytest.param(
            _request_response(), "request_payload_base64", id="request"
        ),
        pytest.param(
            _request_response(), "response_payload_base64", id="response"
        ),
    ],
)
@pytest.mark.parametrize(
    "payload",
    ["", "YQ==\n", "YQ", "あ"],
    ids=["empty", "newline", "missing-padding", "non-ascii"],
)
def test_wire_publication_rejects_malformed_base64(
    message: CorrelatedNotice | CorrelatedRequestResponse,
    field: str,
    payload: str,
) -> None:
    publication = make_publication(
        message, stream_id=STREAM_ID, publication_sequence=1
    )
    data = json.loads(dump_publication_json(publication))
    data[field] = payload

    with pytest.raises(ValidationError) as caught:
        parse_publication_json(json.dumps(data))
    assert any(error["loc"][-1] == field for error in caught.value.errors())


@pytest.mark.parametrize("size", [256, 257, 258])
def test_publication_preserves_binary_payloads(size: int) -> None:
    payload = (bytes(range(256)) * 2)[:size]
    notice = _notice(payload)
    exchange = _request_response(
        request_raw=payload, response_raw=payload[::-1]
    )
    for message in (notice, exchange):
        publication = parse_publication_json(
            dump_publication_json(
                make_publication(
                    message, stream_id=STREAM_ID, publication_sequence=1
                )
            )
        )
        if isinstance(publication, NoticePublication):
            assert base64.b64decode(publication.payload_base64) == payload
        else:
            assert (
                base64.b64decode(publication.request_payload_base64) == payload
            )
            assert (
                base64.b64decode(publication.response_payload_base64)
                == payload[::-1]
            )
