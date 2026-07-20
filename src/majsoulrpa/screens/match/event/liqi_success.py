from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match.event._decode import (
    _get_bool,
    _get_int,
)
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
            seat=validate_seat(_get_int(data, "LiQiSuccess.seat")),
            score=_get_int(data, "LiQiSuccess.score"),
            liqibang=_get_int(data, "LiQiSuccess.liqibang"),
            failed=_get_bool(data, "LiQiSuccess.failed"),
        )
