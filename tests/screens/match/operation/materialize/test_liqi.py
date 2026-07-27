import pytest

from majsoulrpa.screens.match import (
    LiqiOperation,
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


def test_liqi_materialization_preserves_wire_order_and_tile_position() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["4s", "3p"]}],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=2,
        seat=validate_seat(0),
        tile=validate_tile("3p"),
        left_tile_count=60,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        (validate_tile("4s"), validate_tile("3p")),
        validate_tile("3p"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        LiqiOperation(tile=validate_tile("4s"), moqie=False),
        LiqiOperation(tile=validate_tile("3p"), moqie=False),
        LiqiOperation(tile=validate_tile("3p"), moqie=True),
    )


@pytest.mark.parametrize("suit", ["m", "p", "s"])
def test_liqi_materialization_adds_existing_normal_five_for_red_candidate(
    suit: str,
) -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": [f"0{suit}"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile(f"0{suit}"),
        left_tile_count=60,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        (validate_tile(f"5{suit}"),),
        validate_tile(f"0{suit}"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        LiqiOperation(tile=validate_tile(f"0{suit}"), moqie=True),
        LiqiOperation(tile=validate_tile(f"5{suit}"), moqie=False),
    )


def test_liqi_materialization_does_not_add_absent_normal_five() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["0m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("0m"),
        left_tile_count=60,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        (),
        validate_tile("0m"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        LiqiOperation(tile=validate_tile("0m"), moqie=True),
    )


def test_liqi_materialization_does_not_add_red_for_normal_five() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["5m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("5m"),
        left_tile_count=60,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        (validate_tile("0m"),),
        validate_tile("5m"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        LiqiOperation(tile=validate_tile("5m"), moqie=True),
    )


def test_liqi_marks_dealer_initial_tile_as_hand_discard() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["9s"]}],
                "time_add": 0,
                "time_fixed": 0,
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
        tuple(validate_tile("1m") for _ in range(13)),
        validate_tile("9s"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        LiqiOperation(tile=validate_tile("9s"), moqie=False),
    )


def test_liqi_materialization_rejects_candidate_absent_from_tiles() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["0m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("1m"),
        left_tile_count=60,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="candidate must exist"):
        materialize_operation_candidates(
            specification,
            event,
            (validate_tile("5m"),),
            validate_tile("1m"),
            (),
            validate_seat(0),
            4,
        )


def test_liqi_materialization_requires_drawn_tile() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 7, "combination": ["4s"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=1,
        seat=validate_seat(0),
        tile=validate_tile("4s"),
        left_tile_count=60,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="requires a drawn tile"):
        materialize_operation_candidates(
            specification,
            event,
            (validate_tile("4s"),),
            None,
            (),
            validate_seat(0),
            4,
        )
