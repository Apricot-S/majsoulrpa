from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._common import canonicalize_angang_consumed
from majsoulrpa.screens.match._decode import _get_int, _get_str, _get_str_list
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import MAX_DORA_INDICATORS
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AngangEvent(_MatchEventBase):
    seat: Seat
    consumed: tuple[Tile, Tile, Tile, Tile]
    dora_indicators: tuple[Tile, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.consumed != canonicalize_angang_consumed(self.consumed[0]):
            msg = "consumed must use the canonical angang representation."
            raise ValueError(msg)
        if len(self.dora_indicators) > MAX_DORA_INDICATORS:
            msg = "dora_indicators must contain at most five tiles."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        if _get_int(data, "ActionAnGangAddGang.type") != 3:  # noqa: PLR2004
            msg = "ActionAnGangAddGang.type must identify angang."
            raise ValueError(msg)
        tile = validate_tile(_get_str(data, "ActionAnGangAddGang.tiles"))
        return cls(
            action_step=action_step,
            seat=validate_seat(_get_int(data, "ActionAnGangAddGang.seat")),
            consumed=canonicalize_angang_consumed(tile),
            dora_indicators=tuple(
                validate_tile(dora)
                for dora in _get_str_list(data, "ActionAnGangAddGang.doras")
            ),
        )
