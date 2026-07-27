from dataclasses import dataclass
from typing import final

from majsoulrpa.screens.match.types import Tile


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _DapaiOperationSpecification:
    forbidden_tiles: tuple[Tile, ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _ChiOperationSpecification:
    consumed_candidates: tuple[tuple[Tile, Tile], ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _PengOperationSpecification:
    consumed_candidates: tuple[tuple[Tile, Tile], ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _AngangOperationSpecification:
    consumed_candidates: tuple[tuple[Tile, Tile, Tile, Tile], ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _DaminggangOperationSpecification:
    consumed_candidates: tuple[tuple[Tile, Tile, Tile], ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _JiagangOperationSpecification:
    tile_candidates: tuple[tuple[Tile, Tile, Tile, Tile], ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _LiqiOperationSpecification:
    candidate_tiles: tuple[Tile, ...]


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _ZimohuOperationSpecification:
    pass


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _RongOperationSpecification:
    pass


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _LiujuOperationSpecification:
    pass


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _BabeiOperationSpecification:
    pass


type _MatchOperationSpecification = (
    _DapaiOperationSpecification
    | _ChiOperationSpecification
    | _PengOperationSpecification
    | _AngangOperationSpecification
    | _DaminggangOperationSpecification
    | _JiagangOperationSpecification
    | _LiqiOperationSpecification
    | _ZimohuOperationSpecification
    | _RongOperationSpecification
    | _LiujuOperationSpecification
    | _BabeiOperationSpecification
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _OperationCandidatesSpecification:
    time_fixed_ms: int
    time_add_ms: int
    operations: tuple[_MatchOperationSpecification, ...]
