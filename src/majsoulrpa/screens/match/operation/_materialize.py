from typing import assert_never

from majsoulrpa.screens.match.event import (
    DapaiEvent,
    MatchEvent,
    NewRoundEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation._specification import (
    _ChiOperationSpecification,
    _DapaiOperationSpecification,
    _OperationCandidatesSpecification,
)
from majsoulrpa.screens.match.operation.candidates import (
    MatchOperation,
    OperationCandidates,
)
from majsoulrpa.screens.match.operation.chi import ChiOperation
from majsoulrpa.screens.match.operation.dapai import DapaiOperation
from majsoulrpa.screens.match.types import Seat, Tile

_FOUR_PLAYER_COUNT = 4


def materialize_operation_candidates(
    specification: _OperationCandidatesSpecification | None,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> OperationCandidates | None:
    if specification is None:
        return None

    operations: list[MatchOperation] = []
    for operation_specification in specification.operations:
        match operation_specification:
            case _DapaiOperationSpecification():
                if isinstance(event, NewRoundEvent) and event.ju != self_seat:
                    msg = "Only the dealer can discard after ActionNewRound."
                    raise ValueError(msg)
                if isinstance(event, ZimoEvent) and event.seat != self_seat:
                    msg = "An opponent draw cannot provide self operations."
                    raise ValueError(msg)
                operations.extend(
                    _materialize_dapai_operations(
                        operation_specification,
                        event,
                        shoupai,
                        zimopai,
                    )
                )
                continue
            case _ChiOperationSpecification():
                if player_count != _FOUR_PLAYER_COUNT:
                    msg = (
                        "A chi operation is only valid in a four-player match."
                    )
                    raise ValueError(msg)
                if not isinstance(event, DapaiEvent):
                    msg = "A chi operation must follow a discard."
                    raise TypeError(msg)
                if event.seat != (self_seat - 1) % _FOUR_PLAYER_COUNT:
                    msg = (
                        "A chi must claim a discard from the preceding player."
                    )
                    raise ValueError(msg)
                if zimopai is not None:
                    msg = "A chi cannot be selected with an unresolved draw."
                    raise ValueError(msg)
                operations.extend(
                    _materialize_chi_operations(
                        operation_specification,
                        event,
                        shoupai,
                    )
                )
                continue
        assert_never(operation_specification)

    deduplicated_operations = tuple(dict.fromkeys(operations))
    if not deduplicated_operations:
        msg = "OptionalOperationList has no selectable operations."
        raise ValueError(msg)
    return OperationCandidates(
        time_fixed_ms=specification.time_fixed_ms,
        time_add_ms=specification.time_add_ms,
        operations=deduplicated_operations,
    )


def _materialize_dapai_operations(
    specification: _DapaiOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
) -> list[DapaiOperation]:
    forbidden_tiles = set(specification.forbidden_tiles)
    for tile in specification.forbidden_tiles:
        # Work around a Majsoul API inconsistency. When a swap calling
        # forbids a normal five, combination may omit the matching
        # red five.
        if tile in {"5m", "5p", "5s"}:
            forbidden_tiles.add(Tile(f"0{tile[1]}"))

    candidates = [
        DapaiOperation(tile=tile, moqie=False)
        for tile in shoupai
        if tile not in forbidden_tiles
    ]
    if zimopai is not None and zimopai not in forbidden_tiles:
        # The dealer's first discard is not moqie. All 14 tiles belong
        # to the initial deal, although the last one is displayed apart.
        candidates.append(
            DapaiOperation(
                tile=zimopai,
                moqie=not isinstance(event, NewRoundEvent),
            )
        )
    return candidates


def _materialize_chi_operations(
    specification: _ChiOperationSpecification,
    event: DapaiEvent,
    shoupai: tuple[Tile, ...],
) -> list[ChiOperation]:
    operations: list[ChiOperation] = []
    for consumed in specification.consumed_candidates:
        remaining_tiles = list(shoupai)
        for tile in consumed:
            try:
                remaining_tiles.remove(tile)
            except ValueError:
                msg = "A chi operation must consume tiles in the hand."
                raise ValueError(msg) from None
        operations.append(
            ChiOperation(
                from_seat=event.seat,
                tile=event.tile,
                consumed=consumed,
            )
        )
    return operations
