import base64

from majsoulrpa.sniffer.events import (
    RawNotice,
    RawRequestResponse,
    RawSnifferMessage,
)
from majsoulrpa.sniffer.publication import (
    NoticePublication,
    RequestResponsePublication,
    SnifferPublication,
)


def raw_event_from_publication(
    publication: SnifferPublication,
) -> RawSnifferMessage:
    match publication:
        case NoticePublication():
            return RawNotice(
                direction=publication.direction,
                name=publication.api_name,
                payload=_decoded(publication.payload_base64),
                observed_at=publication.observed_at,
            )
        case RequestResponsePublication():
            return RawRequestResponse(
                request_direction=publication.request_direction,
                name=publication.api_name,
                request=_decoded(publication.request_payload_base64),
                response=_decoded(publication.response_payload_base64),
                request_observed_at=publication.request_observed_at,
                response_observed_at=publication.response_observed_at,
            )


def _decoded(payload_base64: str) -> bytes:
    return base64.b64decode(payload_base64, validate=True)
