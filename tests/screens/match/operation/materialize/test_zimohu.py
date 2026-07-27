import pytest

from majsoulrpa.screens.match import (
    DapaiOperation,
    NewRoundEvent,
    ZimoEvent,
    ZimohuOperation,
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


def test_zimohu_uses_self_draw_without_normalizing_red() -> None:
    candidates = materialize_operation_candidates(
        _specification(),
        _zimo_event(),
        tuple(validate_tile("1m") for _ in range(13)),
        validate_tile("0m"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        ZimohuOperation(tile=validate_tile("0m")),
    )


def test_zimohu_materialization_uses_dealer_presentation_zimopai() -> None:
    event = NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(0),
        ben=0,
        scores=(25000, 25000, 25000, 25000),
        liqibang=0,
        left_tile_count=69,
        dora_indicators=(validate_tile("3p"),),
        shoupai=tuple(validate_tile("1m") for _ in range(13)),
        zimopai=validate_tile("9s"),
    )

    candidates = materialize_operation_candidates(
        _specification(),
        event,
        event.shoupai,
        event.zimopai,
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        ZimohuOperation(tile=validate_tile("9s")),
    )


def test_tenhou_candidate_does_not_change_initial_dapai_moqie() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {"type": 1, "combination": []},
                    {"type": 8, "combination": []},
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    event = NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(0),
        ben=0,
        scores=(25000, 25000, 25000, 25000),
        liqibang=0,
        left_tile_count=69,
        dora_indicators=(validate_tile("3p"),),
        shoupai=tuple(validate_tile("1m") for _ in range(13)),
        zimopai=validate_tile("9s"),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        event.shoupai,
        event.zimopai,
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        DapaiOperation(tile=validate_tile("1m"), moqie=False),
        DapaiOperation(tile=validate_tile("9s"), moqie=False),
        ZimohuOperation(tile=validate_tile("9s")),
    )


def test_zimohu_materialization_rejects_opponent_draw() -> None:
    with pytest.raises(ValueError, match="opponent draw"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(seat=1),
            tuple(validate_tile("1m") for _ in range(13)),
            validate_tile("0m"),
            (),
            validate_seat(0),
            4,
        )


def test_zimohu_materialization_requires_drawn_tile() -> None:
    with pytest.raises(ValueError, match="requires a drawn tile"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(),
            tuple(validate_tile("1m") for _ in range(13)),
            None,
            (),
            validate_seat(0),
            4,
        )


def test_zimohu_materialization_rejects_different_event_tile() -> None:
    with pytest.raises(ValueError, match="must match"):
        materialize_operation_candidates(
            _specification(),
            _zimo_event(),
            tuple(validate_tile("1m") for _ in range(13)),
            validate_tile("5m"),
            (),
            validate_seat(0),
            4,
        )


def _specification() -> _OperationCandidatesSpecification:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 8, "combination": []}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    return specification


def _zimo_event(*, seat: int = 0) -> ZimoEvent:
    return ZimoEvent(
        action_step=2,
        seat=validate_seat(seat),
        tile=validate_tile("0m") if seat == 0 else None,
        left_tile_count=68,
        dora_indicators=(),
    )
