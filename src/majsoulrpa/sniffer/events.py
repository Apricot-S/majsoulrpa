import datetime
from dataclasses import dataclass
from enum import StrEnum

from pydantic import JsonValue


class Direction(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def opposite(self) -> "Direction":
        if self is Direction.INBOUND:
            return Direction.OUTBOUND
        return Direction.INBOUND


@dataclass(frozen=True, slots=True)
class RawNotice:
    direction: Direction
    name: str
    payload: bytes
    observed_at: datetime.datetime


@dataclass(frozen=True, slots=True)
class RawRequestResponse:
    request_direction: Direction
    name: str
    request: bytes
    response: bytes
    request_observed_at: datetime.datetime
    response_observed_at: datetime.datetime


type RawSnifferMessage = RawNotice | RawRequestResponse


@dataclass(frozen=True, slots=True)
class DecodedNotice:
    raw: RawNotice
    message: dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class DecodedRequestResponse:
    raw: RawRequestResponse
    request: dict[str, JsonValue]
    response: dict[str, JsonValue]


type DecodedSnifferMessage = DecodedNotice | DecodedRequestResponse
