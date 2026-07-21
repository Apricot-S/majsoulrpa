from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match.types import Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiOperation:
    tile: Tile
    moqie: bool
