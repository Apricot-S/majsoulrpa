from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match._common import validate_chi_tiles
from majsoulrpa.screens.match.types import Seat, Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ChiOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]

    def __post_init__(self) -> None:
        validate_chi_tiles(self.tile, self.consumed)
