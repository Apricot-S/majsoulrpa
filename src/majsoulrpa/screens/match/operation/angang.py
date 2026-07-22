from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match._common import validate_same_tile_kind
from majsoulrpa.screens.match.types import Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AngangOperation:
    consumed: tuple[Tile, Tile, Tile, Tile]

    def __post_init__(self) -> None:
        validate_same_tile_kind(self.consumed[0], self.consumed[1:])
