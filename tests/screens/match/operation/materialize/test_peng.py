import pytest

from majsoulrpa.screens.match import (
    DapaiEvent,
    PengOperation,
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


def test_peng_materialization_expands_each_combination_in_wire_order() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 3,
                        "combination": ["0m|5m", "5m|5m"],
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
        seat=validate_seat(2),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        tuple(validate_tile(tile) for tile in ("0m", "5m", "5m")),
        None,
        validate_seat(0),
        3,
    )

    assert candidates is not None
    assert candidates.operations == (
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
        ),
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("5m"), validate_tile("5m")),
        ),
    )


def test_peng_materialization_rejects_non_discard_event() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 3, "combination": ["5m|5m"]}],
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
            (validate_tile("5m"), validate_tile("5m")),
            None,
            validate_seat(0),
            4,
        )


def test_peng_materialization_rejects_tiles_absent_from_hand() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 3, "combination": ["5m|5m"]}],
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

    with pytest.raises(ValueError, match="in the hand"):
        materialize_operation_candidates(
            specification,
            event,
            (validate_tile("5m"), validate_tile("6m")),
            None,
            validate_seat(0),
            4,
        )
