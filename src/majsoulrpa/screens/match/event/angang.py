from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import _get_int, _get_str, _get_str_list
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import MAX_DORA_INDICATORS
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


def _canonicalize_consumed(tile: Tile) -> tuple[Tile, Tile, Tile, Tile]:
    if tile in {"0m", "5m", "0p", "5p", "0s", "5s"}:
        red = Tile(f"0{tile[1]}")
        normal = Tile(f"5{tile[1]}")
        return red, normal, normal, normal
    return tile, tile, tile, tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AngangEvent(_MatchEventBase):
    seat: Seat
    consumed: tuple[Tile, Tile, Tile, Tile]
    dora_indicators: tuple[Tile, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.consumed != _canonicalize_consumed(self.consumed[0]):
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
            consumed=_canonicalize_consumed(tile),
            dora_indicators=tuple(
                validate_tile(dora)
                for dora in _get_str_list(data, "ActionAnGangAddGang.doras")
            ),
        )
