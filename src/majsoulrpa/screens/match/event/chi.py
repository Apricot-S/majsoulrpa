from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_int,
    _get_int_list,
    _get_optional_dict,
    _get_str_list,
)
from majsoulrpa.screens.match.event._base import _MatchEventBase
from majsoulrpa.screens.match.event._constants import CHI_TILE_COUNT
from majsoulrpa.screens.match.event.liqi_success import LiqiSuccess
from majsoulrpa.screens.match.types import (
    Seat,
    Tile,
    validate_seat,
    validate_tile,
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ChiEvent(_MatchEventBase):
    seat: Seat
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    liqi_success: LiqiSuccess | None = None

    def __post_init__(self) -> None:
        _MatchEventBase.__post_init__(self)
        if self.seat == self.from_seat:
            msg = "seat and from_seat must identify different players."
            raise ValueError(msg)
        if len(self.consumed) != CHI_TILE_COUNT - 1:
            msg = "consumed must contain two tiles."
            raise ValueError(msg)
        tiles = (*self.consumed, self.tile)
        suits = {tile[1] for tile in tiles}
        numbers = sorted(
            5 if tile[0] == "0" else int(tile[0]) for tile in tiles
        )
        if (
            len(suits) != 1
            or not suits <= {"m", "p", "s"}
            or numbers != list(range(numbers[0], numbers[0] + 3))
        ):
            msg = "tiles must form a suited sequence."
            raise ValueError(msg)

    @classmethod
    def from_dict(
        cls,
        action_step: int,
        data: Mapping[str, JsonValue],
    ) -> Self:
        if _get_int(data, "ActionChiPengGang.type") != 0:
            msg = "ActionChiPengGang.type must identify chi."
            raise ValueError(msg)
        seat = validate_seat(_get_int(data, "ActionChiPengGang.seat"))
        tile_values = _get_str_list(data, "ActionChiPengGang.tiles")
        from_values = _get_int_list(data, "ActionChiPengGang.froms")
        if (
            len(tile_values) != CHI_TILE_COUNT
            or len(from_values) != CHI_TILE_COUNT
        ):
            msg = "A chi must contain three tiles and three source seats."
            raise ValueError(msg)
        if from_values[:2] != [seat, seat]:
            msg = "The first two chi tiles must come from the calling player."
            raise ValueError(msg)
        liqi = _get_optional_dict(data, "ActionChiPengGang.liqi")
        return cls(
            action_step=action_step,
            seat=seat,
            from_seat=validate_seat(from_values[-1]),
            tile=validate_tile(tile_values[-1]),
            consumed=(
                validate_tile(tile_values[0]),
                validate_tile(tile_values[1]),
            ),
            liqi_success=None if liqi is None else LiqiSuccess.from_dict(liqi),
        )
