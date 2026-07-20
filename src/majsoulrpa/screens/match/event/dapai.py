from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._decode import (
    _get_bool,
    _get_int,
    _get_str,
    _get_str_list,
)
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiEvent(_MatchEventBase):
    seat: Seat
    tile: Tile
    moqie: bool
    liqi: bool
    wliqi: bool
    dora_indicators: tuple[Tile, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.liqi and self.wliqi:
            msg = "liqi and wliqi must not both be true."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        return cls(
            action_step=action_step,
            seat=validate_seat(_get_int(data, "ActionDiscardTile.seat")),
            tile=validate_tile(_get_str(data, "ActionDiscardTile.tile")),
            moqie=_get_bool(data, "ActionDiscardTile.moqie"),
            liqi=_get_bool(data, "ActionDiscardTile.is_liqi"),
            wliqi=_get_bool(data, "ActionDiscardTile.is_wliqi"),
            dora_indicators=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "ActionDiscardTile.doras")
            ),
        )
