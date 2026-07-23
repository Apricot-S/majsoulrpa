from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._common import tile_sort_key
from majsoulrpa.screens.match._decode import (
    _get_int,
    _get_int_list,
    _get_str_list,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import (
    MAX_DORA_INDICATORS,
    MAX_LEFT_TILE_COUNT,
)
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)

_NUM_CHANG = 3
_SHOUPAI_SIZE = 13
_DEALT_TILE_COUNTS = (13, 14)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NewRoundEvent(_MatchEventBase):
    chang: int
    ju: Seat
    ben: int
    liqibang: int
    dora_indicators: tuple[Tile, ...]
    left_tile_count: int
    scores: tuple[int, ...]
    shoupai: tuple[Tile, ...]
    zimopai: Tile | None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.action_step not in (0, 1):
            msg = "ActionNewRound must be step 0 or 1."
            raise ValueError(msg)
        if not 0 <= self.chang < _NUM_CHANG:
            msg = "chang must be between 0 and 2."
            raise ValueError(msg)
        if len(self.scores) not in (3, 4):
            msg = "scores must contain three or four values."
            raise ValueError(msg)
        if not 0 <= self.ju < len(self.scores):
            msg = "ju must identify a seat in scores."
            raise ValueError(msg)
        if self.ben < 0:
            msg = "ben must be nonnegative."
            raise ValueError(msg)
        if self.liqibang < 0:
            msg = "liqibang must be nonnegative."
            raise ValueError(msg)
        if not 1 <= len(self.dora_indicators) <= MAX_DORA_INDICATORS:
            msg = "dora_indicators must contain between one and five tiles."
            raise ValueError(msg)
        if not 0 <= self.left_tile_count <= MAX_LEFT_TILE_COUNT:
            msg = "left_tile_count must be between 0 and 69."
            raise ValueError(msg)
        if len(self.shoupai) != _SHOUPAI_SIZE:
            msg = "shoupai must contain thirteen tiles."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        tiles = tuple(
            validate_tile(tile)
            for tile in _get_str_list(data, "ActionNewRound.tiles")
        )
        if len(tiles) not in _DEALT_TILE_COUNTS:
            msg = (
                "ActionNewRound.tiles must contain thirteen or fourteen tiles."
            )
            raise ValueError(msg)
        sorted_tiles = tuple(sorted(tiles, key=tile_sort_key))
        shoupai = sorted_tiles[:_SHOUPAI_SIZE]
        zimopai = (
            sorted_tiles[_SHOUPAI_SIZE]
            if len(sorted_tiles) > _SHOUPAI_SIZE
            else None
        )

        return cls(
            action_step=action_step,
            chang=_get_int(data, "ActionNewRound.chang"),
            ju=validate_seat(_get_int(data, "ActionNewRound.ju")),
            ben=_get_int(data, "ActionNewRound.ben"),
            liqibang=_get_int(data, "ActionNewRound.liqibang"),
            dora_indicators=tuple(
                validate_tile(tile)
                for tile in _get_str_list(data, "ActionNewRound.doras")
            ),
            left_tile_count=_get_int(
                data,
                "ActionNewRound.left_tile_count",
            ),
            scores=tuple(_get_int_list(data, "ActionNewRound.scores")),
            shoupai=shoupai,
            zimopai=zimopai,
        )
