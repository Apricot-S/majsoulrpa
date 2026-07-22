import pytest

from majsoulrpa.screens.match import (
    ChiOperation,
    DaminggangOperation,
    DapaiEvent,
    DapaiOperation,
    LiqiOperation,
    NewRoundEvent,
    PengOperation,
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
    )

    assert candidates is not None
    assert candidates.operations == (
        DapaiOperation(tile=validate_tile("0m"), moqie=False),
        DapaiOperation(tile=validate_tile("5m"), moqie=False),
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
            validate_seat(0),
            4,
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
            validate_seat(0),
            4,
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
            validate_seat(0),
            4,
        )
