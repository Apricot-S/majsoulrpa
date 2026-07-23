import pytest

from majsoulrpa.screens.match import (
    ChiOperation,
    DapaiEvent,
    StartMatchEvent,
    validate_seat,
    validate_tile,
)
from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)


def test_chi_materialization_expands_each_combination_in_wire_order() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 2,
                        "combination": ["3m|4m", "4m|6m", "6m|7m"],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    event = DapaiEvent(
        action_step=2,
        seat=validate_seat(3),
        tile=validate_tile("0m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        tuple(
            validate_tile(tile)
            for tile in ("3m", "4m", "4m", "6m", "6m", "7m")
        ),
        None,
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("0m"),
            consumed=(validate_tile("3m"), validate_tile("4m")),
        ),
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("0m"),
            consumed=(validate_tile("4m"), validate_tile("6m")),
        ),
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("0m"),
            consumed=(validate_tile("6m"), validate_tile("7m")),
        ),
    )


def test_chi_rejects_discard_from_nonpreceding_player() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 2, "combination": ["3m|4m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = DapaiEvent(
        action_step=2,
        seat=validate_seat(2),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="preceding"):
        materialize_operation_candidates(
            specification,
            event,
            (validate_tile("3m"), validate_tile("4m")),
            None,
            (),
            validate_seat(0),
            4,
        )


def test_chi_materialization_rejects_non_discard_event() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 2, "combination": ["3m|4m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None

    with pytest.raises(TypeError, match="follow a discard"):
        materialize_operation_candidates(
            specification,
            StartMatchEvent(action_step=0),
            (validate_tile("3m"), validate_tile("4m")),
            None,
            (),
            validate_seat(0),
            4,
        )


def test_chi_materialization_rejects_tiles_absent_from_hand() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 2, "combination": ["3m|4m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = DapaiEvent(
        action_step=2,
        seat=validate_seat(3),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    with pytest.raises(ValueError, match="in the hand"):
        materialize_operation_candidates(
            specification,
            event,
            (validate_tile("3m"), validate_tile("6m")),
            None,
            (),
            validate_seat(0),
            4,
        )
