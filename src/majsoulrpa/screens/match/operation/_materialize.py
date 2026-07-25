from collections import Counter
from collections.abc import Sequence
from typing import assert_never

from majsoulrpa.screens.match._common import is_preceding_seat
from majsoulrpa.screens.match.event import (
    AngangEvent,
    BabeiEvent,
    DapaiEvent,
    JiagangEvent,
    MatchEvent,
    NewRoundEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match.operation._specification import (
    _AngangOperationSpecification,
    _BabeiOperationSpecification,
    _ChiOperationSpecification,
    _DaminggangOperationSpecification,
    _DapaiOperationSpecification,
    _JiagangOperationSpecification,
    _LiqiOperationSpecification,
    _LiujuOperationSpecification,
    _MatchOperationSpecification,
    _OperationCandidatesSpecification,
    _PengOperationSpecification,
    _RongOperationSpecification,
    _ZimohuOperationSpecification,
)
from majsoulrpa.screens.match.operation.models import (
    AngangOperation,
    BabeiOperation,
    ChiOperation,
    DaminggangOperation,
    DapaiOperation,
    JiagangOperation,
    LiqiOperation,
    LiujuOperation,
    MatchOperation,
    OperationCandidates,
    PengOperation,
    RongOperation,
    ZimohuOperation,
)
from majsoulrpa.screens.match.state import Angang, Fulu, Peng
from majsoulrpa.screens.match.types import Seat, Tile

_THREE_PLAYER_COUNT = 3
_FOUR_PLAYER_COUNT = 4
_MAX_FULU_COUNT = 4
_NON_SIMPLE_TILES = frozenset(
    {
        Tile("1m"),
        Tile("9m"),
        Tile("1p"),
        Tile("9p"),
        Tile("1s"),
        Tile("9s"),
        Tile("1z"),
        Tile("2z"),
        Tile("3z"),
        Tile("4z"),
        Tile("5z"),
        Tile("6z"),
        Tile("7z"),
    }
)


def materialize_operation_candidates(
    specification: _OperationCandidatesSpecification | None,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
    player_count: int,
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
                fulu,
                self_seat,
                player_count,
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
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
    player_count: int,
) -> Sequence[MatchOperation]:
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
                fulu,
                self_seat,
                player_count,
            )
        case _PengOperationSpecification():
            return _materialize_peng_specification(
                specification,
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
                player_count,
            )
        case _AngangOperationSpecification():
            return _materialize_angang_specification(
                specification,
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
            )
        case _DaminggangOperationSpecification():
            return _materialize_daminggang_specification(
                specification,
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
                player_count,
            )
        case _JiagangOperationSpecification():
            return _materialize_jiagang_specification(
                specification,
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
            )
        case _LiqiOperationSpecification():
            return _materialize_liqi_specification(
                specification,
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
            )
        case _ZimohuOperationSpecification():
            return _materialize_zimohu_specification(
                event,
                zimopai,
                self_seat,
            )
        case _RongOperationSpecification():
            return _materialize_rong_specification(
                event,
                zimopai,
                self_seat,
                player_count,
            )
        case _LiujuOperationSpecification():
            return _materialize_liuju_specification(
                event,
                shoupai,
                zimopai,
                fulu,
                self_seat,
            )
        case _BabeiOperationSpecification():
            return _materialize_babei_specification(
                event,
                shoupai,
                zimopai,
                self_seat,
                player_count,
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
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
    player_count: int,
) -> list[ChiOperation]:
    _validate_new_fulu_allowed(fulu, "chi")
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
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
    player_count: int,
) -> list[PengOperation]:
    _validate_new_fulu_allowed(fulu, "peng")
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
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
) -> list[AngangOperation]:
    _validate_new_fulu_allowed(fulu, "angang")
    _, angang_zimopai = _validate_self_draw_operation_event(
        event,
        zimopai,
        self_seat,
        "angang",
    )
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
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
    player_count: int,
) -> list[DaminggangOperation]:
    _validate_new_fulu_allowed(fulu, "daminggang")
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


def _materialize_jiagang_specification(
    specification: _JiagangOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
) -> list[JiagangOperation]:
    if not isinstance(event, ZimoEvent):
        msg = "A jiagang operation must follow a self draw."
        raise TypeError(msg)
    if event.seat != self_seat:
        msg = "An opponent draw cannot provide a jiagang operation."
        raise ValueError(msg)
    if zimopai is None:
        msg = "A jiagang operation requires a drawn tile."
        raise ValueError(msg)

    available_tiles = {*shoupai, zimopai}
    operations: list[JiagangOperation] = []
    for tile_candidate in specification.tile_candidates:
        candidate_counts = Counter(tile_candidate)
        matching_pengs: list[tuple[Peng, Tile]] = []
        for entry in fulu:
            if not isinstance(entry, Peng):
                continue
            remaining_counts = candidate_counts.copy()
            for tile in (entry.tile, *entry.consumed):
                if remaining_counts[tile] == 0:
                    break
                remaining_counts[tile] -= 1
            else:
                added_tiles = list(remaining_counts.elements())
                if len(added_tiles) == 1:
                    matching_pengs.append((entry, added_tiles[0]))

        if len(matching_pengs) != 1:
            msg = "A jiagang operation must have exactly one matching peng."
            raise ValueError(msg)
        peng, added = matching_pengs[0]
        if added not in available_tiles:
            msg = (
                "A jiagang operation must add a tile from the hand "
                "or drawn tile."
            )
            raise ValueError(msg)
        operations.append(
            JiagangOperation(
                from_seat=peng.from_seat,
                tile=peng.tile,
                consumed=peng.consumed,
                added=added,
            )
        )
    return operations


def _materialize_liqi_specification(
    specification: _LiqiOperationSpecification,
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
) -> list[LiqiOperation]:
    if any(not isinstance(item, Angang) for item in fulu):
        msg = "A liqi operation requires a closed hand."
        raise ValueError(msg)

    liqi_event, liqi_zimopai = _validate_self_draw_operation_event(
        event,
        zimopai,
        self_seat,
        "liqi",
    )

    operations: list[LiqiOperation] = []
    for tile in specification.candidate_tiles:
        candidate_operations = _materialize_liqi_tile(
            tile,
            liqi_event,
            shoupai,
            liqi_zimopai,
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
                    liqi_event,
                    shoupai,
                    liqi_zimopai,
                )
            )
    return operations


def _materialize_zimohu_specification(
    event: MatchEvent,
    zimopai: Tile | None,
    self_seat: Seat,
) -> list[ZimohuOperation]:
    draw_event, zimohu_tile = _validate_self_draw_operation_event(
        event,
        zimopai,
        self_seat,
        "zimohu",
    )
    event_tile = (
        draw_event.zimopai
        if isinstance(draw_event, NewRoundEvent)
        else draw_event.tile
    )
    if event_tile != zimohu_tile:
        msg = "A zimohu tile must match the event's drawn tile."
        raise ValueError(msg)
    return [ZimohuOperation(tile=zimohu_tile)]


def _materialize_rong_specification(
    event: MatchEvent,
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> list[RongOperation]:
    match event:
        case DapaiEvent():
            from_seat = event.seat
            tile = event.tile
        case AngangEvent():
            from_seat = event.seat
            tile = event.consumed[0]
        case JiagangEvent():
            from_seat = event.seat
            tile = event.added
        case BabeiEvent():
            from_seat = event.seat
            tile = Tile("4z")
        case _:
            msg = "A rong operation must follow an action target."
            raise TypeError(msg)

    if from_seat >= player_count:
        msg = "A rong source seat must identify a player."
        raise ValueError(msg)
    if from_seat == self_seat:
        msg = "A rong cannot claim the self player's action target."
        raise ValueError(msg)
    if zimopai is not None:
        msg = "A rong cannot be selected with an unresolved draw."
        raise ValueError(msg)
    return [RongOperation(from_seat=from_seat, tile=tile)]


def _materialize_liuju_specification(
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    fulu: tuple[Fulu, ...],
    self_seat: Seat,
) -> list[LiujuOperation]:
    if fulu:
        msg = "A liuju operation cannot follow a fulu."
        raise ValueError(msg)
    _, liuju_zimopai = _validate_self_draw_operation_event(
        event,
        zimopai,
        self_seat,
        "liuju",
    )
    non_simple_kinds = {*shoupai, liuju_zimopai} & _NON_SIMPLE_TILES
    if len(non_simple_kinds) < 9:  # noqa: PLR2004
        msg = "A liuju operation requires nine distinct non-simple tiles."
        raise ValueError(msg)
    return [LiujuOperation()]


def _materialize_babei_specification(
    event: MatchEvent,
    shoupai: tuple[Tile, ...],
    zimopai: Tile | None,
    self_seat: Seat,
    player_count: int,
) -> list[BabeiOperation]:
    if player_count != _THREE_PLAYER_COUNT:
        msg = "A babei operation is only valid in a three-player match."
        raise ValueError(msg)
    _validate_self_draw_operation_event(
        event,
        zimopai,
        self_seat,
        "babei",
    )
    north = Tile("4z")
    if north not in shoupai and zimopai != north:
        msg = "A babei operation requires a north in the hand or drawn tile."
        raise ValueError(msg)
    return [BabeiOperation()]


def _validate_new_fulu_allowed(
    fulu: tuple[Fulu, ...],
    operation_name: str,
) -> None:
    if len(fulu) >= _MAX_FULU_COUNT:
        msg = f"A {operation_name} operation cannot add a fifth fulu."
        raise ValueError(msg)


def _validate_self_draw_operation_event(
    event: MatchEvent,
    zimopai: Tile | None,
    self_seat: Seat,
    operation_name: str,
) -> tuple[NewRoundEvent | ZimoEvent, Tile]:
    if isinstance(event, NewRoundEvent):
        if event.ju != self_seat:
            msg = (
                f"Only the dealer can select {operation_name} "
                "after ActionNewRound."
            )
            raise ValueError(msg)
    elif isinstance(event, ZimoEvent):
        if event.seat != self_seat:
            msg = (
                f"An opponent draw cannot provide the {operation_name} "
                "operation."
            )
            raise ValueError(msg)
    else:
        msg = f"The {operation_name} operation must follow a self draw."
        raise TypeError(msg)

    if zimopai is None:
        msg = f"The {operation_name} operation requires a drawn tile."
        raise ValueError(msg)
    return event, zimopai


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
    zimopai: Tile,
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
