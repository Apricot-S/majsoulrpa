from dataclasses import dataclass

from google.protobuf.descriptor import FileDescriptor
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError, Message
from google.protobuf.message_factory import GetMessageClass
from pydantic import JsonValue

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.sniffer.envelope import (
    NoticeEnvelope,
    RequestEnvelope,
    ResponseEnvelope,
    parse_liqi_envelope,
)
from majsoulrpa.sniffer.event_adapter import raw_event_from_publication
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    DecodedSnifferMessage,
    RawNotice,
    RawRequestResponse,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
    SnifferPublication,
)


class SnifferMessageDecodeError(RuntimeError):
    """Base class for client-side Sniffer decode failures."""


class UnknownAPIError(SnifferMessageDecodeError):
    """Raised when the protocol descriptor has no requested API."""


class MissingResponseTypeError(SnifferMessageDecodeError):
    """Raised when an API has no response message type."""


class LiqiBodyDecodeError(SnifferMessageDecodeError):
    """Raised when a known protobuf message body is malformed."""


class PublicationEnvelopeMismatchError(SnifferMessageDecodeError):
    """Raised when metadata differs from its raw envelope."""


@dataclass(frozen=True, slots=True)
class _MessageTypes:
    request: type[Message]
    response: type[Message] | None


class SnifferMessageDecoder:
    def __init__(
        self,
        descriptor: FileDescriptor = liqi_pb2.DESCRIPTOR,
    ) -> None:
        self._message_types = _build_message_type_map(descriptor)

    def decode(
        self,
        publication: SnifferPublication,
    ) -> DecodedSnifferMessage:
        match publication:
            case NoticePublication():
                return self._decode_notice(publication)
            case RequestResponsePublication():
                return self._decode_request_response(publication)

    def _decode_notice(
        self,
        publication: NoticePublication,
    ) -> DecodedNotice:
        raw = raw_event_from_publication(publication)
        if not isinstance(raw, RawNotice):
            msg = "Notice publication did not produce a raw Notice event."
            raise PublicationEnvelopeMismatchError(msg)
        envelope = parse_liqi_envelope(raw.payload)
        if not isinstance(envelope, NoticeEnvelope):
            msg = "Notice publication does not contain a Notice envelope."
            raise PublicationEnvelopeMismatchError(msg)
        _require_api_name(publication.api_name, envelope.api_name)

        message_types = self._get_message_types(publication.api_name)
        message = _decode_body(message_types.request, envelope.body)
        return DecodedNotice(raw=raw, message=message)

    def _decode_request_response(
        self,
        publication: RequestResponsePublication,
    ) -> DecodedRequestResponse:
        raw = raw_event_from_publication(publication)
        if not isinstance(raw, RawRequestResponse):
            msg = "Req/Res publication did not produce a raw Req/Res event."
            raise PublicationEnvelopeMismatchError(msg)
        request_envelope = parse_liqi_envelope(raw.request)
        response_envelope = parse_liqi_envelope(raw.response)
        if not isinstance(request_envelope, RequestEnvelope):
            msg = "Req/Res publication does not contain a Request envelope."
            raise PublicationEnvelopeMismatchError(msg)
        if not isinstance(response_envelope, ResponseEnvelope):
            msg = "Req/Res publication does not contain a Response envelope."
            raise PublicationEnvelopeMismatchError(msg)
        _require_api_name(publication.api_name, request_envelope.api_name)
        if (
            publication.request_number != request_envelope.request_number
            or publication.request_number != response_envelope.request_number
        ):
            msg = (
                "Publication and raw envelopes use different request numbers."
            )
            raise PublicationEnvelopeMismatchError(msg)

        message_types = self._get_message_types(publication.api_name)
        if message_types.response is None:
            msg = (
                f"API {publication.api_name!r} does not define a response "
                "type."
            )
            raise MissingResponseTypeError(msg)
        request = _decode_body(message_types.request, request_envelope.body)
        response = _decode_body(
            message_types.response,
            response_envelope.body,
        )
        return DecodedRequestResponse(
            raw=raw,
            request=request,
            response=response,
        )

    def _get_message_types(self, api_name: str) -> _MessageTypes:
        try:
            return self._message_types[api_name]
        except KeyError as error:
            msg = f"Unknown API name: {api_name!r}."
            raise UnknownAPIError(msg) from error


def _build_message_type_map(
    descriptor: FileDescriptor,
) -> dict[str, _MessageTypes]:
    mapping: dict[str, _MessageTypes] = {}
    for service in descriptor.services_by_name.values():
        for method in service.methods:
            mapping[f".{method.full_name}"] = _MessageTypes(
                request=GetMessageClass(method.input_type),
                response=GetMessageClass(method.output_type),
            )
    for message in descriptor.message_types_by_name.values():
        mapping[f".{message.full_name}"] = _MessageTypes(
            request=GetMessageClass(message),
            response=None,
        )
    return mapping


def _decode_body(
    message_type: type[Message],
    body: bytes,
) -> dict[str, JsonValue]:
    message = message_type()
    try:
        message.ParseFromString(body)
    except DecodeError as error:
        msg = "Could not decode protobuf body for a known API."
        raise LiqiBodyDecodeError(msg) from error
    return MessageToDict(
        message,
        always_print_fields_with_no_presence=True,
        preserving_proto_field_name=True,
    )


def _require_api_name(publication_name: str, envelope_name: str) -> None:
    if publication_name != envelope_name:
        msg = "Publication and raw envelope use different API names."
        raise PublicationEnvelopeMismatchError(msg)
