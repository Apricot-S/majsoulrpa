import pytest

from majsoulrpa.screens.match import (
    AngangOperation,
    NewRoundEvent,
    StartMatchEvent,
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


def test_angang_materialization_preserves_unsorted_wire_order() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {
                        "type": 4,
                        "combination": [
                            "4p|4p|4p|4p",
                            "0p|5p|5p|5p",
                            "1m|1m|1m|1m",
                        ],
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )
    assert specification is not None
    event = ZimoEvent(
        action_step=2,
        seat=validate_seat(0),
        tile=validate_tile("1m"),
        left_tile_count=60,
        dora_indicators=(),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        tuple(
            validate_tile(tile)
            for tile in (
                "4p",
                "4p",
                "4p",
                "4p",
                "0p",
                "5p",
                "5p",
                "5p",
                "1m",
                "1m",
                "1m",
            )
        ),
        validate_tile("1m"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        AngangOperation(
            consumed=(
                validate_tile("4p"),
                validate_tile("4p"),
                validate_tile("4p"),
                validate_tile("4p"),
            )
        ),
        AngangOperation(
            consumed=(
                validate_tile("0p"),
                validate_tile("5p"),
                validate_tile("5p"),
                validate_tile("5p"),
            )
        ),
        AngangOperation(
            consumed=(
                validate_tile("1m"),
                validate_tile("1m"),
                validate_tile("1m"),
                validate_tile("1m"),
            )
        ),
    )


def test_angang_materialization_includes_dealer_presentation_tile() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {"type": 4, "combination": ["1z|1z|1z|1z"]}
                ],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None
    shoupai = tuple(validate_tile("1z") for _ in range(3)) + tuple(
        validate_tile("2m") for _ in range(10)
    )
    event = NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(0),
        ben=0,
        scores=(25000, 25000, 25000, 25000),
        liqibang=0,
        left_tile_count=69,
        dora_indicators=(validate_tile("3p"),),
        shoupai=shoupai,
        zimopai=validate_tile("1z"),
    )

    candidates = materialize_operation_candidates(
        specification,
        event,
        shoupai,
        validate_tile("1z"),
        (),
        validate_seat(0),
        4,
    )

    assert candidates is not None
    assert candidates.operations == (
        AngangOperation(
            consumed=(
                validate_tile("1z"),
                validate_tile("1z"),
                validate_tile("1z"),
                validate_tile("1z"),
            )
        ),
    )


@pytest.mark.parametrize(
    ("event", "shoupai", "zimopai", "error_match"),
    [
        (
            StartMatchEvent(action_step=0),
            ("1z", "1z", "1z", "1z"),
            None,
            "self draw",
        ),
        (
            ZimoEvent(
                action_step=2,
                seat=validate_seat(1),
                tile=None,
                left_tile_count=60,
                dora_indicators=(),
            ),
            ("1z", "1z", "1z", "1z"),
            None,
            "opponent draw",
        ),
        (
            ZimoEvent(
                action_step=2,
                seat=validate_seat(0),
                tile=validate_tile("2m"),
                left_tile_count=60,
                dora_indicators=(),
            ),
            ("1z", "1z", "1z", "2m"),
            "2m",
            "in the hand",
        ),
    ],
)
def test_angang_materialization_rejects_inconsistent_state(
    event: StartMatchEvent | ZimoEvent,
    shoupai: tuple[str, ...],
    zimopai: str | None,
    error_match: str,
) -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "operation_list": [
                    {"type": 4, "combination": ["1z|1z|1z|1z"]}
                ],
                "time_add": 0,
                "time_fixed": 0,
            }
        }
    )
    assert specification is not None

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
