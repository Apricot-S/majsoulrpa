from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens._json_fields import get_bool, get_int
from majsoulrpa.screens.match.types import Seat, validate_seat


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiqiSuccess:
    seat: Seat
    score: int
    liqibang: int
    failed: bool

    def __post_init__(self) -> None:
        if self.liqibang < 0:
            msg = "liqibang must be nonnegative."
            raise ValueError(msg)

    @classmethod
    def from_dict(cls, data: Mapping[str, JsonValue]) -> Self:
        return cls(
            seat=validate_seat(get_int(data, "seat")),
            score=get_int(data, "score"),
            liqibang=get_int(data, "liqibang"),
            failed=get_bool(data, "failed"),
        )
