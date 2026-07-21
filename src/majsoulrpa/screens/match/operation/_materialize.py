from typing import assert_never

from majsoulrpa.screens.match.event import MatchEvent, NewRoundEvent, ZimoEvent
from majsoulrpa.screens.match.operation._specification import (
    _DapaiOperationSpecification,
    _OperationCandidatesSpecification,
)
from majsoulrpa.screens.match.operation.candidates import OperationCandidates
from majsoulrpa.screens.match.operation.dapai import DapaiOperation
from majsoulrpa.screens.match.types import Seat, Tile


def materialize_operation_candidates(
    specification: _OperationCandidatesSpecification | None,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
) -> OperationCandidates | None:
    if specification is None:
        return None

    operations: list[DapaiOperation] = []
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
        if tile[0] == "5" and tile[1] in {"m", "p", "s"}:
            forbidden_tiles.add(Tile(f"0{tile[1]}"))

    candidates = [
        DapaiOperation(tile=tile, moqie=False)
        for tile in shoupai
        if tile not in forbidden_tiles
    ]
    if zimopai is not None and zimopai not in forbidden_tiles:
        candidates.append(
            DapaiOperation(
                tile=zimopai,
                moqie=not isinstance(event, NewRoundEvent),
            )
        )
    return candidates
