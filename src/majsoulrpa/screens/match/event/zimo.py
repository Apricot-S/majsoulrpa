from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    get_int,
    get_optional_dict,
    get_str,
    get_str_list,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import (
    MAX_DORA_INDICATORS,
    MAX_LEFT_TILE_COUNT,
)
from majsoulrpa.screens.match.event.liqi_success import LiqiSuccess
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ZimoEvent(_MatchEventBase):
    seat: Seat
    tile: Tile | None
    left_tile_count: int
    dora_indicators: tuple[Tile, ...]
    liqi_success: LiqiSuccess | None = None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if not 0 <= self.left_tile_count <= MAX_LEFT_TILE_COUNT:
            msg = "left_tile_count must be between 0 and 69."
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
        tile_value = get_str(data, "tile")
        liqi = get_optional_dict(data, "liqi")
        return cls(
            action_step=action_step,
            seat=validate_seat(get_int(data, "seat")),
            tile=None if tile_value == "" else validate_tile(tile_value),
            left_tile_count=get_int(data, "left_tile_count"),
            dora_indicators=tuple(
                validate_tile(tile) for tile in get_str_list(data, "doras")
            ),
            liqi_success=None if liqi is None else LiqiSuccess.from_dict(liqi),
        )
