from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match._common import (
    validate_chi_tiles,
    validate_same_tile_kind,
)
from majsoulrpa.screens.match.types import Seat, Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DapaiOperation:
    tile: Tile
    moqie: bool


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ChiOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]

    def __post_init__(self) -> None:
        validate_chi_tiles(self.tile, self.consumed)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class PengOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]

    def __post_init__(self) -> None:
        validate_same_tile_kind(self.tile, self.consumed)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AngangOperation:
    consumed: tuple[Tile, Tile, Tile, Tile]

    def __post_init__(self) -> None:
        validate_same_tile_kind(self.consumed[0], self.consumed[1:])


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class DaminggangOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile, Tile]

    def __post_init__(self) -> None:
        validate_same_tile_kind(self.tile, self.consumed)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class JiagangOperation:
    from_seat: Seat
    tile: Tile
    consumed: tuple[Tile, Tile]
    added: Tile

    def __post_init__(self) -> None:
        validate_same_tile_kind(self.tile, (*self.consumed, self.added))


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiqiOperation:
    tile: Tile
    moqie: bool


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ZimohuOperation:
    tile: Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RongOperation:
    from_seat: Seat
    tile: Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class LiujuOperation:
    pass


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class BabeiOperation:
    pass


type MatchOperation = (
    DapaiOperation
    | ChiOperation
    | PengOperation
    | AngangOperation
    | DaminggangOperation
    | JiagangOperation
    | LiqiOperation
    | ZimohuOperation
    | RongOperation
    | LiujuOperation
    | BabeiOperation
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class OperationCandidates:
    time_fixed_ms: int
    time_add_ms: int
    operations: tuple[MatchOperation, ...]

    def __post_init__(self) -> None:
        if self.time_fixed_ms < 0 or self.time_add_ms < 0:
            msg = "Operation time must be nonnegative."
            raise ValueError(msg)
        if not self.operations:
            msg = "Operation candidates must not be empty."
            raise ValueError(msg)
