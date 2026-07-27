import pytest

from majsoulrpa.screens.match import (
    BabeiOperation,
    NewRoundEvent,
    ZimoEvent,
    validate_seat,
    validate_tile,
)
from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)
from majsoulrpa.screens.match.operation._specification import (
    _OperationCandidatesSpecification,
)

_INITIAL_SHOUPAI = (
    "1m",
    "2m",
    "3m",
    "4m",
    "5m",
    "6m",
    "7m",
    "8m",
    "9m",
    "1p",
    "2p",
    "3p",
    "4p",
)
_INITIAL_SHOUPAI_WITH_NORTH = (*_INITIAL_SHOUPAI[:-1], "4z")


def _specification() -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 11, "combination": []}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


def _zimo_event(*, seat: int = 0, tile: str = "4z") -> ZimoEvent:
    return ZimoEvent(
        action_step=2,
        seat=validate_seat(seat),
        tile=validate_tile(tile),
        left_tile_count=54,
        dora_indicators=(),
    )


@pytest.mark.parametrize(
    ("shoupai", "zimopai"),
    [
        (_INITIAL_SHOUPAI, "4z"),
        (_INITIAL_SHOUPAI_WITH_NORTH, "2p"),
    ],
)
def test_babei_materialization_accepts_north_in_hand_or_drawn_tile(
    shoupai: tuple[str, ...],
    zimopai: str,
) -> None:
    candidates = materialize_operation_candidates(
        _specification(),
        _zimo_event(tile=zimopai),
        tuple(validate_tile(tile) for tile in shoupai),
        validate_tile(zimopai),
        (),
        validate_seat(0),
        3,
    )

    assert candidates is not None
    assert candidates.operations == (BabeiOperation(),)


@pytest.mark.parametrize(
    ("shoupai", "zimopai"),
    [
        (_INITIAL_SHOUPAI, "4z"),
        (_INITIAL_SHOUPAI_WITH_NORTH, "2p"),
    ],
)
def test_babei_materialization_accepts_dealer_initial_hand(
    shoupai: tuple[str, ...],
    zimopai: str,
) -> None:
    event = NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(0),
        ben=0,
        scores=(35000, 35000, 35000),
        liqibang=0,
        left_tile_count=55,
        dora_indicators=(validate_tile("3p"),),
        shoupai=tuple(validate_tile(tile) for tile in shoupai),
        zimopai=validate_tile(zimopai),
    )

    candidates = materialize_operation_candidates(
        _specification(),
        event,
        event.shoupai,
        event.zimopai,
        (),
        validate_seat(0),
        3,
    )

    assert candidates is not None
    assert candidates.operations == (BabeiOperation(),)


@pytest.mark.parametrize(
    ("event", "shoupai", "zimopai", "player_count", "error_match"),
    [
        (_zimo_event(tile="2p"), ("1m",), "2p", 3, "north"),
        (_zimo_event(seat=1), ("4z",), "2p", 3, "opponent draw"),
        (_zimo_event(), ("1m",), "4z", 4, "three-player"),
    ],
)
def test_babei_materialization_rejects_inconsistent_state(
    event: ZimoEvent,
    shoupai: tuple[str, ...],
    zimopai: str,
    player_count: int,
    error_match: str,
) -> None:
    with pytest.raises((TypeError, ValueError), match=error_match):
        materialize_operation_candidates(
            _specification(),
            event,
            tuple(validate_tile(tile) for tile in shoupai),
            validate_tile(zimopai),
            (),
            validate_seat(0),
            player_count,
        )
