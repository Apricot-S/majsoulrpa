import pytest

from majsoulrpa.screens.match import (
    Angang,
    LiujuOperation,
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

_ELIGIBLE_SHOUPAI = (
    "1m",
    "9m",
    "1p",
    "9p",
    "1s",
    "9s",
    "1z",
    "2z",
    "3z",
    "4z",
    "2m",
    "3m",
    "4m",
)


def _specification() -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 10, "combination": []}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


def _new_round_event() -> NewRoundEvent:
    return NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(0),
        ben=0,
        scores=(25000, 25000, 25000, 25000),
        liqibang=0,
        left_tile_count=69,
        dora_indicators=(validate_tile("3p"),),
        shoupai=tuple(validate_tile(tile) for tile in _ELIGIBLE_SHOUPAI),
        zimopai=validate_tile("5z"),
    )


def _zimo_event(*, seat: int = 0) -> ZimoEvent:
    return ZimoEvent(
        action_step=2,
        seat=validate_seat(seat),
        tile=validate_tile("5z") if seat == 0 else None,
        left_tile_count=68,
        dora_indicators=(),
    )


@pytest.mark.parametrize("event", [_new_round_event(), _zimo_event()])
def test_liuju_materialization_accepts_dealer_deal_or_self_draw(
    event: NewRoundEvent | ZimoEvent,
) -> None:
    candidates = materialize_operation_candidates(
        _specification(),
        event,
        tuple(validate_tile(tile) for tile in _ELIGIBLE_SHOUPAI),
        validate_tile("5z"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (LiujuOperation(),)


def test_liuju_materialization_rejects_opponent_draw() -> None:
    with pytest.raises(ValueError, match="opponent draw"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(seat=1),
            tuple(validate_tile(tile) for tile in _ELIGIBLE_SHOUPAI),
            validate_tile("5z"),
            (),
            validate_seat(0),
            4,
        )


def test_liuju_materialization_requires_nine_non_simple_kinds() -> None:
    with pytest.raises(ValueError, match="nine distinct"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(),
            tuple(validate_tile("2m") for _ in range(13)),
            validate_tile("1m"),
            (),
            validate_seat(0),
            4,
        )


def test_liuju_materialization_rejects_existing_fulu() -> None:
    with pytest.raises(ValueError, match="cannot follow a fulu"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(),
            tuple(validate_tile(tile) for tile in _ELIGIBLE_SHOUPAI),
            validate_tile("5z"),
            (
                Angang(
                    consumed=(
                        validate_tile("1z"),
                        validate_tile("1z"),
                        validate_tile("1z"),
                        validate_tile("1z"),
                    )
                ),
            ),
            validate_seat(0),
            4,
        )
