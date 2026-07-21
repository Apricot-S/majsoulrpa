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


type _MatchOperationSpecification = (
    _DapaiOperationSpecification
    | _ChiOperationSpecification
    | _PengOperationSpecification
)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class _OperationCandidatesSpecification:
    time_fixed_ms: int
    time_add_ms: int
    operations: tuple[_MatchOperationSpecification, ...]
