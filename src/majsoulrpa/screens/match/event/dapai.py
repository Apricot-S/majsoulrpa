from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._common import validate_tile
from majsoulrpa.screens.match.event._decode import (
    _get_bool,
    _get_int,
    _get_str,
    _get_str_list,
)

_MAX_SEAT = 3


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiEvent(_MatchEventBase):
    seat: int
    tile: str
    moqie: bool
    liqi: bool
    wliqi: bool
    dora_indicators: tuple[str, ...]

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if not 0 <= self.seat <= _MAX_SEAT:
            msg = "Dapai seat must be between 0 and 3."
            raise ValueError(msg)
        validate_tile(self.tile)
        if self.liqi and self.wliqi:
            msg = "liqi and wliqi must not both be true."
            raise ValueError(msg)
        for tile in self.dora_indicators:
            validate_tile(tile)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        return cls(
            action_step=action_step,
            seat=_get_int(data, "ActionDiscardTile.seat"),
            tile=_get_str(data, "ActionDiscardTile.tile"),
            moqie=_get_bool(data, "ActionDiscardTile.moqie"),
            liqi=_get_bool(data, "ActionDiscardTile.is_liqi"),
            wliqi=_get_bool(data, "ActionDiscardTile.is_wliqi"),
            dora_indicators=tuple(
                _get_str_list(data, "ActionDiscardTile.doras")
            ),
        )
