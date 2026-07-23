from majsoulrpa.screens.match import (
    DapaiEvent,
    DapaiOperation,
    validate_seat,
    validate_tile,
)
from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)
from majsoulrpa.screens.match.operation._materialize import (
    materialize_operation_candidates,
)


def test_dapai_materialization_does_not_forbid_unrelated_red_five() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 1, "combination": ["1p"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = DapaiEvent(
        action_step=2,
        seat=validate_seat(1),
        tile=validate_tile("9s"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        (
            validate_tile("0m"),
            validate_tile("5m"),
            validate_tile("1p"),
        ),
        None,
        validate_seat(0),
        4,
        self_fulu=(),
    )

    assert candidates is not None
    assert candidates.operations == (
        DapaiOperation(tile=validate_tile("0m"), moqie=False),
        DapaiOperation(tile=validate_tile("5m"), moqie=False),
    )
