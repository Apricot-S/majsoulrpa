import base64
import binascii
import uuid
from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    field_validator,
)

from majsoulrpa.sniffer.correlator import (
    CorrelatedMessage,
    CorrelatedNotice,
    CorrelatedRequestResponse,
    Direction,
)
from majsoulrpa.sniffer.envelope import (
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
)

SCHEMA_VERSION = 1
SNIFFER_TOPIC = b"majsoulrpa.sniffer.v1"

NonEmptyString = Annotated[str, Field(min_length=1)]
PositiveSequence = Annotated[int, Field(ge=1)]
RequestNumber = Annotated[int, Field(ge=0, le=0xFFFF)]


class _PublicationBase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1] = SCHEMA_VERSION
    stream_id: uuid.UUID
    publication_sequence: PositiveSequence
    connection_id: NonEmptyString


class NoticePublication(_PublicationBase):
    kind: Literal["notice"] = "notice"
    direction: Direction
    frame_sequence: PositiveSequence
    observed_at: AwareDatetime
    api_name: NonEmptyString
    payload_base64: NonEmptyString

    @field_validator("payload_base64")
    @classmethod
    def _validate_payload_base64(cls, value: str) -> str:
        return _validated_base64(value)


class RequestResponsePublication(_PublicationBase):
    kind: Literal["request_response"] = "request_response"
    request_direction: Direction
    request_number: RequestNumber
    request_frame_sequence: PositiveSequence
    request_observed_at: AwareDatetime
    response_frame_sequence: PositiveSequence
    response_observed_at: AwareDatetime
    api_name: NonEmptyString
    request_payload_base64: NonEmptyString
    response_payload_base64: NonEmptyString

    @field_validator("request_payload_base64", "response_payload_base64")
    @classmethod
    def _validate_payload_base64(cls, value: str) -> str:
        return _validated_base64(value)


type SnifferPublication = NoticePublication | RequestResponsePublication

_PUBLICATION_ADAPTER = TypeAdapter(
    Annotated[SnifferPublication, Field(discriminator="kind")],
)


def make_publication(
    message: CorrelatedMessage,
    *,
    stream_id: uuid.UUID,
    publication_sequence: int,
) -> SnifferPublication:
    match message:
        case CorrelatedNotice():
            return _make_notice_publication(
                message,
                stream_id=stream_id,
                publication_sequence=publication_sequence,
            )
        case CorrelatedRequestResponse():
            return _make_request_response_publication(
                message,
                stream_id=stream_id,
                publication_sequence=publication_sequence,
            )


def dump_publication_json(publication: SnifferPublication) -> bytes:
    return _PUBLICATION_ADAPTER.dump_json(publication)


def parse_publication_json(payload: str | bytes) -> SnifferPublication:
    return _PUBLICATION_ADAPTER.validate_json(payload)


def _make_notice_publication(
    message: CorrelatedNotice,
    *,
    stream_id: uuid.UUID,
    publication_sequence: int,
) -> NoticePublication:
    observation = message.observation
    envelope = observation.envelope
    if not isinstance(envelope, NoticeEnvelope):
        msg = "Correlated Notice does not contain a Notice envelope."
        raise TypeError(msg)
    return NoticePublication(
        stream_id=stream_id,
        publication_sequence=publication_sequence,
        connection_id=observation.connection_id,
        direction=observation.direction,
        frame_sequence=observation.frame_sequence,
        observed_at=observation.observed_at,
        api_name=envelope.api_name,
        payload_base64=_encoded(envelope.raw_payload),
    )


def _make_request_response_publication(
    message: CorrelatedRequestResponse,
    *,
    stream_id: uuid.UUID,
    publication_sequence: int,
) -> RequestResponsePublication:
    request = message.request
    response = message.response
    request_envelope = request.envelope
    response_envelope = response.envelope
    if not isinstance(request_envelope, RequestEnvelope):
        msg = "Correlated exchange does not contain a Request envelope."
        raise TypeError(msg)
    if not isinstance(response_envelope, ResponseEnvelope):
        msg = "Correlated exchange does not contain a Response envelope."
        raise TypeError(msg)
    if request.connection_id != response.connection_id:
        msg = "Correlated Request and Response use different connections."
        raise ValueError(msg)
    if request_envelope.request_number != response_envelope.request_number:
        msg = "Correlated Request and Response use different request numbers."
        raise ValueError(msg)
    if request.direction is not response.direction.opposite():
        msg = "Correlated Request and Response do not use opposite directions."
        raise ValueError(msg)

    return RequestResponsePublication(
        stream_id=stream_id,
        publication_sequence=publication_sequence,
        connection_id=request.connection_id,
        request_direction=request.direction,
        request_number=request_envelope.request_number,
        request_frame_sequence=request.frame_sequence,
        request_observed_at=request.observed_at,
        response_frame_sequence=response.frame_sequence,
        response_observed_at=response.observed_at,
        api_name=request_envelope.api_name,
        request_payload_base64=_encoded(request_envelope.raw_payload),
        response_payload_base64=_encoded(response_envelope.raw_payload),
    )


def _encoded(payload: bytes) -> str:
    return base64.b64encode(payload).decode("ascii")


def _validated_base64(value: str) -> str:
    try:
        base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as error:
        msg = "Payload must contain valid base64."
        raise ValueError(msg) from error
    return value
