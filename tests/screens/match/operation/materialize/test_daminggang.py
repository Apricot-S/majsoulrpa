import pytest

from majsoulrpa.screens.match import (
    DaminggangOperation,
    DapaiEvent,
    SkipOperation,
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


def test_daminggang_materialization_preserves_wire_order() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 5,
                        "combination": ["0m|5m|5m", "5m|5m|5m"],
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
        tuple(validate_tile(tile) for tile in ("0m", "5m", "5m", "5m")),
        None,
        (),
        validate_seat(0),
        3,
    )

    assert candidates is not None
    assert candidates.operations == (
        DaminggangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("0m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
        DaminggangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("5m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
        SkipOperation(),
    )


def test_daminggang_materialization_rejects_non_discard_event() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 5, "combination": ["5m|5m|5m"]}],
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
            tuple(validate_tile("5m") for _ in range(3)),
            None,
            (),
            validate_seat(0),
            4,
        )


@pytest.mark.parametrize(
    ("event_seat", "shoupai", "zimopai", "error_match"),
    [
        (0, ("5m", "5m", "5m"), None, "self player's discard"),
        (2, ("5m", "5m", "5m"), "1p", "unresolved draw"),
        (2, ("5m", "5m", "6m"), None, "in the hand"),
    ],
)
def test_daminggang_materialization_rejects_inconsistent_state(
    event_seat: int,
    shoupai: tuple[str, ...],
    zimopai: str | None,
    error_match: str,
) -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [{"type": 5, "combination": ["5m|5m|5m"]}],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    event = DapaiEvent(
        action_step=2,
        seat=validate_seat(event_seat),
        tile=validate_tile("5m"),
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=(),
    )

    with pytest.raises((TypeError, ValueError), match=error_match):
        materialize_operation_candidates(
            specification,
            event,
            tuple(validate_tile(tile) for tile in shoupai),
            None if zimopai is None else validate_tile(zimopai),
            (),
            validate_seat(0),
            4,
        )
