from collections.abc import Sequence
from typing import assert_never

from majsoulrpa.screens.match._common import is_preceding_seat
from majsoulrpa.screens.match.event import (
    DapaiEvent,
    MatchEvent,
    NewRoundEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation._specification import (
    _AngangOperationSpecification,
    _ChiOperationSpecification,
    _DaminggangOperationSpecification,
    _DapaiOperationSpecification,
    _LiqiOperationSpecification,
    _MatchOperationSpecification,
    _OperationCandidatesSpecification,
    _PengOperationSpecification,
)
from majsoulrpa.screens.match.operation.models import (
    AngangOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    LiqiOperation,
    MatchOperation,
    OperationCandidates,
    PengOperation,
)
from majsoulrpa.screens.match.state import Fulu
from majsoulrpa.screens.match.types import Seat, Tile

_FOUR_PLAYER_COUNT = 4


def materialize_operation_candidates(
    specification: _OperationCandidatesSpecification | None,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
    *,
    self_fulu: tuple[Fulu, ...] = (),
) -> OperationCandidates | None:
    if specification is None:
        return None

    operations: list[MatchOperation] = []
    for operation_specification in specification.operations:
        operations.extend(
            _materialize_operation_specification(
                operation_specification,
                event,
                shoupai,
                zimopai,
                self_seat,
                player_count,
                self_fulu,
            )
        )

    deduplicated_operations = tuple(dict.fromkeys(operations))
    if not deduplicated_operations:
        msg = "OptionalOperationList has no selectable operations."
        raise ValueError(msg)
    return OperationCandidates(
        time_fixed_ms=specification.time_fixed_ms,
        time_add_ms=specification.time_add_ms,
        operations=deduplicated_operations,
    )


def _materialize_operation_specification(
    specification: _MatchOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
    self_fulu: tuple[Fulu, ...],
) -> Sequence[MatchOperation]:
    # Jiagang materialization will use the current self melds. Keep this
    # context on every dispatch path.
    _ = self_fulu
    match specification:
        case _DapaiOperationSpecification():
            return _materialize_dapai_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
            )
        case _ChiOperationSpecification():
            return _materialize_chi_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
                player_count,
            )
        case _PengOperationSpecification():
            return _materialize_peng_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
                player_count,
            )
        case _AngangOperationSpecification():
            return _materialize_angang_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
            )
        case _DaminggangOperationSpecification():
            return _materialize_daminggang_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
                player_count,
            )
        case _LiqiOperationSpecification():
            return _materialize_liqi_specification(
                specification,
                event,
                shoupai,
                zimopai,
                self_seat,
            )
    assert_never(specification)


def _materialize_dapai_specification(
    specification: _DapaiOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
) -> list[DapaiOperation]:
    if isinstance(event, NewRoundEvent) and event.ju != self_seat:
        msg = "Only the dealer can discard after ActionNewRound."
        raise ValueError(msg)
    if isinstance(event, ZimoEvent) and event.seat != self_seat:
        msg = "An opponent draw cannot provide self operations."
        raise ValueError(msg)

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


def _materialize_chi_specification(
    specification: _ChiOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> list[ChiOperation]:
    if player_count != _FOUR_PLAYER_COUNT:
        msg = "A chi operation is only valid in a four-player match."
        raise ValueError(msg)

    call_event = _validate_call_event(
        event,
        zimopai,
        self_seat,
        player_count,
        "chi",
    )
    if not is_preceding_seat(
        call_event.seat,
        relative_to=self_seat,
        player_count=player_count,
    ):
        msg = "A chi must claim a discard from the preceding player."
        raise ValueError(msg)

    operations: list[ChiOperation] = []
    for consumed in specification.consumed_candidates:
        _validate_consumed_tiles_in_hand(consumed, shoupai, "chi")
        operations.append(
            ChiOperation(
                from_seat=call_event.seat,
                tile=call_event.tile,
                consumed=consumed,
            )
        )
    return operations


def _materialize_peng_specification(
    specification: _PengOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> list[PengOperation]:
    call_event = _validate_call_event(
        event,
        zimopai,
        self_seat,
        player_count,
        "peng",
    )
    operations: list[PengOperation] = []
    for consumed in specification.consumed_candidates:
        _validate_consumed_tiles_in_hand(consumed, shoupai, "peng")
        operations.append(
            PengOperation(
                from_seat=call_event.seat,
                tile=call_event.tile,
                consumed=consumed,
            )
        )
    return operations


def _materialize_angang_specification(
    specification: _AngangOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
) -> list[AngangOperation]:
    angang_zimopai = _validate_angang_event(event, zimopai, self_seat)
    available_tiles = (*shoupai, angang_zimopai)
    operations: list[AngangOperation] = []
    for consumed in specification.consumed_candidates:
        _validate_consumed_tiles_in_hand(consumed, available_tiles, "angang")
        operations.append(AngangOperation(consumed=consumed))
    return operations


def _materialize_daminggang_specification(
    specification: _DaminggangOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> list[DaminggangOperation]:
    call_event = _validate_call_event(
        event,
        zimopai,
        self_seat,
        player_count,
        "daminggang",
    )
    operations: list[DaminggangOperation] = []
    for consumed in specification.consumed_candidates:
        _validate_consumed_tiles_in_hand(consumed, shoupai, "daminggang")
        operations.append(
            DaminggangOperation(
                from_seat=call_event.seat,
                tile=call_event.tile,
                consumed=consumed,
            )
        )
    return operations


def _materialize_liqi_specification(
    specification: _LiqiOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
) -> list[LiqiOperation]:
    if isinstance(event, NewRoundEvent):
        if event.ju != self_seat:
            msg = "Only the dealer can declare liqi after ActionNewRound."
            raise ValueError(msg)
    elif isinstance(event, ZimoEvent):
        if event.seat != self_seat:
            msg = "An opponent draw cannot provide a liqi operation."
            raise ValueError(msg)
    else:
        msg = "A liqi operation must follow a self draw."
        raise TypeError(msg)

    operations: list[LiqiOperation] = []
    for tile in specification.candidate_tiles:
        candidate_operations = _materialize_liqi_tile(
            tile,
            event,
            shoupai,
            zimopai,
        )
        if not candidate_operations:
            msg = "A liqi candidate must exist in the hand or drawn tile."
            raise ValueError(msg)
        operations.extend(candidate_operations)

        # Work around a Majsoul API inconsistency. When both a red five
        # and its normal counterpart can declare liqi, combination may
        # contain only the red five.
        if tile in {"0m", "0p", "0s"}:
            normal_five = Tile(f"5{tile[1]}")
            operations.extend(
                _materialize_liqi_tile(
                    normal_five,
                    event,
                    shoupai,
                    zimopai,
                )
            )
    return operations


def _validate_angang_event(
    event: MatchEvent,
    zimopai: Tile | None,
    self_seat: Seat,
) -> Tile:
    if isinstance(event, NewRoundEvent):
        if event.ju != self_seat:
            msg = "Only the dealer can declare angang after ActionNewRound."
            raise ValueError(msg)
    elif isinstance(event, ZimoEvent):
        if event.seat != self_seat:
            msg = "An opponent draw cannot provide an angang operation."
            raise ValueError(msg)
    else:
        msg = "An angang operation must follow a self draw."
        raise TypeError(msg)

    if zimopai is None:
        msg = "An angang operation requires a drawn tile."
        raise ValueError(msg)
    return zimopai


def _validate_consumed_tiles_in_hand(
    consumed: tuple[Tile, ...],
    shoupai: tuple[Tile, ...],
    operation_name: str,
) -> None:
    remaining_tiles = list(shoupai)
    for tile in consumed:
        try:
            remaining_tiles.remove(tile)
        except ValueError:
            msg = (
                f"A {operation_name} operation must consume tiles in the hand."
            )
            raise ValueError(msg) from None


def _validate_call_event(
    event: MatchEvent,
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
    operation_name: str,
) -> DapaiEvent:
    if not isinstance(event, DapaiEvent):
        msg = f"A {operation_name} operation must follow a discard."
        raise TypeError(msg)
    if event.seat >= player_count:
        msg = "A call source seat must identify a player."
        raise ValueError(msg)
    if event.seat == self_seat:
        msg = "A call cannot claim the self player's discard."
        raise ValueError(msg)
    if zimopai is not None:
        msg = f"A {operation_name} cannot be selected with an unresolved draw."
        raise ValueError(msg)
    return event


def _materialize_liqi_tile(
    tile: Tile,
    event: NewRoundEvent | ZimoEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
) -> list[LiqiOperation]:
    operations: list[LiqiOperation] = []
    if tile in shoupai:
        operations.append(LiqiOperation(tile=tile, moqie=False))
    if tile == zimopai:
        operations.append(
            LiqiOperation(
                tile=tile,
                moqie=not isinstance(event, NewRoundEvent),
            )
        )
    return operations
